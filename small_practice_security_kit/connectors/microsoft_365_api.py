from __future__ import annotations

import urllib.parse
from typing import Any, Callable

from .base import build_bundle, make_evidence_item, utc_now
from .http_client import get_json
from .oauth import access_token, loopback_oauth_authorization_code
from .token_store import TokenStore


MICROSOFT_365_ACCOUNT = "microsoft_365_api"
MICROSOFT_AUTH_BASE = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize"
MICROSOFT_TOKEN_BASE = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
MICROSOFT_SCOPES = [
    "offline_access",
    "https://graph.microsoft.com/User.Read.All",
    "https://graph.microsoft.com/AuditLog.Read.All",
]
GRAPH_USERS_URL = "https://graph.microsoft.com/v1.0/users"
GRAPH_MFA_REPORT_URL = "https://graph.microsoft.com/v1.0/reports/authenticationMethods/userRegistrationDetails"

MicrosoftFetcher = Callable[[str, str, dict[str, str] | None], dict[str, Any]]


def connect_microsoft_365(
    *,
    client_id: str,
    tenant: str = "organizations",
    token_store: TokenStore | None = None,
    open_browser: bool = True,
) -> dict[str, Any]:
    store = token_store or TokenStore()
    return loopback_oauth_authorization_code(
        provider="microsoft_365",
        account=MICROSOFT_365_ACCOUNT,
        auth_url=MICROSOFT_AUTH_BASE.format(tenant=tenant),
        token_url=MICROSOFT_TOKEN_BASE.format(tenant=tenant),
        client_id=client_id,
        scopes=MICROSOFT_SCOPES,
        token_store=store,
        auth_params={"response_mode": "query"},
        open_browser=open_browser,
    )


def _fetch_graph_page(url: str, token: str, headers: dict[str, str] | None = None) -> dict[str, Any]:
    return get_json(url, access_token=token, headers=headers)


def _paged(url: str, token: str, fetcher: MicrosoftFetcher | None = None, headers: dict[str, str] | None = None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    next_url: str | None = url
    while next_url:
        payload = fetcher(next_url, token, headers) if fetcher else _fetch_graph_page(next_url, token, headers)
        rows.extend(payload.get("value", []))
        next_url = payload.get("@odata.nextLink")
    return rows


def collect_microsoft_365(
    *,
    generated_at: str | None = None,
    token_store: TokenStore | None = None,
    fetcher: MicrosoftFetcher | None = None,
) -> dict[str, Any]:
    collected_at = generated_at or utc_now()
    store = token_store or TokenStore()
    token = "test-token" if fetcher else access_token(MICROSOFT_365_ACCOUNT, store)
    users_url = f"{GRAPH_USERS_URL}?{urllib.parse.urlencode({'$select': 'id,accountEnabled,userType', '$top': '999'})}"
    report_url = f"{GRAPH_MFA_REPORT_URL}?{urllib.parse.urlencode({'$select': 'isMfaRegistered,isMfaCapable,isSsprRegistered,isSsprEnabled'})}"

    warnings: list[str] = []
    users = _paged(users_url, token, fetcher)
    try:
        registrations = _paged(report_url, token, fetcher)
    except Exception as exc:
        registrations = []
        warnings.append(f"MFA registration report was not available: {exc}")

    total = len(users)
    enabled = sum(1 for row in users if row.get("accountEnabled") is not False)
    guests = sum(1 for row in users if str(row.get("userType", "")).lower() == "guest")
    mfa_registered = sum(1 for row in registrations if bool(row.get("isMfaRegistered")))
    mfa_capable = sum(1 for row in registrations if bool(row.get("isMfaCapable", row.get("isCapable"))))
    mfa_missing = max(0, enabled - mfa_registered) if registrations else 0
    mfa_status = "missing" if registrations and mfa_missing else "observed" if registrations else "requested"
    mfa_priority = "high" if registrations and mfa_missing else "low" if registrations else "medium"

    evidence = [
        make_evidence_item(
            evidence_id="CONN-M365-API-MFA-001",
            title="Microsoft 365 official MFA registration summary",
            source_system="microsoft_365",
            source_type="api_read_only",
            collected_at=collected_at,
            control_area="access_mfa",
            subject="user_mfa_registration",
            summary=(
                f"{mfa_registered} Microsoft 365 users show MFA registration and {mfa_capable} show MFA capability in the Graph report. "
                "User principal names are not stored."
                if registrations
                else "Microsoft 365 MFA registration report was not available; request MSP confirmation instead of storing raw sign-in logs."
            ),
            status=mfa_status,
            confidence="observed_from_api" if registrations else "unknown",
            owner_lane="msp",
            recommended_question="Can the MSP confirm MFA or Conditional Access enforcement for all users, admins, remote access, and vendor-support accounts?",
            acceptable_evidence=["Microsoft Graph collection timestamp", "MFA registration count", "Conditional Access policy summary", "exception list", "MSP signoff"],
            next_action="Use the official Microsoft 365 metadata result to close MFA gaps or request MSP confirmation if the report is unavailable.",
            stage_id="access_offboarding_review",
            priority=mfa_priority,
            counts={"enabled_users": enabled, "mfa_registered": mfa_registered, "mfa_capable": mfa_capable, "mfa_missing": mfa_missing},
            unsafe_fields_excluded=["user principal names", "mailbox contents", "Teams chat contents", "SharePoint or OneDrive file contents", "raw sign-in logs", "credentials"],
        ),
        make_evidence_item(
            evidence_id="CONN-M365-API-USERS-001",
            title="Microsoft 365 official enabled and guest-user summary",
            source_system="microsoft_365",
            source_type="api_read_only",
            collected_at=collected_at,
            control_area="admin_access",
            subject="enabled_guest_user_review",
            summary=f"{enabled} enabled Microsoft 365 users and {guests} guest users were counted through Microsoft Graph. Row-level identities are not stored.",
            status="needs_review" if guests else "observed",
            confidence="observed_from_api",
            owner_lane="msp",
            recommended_question="Can the MSP confirm guest user ownership, external access, admin role evidence, and offboarding evidence?",
            acceptable_evidence=["Microsoft Graph collection timestamp", "enabled user count", "guest user count", "external access review", "owner/MSP signoff"],
            next_action="Review official Microsoft enabled-user and guest-user counts with the MSP and owner before closeout.",
            stage_id="access_offboarding_review",
            priority="medium" if guests else "low",
            counts={"total_users": total, "enabled_users": enabled, "guest_users": guests},
            unsafe_fields_excluded=["user principal names", "mailbox contents", "Teams chat contents", "SharePoint or OneDrive file contents", "raw sign-in logs", "credentials"],
        ),
    ]
    return build_bundle(
        connector="microsoft_365_api",
        mode="oauth_read_only_metadata",
        input_ref="microsoft_graph",
        evidence=evidence,
        generated_at=collected_at,
        warnings=warnings,
    )
