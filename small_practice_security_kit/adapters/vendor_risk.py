from __future__ import annotations

import csv
from pathlib import Path

from ..exchange import ExchangeRecord, records_to_csv, records_to_markdown
from ..profile import load_profile, write_profile
from ..validation import REQUIRED_VENDOR, parse_bool, validate_required_columns, validate_risk
from ..vendor_evidence import (
    DEFAULT_EVIDENCE_STATUS,
    HITRUST_STATUS_FIELD,
    SOC2_STATUS_FIELD,
    vendor_hitrust_status,
    vendor_soc2_status,
)


def read_vendor_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        validate_required_columns(set(reader.fieldnames or []), REQUIRED_VENDOR, str(path))
        vendors = []
        for index, row in enumerate(reader, start=1):
            risk = row["risk"].strip().lower()
            validate_risk(risk, f"{path} row {index} risk")
            vendors.append(
                {
                    "name": row["name"].strip(),
                    "service": row["service"].strip(),
                    "touches_ephi": parse_bool(row["touches_ephi"], f"{path} row {index} touches_ephi"),
                    "baa_status": row["baa_status"].strip(),
                    SOC2_STATUS_FIELD: row.get(SOC2_STATUS_FIELD, "").strip() or DEFAULT_EVIDENCE_STATUS,
                    HITRUST_STATUS_FIELD: row.get(HITRUST_STATUS_FIELD, "").strip() or DEFAULT_EVIDENCE_STATUS,
                    "ai_training_use": row["ai_training_use"].strip(),
                    "subcontractors_known": row["subcontractors_known"].strip(),
                    "incident_notification_terms": row["incident_notification_terms"].strip(),
                    "risk": risk,
                }
            )
    return vendors


def vendor_exchange_records(csv_path: Path, vendors: list[dict]) -> list[ExchangeRecord]:
    return [
        ExchangeRecord(
            source_repo="vendor-risk-manager",
            source_artifact=str(csv_path),
            item_id=f"VENDOR-{vendor['name'].upper().replace(' ', '-')}",
            module="04-vendor-baa-review",
            title=vendor["name"],
            status="imported",
            risk=vendor["risk"],
            owner="Office Manager",
            evidence_needed=(
                f"BAA status, SOC 2/HITRUST status, security contact, AI data-use review, "
                f"subcontractor review, and incident terms for {vendor['name']}"
            ),
            evidence_reference=f"restricted-evidence/vendors/{vendor['name'].lower().replace(' ', '-')}.md",
            source_mapping="HIPAA Business Associate Requirements; NIST SP 800-66 Rev. 2",
            next_review_due="not_scheduled",
            notes=(
                f"BAA status: {vendor['baa_status']}; SOC 2 status: {vendor_soc2_status(vendor)}; "
                f"HITRUST status: {vendor_hitrust_status(vendor)}; AI training use: {vendor['ai_training_use']}"
            ),
        )
        for vendor in vendors
    ]


def import_vendors(csv_path: Path, base_profile: Path, output_profile: Path, append: bool = False) -> Path:
    profile = load_profile(base_profile)
    vendors = read_vendor_csv(csv_path)
    profile["vendors"] = [*profile["vendors"], *vendors] if append else vendors
    write_profile(profile, output_profile)
    records = vendor_exchange_records(csv_path, vendors)
    out_dir = output_profile.parent / "vendor-register-import"
    records_to_csv(records, out_dir / "exchange-records.csv")
    records_to_markdown(records, out_dir / "imported-vendor-register.md", "Imported Vendor Register")
    return output_profile
