from __future__ import annotations

import copy
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalogs" / "control_evidence_matrix.yaml"
UNSAFE_WARNING = "Do not send PHI, patient identifiers, credentials, private admin URLs, raw logs, patient screenshots, full private contracts, or incident-sensitive details."

CONTROL_EVIDENCE_FIELDNAMES = [
    "control_id",
    "control_name",
    "control_family",
    "control_refs",
    "risk_area",
    "practice_applicability",
    "evidence_id",
    "evidence_name",
    "evidence_type",
    "evidence_owner",
    "evidence_provider",
    "accountable_owner",
    "reviewer_needed",
    "evidence_status",
    "freshness_status",
    "last_collected_at",
    "last_reviewed_at",
    "effective_date",
    "cadence",
    "stale_after_days",
    "retention_years",
    "source_systems",
    "acceptable_evidence",
    "unsafe_inputs",
    "linked_answer_packet_ids",
    "next_action",
]

_OWNER_SYNONYMS = {
    "owner": {"owner", "practice_owner", "practice owner"},
    "office_manager": {"office_manager", "office manager"},
    "msp": {"msp", "technical_owner", "it", "it provider", "technical owner"},
    "vendor": {"vendor", "vendor_owner", "vendor owner"},
    "legal_compliance": {"legal", "compliance", "legal_compliance", "legal_or_compliance_reviewer"},
    "insurer": {"insurer", "cyber insurer"},
    "clinical_lead": {"clinical", "clinical_lead", "clinical lead"},
    "velari_reviewer": {"velari", "velari_reviewer"},
    "incident_responder": {"incident", "incident_responder", "incident responder"},
}


def _norm(value: Any) -> str:
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def _csv_value(value: Any) -> str:
    if isinstance(value, list):
        return "; ".join(str(item) for item in value)
    if isinstance(value, dict):
        return json.dumps(value, sort_keys=True)
    if value is None:
        return ""
    return str(value)


def load_control_evidence_catalog(path: Path | None = None) -> list[dict[str, Any]]:
    catalog_path = path or CATALOG_PATH
    data = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
    rows = data.get("controls", []) if isinstance(data, dict) else []
    if not rows:
        raise ValueError(f"control evidence catalog has no controls: {catalog_path}")
    return [copy.deepcopy(row) for row in rows]


def validate_control_evidence_row(row: dict[str, Any]) -> None:
    missing = [field for field in CONTROL_EVIDENCE_FIELDNAMES if field not in row]
    if missing:
        raise ValueError(f"control evidence row missing fields: {', '.join(missing)}")
    for field in ["control_refs", "practice_applicability", "reviewer_needed", "source_systems", "acceptable_evidence", "unsafe_inputs"]:
        if not isinstance(row.get(field), list) or not row[field]:
            raise ValueError(f"control evidence row {row.get('control_id')} has invalid {field}")
    if not row.get("control_id") or not row.get("evidence_id"):
        raise ValueError("control evidence row requires control_id and evidence_id")


