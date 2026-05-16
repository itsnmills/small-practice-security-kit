from __future__ import annotations

import csv
import html
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .adapters.evidence_binder import export_binder_index
from .manifest import utc_now
from .offering import (
    build_offering_summary,
    render_day_one_workshop_agenda,
    render_evidence_collection_checklist,
    render_msp_remediation_brief,
    render_owner_action_plan,
    render_source_map,
    render_sprint_offering_readout,
    render_vendor_baa_ai_questionnaire,
)
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

SPRINT_OUTPUTS = [
    "sprint-index.md",
    "sprint-client-readout.md",
    "sprint-command-center.html",
    "sprint-offering-readout.md",
    "owner-action-plan.md",
    "msp-remediation-brief.md",
    "vendor-baa-ai-questionnaire.md",
    "evidence-collection-checklist.md",
    "day-one-workshop-agenda.md",
    "source-map.md",
    "sprint-summary.json",
    "risk-register.csv",
    "evidence-index.json",
    "handoff-actions.csv",
]

STATUS_LABELS = {
    "not_started": "Not started",
    "needs_evidence": "Needs evidence",
    "ready_for_review": "Ready for review",
    "complete": "Complete",
}


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


def _recipient_for_stage(stage_id: str) -> str:
    mapping = {
        "patient_data_outside_ehr_map": "MSP",
        "ai_phi_review": "Owner",
        "vendor_baa_review": "Vendor",
        "access_offboarding_review": "MSP",
        "downtime_ransomware_review": "MSP",
        "findings_risk_register": "Owner",
        "evidence_packet_export": "Legal/compliance reviewer",
        "owner_msp_handoff": "Owner/MSP",
    }
    return mapping.get(stage_id, "Owner/MSP")


def _audience_for_stage(stage_id: str) -> str:
    return _recipient_for_stage(stage_id).lower().replace("/", "_").replace(" ", "_")


def _roadmap_bucket_for_stage(stage_id: str, priority: str = "medium") -> str:
    if priority in {"critical", "high"}:
        return "30_days"
    if stage_id in {"vendor_baa_review", "access_offboarding_review", "downtime_ransomware_review"}:
        return "60_days"
    return "90_days"


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
                "priority": str(finding.get("severity", "medium")),
                "title": str(finding.get("title", "")),
                "owner": str(finding.get("owner", "Practice owner/MSP")),
                "audience": _audience_for_stage(stage_id),
                "recipient": _recipient_for_stage(stage_id),
                "evidence_status": _evidence_status(evidence_refs, evidence_by_id),
                "evidence_refs": ";".join(evidence_refs),
                "recommended_action": _recommended_action(str(finding.get("title", "")), stage_id),
                "artifact_ref": _artifact_for_stage(stage_id),
                "roadmap_bucket": _roadmap_bucket_for_stage(stage_id, str(finding.get("severity", "medium"))),
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
                    "recipient": _recipient_for_stage(str(stage["id"])),
                    "stage_id": str(stage["id"]),
                    "priority": "high" if stage["status"] == "needs_evidence" else "medium",
                    "owner": str(stage["owner"]),
                    "action": str(stage["next_action"]),
                    "evidence_ref": "",
                    "artifact_ref": str(stage["artifact_refs"][0]),
                    "roadmap_bucket": _roadmap_bucket_for_stage(
                        str(stage["id"]),
                        "high" if stage["status"] == "needs_evidence" else "medium",
                    ),
                }
            )

    for question_index, question in enumerate(profile.get("handoff_questions", []), start=1):
        stage_id = str(question.get("stage_id", "owner_msp_handoff"))
        audience = str(question.get("audience", "owner_msp")).lower().replace(" ", "_")
        rows.append(
            {
                "action_id": f"QUESTION-{question_index:03d}",
                "audience": audience,
                "recipient": str(question.get("audience", _recipient_for_stage(stage_id))),
                "stage_id": stage_id,
                "priority": str(question.get("priority", "medium")),
                "owner": str(question.get("owner", _recipient_for_stage(stage_id))),
                "action": str(question.get("question", question.get("action", ""))),
                "evidence_ref": str(question.get("evidence_ref", "")),
                "artifact_ref": str(question.get("artifact_ref", "owner-msp-handoff.md")),
                "roadmap_bucket": _roadmap_bucket_for_stage(stage_id, str(question.get("priority", "medium"))),
            }
        )

    for risk in risk_rows[:5]:
        rows.append(
            {
                "action_id": f"RISK-{risk['finding_id']}",
                "audience": risk["audience"],
                "recipient": risk["recipient"],
                "stage_id": risk["stage_id"],
                "priority": risk["severity"],
                "owner": risk["owner"],
                "action": risk["recommended_action"],
                "evidence_ref": risk["evidence_refs"],
                "artifact_ref": risk["artifact_ref"],
                "roadmap_bucket": risk["roadmap_bucket"],
            }
        )
    return rows


