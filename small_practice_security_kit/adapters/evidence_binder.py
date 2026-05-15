from __future__ import annotations

import csv
from pathlib import Path

from ..exchange import ExchangeRecord, records_to_csv, records_to_markdown
from ..profile import load_profile, slugify


BINDER_FIELDS = [
    "evidence_id",
    "section",
    "evidence_type",
    "owner_role",
    "priority",
    "review_frequency",
    "evidence_needed",
    "evidence_reference",
    "source_mapping",
    "share_safety",
    "notes",
]


def _binder_row(
    evidence_id: str,
    section: str,
    evidence_type: str,
    owner_role: str,
    priority: str,
    review_frequency: str,
    evidence_needed: str,
    evidence_reference: str,
    source_mapping: str,
    notes: str,
    share_safety: str = "internal_restricted",
) -> dict[str, str]:
    return {
        "evidence_id": evidence_id,
        "section": section,
        "evidence_type": evidence_type,
        "owner_role": owner_role,
        "priority": priority,
        "review_frequency": review_frequency,
        "evidence_needed": evidence_needed,
        "evidence_reference": evidence_reference,
        "source_mapping": source_mapping,
        "share_safety": share_safety,
        "notes": notes,
    }


def build_binder_rows(profile: dict) -> list[dict[str, str]]:
    practice = profile["practice"]
    rows: list[dict[str, str]] = []
    for flow in profile["flows"]:
        rows.append(
            _binder_row(
                evidence_id=f"FLOW-{flow['id']}",
                section="03_ephi_systems_data_flows/ephi_flow_register.md",
                evidence_type="ephi_flow_register",
                owner_role=practice["technical_owner"],
                priority=flow["risk"],
                review_frequency="quarterly",
                evidence_needed=flow["evidence_needed"],
                evidence_reference=f"restricted-evidence/ephi-flows/{flow['id']}.md",
                source_mapping="HHS Risk Analysis Guidance; NIST SP 800-66 Rev. 2",
                notes=f"{flow['source']} to {flow['destination']} via {flow['transmission']}",
            )
        )
    for vendor in profile["vendors"]:
        priority = "high" if vendor["risk"] == "high" or "missing" in vendor["baa_status"].lower() else vendor["risk"]
        rows.append(
            _binder_row(
                evidence_id=f"VENDOR-{vendor['name'].upper().replace(' ', '-')}",
                section="07_vendors_baas/vendor_baa_register.md",
                evidence_type="vendor_baa_register",
                owner_role=practice["security_owner"],
                priority=priority,
                review_frequency="quarterly",
                evidence_needed=f"BAA, security contact, AI data-use review, and incident terms for {vendor['name']}",
                evidence_reference=f"restricted-evidence/vendors/{vendor['name'].lower().replace(' ', '-')}.md",
                source_mapping="HIPAA Business Associate Requirements; NIST SP 800-66 Rev. 2",
                notes=f"BAA status: {vendor['baa_status']}; AI training use: {vendor['ai_training_use']}",
            )
        )
    rows.extend(
        [
            _binder_row("ACCESS-QTR", "04_access/access_review.md", "access_review", practice["security_owner"], "critical", "quarterly", "Quarterly access review for EHR, billing, email, remote access, and administrator accounts", "restricted-evidence/access/quarterly-access-review.xlsx", "HIPAA Security Rule; NIST SP 800-66 Rev. 2", "Generated from readiness profile"),
            _binder_row("BACKUP-RESTORE", "06_backups_downtime_incidents/backup_restore_test.md", "backup_restore_test", practice["technical_owner"], "critical", "quarterly", "Restore test record for EHR, billing, shared drive, phone system, and key workstation", "restricted-evidence/backups/restore-test.md", "HIPAA Security Rule Contingency Plan; CISA CPG", "Generated from downtime profile"),
            _binder_row("DOWNTIME-TABLETOP", "06_backups_downtime_incidents/downtime_drill.md", "downtime_drill", practice["security_owner"], "high", "annual", "Downtime tabletop and patient-safety continuity walkthrough", "restricted-evidence/downtime/tabletop.md", "HIPAA Security Rule Contingency Plan; HHS HPH CPG", "Generated from downtime profile"),
            _binder_row("AI-POLICY", "05-ai-workflow-review", "ai_workflow_policy", practice["security_owner"], "high", "annual", "Allowed/prohibited AI use guidance and staff acknowledgement", "restricted-evidence/ai/ai-workflow-guidance.md", "HIPAA Security Rule; NIST AI RMF; HHS HPH CPG", "Use as a companion evidence reference until binder has a dedicated AI section"),
            _binder_row("LOG-REVIEW", "10_monitoring/log_review_record.md", "log_review_record", practice["technical_owner"], "high", "monthly", "Monthly log review record for email, EHR, remote access, endpoint, and firewall events", "restricted-evidence/monitoring/monthly-log-review.md", "HIPAA Audit Controls; CISA CPG", "Generated from readiness profile"),
            _binder_row("MGMT-SIGNOFF", "11_reviews_signoffs/management_review_signoff.md", "management_review_signoff", "Practice Owner", "critical", "quarterly", "Management signoff on open gaps, evidence status, and 30/60/90 roadmap", "restricted-evidence/signoff/management-review.md", "HIPAA documentation requirements; NIST SP 800-66 Rev. 2", "Generated from review packet"),
        ]
    )
    return rows


def binder_rows_to_exchange(profile_path: Path, rows: list[dict[str, str]]) -> list[ExchangeRecord]:
    return [
        ExchangeRecord(
            source_repo="small-practice-security-kit",
            source_artifact=str(profile_path),
            item_id=row["evidence_id"],
            module="03-hipaa-evidence-binder",
            title=row["evidence_type"],
            status="not_started",
            risk=row["priority"],
            owner=row["owner_role"],
            evidence_needed=row["evidence_needed"],
            evidence_reference=row["evidence_reference"],
            source_mapping=row["source_mapping"],
            next_review_due="not_scheduled",
            notes=row["notes"],
        )
        for row in rows
    ]


def export_binder_index(profile_path: Path, output_dir: Path | None = None) -> Path:
    profile = load_profile(profile_path)
    output_dir = output_dir or Path("out") / slugify(profile["practice"]["name"]) / "evidence-binder-export"
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = build_binder_rows(profile)
    with (output_dir / "evidence-binder-index.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=BINDER_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    markdown = ["# Evidence Binder Export", "", "Target companion repo: `hipaa-evidence-binder-template`", "", "| Evidence ID | Section | Priority | Frequency | Evidence Needed |", "|---|---|---|---|---|"]
    for row in rows:
        markdown.append(f"| {row['evidence_id']} | {row['section']} | {row['priority']} | {row['review_frequency']} | {row['evidence_needed']} |")
    (output_dir / "evidence-binder-index.md").write_text("\n".join(markdown) + "\n", encoding="utf-8")
    (output_dir / "binder-import-notes.md").write_text(
        "# Binder Import Notes\n\n"
        "This export contains evidence references and expected evidence items for the companion `hipaa-evidence-binder-template` repo. "
        "It does not include PHI, secrets, credentials, or raw evidence files. Store real evidence in approved restricted folders.\n",
        encoding="utf-8",
        newline="\n",
    )
    exchange_records = binder_rows_to_exchange(profile_path, rows)
    records_to_csv(exchange_records, output_dir / "exchange-records.csv")
    records_to_markdown(exchange_records, output_dir / "exchange-records.md", "Evidence Binder Exchange Records")
    return output_dir