def compute_freshness_status(row: dict[str, Any], generated_at: str | None = None) -> str:
    if row.get("evidence_status") == "not_applicable":
        return "not_applicable"
    if not row.get("last_reviewed_at") and not row.get("last_collected_at"):
        return "missing"
    timestamp = row.get("last_reviewed_at") or row.get("last_collected_at")
    try:
        observed = datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
        now = datetime.fromisoformat(str(generated_at).replace("Z", "+00:00")) if generated_at else datetime.now(timezone.utc)
    except ValueError:
        return "stale"
    if observed.tzinfo is None:
        observed = observed.replace(tzinfo=timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    age_days = (now - observed).days
    stale_after = int(row.get("stale_after_days") or 365)
    if age_days > stale_after:
        return "stale"
    if age_days > max(1, int(stale_after * 0.8)):
        return "due_soon"
    return "current"


def _matches_control(row: dict[str, Any], packet: dict[str, Any]) -> bool:
    haystack = " ".join(
        str(packet.get(field, ""))
        for field in ["finding_id", "action_packet_id", "title", "risk_area", "stage_id", "plain_english_summary", "next_action"]
    ).lower()
    control_id = str(row.get("control_id", "")).lower()
    risk_area = str(row.get("risk_area", "")).lower()
    control_name = str(row.get("control_name", "")).lower()
    checks = {
        "mfa": ["mfa", "multifactor", "remote access", "admin"],
        "access": ["access", "offboarding", "termination", "privileged", "break-glass"],
        "baa": ["baa", "vendor", "business associate", "subcontractor", "subprocessor"],
        "vendor": ["vendor", "baa", "soc 2", "retention", "deletion"],
        "ai": ["ai", "model", "training", "scribe", "allowed", "restricted", "prohibited"],
        "backup": ["backup", "restore", "downtime", "ransomware", "contingency"],
        "downtime": ["downtime", "ransomware", "tabletop", "incident"],
        "log": ["log", "audit", "activity"],
        "vuln": ["vulnerability", "patch", "scan", "edr", "endpoint"],
        "risk": ["risk", "corrective", "roadmap", "finding"],
        "policy": ["policy", "procedure", "training"],
        "device": ["device", "media", "physical", "encryption", "asset", "iot", "iomt"],
        "insurance": ["insurance", "insurer"],
    }
    for key, terms in checks.items():
        if key in control_id or key in risk_area or key in control_name:
            if any(term in haystack for term in terms):
                return True
    return False


def _packet_id(packet: dict[str, Any]) -> str:
    return str(packet.get("action_packet_id") or packet.get("finding_id") or packet.get("title") or "packet")


def build_control_evidence_matrix(
    profile: dict[str, Any],
    answer_packets: list[dict[str, Any]],
    *,
    generated_at: str | None = None,
) -> list[dict[str, Any]]:
    del profile
    rows = load_control_evidence_catalog()
    default_row = next((row for row in rows if row.get("control_id") == "VEL-GOV-RISK-001"), rows[0])
    packet_to_control: dict[str, set[str]] = defaultdict(set)

    for packet in answer_packets:
        packet_id = _packet_id(packet)
        matched = False
        for row in rows:
            if _matches_control(row, packet):
                row.setdefault("linked_answer_packet_ids", [])
                if packet_id not in row["linked_answer_packet_ids"]:
                    row["linked_answer_packet_ids"].append(packet_id)
                packet_to_control[packet_id].add(str(row["control_id"]))
                matched = True
        if not matched:
            default_row.setdefault("linked_answer_packet_ids", [])
            if packet_id not in default_row["linked_answer_packet_ids"]:
                default_row["linked_answer_packet_ids"].append(packet_id)
            packet_to_control[packet_id].add(str(default_row["control_id"]))

    for row in rows:
        if row.get("linked_answer_packet_ids"):
            if row.get("evidence_status") == "present":
                row["evidence_status"] = "current"
            elif row.get("evidence_status") == "gated":
                row["freshness_status"] = "missing"
            elif row.get("evidence_status") not in {"needs_professional_review", "not_applicable"}:
                row["evidence_status"] = "missing"
        row["freshness_status"] = compute_freshness_status(row, generated_at=generated_at)
        validate_control_evidence_row(row)
    return rows


def summarize_evidence_freshness(rows: list[dict[str, Any]]) -> dict[str, Any]:
    evidence_status = Counter(str(row["evidence_status"]) for row in rows)
    freshness_status = Counter(str(row["freshness_status"]) for row in rows)
    owner_counts = Counter(str(row["evidence_owner"]) for row in rows if row["freshness_status"] in {"missing", "stale", "due_soon"})
    mapped_rows = [row for row in rows if row.get("linked_answer_packet_ids")]
    return {
        "total_controls": len(rows),
        "mapped_controls": len(mapped_rows),
        "linked_answer_packets": sorted({packet_id for row in rows for packet_id in row.get("linked_answer_packet_ids", [])}),
        "by_evidence_status": dict(sorted(evidence_status.items())),
        "by_freshness_status": dict(sorted(freshness_status.items())),
        "needs_attention": sum(freshness_status.get(status, 0) for status in ["missing", "stale", "due_soon"]),
        "by_owner_needing_attention": dict(sorted(owner_counts.items())),
    }


def rows_for_owner(rows: list[dict[str, Any]], owner_lane: str) -> list[dict[str, Any]]:
    wanted = _norm(owner_lane)
    synonyms = _OWNER_SYNONYMS.get(wanted, {wanted})
    return [
        row
        for row in rows
        if _norm(row.get("evidence_owner")) in synonyms
        or _norm(row.get("evidence_provider")) in synonyms
        or _norm(row.get("accountable_owner")) in synonyms
    ]


def write_control_evidence_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CONTROL_EVIDENCE_FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: _csv_value(row.get(field, "")) for field in CONTROL_EVIDENCE_FIELDNAMES})


