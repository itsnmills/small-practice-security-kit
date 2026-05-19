from __future__ import annotations

import urllib.parse
from datetime import UTC, datetime, timedelta
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
MICROSOFT_UNSAFE_FIELDS = [
    "user principal names",
    "mailbox contents",
    "Teams chat contents",
    "SharePoint or OneDrive file contents",
    "raw sign-in logs",
    "credentials",
    "private admin URLs",
]

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


def _build_users_url(*, include_activity: bool = True) -> str:
    selected = ["id", "accountEnabled", "userType", "createdDateTime"]
    if include_activity:
        selected.append("signInActivity")
    return f"{GRAPH_USERS_URL}?{urllib.parse.urlencode({'$select': ','.join(selected), '$top': '999'})}"


def _parse_graph_time(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _reference_time(collected_at: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(collected_at.replace("Z", "+00:00"))
    except ValueError:
        return datetime.now(UTC)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _last_sign_in(row: dict[str, Any]) -> datetime | None:
    activity = row.get("signInActivity")
    if not isinstance(activity, dict):
        return None
    return _parse_graph_time(activity.get("lastSuccessfulSignInDateTime") or activity.get("lastSignInDateTime"))


def collect_microsoft_365(
    *,
    generated_at: str | None = None,
    token_store: TokenStore | None = None,
    fetcher: MicrosoftFetcher | None = None,
) -> dict[str, Any]:
    collected_at = generated_at or utc_now()
    store = token_store or TokenStore()
    token = "test-token" if fetcher else access_token(MICROSOFT_365_ACCOUNT, store)
    report_url = f"{GRAPH_MFA_REPORT_URL}?{urllib.parse.urlencode({'$select': 'isMfaRegistered,isMfaCapable,isSsprRegistered,isSsprEnabled'})}"

    warnings: list[str] = []
    try:
        users = _paged(_build_users_url(include_activity=True), token, fetcher)
    except Exception as exc:
        warnings.append(f"User sign-in activity metadata was not available: {exc}")
        users = _paged(_build_users_url(include_activity=False), token, fetcher)
    try:
        registrations = _paged(report_url, token, fetcher)
    except Exception as exc:
        registrations = []
        warnings.append(f"MFA registration report was not available: {exc}")

    total = len(users)
    enabled = sum(1 for row in users if row.get("accountEnabled") is not False)
    disabled = max(0, total - enabled)
    guests = sum(1 for row in users if str(row.get("userType", "")).lower() == "guest")
    enabled_guests = sum(1 for row in users if row.get("accountEnabled") is not False and str(row.get("userType", "")).lower() == "guest")
    mfa_registered = sum(1 for row in registrations if bool(row.get("isMfaRegistered")))
    mfa_capable = sum(1 for row in registrations if bool(row.get("isMfaCapable", row.get("isCapable"))))
    mfa_missing = max(0, enabled - mfa_registered) if registrations else 0
    mfa_status = "missing" if registrations and mfa_missing else "observed" if registrations else "requested"
    mfa_priority = "high" if registrations and mfa_missing else "low" if registrations else "medium"
    sspr_registered = sum(1 for row in registrations if bool(row.get("isSsprRegistered")))
    sspr_enabled = sum(1 for row in registrations if bool(row.get("isSsprEnabled")))
    sspr_missing = max(0, enabled - sspr_registered) if registrations else 0
    sspr_status = "needs_review" if registrations and sspr_missing else "observed" if registrations else "requested"
    sspr_priority = "medium" if registrations and sspr_missing else "low" if registrations else "medium"
    reference_time = _reference_time(collected_at)
    stale_threshold = reference_time - timedelta(days=90)
    new_threshold = reference_time - timedelta(days=30)
    enabled_rows = [row for row in users if row.get("accountEnabled") is not False]
    sign_in_activity_available = any(isinstance(row.get("signInActivity"), dict) for row in users)
    last_sign_ins = [_last_sign_in(row) for row in enabled_rows]
    never_signed_in = (
        sum(1 for row, sign_in in zip(enabled_rows, last_sign_ins) if isinstance(row.get("signInActivity"), dict) and sign_in is None)
        if sign_in_activity_available
        else 0
    )
    inactive_90_days = sum(1 for sign_in in last_sign_ins if sign_in is not None and sign_in < stale_threshold)
    created_30_days = sum(1 for row in enabled_rows if (created := _parse_graph_time(row.get("createdDateTime"))) is not None and created >= new_threshold)
    lifecycle_status = "needs_review" if never_signed_in or inactive_90_days else "observed" if sign_in_activity_available else "requested"
    lifecycle_priority = "medium" if lifecycle_status in {"needs_review", "requested"} else "low"

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
            unsafe_fields_excluded=MICROSOFT_UNSAFE_FIELDS,
            plain_english_summary=(
                f"Microsoft 365 has {mfa_missing} enabled users without observed MFA registration."
                if registrations
                else "Microsoft 365 MFA registration evidence needs MSP confirmation because the Graph report was unavailable."
            ),
            why_it_matters="MFA and Conditional Access evidence are high-value security proof points for email, remote work, admin access, and cyber-insurance preparation.",
            reviewer_needed=["msp", "office_manager"],
            owner_view="Confirm the MSP has reviewed Microsoft 365 MFA or Conditional Access coverage and documented exceptions.",
            msp_view="Return MFA registration, capability, Conditional Access coverage, and exception evidence without sending user principal names or raw sign-in logs.",
        ),
        make_evidence_item(
            evidence_id="CONN-M365-API-USERS-001",
            title="Microsoft 365 official account status summary",
            source_system="microsoft_365",
            source_type="api_read_only",
            collected_at=collected_at,
            control_area="access_offboarding",
            subject="enabled_disabled_user_review",
            summary=f"{enabled} enabled and {disabled} disabled Microsoft 365 users were counted through Microsoft Graph. Row-level identities are not stored.",
            status="observed",
            confidence="observed_from_api",
            owner_lane="msp",
            recommended_question="Can the MSP confirm enabled and disabled account counts, offboarding cadence, and whether admin-role evidence should be exported separately?",
            acceptable_evidence=["Microsoft Graph collection timestamp", "enabled user count", "disabled user count", "offboarding review note", "owner/MSP signoff"],
            next_action="Use Microsoft account-status counts to replace manual user inventory entry and drive the MSP offboarding review.",
            stage_id="access_offboarding_review",
            priority="low",
            counts={"total_users": total, "enabled_users": enabled, "disabled_users": disabled},
            unsafe_fields_excluded=MICROSOFT_UNSAFE_FIELDS,
            plain_english_summary=f"Microsoft 365 account-status evidence counted {enabled} enabled users and {disabled} disabled users without storing identities.",
            why_it_matters="Account status counts help the owner and MSP spot offboarding gaps quickly while keeping user lists out of Velari artifacts.",
            reviewer_needed=["msp", "office_manager"],
            owner_view="Ask the MSP to compare enabled and disabled Microsoft 365 counts against staff and vendor-access changes.",
            msp_view="Provide a dated offboarding summary and any exception counts; keep user principal names and raw logs out of the export.",
        ),
        make_evidence_item(
            evidence_id="CONN-M365-API-SSPR-001",
            title="Microsoft 365 official self-service password reset summary",
            source_system="microsoft_365",
            source_type="api_read_only",
            collected_at=collected_at,
            control_area="identity_recovery",
            subject="sspr_registration_review",
            summary=(
                f"{sspr_registered} enabled Microsoft 365 users show self-service password reset registration; {sspr_enabled} show SSPR enabled in the Graph report."
                if registrations
                else "Microsoft 365 self-service password reset registration report was not available; request MSP confirmation instead."
            ),
            status=sspr_status,
            confidence="observed_from_api" if registrations else "unknown",
            owner_lane="msp",
            recommended_question="Can the MSP confirm self-service password reset coverage, helpdesk reset workflow, and recovery-method exceptions?",
            acceptable_evidence=["Microsoft Graph collection timestamp", "SSPR registration count", "SSPR enabled count", "password reset workflow summary", "MSP signoff"],
            next_action="Use SSPR metadata to reduce manual password-reset workflow questions and route gaps to the MSP.",
            stage_id="access_offboarding_review",
            priority=sspr_priority,
            counts={"enabled_users": enabled, "sspr_registered": sspr_registered, "sspr_enabled": sspr_enabled, "sspr_missing": sspr_missing},
            unsafe_fields_excluded=MICROSOFT_UNSAFE_FIELDS,
            plain_english_summary=(
                f"Microsoft 365 has {sspr_missing} enabled users without observed self-service password reset registration."
                if registrations
                else "Microsoft 365 password recovery evidence needs MSP confirmation because the Graph report was unavailable."
            ),
            why_it_matters="Clear password recovery evidence reduces helpdesk guesswork and helps prevent rushed account resets from becoming a security weak point.",
            reviewer_needed=["msp", "office_manager"],
            owner_view="Confirm whether password reset workflows are handled by SSPR, MSP helpdesk, or an owner-approved exception path.",
            msp_view="Return SSPR coverage and helpdesk reset workflow evidence as aggregate counts and dated summaries only.",
        ),
        make_evidence_item(
            evidence_id="CONN-M365-API-GUESTS-001",
            title="Microsoft 365 official guest and external-user summary",
            source_system="microsoft_365",
            source_type="api_read_only",
            collected_at=collected_at,
            control_area="external_access",
            subject="guest_user_review",
            summary=f"{guests} total Microsoft 365 guest users and {enabled_guests} enabled guest users were counted through Microsoft Graph. Guest identities are not stored.",
            status="needs_review" if enabled_guests else "observed",
            confidence="observed_from_api",
            owner_lane="msp",
            recommended_question="Can the MSP confirm guest-user ownership, external sharing purpose, review cadence, and removal of stale external access?",
            acceptable_evidence=["Microsoft Graph collection timestamp", "guest user count", "enabled guest count", "external access review", "owner/MSP signoff"],
            next_action="Review enabled guest counts with the MSP and owner before closeout.",
            stage_id="access_offboarding_review",
            priority="medium" if enabled_guests else "low",
            counts={"total_users": total, "guest_users": guests, "enabled_guest_users": enabled_guests},
            unsafe_fields_excluded=MICROSOFT_UNSAFE_FIELDS,
            plain_english_summary=f"Microsoft 365 has {enabled_guests} enabled guest users that need an external-access review question.",
            why_it_matters="Guest access can be legitimate, but owner and MSP review prevents forgotten vendor or collaborator access from becoming a quiet exposure.",
            reviewer_needed=["msp", "office_manager"],
            owner_view="Ask the MSP which guest accounts are still needed and who owns each external-access exception.",
            msp_view="Return external-access review evidence with counts, purposes, exception owners, and removal notes, not guest identities.",
        ),
        make_evidence_item(
            evidence_id="CONN-M365-API-LIFECYCLE-001",
            title="Microsoft 365 official account lifecycle summary",
            source_system="microsoft_365",
            source_type="api_read_only",
            collected_at=collected_at,
            control_area="access_offboarding",
            subject="inactive_and_new_account_review",
            summary=(
                f"{inactive_90_days} enabled Microsoft 365 users appear inactive for 90+ days, {never_signed_in} appear never signed in, and {created_30_days} were created in the last 30 days. User identities are not stored."
                if sign_in_activity_available
                else "Microsoft 365 sign-in activity metadata was not available; request MSP access-review confirmation instead of collecting raw sign-in logs."
            ),
            status=lifecycle_status,
            confidence="observed_from_api" if sign_in_activity_available else "unknown",
            owner_lane="msp",
            recommended_question="Can the MSP confirm inactive account handling, recent-account approvals, offboarding, and whether any stale active accounts should be disabled?",
            acceptable_evidence=["Microsoft Graph collection timestamp", "inactive account count", "never-signed-in account count", "recent account count", "owner access-review signoff"],
            next_action="Use lifecycle metadata to drive an MSP access review without collecting raw sign-in logs or user principal names.",
            stage_id="access_offboarding_review",
            priority=lifecycle_priority,
            counts={
                "enabled_users": enabled,
                "disabled_users": disabled,
                "sign_in_activity_available": sign_in_activity_available,
                "inactive_90_day_enabled_users": inactive_90_days,
                "never_signed_in_enabled_users": never_signed_in,
                "new_30_day_enabled_users": created_30_days,
            },
            unsafe_fields_excluded=MICROSOFT_UNSAFE_FIELDS,
            plain_english_summary=(
                f"Microsoft 365 lifecycle evidence found {inactive_90_days + never_signed_in} enabled accounts that need an access-review question."
                if sign_in_activity_available
                else "Microsoft 365 lifecycle evidence needs MSP confirmation because sign-in activity metadata was unavailable."
            ),
            why_it_matters="Inactive, never-used, or newly created accounts are fast signals for access-review and offboarding work the MSP can validate.",
            reviewer_needed=["msp", "office_manager"],
            owner_view="Have the MSP confirm stale, never-used, and newly created Microsoft 365 accounts during the access review.",
            msp_view="Review inactive, never-signed-in, recent, enabled, and disabled account counts and provide a reference-only access-review signoff.",
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
