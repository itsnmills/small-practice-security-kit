from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .adapters.evidence_binder import export_binder_index
from .manifest import utc_now
from .packet import OUT, build_packet, risk_level
from .profile import load_profile, slugify
from .sensitive_data import blocking_findings


SPRINT_SCHEMA_VERSION = "2026-05-16"
STAGE_ORDER = [
    "intake",
    "patient_data_outside_ehr_map",
    "ai_phi_review",
    "vendor_baa_review",
    "access_offboarding_review",
    "downtime_ransomware_review",
    "findings_risk_register",
    "evidence_packet_export",
    "owner_msp_handoff",
]


@dataclass(frozen=True)
class SprintBuildResult:
    output_dir: Path
    packet_dir: Path
    binder_dir: Path
    artifacts: list[Path]


def _write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _status(has_gaps: bool, *, generated: bool = True) -> str:
    if not generated:
        return "not_started"
    return "needs_evidence" if has_gaps else "ready_for_review"


def _readiness_gap_lookup(gaps: list[str]) -> dict[str, bool]:
    lowered = " ".join(gap.lower() for gap in gaps)
    return {
        "mfa": "mfa" in lowered,
        "access": "access review" in lowered or "shared account" in lowered,
        "backup": "backup" in lowered or "restore" in lowered,
        "baa": "baa" in lowered,
        "downtime": "downtime" in lowered,
        "log": "log review" in lowered,
    }


