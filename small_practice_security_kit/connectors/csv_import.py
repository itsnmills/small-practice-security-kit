from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .base import build_bundle, make_evidence_item, utc_now


def _truthy(value: Any) -> bool:
    return str(value or "").strip().lower() in {"true", "yes", "y", "1", "enabled", "enforced", "active", "signed", "current", "ok", "pass"}


def _has_value(value: Any) -> bool:
    return bool(str(value or "").strip())


def _norm(value: str) -> str:
    return value.strip().lower().replace(" ", "_").replace("-", "_")


def _value(row: dict[str, str], *names: str) -> str:
    normalized = {_norm(key): value for key, value in row.items()}
    for name in names:
        if _norm(name) in normalized:
            return normalized[_norm(name)]
    return ""


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _infer_users_import_type(rows: list[dict[str, str]], csv_path: Path) -> str:
    headers = {_norm(key) for row in rows for key in row}
    filename = csv_path.name.lower()
    google_signals = {
        "is_2sv_enrolled",
        "is_2sv_enforced",
        "2sv_enrolled",
        "2sv_enforced",
        "is_delegated_admin",
    }
    microsoft_signals = {
        "user_principal_name",
        "mfa_status",
        "mfa_registered",
        "strong_authentication_registered",
        "admin_roles",
        "directory_roles",
    }
    looks_google = bool(headers & google_signals) or "google" in filename or "workspace" in filename
    looks_microsoft = bool(headers & microsoft_signals) or "microsoft" in filename or "m365" in filename or "entra" in filename
    if looks_google and not looks_microsoft:
        return "google-users"
    if looks_microsoft and not looks_google:
        return "microsoft-users"
    raise ValueError(
        "CSV import type 'users' needs a recognizable Google Workspace or Microsoft 365 export. "
        "Use 'google-users' or 'microsoft-users' when the file is ambiguous."
    )


def _status_priority(count: int, *, medium_threshold: int = 1) -> tuple[str, str]:
    if count <= 0:
        return "observed", "low"
    if count >= medium_threshold:
        return "missing", "high"
    return "needs_review", "medium"


def _google_users(rows: list[dict[str, str]], collected_at: str) -> list[dict[str, Any]]:
    total = len(rows)
    admins = sum(1 for row in rows if _truthy(_value(row, "is_admin", "admin", "is_delegated_admin")))
    suspended = sum(1 for row in rows if _truthy(_value(row, "suspended", "is_suspended")))
    mfa_enrolled = sum(1 for row in rows if _truthy(_value(row, "is_2sv_enrolled", "2sv_enrolled", "mfa_enrolled")))
    mfa_enforced = sum(1 for row in rows if _truthy(_value(row, "is_2sv_enforced", "2sv_enforced", "mfa_enforced")))
    mfa_missing = max(0, total - mfa_enrolled)
    enforced_missing = max(0, total - mfa_enforced)
    status, priority = _status_priority(mfa_missing + enforced_missing)
    return [
        make_evidence_item(
            evidence_id="CONN-GW-MFA-001",
            title="Google Workspace MFA enrollment and enforcement summary",
            source_system="google_workspace",
            source_type="csv_import",
            collected_at=collected_at,
            control_area="access_mfa",
            subject="user_mfa_enrollment",
            summary=f"{mfa_enrolled} of {total} users show 2-Step Verification enrollment; {mfa_enforced} show enforcement. No user emails are stored in this packet.",
            status=status,
            confidence="imported_from_client_export",
            owner_lane="msp",
            recommended_question="Can the MSP confirm 2-Step Verification is enforced for all users, admins, remote access, and vendor-support accounts?",
            acceptable_evidence=["Google Admin 2SV enrollment export", "OU enforcement setting", "exception list", "date observed", "MSP attestation"],
            next_action="Ask the MSP to remediate missing Google 2SV enrollment or enforcement and document any exceptions.",
            stage_id="access_offboarding_review",
            priority=priority,
            counts={"total_users": total, "mfa_enrolled": mfa_enrolled, "mfa_missing": mfa_missing, "mfa_enforced": mfa_enforced, "mfa_enforcement_missing": enforced_missing},
        ),
        make_evidence_item(
            evidence_id="CONN-GW-ADMIN-001",
            title="Google Workspace admin and suspended-user summary",
            source_system="google_workspace",
            source_type="csv_import",
            collected_at=collected_at,
            control_area="admin_access",
            subject="admin_account_review",
            summary=f"{admins} admin users and {suspended} suspended users were counted from the Google export. No row-level identities are stored.",
            status="needs_review" if admins > 2 else "observed",
            confidence="imported_from_client_export",
            owner_lane="msp",
            recommended_question="Can the MSP confirm admin roles, break-glass accounts, shared-account exceptions, and terminated-user handling?",
            acceptable_evidence=["admin role export", "suspended user count", "owner signoff", "exception list", "date observed"],
            next_action="Review admin counts with the owner and MSP, then record signoff or remediation tasks.",
            stage_id="access_offboarding_review",
            priority="medium" if admins > 2 else "low",
            counts={"total_users": total, "admin_users": admins, "suspended_users": suspended},
        ),
    ]


