from __future__ import annotations

import urllib.parse
from typing import Any, Callable

from .base import build_bundle, make_evidence_item, utc_now
from .http_client import get_json
from .oauth import access_token, loopback_oauth_authorization_code
from .token_store import TokenStore


GOOGLE_WORKSPACE_ACCOUNT = "google_workspace_api"
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_SCOPES = ["https://www.googleapis.com/auth/admin.directory.user.readonly"]
GOOGLE_USERS_URL = "https://admin.googleapis.com/admin/directory/v1/users"

GoogleFetcher = Callable[[str, str], dict[str, Any]]


def connect_google_workspace(
    *,
    client_id: str,
    client_secret: str | None = None,
    token_store: TokenStore | None = None,
    open_browser: bool = True,
) -> dict[str, Any]:
    store = token_store or TokenStore()
    return loopback_oauth_authorization_code(
        provider="google_workspace",
        account=GOOGLE_WORKSPACE_ACCOUNT,
        auth_url=GOOGLE_AUTH_URL,
        token_url=GOOGLE_TOKEN_URL,
        client_id=client_id,
        client_secret=client_secret,
        scopes=GOOGLE_SCOPES,
        token_store=store,
        auth_params={"access_type": "offline", "prompt": "consent"},
        open_browser=open_browser,
    )


def _fetch_google_page(url: str, token: str) -> dict[str, Any]:
    return get_json(url, access_token=token)


def _build_users_url(*, customer: str, domain: str | None, page_token: str | None = None) -> str:
    params = {
        "maxResults": "500",
        "projection": "full",
        "viewType": "admin_view",
        "fields": "users(isAdmin,isDelegatedAdmin,suspended,isEnrolledIn2Sv,isEnforcedIn2Sv),nextPageToken",
    }
    if domain:
        params["domain"] = domain
    else:
        params["customer"] = customer
    if page_token:
        params["pageToken"] = page_token
    return f"{GOOGLE_USERS_URL}?{urllib.parse.urlencode(params)}"


def collect_google_workspace(
    *,
    customer: str = "my_customer",
    domain: str | None = None,
    generated_at: str | None = None,
    token_store: TokenStore | None = None,
    fetcher: GoogleFetcher | None = None,
) -> dict[str, Any]:
    collected_at = generated_at or utc_now()
    store = token_store or TokenStore()
    token = "test-token" if fetcher else access_token(GOOGLE_WORKSPACE_ACCOUNT, store)
    page_token: str | None = None
    rows: list[dict[str, Any]] = []
    while True:
        url = _build_users_url(customer=customer, domain=domain, page_token=page_token)
        payload = fetcher(url, token) if fetcher else _fetch_google_page(url, token)
        rows.extend(payload.get("users", []))
        page_token = payload.get("nextPageToken")
        if not page_token:
            break

    total = len(rows)
    admins = sum(1 for row in rows if bool(row.get("isAdmin") or row.get("isDelegatedAdmin")))
    suspended = sum(1 for row in rows if bool(row.get("suspended")))
    mfa_enrolled = sum(1 for row in rows if bool(row.get("isEnrolledIn2Sv")))
    mfa_enforced = sum(1 for row in rows if bool(row.get("isEnforcedIn2Sv")))
    mfa_missing = max(0, total - mfa_enrolled)
    enforced_missing = max(0, total - mfa_enforced)
    status = "missing" if mfa_missing or enforced_missing else "observed"
    priority = "high" if mfa_missing or enforced_missing else "low"

    evidence = [
        make_evidence_item(
            evidence_id="CONN-GW-API-MFA-001",
            title="Google Workspace official MFA enrollment and enforcement summary",
            source_system="google_workspace",
            source_type="api_read_only",
            collected_at=collected_at,
            control_area="access_mfa",
            subject="user_mfa_enrollment",
            summary=f"{mfa_enrolled} of {total} Google Workspace users show 2-Step Verification enrollment; {mfa_enforced} show enforcement. User identities are not stored.",
            status=status,
            confidence="observed_from_api",
            owner_lane="msp",
            recommended_question="Can the MSP confirm Google 2-Step Verification enforcement for all users, admins, remote access, and vendor-support accounts?",
            acceptable_evidence=["Google Admin API collection timestamp", "2SV enrollment count", "2SV enforcement count", "exception list", "MSP signoff"],
            next_action="Use the official Google Workspace metadata result to close MFA gaps or record owner-approved exceptions.",
            stage_id="access_offboarding_review",
            priority=priority,
            counts={"total_users": total, "mfa_enrolled": mfa_enrolled, "mfa_missing": mfa_missing, "mfa_enforced": mfa_enforced, "mfa_enforcement_missing": enforced_missing},
            unsafe_fields_excluded=["user emails", "mailbox contents", "Drive contents", "private admin URLs", "credentials", "raw logs"],
        ),
        make_evidence_item(
            evidence_id="CONN-GW-API-ADMIN-001",
            title="Google Workspace official admin and suspended-user summary",
            source_system="google_workspace",
            source_type="api_read_only",
            collected_at=collected_at,
            control_area="admin_access",
            subject="admin_account_review",
            summary=f"{admins} Google Workspace admin users and {suspended} suspended users were counted through the official Directory API. Row-level identities are not stored.",
            status="needs_review" if admins > 2 else "observed",
            confidence="observed_from_api",
            owner_lane="msp",
            recommended_question="Can the MSP confirm admin role need, break-glass handling, shared-account exceptions, and terminated-user handling?",
            acceptable_evidence=["Google Admin API collection timestamp", "admin count", "suspended user count", "exception list", "owner/MSP signoff"],
            next_action="Review official Google admin and suspended-user counts with the MSP and owner before closeout.",
            stage_id="access_offboarding_review",
            priority="medium" if admins > 2 else "low",
            counts={"total_users": total, "admin_users": admins, "suspended_users": suspended},
            unsafe_fields_excluded=["user emails", "mailbox contents", "Drive contents", "private admin URLs", "credentials", "raw logs"],
        ),
    ]
    return build_bundle(
        connector="google_workspace_api",
        mode="oauth_read_only_metadata",
        input_ref=domain or customer,
        evidence=evidence,
        generated_at=collected_at,
    )

