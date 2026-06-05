from __future__ import annotations

import hashlib
import re
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from .answer_standard import build_action_packet, flattened_output_views
from .evidence_lifecycle import build_evidence_lifecycle, normalize_lifecycle_status
from .external_precheck import (
    EXTERNAL_PRECHECK_SECTION,
    external_finding_id,
    external_finding_owner,
    external_finding_severity,
    external_finding_title,
    external_precheck_findings,
)


SCHEMA_VERSION = "2026-05-19"


SECTION_MODEL = [
    {
        "id": "executive_scorecard",
        "title": "Executive Scorecard",
        "artifact": "readiness-review.md",
        "source_modules": ["readiness"],
    },
    {
        "id": "ai_findings",
        "title": "AI Findings",
        "artifact": "ai-workflow-review.md",
        "source_modules": ["ai_workflows"],
    },
    {
        "id": "vendor_baa_exposure",
        "title": "Vendor/BAA Exposure",
        "artifact": "vendor-baa-review.md",
        "source_modules": ["vendors"],
    },
    {
        "id": "ephi_map_lite",
        "title": "ePHI Map Lite",
        "artifact": "ephi-flow-map.md",
        "source_modules": ["systems", "flows"],
    },
    {
        "id": "access_mfa_offboarding",
        "title": "Access, MFA, and Offboarding",
        "artifact": "readiness-review.md",
        "source_modules": ["readiness"],
    },
    {
        "id": "downtime_ransomware",
        "title": "Downtime and Ransomware",
        "artifact": "downtime-ransomware-tabletop.md",
        "source_modules": ["downtime"],
    },
    {
        "id": "connected_device_inventory",
        "title": "Connected Device Inventory",
        "artifact": "connected-device-inventory.md",
        "source_modules": ["systems", "downtime"],
    },
    {
        "id": "portal_api_flow_review",
        "title": "Portal and API Flow Review",
        "artifact": "portal-api-flow-review.md",
        "source_modules": ["systems", "flows", "vendors"],
    },
    {
        "id": "incident_decision_log",
        "title": "Incident Decision Log",
        "artifact": "incident-decision-log.md",
        "source_modules": ["downtime", "handoff_questions", "packet_notice"],
    },
    {
        "id": "incident_evidence_timeline",
        "title": "Incident Evidence Timeline",
        "artifact": "incident-evidence-timeline.md",
        "source_modules": ["incident_timeline", "downtime", "evidence"],
    },
    {
        "id": "incident_after_action",
        "title": "Incident After-Action Report",
        "artifact": "incident-after-action-report.md",
        "source_modules": ["incident_timeline", "downtime", "readiness"],
    },
    {
        "id": "external_evidence_precheck",
        "title": "External Evidence Pre-Check",
        "artifact": "external-evidence-precheck.md",
        "source_modules": ["external_precheck"],
    },
    {
        "id": "evidence_index",
        "title": "Evidence Index",
        "artifact": "evidence-binder-index.md",
        "source_modules": ["evidence", "flows", "vendors"],
    },
    {
        "id": "owner_msp_handoff",
        "title": "Owner/MSP Handoff",
        "artifact": "owner-msp-handoff.md",
        "source_modules": ["readiness", "vendors", "downtime"],
    },
    {
        "id": "roadmap_30_60_90",
        "title": "30/60/90 Roadmap",
        "artifact": "30-60-90-roadmap.md",
        "source_modules": ["readiness"],
    },
    {
        "id": "limitations_appendix",
        "title": "Limitations Appendix",
        "artifact": "limitations-appendix.md",
        "source_modules": ["packet_notice"],
    },
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slug(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_").lower()
    return cleaned or "packet"


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def profile_hash(profile_path: Path) -> str:
    return sha256_file(profile_path)


def safe_profile_ref(profile_path: Path) -> str:
    """Return a non-absolute source profile reference for manifests."""
    try:
        rel = profile_path.resolve().relative_to(Path.cwd().resolve())
        return rel.as_posix()
    except ValueError:
        return profile_path.name


def normalized_evidence_status(raw: Any) -> str:
    return normalize_lifecycle_status(raw)


def artifact_entry(out_dir: Path, name: str) -> dict[str, Any]:
    path = out_dir / name
    return {
        "path": name,
        "media_type": "text/html" if name.endswith(".html") else "text/markdown",
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
        "hash_scope": "file_bytes",
    }


def section_entries(out_dir: Path) -> list[dict[str, Any]]:
    sections = []
    for item in SECTION_MODEL:
        artifact = item["artifact"]
        status = "generated" if artifact and (out_dir / artifact).exists() else "planned"
        sections.append(
            {
                "id": item["id"],
                "title": item["title"],
                "status": status,
                "artifact_refs": [artifact] if status == "generated" and artifact else [],
                "source_modules": item["source_modules"],
            }
        )
    return sections


def evidence_references(profile: dict[str, Any], generated_date: date) -> list[dict[str, Any]]:
    return build_evidence_lifecycle(profile, generated_date)


def finding_entries(profile: dict[str, Any], risk: str, gaps: list[str]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    readiness_severity = "high" if risk == "High" else "medium" if risk == "Medium" else "low"
    for index, gap in enumerate(gaps, start=1):
        packet = build_action_packet(
            finding_id=f"READINESS-{index:03d}",
            section_id="executive_scorecard",
            severity=readiness_severity,
            title=gap.rstrip("."),
            owner="Practice owner/MSP",
            evidence_refs=[],
            service_context="Readiness review",
        )
        findings.append(
            {
                **packet,
                **flattened_output_views(packet),
                "section_id": "executive_scorecard",
                "severity": readiness_severity,
            }
        )

    for workflow in profile.get("ai_workflows", []):
        if workflow.get("decision") != "allowed":
            severity = "high" if workflow.get("decision") == "prohibited" else "medium"
            packet = build_action_packet(
                finding_id=f"AI-{slug(str(workflow['name'])).upper()}",
                section_id="ai_findings",
                severity=severity,
                title=f"AI workflow requires action: {workflow['name']}",
                owner="Practice owner",
                evidence_refs=["AI-POLICY"],
                service_context="AI workflow review",
            )
            findings.append(
                {
                    **packet,
                    **flattened_output_views(packet),
                    "section_id": "ai_findings",
                    "severity": severity,
                }
            )

    for vendor in profile.get("vendors", []):
        if vendor.get("touches_ephi") and vendor.get("baa_status") != "signed":
            severity = str(vendor.get("risk", "medium"))
            packet = build_action_packet(
                finding_id=f"VENDOR-{slug(str(vendor['name'])).upper()}",
                section_id="vendor_baa_exposure",
                severity=severity,
                title=f"BAA status needs review for {vendor['name']}",
                owner="Practice manager",
                evidence_refs=[f"VENDOR-{slug(str(vendor['name'])).upper()}"],
                service_context="Vendor/BAA review",
            )
            findings.append(
                {
                    **packet,
                    **flattened_output_views(packet),
                    "section_id": "vendor_baa_exposure",
                    "severity": severity,
                }
            )

    for index, item in enumerate(external_precheck_findings(profile), start=1):
        finding_id = external_finding_id(item, index)
        severity = external_finding_severity(item)
        packet = build_action_packet(
            finding_id=finding_id,
            section_id=EXTERNAL_PRECHECK_SECTION,
            stage_id=EXTERNAL_PRECHECK_SECTION,
            severity=severity,
            title=external_finding_title(item),
            owner=external_finding_owner(item, profile),
            evidence_refs=[finding_id],
            service_context="External evidence pre-check",
        )
        findings.append(
            {
                **packet,
                **flattened_output_views(packet),
                "section_id": EXTERNAL_PRECHECK_SECTION,
                "severity": severity,
            }
        )

    return findings


def roadmap_entries(gaps: list[str]) -> list[dict[str, Any]]:
    items = gaps or ["Review generated packet with practice owner and MSP."]
    entries = []
    for index, item in enumerate(items[:3], start=1):
        entries.append({"horizon": "30_days", "priority": index, "action": item, "owner": "Practice owner/MSP"})
    for index, item in enumerate(items[3:6], start=1):
        entries.append({"horizon": "60_days", "priority": index, "action": item, "owner": "Practice owner/MSP"})
    for index, item in enumerate(
        [
            "Run a tabletop exercise and record lessons learned.",
            "Repeat access, vendor, and backup evidence review.",
            "Prepare management signoff packet.",
        ],
        start=1,
    ):
        entries.append({"horizon": "90_days", "priority": index, "action": item, "owner": "Practice owner/MSP"})
    return entries


def build_packet_manifest(
    profile: dict[str, Any],
    profile_path: Path,
    out_dir: Path,
    artifact_names: list[str],
    risk: str,
    gaps: list[str],
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or utc_now()
    generated_date = date.fromisoformat(generated_at[:10])
    practice = profile["practice"]
    review_period_slug = slug(str(practice["review_period"]))
    practice_slug = slug(str(practice["name"]))

    return {
        "schema_version": SCHEMA_VERSION,
        "packet_id": f"pkt_{practice_slug}_{review_period_slug}",
        "generated_at": generated_at,
        "generator": {
            "name": "small-practice-security-kit",
            "mode": "local_packet_builder",
        },
        "practice": {
            "label": str(practice["name"]),
            "type": str(practice["type"]),
            "review_period": str(practice["review_period"]),
            "staff_count": practice["staff_count"],
            "locations": practice["locations"],
        },
        "data_boundary": {
            "classification": "synthetic_or_client_reference_metadata_only",
            "phi_allowed": False,
            "secrets_allowed": False,
            "raw_evidence_allowed": False,
        },
        "source_profile": {
            "path": safe_profile_ref(profile_path),
            "sha256": profile_hash(profile_path),
        },
        "overall_risk": risk.lower(),
        "sections": section_entries(out_dir),
        "evidence_references": evidence_references(profile, generated_date),
        "findings": finding_entries(profile, risk, gaps),
        "roadmap_items": roadmap_entries(gaps),
        "artifacts": [artifact_entry(out_dir, name) for name in artifact_names],
        "limitations": [
            "Operational planning aid only.",
            "Not legal advice, not legal or regulatory status, not an incident reporting decision, not penetration testing, vulnerability scanning, MDR, SOC, or a formal Security Risk Analysis.",
            "Evidence references must not include PHI, patient identifiers, production secrets, private URLs, or raw restricted evidence.",
        ],
    }