def build_stage_statuses(profile: dict[str, Any], out_dir: Path, gaps: list[str]) -> list[dict[str, Any]]:
    gap_lookup = _readiness_gap_lookup(gaps)
    flows = profile.get("flows", [])
    vendors = profile.get("vendors", [])
    workflows = profile.get("ai_workflows", [])
    readiness = profile["readiness"]
    downtime = profile["downtime"]

    high_risk_flows = [flow for flow in flows if flow.get("risk") in {"high", "critical"}]
    ai_needs_review = [workflow for workflow in workflows if workflow.get("decision") != "allowed"]
    vendor_gaps = [
        vendor
        for vendor in vendors
        if vendor.get("touches_ephi") and str(vendor.get("baa_status", "")).strip().lower() != "signed"
    ]
    access_gaps = [
        label
        for label, present in [
            ("EHR MFA", readiness.get("mfa_ehr")),
            ("quarterly access review", readiness.get("quarterly_access_review")),
            ("unique accounts", readiness.get("unique_accounts")),
        ]
        if not present
    ]
    downtime_gaps = [
        label
        for label, present in [
            ("backup restore test evidence", readiness.get("tested_backups")),
            ("downtime plan", readiness.get("downtime_plan")),
        ]
        if not present
    ]
    if not str(downtime.get("last_restore_test", "")).strip():
        downtime_gaps.append("last restore test date")
    if "not" in str(downtime.get("tabletop_status", "")).lower():
        downtime_gaps.append("tabletop exercise record")

    stage_rows = [
        {
            "id": "intake",
            "name": "Intake",
            "status": "ready_for_review",
            "owner": profile["practice"]["security_owner"],
            "artifact_refs": ["packet-manifest.json"],
            "evidence_gap_count": 0,
            "next_action": "Confirm the practice profile, owners, review period, and no-PHI evidence-reference boundary.",
        },
        {
            "id": "patient_data_outside_ehr_map",
            "name": "Patient data outside the EHR map",
            "status": _status(bool(high_risk_flows)),
            "owner": profile["practice"]["technical_owner"],
            "artifact_refs": ["ephi-flow-map.md"],
            "evidence_gap_count": len(high_risk_flows),
            "next_action": "Confirm each high-risk flow owner, channel, BAA need, and reference-only evidence location.",
        },
        {
            "id": "ai_phi_review",
            "name": "AI/PHI review",
            "status": _status(bool(ai_needs_review)),
            "owner": profile["practice"]["security_owner"],
            "artifact_refs": ["ai-workflow-review.md"],
            "evidence_gap_count": len(ai_needs_review),
            "next_action": "Separate no-PHI administrative AI use from restricted or prohibited PHI workflows before staff rollout.",
        },
        {
            "id": "vendor_baa_review",
            "name": "Vendor/BAA review",
            "status": _status(bool(vendor_gaps) or gap_lookup["baa"]),
            "owner": profile["practice"]["security_owner"],
            "artifact_refs": ["vendor-baa-review.md"],
            "evidence_gap_count": len(vendor_gaps) + int(gap_lookup["baa"]),
            "next_action": "Collect BAA status, security contact, incident terms, subcontractor posture, and AI/data-use answers.",
        },
        {
            "id": "access_offboarding_review",
            "name": "Access/offboarding review",
            "status": _status(bool(access_gaps) or gap_lookup["access"] or gap_lookup["mfa"]),
            "owner": profile["practice"]["technical_owner"],
            "artifact_refs": ["readiness-review.md", "owner-msp-handoff.md"],
            "evidence_gap_count": len(access_gaps),
            "next_action": "Export user lists, verify MFA enforcement, and document owner signoff for access and offboarding review.",
        },
        {
            "id": "downtime_ransomware_review",
            "name": "Downtime/ransomware review",
            "status": _status(bool(downtime_gaps) or gap_lookup["backup"] or gap_lookup["downtime"]),
            "owner": profile["practice"]["technical_owner"],
            "artifact_refs": ["downtime-ransomware-tabletop.md"],
            "evidence_gap_count": len(downtime_gaps),
            "next_action": "Run or schedule a restore test and tabletop, then record reference IDs and lessons learned.",
        },
        {
            "id": "findings_risk_register",
            "name": "Findings/risk register",
            "status": "ready_for_review",
            "owner": "Practice owner/MSP",
            "artifact_refs": ["risk-register.csv", "30-60-90-roadmap.md"],
            "evidence_gap_count": len(gaps),
            "next_action": "Review top findings with the owner and assign 30-day remediation owners.",
        },
        {
            "id": "evidence_packet_export",
            "name": "Evidence packet/export",
            "status": "complete" if (out_dir / "packet-manifest.json").exists() else "not_started",
            "owner": profile["practice"]["security_owner"],
            "artifact_refs": ["review-packet.md", "review-packet.html", "packet-manifest.json", "evidence-index.json"],
            "evidence_gap_count": 0,
            "next_action": "Share generated packet artifacts only after confirming they contain references, not PHI or secrets.",
        },
        {
            "id": "owner_msp_handoff",
            "name": "Owner/MSP handoff",
            "status": "ready_for_review",
            "owner": "Practice owner/MSP",
            "artifact_refs": ["owner-msp-handoff.md", "handoff-actions.csv"],
            "evidence_gap_count": len(vendor_gaps) + len(access_gaps) + len(downtime_gaps),
            "next_action": "Use the handoff actions to collect MSP, vendor, owner, and legal/compliance reviewer responses.",
        },
    ]
    return stage_rows


def _stage_by_section(section_id: str) -> str:
    mapping = {
        "executive_scorecard": "access_offboarding_review",
        "ai_findings": "ai_phi_review",
        "vendor_baa_exposure": "vendor_baa_review",
        "ephi_map_lite": "patient_data_outside_ehr_map",
        "access_mfa_offboarding": "access_offboarding_review",
        "downtime_ransomware": "downtime_ransomware_review",
        "evidence_index": "evidence_packet_export",
        "owner_msp_handoff": "owner_msp_handoff",
        "roadmap_30_60_90": "findings_risk_register",
    }
    return mapping.get(section_id, "findings_risk_register")


def _stage_for_finding(finding: dict[str, Any]) -> str:
    title = str(finding.get("title", "")).lower()
    if "backup" in title or "restore" in title or "downtime" in title:
        return "downtime_ransomware_review"
    if "baa" in title or "vendor" in title:
        return "vendor_baa_review"
    if "ai workflow" in title or "chatbot" in title or "scribe" in title:
        return "ai_phi_review"
    if "mfa" in title or "access" in title or "account" in title:
        return "access_offboarding_review"
    return _stage_by_section(str(finding.get("section_id", "")))