def render_evidence_freshness_report(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    freshness = summarize_evidence_freshness(rows)
    attention = [row for row in rows if row["freshness_status"] in {"missing", "stale", "due_soon"}][:12]
    lines = ["| Control | Owner | Evidence status | Freshness | Cadence | Next action |", "|---|---|---|---|---|---|"]
    for row in attention:
        lines.append(
            f"| {row['control_name']} | {row['evidence_owner']} | {row['evidence_status']} | {row['freshness_status']} | {row['cadence']} | {row['next_action']} |"
        )
    return f"""# Evidence Freshness Report

Practice: **{summary['practice']['label']}**

Review period: **{summary['practice']['review_period']}**

This report maps Velari action packets to dated evidence expectations. It supports readiness review and professional assessment; it does not provide legal advice, establish legal or regulatory status, guarantee insurer acceptance, or replace a formal Security Risk Analysis.

## Safety Boundary

{UNSAFE_WARNING}

## Summary

- Total control/evidence rows: {freshness['total_controls']}
- Mapped controls: {freshness['mapped_controls']}
- Evidence needing attention: {freshness['needs_attention']}
- Freshness statuses: {json.dumps(freshness['by_freshness_status'], sort_keys=True)}
- Evidence statuses: {json.dumps(freshness['by_evidence_status'], sort_keys=True)}

## Top Missing Or Stale Evidence

{chr(10).join(lines)}

## This Week

- Review the missing MSP-owned and vendor-owned evidence rows.
- Send `msp-evidence-request.md` and `vendor-evidence-request.md` instead of forwarding raw exports.
- Record evidence pointers, dates, owners, and reviewer notes before uploading any files.

## 30 / 60 / 90 Day Use

- 30 days: close MFA, access review, BAA, backup restore, and incident contact evidence gaps.
- 60 days: verify patch/vulnerability, log review, endpoint, device, and policy evidence.
- 90 days: refresh the matrix, review exceptions, and export a PHI-safe owner/MSP packet.
"""


def render_msp_evidence_request(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    msp_rows = rows_for_owner(rows, "msp")
    lines = ["| Evidence | Cadence | Acceptable proof | Do not send | Next action |", "|---|---|---|---|---|"]
    for row in msp_rows:
        lines.append(
            f"| {row['evidence_name']} | {row['cadence']} | {'; '.join(row['acceptable_evidence'])} | {'; '.join(row['unsafe_inputs'])} | {row['next_action']} |"
        )
    return f"""# MSP Evidence Request

Practice: **{summary['practice']['label']}**

Purpose: give the MSP a narrow evidence request list without asking for PHI, credentials, private admin URLs, or raw logs.

## Do Not Send

{UNSAFE_WARNING}

## Requested MSP Evidence

{chr(10).join(lines)}

## Preferred Response Format

- Evidence pointer or ticket/reference ID
- Source system
- Date observed
- Scope covered
- Reviewer/contact
- Exceptions and due dates

## Professional Review Boundary

This request supports readiness evidence collection. It does not ask the MSP to make legal conclusions, breach determinations, or compliance guarantees.
"""


def render_vendor_evidence_request(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    vendor_rows = rows_for_owner(rows, "vendor")
    lines = ["| Evidence | Acceptable proof | Question | Unsafe inputs |", "|---|---|---|---|"]
    for row in vendor_rows:
        lines.append(
            f"| {row['evidence_name']} | {'; '.join(row['acceptable_evidence'])} | {row['next_action']} | {'; '.join(row['unsafe_inputs'])} |"
        )
    return f"""# Vendor Evidence Request

Practice: **{summary['practice']['label']}**

Purpose: request BAA, security, incident-notification, retention/deletion, subprocessor, and AI data-use evidence without treating any vendor as approved.

## Safety Boundary

{UNSAFE_WARNING}

## Requested Vendor Evidence

{chr(10).join(lines)}

## Vendor Language

Use public evidence, gated proof, missing evidence, and professional review recommended. Do not treat this request as vendor approval, legal advice, or authorization for PHI use.
"""


def render_insurance_evidence_packet(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    priority_terms = ["mfa", "backup", "restore", "endpoint", "patch", "vulnerability", "incident", "training", "vendor"]
    selected = [row for row in rows if any(term in " ".join([row['control_id'], row['control_name'], row['risk_area']]).lower() for term in priority_terms)]
    lines = ["| Insurance area | Status | Freshness | Owner | Evidence pointer type |", "|---|---|---|---|---|"]
    for row in selected[:18]:
        lines.append(f"| {row['control_name']} | {row['evidence_status']} | {row['freshness_status']} | {row['evidence_owner']} | {row['evidence_type']} |")
    return f"""# Insurance Evidence Packet

Practice: **{summary['practice']['label']}**

Purpose: summarize evidence support for common cyber-insurance renewal topics such as MFA, backups/restores, endpoint protection, patching, vulnerability management, incident response, training, and vendor/MSP oversight.

## Limitation

This packet supports evidence collection and questionnaire preparation. It is not insurance advice, legal advice, a coverage opinion, or a guarantee of insurer acceptance.

## Safety Boundary

{UNSAFE_WARNING}

## Evidence Summary

{chr(10).join(lines)}
"""
