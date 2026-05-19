from __future__ import annotations

import urllib.parse
from datetime import UTC, datetime, timedelta
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
GOOGLE_UNSAFE_FIELDS = ["user emails", "mailbox contents", "Drive contents", "private admin URLs", "credentials", "raw logs", "MFA recovery codes"]

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
        "fields": "users(isAdmin,isDelegatedAdmin,suspended,isEnrolledIn2Sv,isEnforcedIn2Sv,lastLoginTime,creationTime),nextPageToken",
    }
    if domain:
        params["domain"] = domain
    else:
        params["customer"] = customer
    if page_token:
        params["pageToken"] = page_token
    return f"{GOOGLE_USERS_URL}?{urllib.parse.urlencode(params)}"


def _parse_google_time(value: Any) -> datetime | None:
    if not value:
        return None
    text = str(value)
    if text.startswith("1970-01-01"):
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
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
    active_rows = [row for row in rows if not bool(row.get("suspended"))]
    admin_rows = [row for row in active_rows if bool(row.get("isAdmin") or row.get("isDelegatedAdmin"))]
    active_total = len(active_rows)
    super_admins = sum(1 for row in active_rows if bool(row.get("isAdmin")))
    delegated_admins = sum(1 for row in active_rows if bool(row.get("isDelegatedAdmin")))
    admins = len(admin_rows)
    suspended = sum(1 for row in rows if bool(row.get("suspended")))
    mfa_enrolled = sum(1 for row in active_rows if bool(row.get("isEnrolledIn2Sv")))
    mfa_enforced = sum(1 for row in active_rows if bool(row.get("isEnforcedIn2Sv")))
    admin_mfa_missing = sum(1 for row in admin_rows if not bool(row.get("isEnrolledIn2Sv")))
    admin_mfa_enforcement_missing = sum(1 for row in admin_rows if not bool(row.get("isEnforcedIn2Sv")))
    mfa_missing = max(0, active_total - mfa_enrolled)
    enforced_missing = max(0, active_total - mfa_enforced)
    status = "missing" if mfa_missing or enforced_missing or admin_mfa_enforcement_missing else "observed"
    priority = "high" if mfa_missing or enforced_missing or admin_mfa_enforcement_missing else "low"
    reference_time = _reference_time(collected_at)
    stale_threshold = reference_time - timedelta(days=90)
    new_threshold = reference_time - timedelta(days=30)
    never_logged_in = sum(1 for row in active_rows if str(row.get("lastLoginTime") or "").startswith("1970-01-01"))
    parsed_logins = [_parse_google_time(row.get("lastLoginTime")) for row in active_rows]
    inactive_90_days = sum(1 for login_time in parsed_logins if login_time is not None and login_time < stale_threshold)
    login_unknown = sum(1 for row, login_time in zip(active_rows, parsed_logins) if "lastLoginTime" not in row and login_time is None)
    parsed_created = [_parse_google_time(row.get("creationTime")) for row in active_rows]
    created_30_days = sum(1 for created_time in parsed_created if created_time is not None and created_time >= new_threshold)
    lifecycle_status = "needs_review" if never_logged_in or inactive_90_days else "requested" if login_unknown and not any(parsed_logins) else "observed"
    lifecycle_priority = "medium" if lifecycle_status in {"needs_review", "requested"} else "low"

    evidence = [
        make_evidence_item(
            evidence_id="CONN-GW-API-MFA-001",
            title="Google Workspace official MFA enrollment and enforcement summary",
            source_system="google_workspace",
            source_type="api_read_only",
            collected_at=collected_at,
            control_area="access_mfa",
            subject="user_mfa_enrollment",
            summary=f"{mfa_enrolled} of {active_total} active Google Workspace users show 2-Step Verification enrollment; {mfa_enforced} show enforcement. User identities are not stored.",
            status=status,
            confidence="observed_from_api",
            owner_lane="msp",
            recommended_question="Can the MSP confirm Google 2-Step Verification enforcement for all users, admins, remote access, and vendor-support accounts?",
            acceptable_evidence=["Google Admin API collection timestamp", "active user count", "2SV enrollment count", "2SV enforcement count", "admin exception count", "MSP signoff"],
            next_action="Use the official Google Workspace metadata result to close MFA gaps or record owner-approved exceptions.",
            stage_id="access_offboarding_review",
            priority=priority,
            counts={
                "total_users": total,
                "active_users": active_total,
                "suspended_users": suspended,
                "mfa_enrolled": mfa_enrolled,
                "mfa_missing": mfa_missing,
                "mfa_enforced": mfa_enforced,
                "mfa_enforcement_missing": enforced_missing,
                "admin_mfa_missing": admin_mfa_missing,
                "admin_mfa_enforcement_missing": admin_mfa_enforcement_missing,
            },
            unsafe_fields_excluded=GOOGLE_UNSAFE_FIELDS,
            plain_english_summary=f"Google Workspace has {mfa_missing} active users without observed 2-Step Verification enrollment and {enforced_missing} without observed enforcement.",
            why_it_matters="Email and admin accounts are common entry points; MFA evidence gives the owner and MSP a fast way to find access gaps without exporting user identities or mailbox data.",
            reviewer_needed=["msp", "office_manager"],
            owner_view="Confirm the MSP has reviewed the Google MFA gaps and documented any owner-approved exceptions.",
            msp_view="Review Google 2-Step Verification enrollment and enforcement counts, especially admin exceptions, and return a dated evidence summary.",
        ),
        make_evidence_item(
            evidence_id="CONN-GW-API-ADMIN-001",
            title="Google Workspace official admin and suspended-user summary",
            source_system="google_workspace",
            source_type="api_read_only",
            collected_at=collected_at,
            control_area="admin_access",
            subject="admin_account_review",
            summary=f"{admins} active Google Workspace admin users were counted through the official Directory API: {super_admins} super-admin and {delegated_admins} delegated-admin flags observed. Row-level identities are not stored.",
            status="needs_review" if admins > 2 else "observed",
            confidence="observed_from_api",
            owner_lane="msp",
            recommended_question="Can the MSP confirm admin role need, break-glass handling, shared-account exceptions, and terminated-user handling?",
            acceptable_evidence=["Google Admin API collection timestamp", "super-admin count", "delegated-admin count", "break-glass account status", "exception list", "owner/MSP signoff"],
            next_action="Review official Google admin-role counts with the MSP and owner before closeout.",
            stage_id="access_offboarding_review",
            priority="medium" if admins > 2 else "low",
            counts={"total_users": total, "active_users": active_total, "admin_users": admins, "super_admin_users": super_admins, "delegated_admin_users": delegated_admins},
            unsafe_fields_excluded=GOOGLE_UNSAFE_FIELDS,
            plain_english_summary=f"Google Workspace has {admins} active admin users; Velari stored only counts, not identities.",
            why_it_matters="Admin-role sprawl makes it harder to prove who can change security settings, reset accounts, or approve vendor access.",
            reviewer_needed=["msp", "office_manager"],
            owner_view="Ask the MSP to confirm which Google admins are necessary and whether break-glass accounts are controlled.",
            msp_view="Return admin-role count evidence, exception notes, and owner signoff without sending the admin user list to Velari.",
        ),
        make_evidence_item(
            evidence_id="CONN-GW-API-LIFECYCLE-001",
            title="Google Workspace official account lifecycle summary",
            source_system="google_workspace",
            source_type="api_read_only",
            collected_at=collected_at,
            control_area="access_offboarding",
            subject="inactive_and_new_account_review",
            summary=f"{suspended} suspended Google Workspace users, {never_logged_in} active users that appear never logged in, and {inactive_90_days} active users inactive for 90+ days were counted. User identities are not stored.",
            status=lifecycle_status,
            confidence="observed_from_api" if lifecycle_status != "requested" else "unknown",
            owner_lane="msp",
            recommended_question="Can the MSP confirm offboarding, inactive account handling, new-account approvals, and whether any stale active accounts should be disabled?",
            acceptable_evidence=["Google Admin API collection timestamp", "suspended user count", "inactive account count", "new account count", "owner access-review signoff"],
            next_action="Use the lifecycle counts to drive an MSP access review instead of asking the practice to manually enter user details.",
            stage_id="access_offboarding_review",
            priority=lifecycle_priority,
            counts={
                "total_users": total,
                "active_users": active_total,
                "suspended_users": suspended,
                "never_logged_in_active_users": never_logged_in,
                "inactive_90_day_active_users": inactive_90_days,
                "new_30_day_active_users": created_30_days,
                "login_metadata_unknown_active_users": login_unknown,
            },
            unsafe_fields_excluded=GOOGLE_UNSAFE_FIELDS,
            plain_english_summary=f"Google Workspace lifecycle evidence found {suspended} suspended users and {inactive_90_days + never_logged_in} active accounts that need an access-review question.",
            why_it_matters="Inactive or never-used active accounts can hide missed offboarding, shared-account workarounds, or accounts that no longer need access.",
            reviewer_needed=["msp", "office_manager"],
            owner_view="Have the MSP confirm stale and newly created Google accounts during the access review.",
            msp_view="Review suspended, inactive, never-login, and newly created account counts and provide a reference-only access-review signoff.",
        ),
    ]
    return build_bundle(
        connector="google_workspace_api",
        mode="oauth_read_only_metadata",
        input_ref=domain or customer,
        evidence=evidence,
        generated_at=collected_at,
    )