def _artifact_for_stage(stage_id: str) -> str:
    mapping = {
        "patient_data_outside_ehr_map": "ephi-flow-map.md",
        "ai_phi_review": "ai-workflow-review.md",
        "vendor_baa_review": "vendor-baa-review.md",
        "access_offboarding_review": "owner-msp-handoff.md",
        "downtime_ransomware_review": "downtime-ransomware-tabletop.md",
        "evidence_packet_export": "evidence-index.json",
        "owner_msp_handoff": "owner-msp-handoff.md",
    }
    return mapping.get(stage_id, "30-60-90-roadmap.md")


def _evidence_status(evidence_refs: list[str], evidence_by_id: dict[str, dict[str, Any]]) -> str:
    if not evidence_refs:
        return "missing"
    statuses = {str(evidence_by_id.get(ref, {}).get("status", "requested")) for ref in evidence_refs}
    if "missing" in statuses:
        return "missing"
    if "outdated" in statuses:
        return "stale"
    if statuses & {"requested", "partial"}:
        return "requested"
    return "referenced"


def build_risk_register_rows(manifest: dict[str, Any]) -> list[dict[str, str]]:
    evidence_by_id = {item["evidence_id"]: item for item in manifest.get("evidence_references", [])}
    rows: list[dict[str, str]] = []
    for finding in manifest.get("findings", []):
        stage_id = _stage_for_finding(finding)
        evidence_refs = [str(ref) for ref in finding.get("evidence_refs", [])]
        rows.append(
            {
                "finding_id": str(finding.get("finding_id", "")),
                "stage_id": stage_id,
                "severity": str(finding.get("severity", "medium")),
                "title": str(finding.get("title", "")),
                "owner": str(finding.get("owner", "Practice owner/MSP")),
                "evidence_status": _evidence_status(evidence_refs, evidence_by_id),
                "evidence_refs": ";".join(evidence_refs),
                "recommended_action": _recommended_action(str(finding.get("title", "")), stage_id),
                "artifact_ref": _artifact_for_stage(stage_id),
            }
        )
    return rows


def _recommended_action(title: str, stage_id: str) -> str:
    lowered = title.lower()
    if "mfa" in lowered:
        return "Verify MFA enforcement with an admin export or MSP attestation reference."
    if "access review" in lowered:
        return "Run a quarterly user access review and record owner signoff."
    if "restore" in lowered or "backup" in lowered:
        return "Run a restore test and keep a reference-only evidence record."
    if "baa" in lowered:
        return "Confirm BAA scope, review date, incident terms, and vendor security contact."
    if stage_id == "ai_phi_review":
        return "Approve, restrict, or prohibit the workflow based on PHI use, vendor terms, and human review."
    if stage_id == "downtime_ransomware_review":
        return "Document downtime roles, manual workaround, and tabletop evidence reference."
    return "Assign an owner, collect reference-only evidence, and update the 30/60/90 roadmap."