def _microsoft_users(rows: list[dict[str, str]], collected_at: str) -> list[dict[str, Any]]:
    total = len(rows)
    enabled = sum(1 for row in rows if not _value(row, "account_enabled", "enabled") or _truthy(_value(row, "account_enabled", "enabled")))
    guests = sum(1 for row in rows if str(_value(row, "user_type", "type")).strip().lower() == "guest")
    admins = sum(1 for row in rows if _has_value(_value(row, "admin_roles", "roles", "directory_roles")))
    mfa_ready = sum(1 for row in rows if _truthy(_value(row, "mfa_status", "mfa_registered", "strong_authentication_registered")))
    mfa_missing = max(0, enabled - mfa_ready)
    status, priority = _status_priority(mfa_missing)
    return [
        make_evidence_item(
            evidence_id="CONN-M365-MFA-001",
            title="Microsoft 365 MFA registration summary",
            source_system="microsoft_365",
            source_type="csv_import",
            collected_at=collected_at,
            control_area="access_mfa",
            subject="user_mfa_registration",
            summary=f"{mfa_ready} of {enabled} enabled users show MFA registration in the import. User principal names are not stored.",
            status=status,
            confidence="imported_from_client_export",
            owner_lane="msp",
            recommended_question="Can the MSP confirm MFA or Conditional Access enforcement for all users, admins, remote access, and vendor-support accounts?",
            acceptable_evidence=["Entra MFA registration export", "Conditional Access policy summary", "admin role export", "exception list", "date observed"],
            next_action="Ask the MSP to close any Microsoft 365 MFA gaps and document exceptions.",
            stage_id="access_offboarding_review",
            priority=priority,
            counts={"enabled_users": enabled, "mfa_registered": mfa_ready, "mfa_missing": mfa_missing},
        ),
        make_evidence_item(
            evidence_id="CONN-M365-ADMIN-001",
            title="Microsoft 365 admin and guest account summary",
            source_system="microsoft_365",
            source_type="csv_import",
            collected_at=collected_at,
            control_area="admin_access",
            subject="admin_guest_review",
            summary=f"{admins} users have admin role values and {guests} guest users were counted. Row-level identities are kept in the private source export only.",
            status="needs_review" if admins > 2 or guests > 0 else "observed",
            confidence="imported_from_client_export",
            owner_lane="msp",
            recommended_question="Can the MSP confirm admin role need, guest user ownership, external access, and offboarding evidence?",
            acceptable_evidence=["admin role export", "guest user export", "owner signoff", "exception list", "date observed"],
            next_action="Review Microsoft admin and guest accounts with the MSP and owner before closeout.",
            stage_id="access_offboarding_review",
            priority="medium" if admins > 2 or guests > 0 else "low",
            counts={"admin_users": admins, "guest_users": guests, "total_users": total},
        ),
    ]


def _devices(rows: list[dict[str, str]], collected_at: str) -> list[dict[str, Any]]:
    total = len(rows)
    encrypted = sum(1 for row in rows if _truthy(_value(row, "encrypted", "disk_encryption", "encryption_status")))
    edr_ok = sum(1 for row in rows if _truthy(_value(row, "edr_status", "endpoint_protection", "av_status")))
    patch_current = sum(1 for row in rows if _truthy(_value(row, "patch_status", "patch_current", "up_to_date")))
    missing = (total - encrypted) + (total - edr_ok) + (total - patch_current)
    status, priority = _status_priority(missing)
    return [
        make_evidence_item(
            evidence_id="CONN-DEVICE-POSTURE-001",
            title="Device encryption, endpoint protection, and patch summary",
            source_system="msp_or_rmm_export",
            source_type="csv_import",
            collected_at=collected_at,
            control_area="device_security",
            subject="device_inventory_posture",
            summary=f"{total} devices imported; {encrypted} encrypted, {edr_ok} with endpoint protection marked OK, and {patch_current} marked patch-current.",
            status=status,
            confidence="imported_from_msp_export",
            owner_lane="msp",
            recommended_question="Can the MSP confirm encryption, endpoint protection, patch scope, and excluded devices for all systems supporting patient-data workflows?",
            acceptable_evidence=["RMM inventory export", "encryption status summary", "EDR coverage summary", "patch status report", "excluded device list"],
            next_action="Ask the MSP to remediate missing device controls or provide an exception list with owner signoff.",
            stage_id="access_offboarding_review",
            priority=priority,
            counts={"total_devices": total, "encrypted": encrypted, "edr_ok": edr_ok, "patch_current": patch_current, "missing_control_count": missing},
        )
    ]