def build_evidence_gap_summary(evidence_index: dict[str, Any], stages: list[dict[str, Any]]) -> dict[str, Any]:
    references = evidence_index.get("evidence_references", [])
    status_counts: dict[str, int] = {}
    owner_counts: dict[str, int] = {}
    for item in references:
        status = str(item.get("status", "requested"))
        status_counts[status] = status_counts.get(status, 0) + 1
        if status in {"missing", "requested", "partial", "outdated"}:
            owner = str(item.get("owner", "Practice owner/MSP"))
            owner_counts[owner] = owner_counts.get(owner, 0) + 1

    return {
        "total_references": len(references),
        "needs_attention": sum(status_counts.get(status, 0) for status in ["missing", "requested", "partial", "outdated"]),
        "by_status": status_counts,
        "by_owner": owner_counts,
        "by_stage": [
            {
                "stage_id": str(stage["id"]),
                "stage_name": str(stage["name"]),
                "owner": str(stage["owner"]),
                "evidence_gap_count": int(stage["evidence_gap_count"]),
                "recipient": _recipient_for_stage(str(stage["id"])),
                "artifact_refs": list(stage["artifact_refs"]),
            }
            for stage in stages
            if int(stage["evidence_gap_count"]) > 0
        ],
    }


def build_handoff_lanes(handoff_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    lanes: dict[str, dict[str, Any]] = {}
    for row in handoff_rows:
        recipient = row["recipient"]
        lane = lanes.setdefault(
            recipient,
            {
                "recipient": recipient,
                "audience": row["audience"],
                "actions": 0,
                "high_priority_actions": 0,
                "stage_ids": [],
                "artifact_refs": [],
            },
        )
        lane["actions"] += 1
        if row["priority"] in {"critical", "high"}:
            lane["high_priority_actions"] += 1
        if row["stage_id"] not in lane["stage_ids"]:
            lane["stage_ids"].append(row["stage_id"])
        if row["artifact_ref"] not in lane["artifact_refs"]:
            lane["artifact_refs"].append(row["artifact_ref"])
    return list(lanes.values())


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
    handoff_rows: list[dict[str, str]],
    evidence_index: dict[str, Any],
    generated_at: str,
) -> dict[str, Any]:
    high_or_critical = [risk for risk in risk_rows if risk["severity"] in {"high", "critical"}]
    stages_needing_evidence = [stage for stage in stages if stage["status"] == "needs_evidence"]
    evidence_gap_summary = build_evidence_gap_summary(evidence_index, stages)
    offering_summary = build_offering_summary(profile, stages)
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
        "readiness_signal": {
            "label": manifest["overall_risk"],
            "meaning": "Evidence-backed readiness signal for sprint prioritization only; not a compliance score.",
            "high_or_critical_findings": len(high_or_critical),
            "stages_needing_evidence": len(stages_needing_evidence),
        },
        "target_delivery_signal": {
            "status": "needs_evidence_before_closeout" if stages_needing_evidence else "ready_for_client_readout",
            "primary_blocker": stages_needing_evidence[0]["next_action"] if stages_needing_evidence else "",
            "next_artifact": "sprint-command-center.html",
        },
        "data_boundary": manifest["data_boundary"],
        "stage_statuses": stages,
        "top_risks": risk_rows[:8],
        "evidence_gap_summary": evidence_gap_summary,
        "handoff_lanes": build_handoff_lanes(handoff_rows),
        "offering_summary": offering_summary,
        "counts": {
            "stages": len(stages),
            "stages_needing_evidence": sum(1 for stage in stages if stage["status"] == "needs_evidence"),
            "findings": len(risk_rows),
            "high_or_critical_findings": len(high_or_critical),
            "evidence_references": len(manifest.get("evidence_references", [])),
            "handoff_actions": len(handoff_rows),
        },
        "outputs": {
            "sprint": SPRINT_OUTPUTS,
            "packet": [artifact["path"] for artifact in manifest.get("artifacts", [])],
            "binder_export": "evidence-binder-export/",
        },
        "contract_artifacts": {
            "sprint_summary_schema": "schemas/sprint-summary.schema.json",
            "evidence_index_schema": "schemas/evidence-index.schema.json",
            "private_app_import_hint": "Import sprint-summary.json for stages/actions/offering_summary and evidence-index.json for reference-only evidence gaps.",
        },
        "limitations": [
            "Public Sprint Mode uses synthetic or client-supplied reference metadata only.",
            "It does not establish legal or regulatory status, provide legal advice, decide incident reporting duties, or replace a formal Security Risk Analysis.",
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

This public Sprint Mode packet is a local, reference-only planning aid. It does not provide legal advice, establish legal or regulatory status, decide incident reporting duties, secure insurer acceptance, or replace a formal Security Risk Analysis. Do not add PHI, patient identifiers, credentials, secrets, private URLs, raw contracts, logs, or incident-sensitive details.

## Stage Status

{chr(10).join(stage_lines)}

## Top Findings

{chr(10).join(risk_lines)}

## Generated Outputs

{chr(10).join(output_lines)}

## Owner/MSP Use

- Open `sprint-command-center.html` first for the one-page readout.
- Use `sprint-offering-readout.md` and `owner-action-plan.md` for the real-offering walkthrough.
- Use `sprint-client-readout.md` for a portable Markdown summary.
- Start with `sprint-summary.json` for stage status and counts.
- Use `risk-register.csv` to assign owners and remediation priority.
- Use `evidence-index.json` and `evidence-binder-export/` to collect reference-only evidence.
- Use `msp-remediation-brief.md`, `vendor-baa-ai-questionnaire.md`, `evidence-collection-checklist.md`, `source-map.md`, `owner-msp-handoff.md`, and `handoff-actions.csv` to coordinate owner, MSP, vendor, and legal/compliance reviewer follow-up.
"""


def render_client_readout(summary: dict[str, Any], risk_rows: list[dict[str, str]], handoff_rows: list[dict[str, str]]) -> str:
    practice = summary["practice"]
    top_risks = risk_rows[:5]
    evidence_gaps = summary["evidence_gap_summary"]["by_stage"][:6]
    handoff_lanes = summary["handoff_lanes"]

    risk_lines = [
        "| Finding | Priority | Owner | Recipient | 30/60/90 | Evidence |",
        "|---|---|---|---|---|---|",
    ]
    for risk in top_risks:
        risk_lines.append(
            f"| {risk['title']} | {risk['priority']} | {risk['owner']} | {risk['recipient']} | "
            f"{risk['roadmap_bucket']} | {risk['evidence_status']} |"
        )
    if not top_risks:
        risk_lines.append("| No generated findings | low | Practice owner/MSP | Owner/MSP | 90_days | referenced |")

    gap_lines = [
        "| Stage | Owner | Recipient | Gaps | Artifact |",
        "|---|---|---|---:|---|",
    ]
    for gap in evidence_gaps:
        gap_lines.append(
            f"| {gap['stage_name']} | {gap['owner']} | {gap['recipient']} | "
            f"{gap['evidence_gap_count']} | {', '.join(gap['artifact_refs'])} |"
        )
    if not evidence_gaps:
        gap_lines.append("| Evidence packet/export | Practice owner/MSP | Owner/MSP | 0 | evidence-index.json |")

    lane_lines = [
        "| Recipient | Actions | High priority | Artifacts |",
        "|---|---:|---:|---|",
    ]
    for lane in handoff_lanes:
        lane_lines.append(
            f"| {lane['recipient']} | {lane['actions']} | {lane['high_priority_actions']} | "
            f"{', '.join(lane['artifact_refs'])} |"
        )

    next_actions = [
        row
        for row in handoff_rows
        if row["priority"] in {"critical", "high"}
    ][:8]
    action_lines = [f"- **{row['recipient']}**: {row['action']} (`{row['artifact_ref']}`)" for row in next_actions]

    return f"""# Velari Sprint Client Readout

Practice: **{practice['label']}**

Review period: **{practice['review_period']}**

Readiness signal: **{summary['readiness_signal']['label']}**

Target delivery signal: **{summary['target_delivery_signal']['status']}**

This readout is a local, reference-only planning artifact. It does not provide legal advice, establish legal or regulatory status, decide incident reporting duties, secure insurer or vendor acceptance, authorize AI production use, or replace a formal Security Risk Analysis. Do not add PHI, patient identifiers, credentials, secrets, private URLs, raw contracts, logs, or incident-sensitive details.

## Executive Snapshot

- Stages needing evidence: {summary['counts']['stages_needing_evidence']} of {summary['counts']['stages']}
- High or critical findings: {summary['counts']['high_or_critical_findings']}
- Evidence references: {summary['counts']['evidence_references']}
- Evidence references needing attention: {summary['evidence_gap_summary']['needs_attention']}
- Handoff actions: {summary['counts']['handoff_actions']}

## Top Risks

{chr(10).join(risk_lines)}

## Evidence Gaps By Stage

{chr(10).join(gap_lines)}

## Handoff Lanes

{chr(10).join(lane_lines)}

## Next Actions

{chr(10).join(action_lines) if action_lines else '- Review the packet with the owner and MSP.'}

## Generated Artifacts

- `sprint-command-center.html`
- `sprint-offering-readout.md`
- `owner-action-plan.md`
- `msp-remediation-brief.md`
- `vendor-baa-ai-questionnaire.md`
- `evidence-collection-checklist.md`
- `day-one-workshop-agenda.md`
- `source-map.md`
- `sprint-summary.json`
- `evidence-index.json`
- `risk-register.csv`
- `handoff-actions.csv`
- `review-packet.md`
- `review-packet.html`
- `packet-manifest.json`
"""


def _h(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _status_label(status: str) -> str:
    return STATUS_LABELS.get(status, status.replace("_", " ").title())


def render_command_center(
    summary: dict[str, Any],
    risk_rows: list[dict[str, str]],
    handoff_rows: list[dict[str, str]],
    evidence_index: dict[str, Any],
) -> str:
    practice = summary["practice"]
    stage_cards = []
    for number, stage in enumerate(summary["stage_statuses"], start=1):
        artifact_links = "".join(f"<li>{_h(ref)}</li>" for ref in stage["artifact_refs"])
        stage_cards.append(
            f"""
            <article class="stage-card status-{_h(stage['status'])}">
              <div class="stage-number">{number}</div>
              <div>
                <h3>{_h(stage['name'])}</h3>
                <p class="stage-meta">{_status_label(str(stage['status']))} &middot; Owner: {_h(stage['owner'])}</p>
                <p>{_h(stage['next_action'])}</p>
                <div class="stage-foot">
                  <span>{int(stage['evidence_gap_count'])} evidence gaps</span>
                  <ul>{artifact_links}</ul>
                </div>
              </div>
            </article>
            """
        )

    risk_rows_html = []
    for risk in risk_rows[:8]:
        risk_rows_html.append(
            f"""
            <tr>
              <td><strong>{_h(risk['title'])}</strong><span>{_h(risk['stage_id'])}</span></td>
              <td><b class="pill severity-{_h(risk['severity'])}">{_h(risk['severity'])}</b></td>
              <td>{_h(risk['owner'])}</td>
              <td>{_h(risk['recipient'])}</td>
              <td>{_h(risk['evidence_status'])}</td>
              <td>{_h(risk['roadmap_bucket'])}</td>
            </tr>
            """
        )
    if not risk_rows_html:
        risk_rows_html.append(
            "<tr><td><strong>No generated findings</strong><span>findings_risk_register</span></td><td><b class='pill severity-low'>low</b></td><td>Practice owner/MSP</td><td>Owner/MSP</td><td>referenced</td><td>90_days</td></tr>"
        )

    attention_statuses = {"missing", "requested", "partial", "outdated"}
    evidence_refs = [
        item for item in evidence_index.get("evidence_references", []) if str(item.get("status")) in attention_statuses
    ][:8]
    evidence_rows_html = []
    for item in evidence_refs:
        evidence_rows_html.append(
            f"""
            <tr>
              <td><strong>{_h(item.get('evidence_id', ''))}</strong><span>{_h(item.get('title', ''))}</span></td>
              <td>{_h(item.get('status', 'requested'))}</td>
              <td>{_h(item.get('owner', 'Practice owner/MSP'))}</td>
              <td>{_h(', '.join(item.get('artifact_refs', [])))}</td>
            </tr>
            """
        )
    if not evidence_rows_html:
        evidence_rows_html.append("<tr><td><strong>No open evidence gaps</strong></td><td>reviewed</td><td>Practice owner/MSP</td><td>evidence-index.json</td></tr>")

    lane_cards = []
    for lane in summary["handoff_lanes"]:
        artifacts = "".join(f"<li>{_h(ref)}</li>" for ref in lane["artifact_refs"])
        lane_cards.append(
            f"""
            <article class="lane-card">
              <h3>{_h(lane['recipient'])}</h3>
              <p><strong>{int(lane['high_priority_actions'])}</strong> high-priority actions &middot; {int(lane['actions'])} total</p>
              <ul>{artifacts}</ul>
            </article>
            """
        )

    action_items = []
    for row in handoff_rows[:10]:
        action_items.append(
            f"""
            <li>
              <strong>{_h(row['recipient'])}</strong>
              <span>{_h(row['priority'])} &middot; {_h(row['roadmap_bucket'])} &middot; {_h(row['artifact_ref'])}</span>
              {_h(row['action'])}
            </li>
            """
        )

    artifact_items = []
    for name in summary["outputs"]["sprint"]:
        artifact_items.append(f"<li>{_h(name)}</li>")
    for name in summary["outputs"]["packet"][:8]:
        artifact_items.append(f"<li>{_h(name)}</li>")
    artifact_items.append("<li>evidence-binder-export/</li>")

    offering = summary["offering_summary"]
    value_items = "".join(f"<li>{_h(item)}</li>" for item in offering["top_value_outcomes"][:5])
    first_week_items = "".join(
        f"""
        <li>
          <strong>{_h(action['day'])} &middot; {_h(action['lane'])}</strong>
          <span>{_h(action['artifact_ref'])}</span>
          {_h(action['action'])}
        </li>
        """
        for action in offering["first_7_days_actions"][:7]
    )
    offering_lane_items = "".join(
        f"""
        <article class="offering-lane">
          <h3>{_h(lane['label'])}</h3>
          <p>{_h(lane['value'])}</p>
        </article>
        """
        for lane in offering["audience_lanes"]
    )
    source_theme_items = "".join(
        f"<li><strong>{_h(source['title'])}</strong><span>{_h(source['how_this_changes_the_sprint'])}</span></li>"
        for source in offering["source_anchors"]
    )
    offering_artifact_items = "".join(
        f"<li><strong>{_h(item['path'])}</strong><span>{_h(item['purpose'])}</span></li>"
        for item in offering["artifact_list"]
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{_h(practice['label'])} Sprint Command Center</title>
  <style>
    :root {{
      --bg: #f8f7f2;
      --panel: #fffdf8;
      --ink: #17211b;
      --muted: #5c665f;
      --line: #d6d2c6;
      --accent: #11614f;
      --accent-2: #8a6a24;
      --danger: #9b2f24;
      --warn: #a05a15;
      --ok: #2d6b43;
      --soft: #e8f1ec;
      --gold-soft: #f5ecd0;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.45;
    }}
    .shell {{ max-width: 1240px; margin: 0 auto; padding: 28px 22px 56px; }}
    .hero {{
      border-top: 6px solid var(--accent);
      display: grid;
      grid-template-columns: minmax(0, 1.45fr) minmax(280px, 0.55fr);
      gap: 24px;
      padding: 26px 0 22px;
    }}
    .eyebrow {{ color: var(--accent); font-size: 12px; font-weight: 800; letter-spacing: 0; text-transform: uppercase; }}
    h1, h2, h3, p {{ margin-top: 0; }}
    h1 {{ font-size: clamp(34px, 5vw, 58px); line-height: 1.02; margin-bottom: 12px; letter-spacing: 0; }}
    h2 {{ font-size: 22px; margin-bottom: 14px; letter-spacing: 0; }}
    h3 {{ font-size: 16px; margin-bottom: 6px; letter-spacing: 0; }}
    .lead {{ color: var(--muted); max-width: 760px; font-size: 16px; }}
    .metrics {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }}
    .metric, .boundary, .stage-card, .lane-card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: 0 1px 0 rgba(23, 33, 27, 0.04);
    }}
    .metric {{ padding: 14px; }}
    .metric span {{ display: block; color: var(--muted); font-size: 12px; font-weight: 700; margin-bottom: 6px; }}
    .metric strong {{ font-size: 24px; }}
    .boundary {{ padding: 14px; border-left: 4px solid var(--warn); background: #fff7e7; color: #4f3317; }}
    .grid {{ display: grid; grid-template-columns: minmax(0, 1.35fr) minmax(320px, 0.65fr); gap: 18px; align-items: start; }}
    section {{ margin-top: 22px; }}
    .stages {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }}
    .stage-card {{ display: grid; grid-template-columns: 34px minmax(0, 1fr); gap: 10px; padding: 14px; min-height: 190px; }}
    .stage-number {{
      width: 28px;
      height: 28px;
      border-radius: 50%;
      background: var(--soft);
      color: var(--accent);
      display: grid;
      place-items: center;
      font-weight: 800;
      font-size: 13px;
    }}
    .status-needs_evidence {{ border-left: 4px solid var(--warn); }}
    .status-ready_for_review {{ border-left: 4px solid var(--accent-2); }}
    .status-complete {{ border-left: 4px solid var(--ok); }}
    .stage-meta {{ color: var(--muted); font-size: 12px; font-weight: 700; margin-bottom: 8px; }}
    .stage-card p {{ font-size: 13px; color: #26332b; }}
    .stage-foot {{ display: grid; gap: 8px; margin-top: 12px; color: var(--muted); font-size: 12px; }}
    ul {{ margin: 0; padding-left: 18px; }}
    .stage-foot ul, .lane-card ul, .artifact-list {{ display: flex; flex-wrap: wrap; gap: 6px; padding-left: 0; list-style: none; }}
    .stage-foot li, .lane-card li, .artifact-list li {{
      border: 1px solid var(--line);
      background: #ffffff;
      border-radius: 999px;
      padding: 3px 7px;
      color: var(--muted);
    }}
    .table-wrap {{ overflow-x: auto; background: var(--panel); border: 1px solid var(--line); border-radius: 8px; }}
    table {{ width: 100%; border-collapse: collapse; min-width: 760px; font-size: 13px; }}
    th, td {{ text-align: left; padding: 11px 12px; border-bottom: 1px solid var(--line); vertical-align: top; }}
    th {{ background: #eee8d9; color: #403928; font-size: 12px; }}
    td span {{ display: block; color: var(--muted); margin-top: 4px; font-size: 12px; }}
    tr:last-child td {{ border-bottom: 0; }}
    .pill {{ display: inline-block; border-radius: 999px; padding: 4px 8px; color: #fff; font-size: 12px; }}
    .severity-critical, .severity-high {{ background: var(--danger); }}
    .severity-medium {{ background: var(--warn); }}
    .severity-low {{ background: var(--ok); }}
    .lanes {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }}
    .lane-card {{ padding: 14px; }}
    .lane-card p {{ color: var(--muted); font-size: 13px; }}
    .actions {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px 18px;
    }}
    .actions li {{ margin: 0 0 12px; font-size: 13px; }}
    .actions li span {{ display: block; color: var(--muted); font-size: 12px; margin: 2px 0; }}
    .offering {{
      background: #f0f6f2;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
    }}
    .offering-grid {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(280px, 0.8fr); gap: 14px; }}
    .offering ul {{ margin: 0; padding-left: 18px; }}
    .offering li {{ margin-bottom: 8px; font-size: 13px; }}
    .offering li span {{ display: block; color: var(--muted); font-size: 12px; margin-top: 3px; }}
    .offering-lanes {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; margin-top: 14px; }}
    .offering-lane {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
    }}
    .offering-lane p {{ color: var(--muted); font-size: 12px; margin: 0; }}
    .source-themes, .offering-artifacts {{ columns: 2; }}
    .footer-note {{ color: var(--muted); font-size: 12px; margin-top: 26px; }}
    @media (max-width: 980px) {{
      .hero, .grid {{ grid-template-columns: 1fr; }}
      .stages {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .offering-grid, .offering-lanes {{ grid-template-columns: 1fr; }}
      .source-themes, .offering-artifacts {{ columns: 1; }}
    }}
    @media (max-width: 640px) {{
      .shell {{ padding: 18px 14px 42px; }}
      .metrics, .stages, .lanes {{ grid-template-columns: 1fr; }}
      h1 {{ font-size: 34px; }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <header class="hero">
      <div>
        <div class="eyebrow">Velari Sprint Mode</div>
        <h1>{_h(practice['label'])} Sprint Command Center</h1>
        <p class="lead">One local readout for sprint status, top risks, evidence gaps, handoff lanes, and generated artifacts. This page is self-contained and makes no external network calls.</p>
        <div class="boundary">Reference-only boundary: no PHI, patient identifiers, credentials, secrets, private URLs, raw contracts, raw logs, or incident-sensitive details. This is not legal advice, does not establish legal or regulatory status, does not decide incident reporting duties, and does not replace a formal Security Risk Analysis.</div>
      </div>
      <aside class="metrics" aria-label="Sprint metrics">
        <div class="metric"><span>Readiness signal</span><strong>{_h(summary['readiness_signal']['label'])}</strong></div>
        <div class="metric"><span>Delivery signal</span><strong>{_h(summary['target_delivery_signal']['status'])}</strong></div>
        <div class="metric"><span>High/critical findings</span><strong>{int(summary['counts']['high_or_critical_findings'])}</strong></div>
        <div class="metric"><span>Evidence needing attention</span><strong>{int(summary['evidence_gap_summary']['needs_attention'])}</strong></div>
      </aside>
    </header>

    <section class="offering">
      <h2>Offering Mode</h2>
      <div class="offering-grid">
        <div>
          <h3>Top Value Delivered</h3>
          <ul>{value_items}</ul>
        </div>
        <div>
          <h3>First 7 Days</h3>
          <ol>{first_week_items}</ol>
        </div>
      </div>
      <div class="offering-lanes">{offering_lane_items}</div>
      <div class="offering-grid">
        <div>
          <h3>Source-Backed Themes</h3>
          <ul class="source-themes">{source_theme_items}</ul>
        </div>
        <div>
          <h3>Artifact Checklist</h3>
          <ul class="offering-artifacts">{offering_artifact_items}</ul>
        </div>
      </div>
    </section>

    <section>
      <h2>Stage Status</h2>
      <div class="stages">{''.join(stage_cards)}</div>
    </section>

    <div class="grid">
      <div>
        <section>
          <h2>Top Risks</h2>
          <div class="table-wrap">
            <table>
              <thead><tr><th>Finding</th><th>Priority</th><th>Owner</th><th>Recipient</th><th>Evidence</th><th>Bucket</th></tr></thead>
              <tbody>{''.join(risk_rows_html)}</tbody>
            </table>
          </div>
        </section>

        <section>
          <h2>Evidence Gaps</h2>
          <div class="table-wrap">
            <table>
              <thead><tr><th>Evidence</th><th>Status</th><th>Owner</th><th>Artifact</th></tr></thead>
              <tbody>{''.join(evidence_rows_html)}</tbody>
            </table>
          </div>
        </section>
      </div>

      <aside>
        <section>
          <h2>Handoff Lanes</h2>
          <div class="lanes">{''.join(lane_cards)}</div>
        </section>

        <section>
          <h2>Next Actions</h2>
          <ol class="actions">{''.join(action_items)}</ol>
        </section>

        <section>
          <h2>Generated Artifacts</h2>
          <ul class="artifact-list">{''.join(artifact_items)}</ul>
        </section>
      </aside>
    </div>

    <p class="footer-note">Generated at {_h(summary['generated_at'])}. Source profile hash is tracked in sprint-summary.json and packet-manifest.json for private app import review.</p>
  </main>
</body>
</html>
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
    summary = build_summary(profile, profile_path, manifest, stages, risk_rows, handoff_rows, evidence_index, generated_at)

    sprint_index_path = out_dir / "sprint-index.md"
    client_readout_path = out_dir / "sprint-client-readout.md"
    command_center_path = out_dir / "sprint-command-center.html"
    offering_readout_path = out_dir / "sprint-offering-readout.md"
    owner_action_plan_path = out_dir / "owner-action-plan.md"
    msp_remediation_brief_path = out_dir / "msp-remediation-brief.md"
    vendor_questionnaire_path = out_dir / "vendor-baa-ai-questionnaire.md"
    evidence_checklist_path = out_dir / "evidence-collection-checklist.md"
    workshop_agenda_path = out_dir / "day-one-workshop-agenda.md"
    source_map_path = out_dir / "source-map.md"
    summary_path = out_dir / "sprint-summary.json"
    risk_path = out_dir / "risk-register.csv"
    evidence_path = out_dir / "evidence-index.json"
    handoff_path = out_dir / "handoff-actions.csv"

    sprint_index_path.write_text(render_sprint_index(summary, risk_rows), encoding="utf-8", newline="\n")
    client_readout_path.write_text(render_client_readout(summary, risk_rows, handoff_rows), encoding="utf-8", newline="\n")
    offering_readout_path.write_text(
        render_sprint_offering_readout(summary, risk_rows, handoff_rows),
        encoding="utf-8",
        newline="\n",
    )
    owner_action_plan_path.write_text(render_owner_action_plan(summary, risk_rows), encoding="utf-8", newline="\n")
    msp_remediation_brief_path.write_text(
        render_msp_remediation_brief(summary, risk_rows, handoff_rows),
        encoding="utf-8",
        newline="\n",
    )
    vendor_questionnaire_path.write_text(
        render_vendor_baa_ai_questionnaire(profile, summary),
        encoding="utf-8",
        newline="\n",
    )
    evidence_checklist_path.write_text(
        render_evidence_collection_checklist(profile, summary, evidence_index),
        encoding="utf-8",
        newline="\n",
    )
    workshop_agenda_path.write_text(render_day_one_workshop_agenda(summary, profile), encoding="utf-8", newline="\n")
    source_map_path.write_text(render_source_map(summary), encoding="utf-8", newline="\n")
    command_center_path.write_text(
        render_command_center(summary, risk_rows, handoff_rows, evidence_index),
        encoding="utf-8",
        newline="\n",
    )
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    evidence_path.write_text(json.dumps(evidence_index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_csv(
        risk_path,
        risk_rows,
        [
            "finding_id",
            "stage_id",
            "severity",
            "priority",
            "title",
            "owner",
            "audience",
            "recipient",
            "evidence_status",
            "evidence_refs",
            "recommended_action",
            "artifact_ref",
            "roadmap_bucket",
        ],
    )
    _write_csv(
        handoff_path,
        handoff_rows,
        [
            "action_id",
            "audience",
            "recipient",
            "stage_id",
            "priority",
            "owner",
            "action",
            "evidence_ref",
            "artifact_ref",
            "roadmap_bucket",
        ],
    )

    return SprintBuildResult(
        output_dir=out_dir,
        packet_dir=out_dir,
        binder_dir=binder_dir,
        artifacts=[
            sprint_index_path,
            client_readout_path,
            command_center_path,
            offering_readout_path,
            owner_action_plan_path,
            msp_remediation_brief_path,
            vendor_questionnaire_path,
            evidence_checklist_path,
            workshop_agenda_path,
            source_map_path,
            summary_path,
            risk_path,
            evidence_path,
            handoff_path,
        ],
    )