def build_handoff_rows(profile: dict[str, Any], stages: list[dict[str, Any]], risk_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, stage in enumerate(stages, start=1):
        if stage["status"] in {"needs_evidence", "ready_for_review"}:
            rows.append(
                {
                    "action_id": f"HANDOFF-{index:03d}",
                    "audience": "owner_msp",
                    "stage_id": str(stage["id"]),
                    "priority": "high" if stage["status"] == "needs_evidence" else "medium",
                    "action": str(stage["next_action"]),
                    "evidence_ref": "",
                    "artifact_ref": str(stage["artifact_refs"][0]),
                }
            )

    for question_index, question in enumerate(profile.get("handoff_questions", []), start=1):
        rows.append(
            {
                "action_id": f"QUESTION-{question_index:03d}",
                "audience": str(question.get("audience", "owner_msp")).lower().replace(" ", "_"),
                "stage_id": str(question.get("stage_id", "owner_msp_handoff")),
                "priority": str(question.get("priority", "medium")),
                "action": str(question.get("question", question.get("action", ""))),
                "evidence_ref": str(question.get("evidence_ref", "")),
                "artifact_ref": str(question.get("artifact_ref", "owner-msp-handoff.md")),
            }
        )

    for risk in risk_rows[:5]:
        rows.append(
            {
                "action_id": f"RISK-{risk['finding_id']}",
                "audience": "owner_msp",
                "stage_id": risk["stage_id"],
                "priority": risk["severity"],
                "action": risk["recommended_action"],
                "evidence_ref": risk["evidence_refs"],
                "artifact_ref": risk["artifact_ref"],
            }
        )
    return rows


def build_evidence_index(manifest: dict[str, Any], binder_dir: Path) -> dict[str, Any]:
    return {
        "schema_version": SPRINT_SCHEMA_VERSION,
        "generated_at": manifest["generated_at"],
        "source_manifest": "packet-manifest.json",
        "data_boundary": manifest["data_boundary"],
        "binder_export": {
            "directory": binder_dir.name,
            "artifacts": [
                "evidence-binder-index.csv",
                "evidence-binder-index.md",
                "binder-import-notes.md",
                "exchange-records.csv",
                "exchange-records.md",
            ],
            "share_safety": "reference_only_no_phi_no_secret",
        },
        "evidence_references": manifest.get("evidence_references", []),
    }


def build_summary(
    profile: dict[str, Any],
    profile_path: Path,
    manifest: dict[str, Any],
    stages: list[dict[str, Any]],
    risk_rows: list[dict[str, str]],
    generated_at: str,
) -> dict[str, Any]:
    high_or_critical = [risk for risk in risk_rows if risk["severity"] in {"high", "critical"}]
    return {
        "schema_version": SPRINT_SCHEMA_VERSION,
        "sprint_id": f"sprint_{slugify(profile['practice']['name'])}_{slugify(str(profile['practice']['review_period']))}",
        "generated_at": generated_at,
        "generator": {
            "name": "small-practice-security-kit",
            "mode": "velari_sprint_mode_public_runner",
        },
        "source_profile": manifest["source_profile"] | {"input_path": profile_path.name},
        "practice": manifest["practice"],
        "overall_risk": manifest["overall_risk"],
        "data_boundary": manifest["data_boundary"],
        "stage_statuses": stages,
        "counts": {
            "stages": len(stages),
            "stages_needing_evidence": sum(1 for stage in stages if stage["status"] == "needs_evidence"),
            "findings": len(risk_rows),
            "high_or_critical_findings": len(high_or_critical),
            "evidence_references": len(manifest.get("evidence_references", [])),
        },
        "outputs": {
            "sprint": [
                "sprint-index.md",
                "sprint-summary.json",
                "risk-register.csv",
                "evidence-index.json",
                "handoff-actions.csv",
            ],
            "packet": [artifact["path"] for artifact in manifest.get("artifacts", [])],
            "binder_export": "evidence-binder-export/",
        },
        "limitations": [
            "Public Sprint Mode uses synthetic or client-supplied reference metadata only.",
            "It does not prove HIPAA compliance, provide legal advice, determine breach status, or replace a formal Security Risk Analysis.",
            "Do not include PHI, patient identifiers, credentials, secrets, private URLs, raw contracts, raw logs, or incident-sensitive details.",
        ],
    }


def render_sprint_index(summary: dict[str, Any], risk_rows: list[dict[str, str]]) -> str:
    practice = summary["practice"]
    stages = summary["stage_statuses"]
    top_risks = risk_rows[:8]
    stage_lines = [
        "| Stage | Status | Evidence gaps | Output | Next action |",
        "|---|---|---:|---|---|",
    ]
    for stage in stages:
        stage_lines.append(
            f"| {stage['name']} | {stage['status']} | {stage['evidence_gap_count']} | "
            f"{', '.join(stage['artifact_refs'])} | {stage['next_action']} |"
        )

    risk_lines = [
        "| Finding | Severity | Owner | Evidence status | Action |",
        "|---|---|---|---|---|",
    ]
    for risk in top_risks:
        risk_lines.append(
            f"| {risk['title']} | {risk['severity']} | {risk['owner']} | "
            f"{risk['evidence_status']} | {risk['recommended_action']} |"
        )
    if not top_risks:
        risk_lines.append("| No generated findings | low | Practice owner/MSP | referenced | Review packet with owner and MSP. |")

    output_lines = []
    for name in summary["outputs"]["sprint"] + summary["outputs"]["packet"]:
        output_lines.append(f"- `{name}`")
    output_lines.append("- `evidence-binder-export/`")

    return f"""# Velari Sprint Mode Index

Practice: **{practice['label']}**

Review period: **{practice['review_period']}**

Overall readiness signal: **{summary['overall_risk']}**

This public Sprint Mode packet is a local, reference-only planning aid. It does not provide legal advice, HIPAA certification, breach determination, insurer acceptance, or a formal Security Risk Analysis opinion. Do not add PHI, patient identifiers, credentials, secrets, private URLs, raw contracts, logs, or incident-sensitive details.

## Stage Status

{chr(10).join(stage_lines)}

## Top Findings

{chr(10).join(risk_lines)}

## Generated Outputs

{chr(10).join(output_lines)}

## Owner/MSP Use

- Start with `sprint-summary.json` for stage status and counts.
- Use `risk-register.csv` to assign owners and remediation priority.
- Use `evidence-index.json` and `evidence-binder-export/` to collect reference-only evidence.
- Use `owner-msp-handoff.md` and `handoff-actions.csv` to coordinate owner, MSP, vendor, and legal/compliance reviewer follow-up.
"""


def build_sprint(profile_path: Path, output_root: Path = OUT, *, generated_at: str | None = None) -> SprintBuildResult:
    generated_at = generated_at or utc_now()
    profile = load_profile(profile_path)
    sensitive_findings = blocking_findings(profile)
    if sensitive_findings:
        joined = "; ".join(f"{finding.path}: {finding.message}" for finding in sensitive_findings[:5])
        raise ValueError(f"profile contains blocked sensitive data; use references only ({joined})")

    out_dir = build_packet(profile_path, output_root, generated_at=generated_at)
    binder_dir = export_binder_index(profile_path, out_dir / "evidence-binder-export")
    risk, gaps = risk_level(profile)
    del risk

    manifest = json.loads((out_dir / "packet-manifest.json").read_text(encoding="utf-8"))
    stages = build_stage_statuses(profile, out_dir, gaps)
    risk_rows = build_risk_register_rows(manifest)
    handoff_rows = build_handoff_rows(profile, stages, risk_rows)
    evidence_index = build_evidence_index(manifest, binder_dir)
    summary = build_summary(profile, profile_path, manifest, stages, risk_rows, generated_at)

    sprint_index_path = out_dir / "sprint-index.md"
    summary_path = out_dir / "sprint-summary.json"
    risk_path = out_dir / "risk-register.csv"
    evidence_path = out_dir / "evidence-index.json"
    handoff_path = out_dir / "handoff-actions.csv"

    sprint_index_path.write_text(render_sprint_index(summary, risk_rows), encoding="utf-8", newline="\n")
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    evidence_path.write_text(json.dumps(evidence_index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_csv(
        risk_path,
        risk_rows,
        [
            "finding_id",
            "stage_id",
            "severity",
            "title",
            "owner",
            "evidence_status",
            "evidence_refs",
            "recommended_action",
            "artifact_ref",
        ],
    )
    _write_csv(
        handoff_path,
        handoff_rows,
        ["action_id", "audience", "stage_id", "priority", "action", "evidence_ref", "artifact_ref"],
    )

    return SprintBuildResult(
        output_dir=out_dir,
        packet_dir=out_dir,
        binder_dir=binder_dir,
        artifacts=[sprint_index_path, summary_path, risk_path, evidence_path, handoff_path],
    )
