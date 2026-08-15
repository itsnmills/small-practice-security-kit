from __future__ import annotations

import csv
from pathlib import Path

from ..exchange import ExchangeRecord, records_to_csv, records_to_markdown
from ..profile import load_profile, write_profile
from ..sensitive_data import blocking_findings
from ..validation import REQUIRED_FLOW, parse_bool, validate_required_columns, validate_risk


def read_flow_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        validate_required_columns(set(reader.fieldnames or []), REQUIRED_FLOW, str(path))
        flows = []
        for index, row in enumerate(reader, start=1):
            risk = row["risk"].strip().lower()
            validate_risk(risk, f"{path} row {index} risk")
            flows.append(
                {
                    "id": row["id"].strip(),
                    "source": row["source"].strip(),
                    "destination": row["destination"].strip(),
                    "ephi_type": row["ephi_type"].strip(),
                    "vendor": row["vendor"].strip(),
                    "transmission": row["transmission"].strip(),
                    "baa_needed": parse_bool(row["baa_needed"], f"{path} row {index} baa_needed"),
                    "risk": risk,
                    "evidence_needed": row["evidence_needed"].strip(),
                }
            )
    return flows


def flow_exchange_records(csv_path: Path, flows: list[dict]) -> list[ExchangeRecord]:
    return [
        ExchangeRecord(
            source_repo="ephi-data-flow-mapper",
            source_artifact=str(csv_path),
            item_id=flow["id"],
            module="02-ephi-data-flow-map",
            title=f"{flow['source']} to {flow['destination']}",
            status="imported",
            risk=flow["risk"],
            owner="MSP Lead",
            evidence_needed=flow["evidence_needed"],
            evidence_reference=f"restricted-evidence/ephi-flows/{flow['id']}.md",
            source_mapping="HHS Risk Analysis Guidance; NIST SP 800-66 Rev. 2",
            next_review_due="not_scheduled",
            notes=f"Vendor: {flow['vendor']}; transmission: {flow['transmission']}",
        )
        for flow in flows
    ]


def import_flows(csv_path: Path, base_profile: Path, output_profile: Path, append: bool = False) -> Path:
    profile = load_profile(base_profile)
    flows = read_flow_csv(csv_path)
    profile["flows"] = [*profile["flows"], *flows] if append else flows
    # Security decision: imported CSVs are third-party data, so the same PHI/secret
    # blocker that gates API profile saves must gate this write.
    blocked = blocking_findings(profile)
    if blocked:
        joined = "; ".join(f"{finding.path}: {finding.message}" for finding in blocked[:5])
        raise ValueError(f"import contains blocked sensitive data; use references only ({joined})")
    write_profile(profile, output_profile)
    records = flow_exchange_records(csv_path, flows)
    out_dir = output_profile.parent / "ephi-flow-import"
    records_to_csv(records, out_dir / "exchange-records.csv")
    records_to_markdown(records, out_dir / "imported-ephi-flows.md", "Imported ePHI Flows")
    return output_profile