def _backup_report(rows: list[dict[str, str]], collected_at: str) -> list[dict[str, Any]]:
    total = len(rows)
    successful = sum(1 for row in rows if _truthy(_value(row, "backup_status", "status", "last_backup_status")))
    restore_tested = sum(1 for row in rows if _has_value(_value(row, "restore_test_date", "last_restore_test", "restore_tested_at")))
    missing = (total - successful) + (total - restore_tested)
    status, priority = _status_priority(missing)
    return [
        make_evidence_item(
            evidence_id="CONN-BACKUP-RESTORE-001",
            title="Backup scope and restore-test summary",
            source_system="backup_or_msp_export",
            source_type="csv_import",
            collected_at=collected_at,
            control_area="backup_recovery",
            subject="backup_restore_testing",
            summary=f"{successful} of {total} systems show successful backup status; {restore_tested} include a restore-test date.",
            status=status,
            confidence="imported_from_msp_export",
            owner_lane="msp",
            recommended_question="Can the MSP confirm backup scope, last restore-test date, recovery owner, excluded systems, and next test date?",
            acceptable_evidence=["backup scope summary", "restore-test note", "systems included", "systems excluded", "date observed"],
            next_action="Ask the MSP to schedule or document restore testing for systems without current evidence.",
            stage_id="downtime_ransomware_review",
            priority=priority,
            counts={"systems": total, "successful_backups": successful, "restore_test_dates": restore_tested, "missing_or_untested": missing},
        )
    ]


def _vendor_register(rows: list[dict[str, str]], collected_at: str) -> list[dict[str, Any]]:
    total = len(rows)
    touches_ephi = sum(1 for row in rows if _truthy(_value(row, "touches_ephi", "phi_access", "ephi")))
    baa_signed = sum(1 for row in rows if _truthy(_value(row, "baa_status", "baa_signed", "baa")))
    ai_terms = sum(1 for row in rows if _has_value(_value(row, "ai_data_use", "model_training", "ai_terms")))
    missing_baa = max(0, touches_ephi - baa_signed)
    status, priority = _status_priority(missing_baa)
    return [
        make_evidence_item(
            evidence_id="CONN-VENDOR-BAA-001",
            title="Vendor BAA and AI/data-use evidence summary",
            source_system="vendor_register_import",
            source_type="csv_import",
            collected_at=collected_at,
            control_area="vendor_baa_ai",
            subject="vendor_baa_ai_terms",
            summary=f"{total} vendors imported; {touches_ephi} marked as touching ePHI, {baa_signed} with signed BAA status, and {ai_terms} with AI/data-use terms recorded.",
            status=status,
            confidence="imported_from_client_export",
            owner_lane="vendor",
            recommended_question="Can vendor owners confirm PHI access, BAA status, incident terms, subprocessors, retention/deletion, and AI/customer-data use?",
            acceptable_evidence=["vendor register", "BAA status", "SOC 2 or HITRUST status", "incident terms", "retention/deletion terms", "AI/data-use response"],
            next_action="Route missing BAA or AI/data-use answers to vendor owners and qualified reviewers without uploading raw contracts.",
            stage_id="vendor_baa_review",
            priority=priority,
            counts={"vendors": total, "touches_ephi": touches_ephi, "baa_signed": baa_signed, "missing_baa": missing_baa, "ai_terms_recorded": ai_terms},
        )
    ]


IMPORTERS = {
    "google-users": ("csv_google_users", "client_export_import", _google_users),
    "microsoft-users": ("csv_microsoft_users", "client_export_import", _microsoft_users),
    "devices": ("csv_device_inventory", "msp_export_import", _devices),
    "backup-report": ("csv_backup_report", "msp_export_import", _backup_report),
    "vendor-register": ("csv_vendor_register", "client_export_import", _vendor_register),
}


def collect_csv_import(import_type: str, csv_path: Path, *, generated_at: str | None = None) -> dict[str, Any]:
    collected_at = generated_at or utc_now()
    rows = _read_rows(csv_path)
    if not rows:
        raise ValueError(f"CSV import has no rows: {csv_path}")
    resolved_import_type = _infer_users_import_type(rows, csv_path) if import_type == "users" else import_type
    if resolved_import_type not in IMPORTERS:
        supported = ", ".join(sorted([*IMPORTERS, "users"]))
        raise ValueError(f"unsupported CSV import type '{import_type}'. Supported types: {supported}")
    connector, mode, importer = IMPORTERS[resolved_import_type]
    evidence = importer(rows, collected_at)
    return build_bundle(
        connector=connector,
        mode=mode,
        input_ref=csv_path.name,
        evidence=evidence,
        generated_at=collected_at,
    )
