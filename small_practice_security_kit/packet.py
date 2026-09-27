from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path

from .ephi_map import build_ephi_map
from .evidence_lifecycle import (
    build_evidence_lifecycle,
    closeout_label,
    lifecycle_by_source,
    lifecycle_label,
    summarize_lifecycle,
    trace_label,
)
from .external_precheck import (
    external_finding_id,
    external_finding_owner,
    external_finding_recipient,
    external_finding_severity,
    external_finding_title,
    external_precheck_findings,
    external_precheck_profile,
    external_precheck_scope,
)
from .incident_runner import phase_guidance_for
from .exchange import markdown_cell
from .manifest import build_packet_manifest, finding_entries
from .profile import load_profile, slugify
from .sensitive_data import blocking_findings
from .vendor_evidence import vendor_hitrust_status, vendor_soc2_status


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out"


READINESS_ITEMS = [
    ("mfa_email", "Email MFA", "Access"),
    ("mfa_ehr", "EHR MFA", "Access"),
    ("unique_accounts", "Unique accounts", "Access"),
    ("quarterly_access_review", "Quarterly access review", "Evidence"),
    ("tested_backups", "Tested backups", "Resilience"),
    ("vendor_inventory", "Vendor inventory", "Vendor"),
    ("baa_register", "BAA register", "Vendor"),
    ("incident_contact_list", "Incident contact list", "Incident"),
    ("downtime_plan", "Downtime plan", "Resilience"),
    ("security_training_current", "Training current", "Workforce"),
    ("log_review_cadence", "Log review cadence", "Monitoring"),
]
SETTLED_BAA = {
    "signed",
    "not applicable",
    "not needed for no-PHI demo workflow",
    "payer relationship",
}


def yn(value: bool) -> str:
    return "Yes" if value else "No"


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- None recorded."


def _joined_kinds(labels: list[str]) -> str:
    unique = [label for label in dict.fromkeys(labels) if label]
    if not unique:
        return "sidecar systems"
    if len(unique) == 1:
        return unique[0]
    if len(unique) == 2:
        return f"{unique[0]} and {unique[1]}"
    return f"{', '.join(unique[:-1])}, and {unique[-1]}"


def readiness_insight(profile: dict) -> str:
    readiness = profile["readiness"]
    ready = [label for key, label, _area in READINESS_ITEMS if readiness.get(key)]
    missing = [label for key, label, _area in READINESS_ITEMS if not readiness.get(key)]
    total = len(READINESS_ITEMS)
    if not missing:
        return f"All {total} baseline items have an evidence mark."
    return (
        f"{len(ready)} of {total} baseline items have evidence. "
        f"Still open: {', '.join(missing)}."
    )


def ephi_insight(profile: dict) -> str:
    mapped = build_ephi_map(profile)
    counts = mapped["counts"]
    hot = [
        flow["outside_kind_label"]
        for flow in mapped["never_touches"]
        if str(flow.get("risk", "")).lower() in {"high", "critical"}
    ]
    if not counts["outside_flows"]:
        return "No patient-data paths outside the EHR were mapped."
    lead = (
        f"{counts['never_touches']} flows never touch the EHR; "
        f"{counts['crosses']} leave or enter the chart."
    )
    if hot:
        return f"{lead} The high-risk paths that stay off the chart are {_joined_kinds(hot)}."
    return lead


def vendor_insight(profile: dict) -> str:
    vendors = list(profile.get("vendors") or [])
    ephi = [vendor for vendor in vendors if vendor.get("touches_ephi")]
    open_baa = [vendor for vendor in ephi if str(vendor.get("baa_status", "")).lower() not in SETTLED_BAA]
    if not ephi:
        return "No vendors are marked as touching ePHI."
    if not open_baa:
        return f"All {len(ephi)} ePHI vendors have a settled BAA status. Confirm review dates still."
    names = ", ".join(vendor["name"] for vendor in open_baa)
    return f"{len(open_baa)} of {len(ephi)} ePHI vendors still need a BAA answer: {names}."


def ai_insight(profile: dict) -> str:
    workflows = list(profile.get("ai_workflows") or [])
    if not workflows:
        return "No AI workflows were recorded."
    counts = {"allowed": 0, "restricted": 0, "prohibited": 0}
    for workflow in workflows:
        key = str(workflow.get("decision", "")).lower()
        if key in counts:
            counts[key] += 1
    return (
        f"{len(workflows)} AI workflows recorded: "
        f"{counts['allowed']} allowed, {counts['restricted']} restricted, {counts['prohibited']} prohibited."
    )


MAIN_SECTION_TITLES = {
    "Readiness Review",
    "ePHI Flow Map",
    "Vendor and BAA Review",
    "AI Workflow Review",
}


def _vendor_for_flow(flow: dict, vendors: list[dict]) -> dict:
    name = str(flow.get("vendor") or "").strip()
    for vendor in vendors:
        if vendor.get("name") == name:
            return vendor
    dest = str(flow.get("destination") or "").casefold()
    for vendor in vendors:
        vendor_name = str(vendor.get("name") or "").casefold()
        if dest and (dest in vendor_name or vendor_name in dest):
            return vendor
    return {}


def _owner_for(profile: dict, kind: str) -> str:
    practice = profile.get("practice") or {}
    if kind == "vendor":
        return str(practice.get("security_owner") or "Office Manager")
    return str(practice.get("technical_owner") or "MSP Lead")


def joined_findings(profile: dict) -> list[dict[str, str]]:
    mapped = build_ephi_map(profile)
    vendors = list(profile.get("vendors") or [])
    readiness = profile.get("readiness") or {}
    findings: list[dict[str, str]] = []
    seen: set[str] = set()

    def add(key: str, path: str, why: str, ask: str, owner: str) -> None:
        if key in seen:
            return
        seen.add(key)
        findings.append({"path": path, "why": why, "ask": ask, "owner": owner})

    for flow in mapped["outside_flows"]:
        if str(flow.get("risk", "")).lower() not in {"high", "critical"}:
            continue
        vendor = _vendor_for_flow(flow, vendors)
        parts = [flow["ehr_lane_label"].rstrip(".")]
        if flow.get("outside_kind_label"):
            parts.append(str(flow["outside_kind_label"]))
        if flow.get("ephi_type"):
            parts.append(str(flow["ephi_type"]))
        baa_status = str(vendor.get("baa_status") or "")
        if flow.get("baa_needed") and vendor:
            if baa_status.lower() not in SETTLED_BAA:
                parts.append(f"BAA {baa_status}")
        elif flow.get("baa_needed") and not vendor:
            parts.append("no vendor row in the register")
        if flow.get("outside_kind") in {"files", "imaging"} and not readiness.get("tested_backups"):
            parts.append("no restore-test evidence")
        if flow.get("outside_kind") == "ai":
            ai_use = str(vendor.get("ai_training_use") or "")
            if ai_use:
                parts.append(f"AI/data use {ai_use}")
        path = f"{flow['source']} → {flow['destination']}"
        owner = _owner_for(profile, "vendor" if flow.get("outside_kind") == "ai" else "technical")
        add(path, path, ". ".join(parts) + ".", f"{flow['evidence_needed'].rstrip('.')}.", owner)

    if not readiness.get("mfa_ehr"):
        add(
            "ehr-mfa",
            "EHR access",
            "EHR MFA is unmarked, while billing and intake still enter or leave the chart.",
            "MFA enforcement export for EHR, admin, and vendor-support accounts.",
            _owner_for(profile, "technical"),
        )
    if not readiness.get("tested_backups") and any(
        flow.get("outside_kind") in {"files", "imaging", "email"} for flow in mapped["outside_flows"]
    ):
        add(
            "restore",
            "Backup restore",
            "Patient-data copies sit on shared drives and imaging workstations, and no restore test is recorded.",
            "Backup scope, last restore-test date, recovery owner, private binder reference.",
            _owner_for(profile, "technical"),
        )

    return findings


def verdict(profile: dict) -> str:
    readiness = profile.get("readiness") or {}
    mapped = build_ephi_map(profile)
    vendors = [vendor for vendor in profile.get("vendors") or [] if vendor.get("touches_ephi")]
    open_baa = [
        vendor["name"]
        for vendor in vendors
        if str(vendor.get("baa_status", "")).lower() not in SETTLED_BAA
    ]
    have = []
    if readiness.get("mfa_email"):
        have.append("email MFA")
    if readiness.get("vendor_inventory"):
        have.append("a vendor list")
    if readiness.get("incident_contact_list"):
        have.append("an incident contact list")
    if len(have) >= 3:
        have_text = f"{', '.join(have[:-1])}, and {have[-1]}"
    elif len(have) == 2:
        have_text = f"{have[0]} and {have[1]}"
    else:
        have_text = have[0] if have else "little baseline evidence"
    missing = []
    if not readiness.get("mfa_ehr"):
        missing.append("EHR MFA")
    if not readiness.get("tested_backups"):
        missing.append("a restore test")
    if open_baa:
        missing.append("current BAAs for " + ", ".join(open_baa))
    if len(missing) >= 3:
        missing_text = f"{', '.join(missing[:-1])}, and {missing[-1]}"
    elif len(missing) == 2:
        missing_text = f"{missing[0]} and {missing[1]}"
    else:
        missing_text = missing[0] if missing else "no critical gaps"
    first = f"The practice can show {have_text}. It cannot show {missing_text}."
    hot = [
        flow["outside_kind_label"]
        for flow in mapped["never_touches"]
        if str(flow.get("risk", "")).lower() in {"high", "critical"}
    ]
    if hot:
        return f"{first} Patient data also moves off the chart through {_joined_kinds(hot)}."
    if mapped["counts"]["outside_flows"]:
        return f"{first} {ephi_insight(profile)}"
    return first


def vendor_needs_attention(vendor: dict) -> bool:
    status = str(vendor.get("baa_status", "")).lower()
    ai_use = str(vendor.get("ai_training_use", "")).lower()
    terms = str(vendor.get("incident_notification_terms", "")).lower()
    risk = str(vendor.get("risk", "")).lower()
    if vendor.get("touches_ephi") and status not in SETTLED_BAA:
        return True
    if risk in {"high", "critical"}:
        return True
    if "unknown" in ai_use or ai_use == "not reviewed":
        return True
    return terms in {"unknown", "not reviewed", ""}


def risk_level(profile: dict) -> tuple[str, list[str]]:
    readiness = profile["readiness"]
    gaps = []
    if not readiness["mfa_ehr"]:
        gaps.append("Enable MFA for EHR access.")
    if not readiness["quarterly_access_review"]:
        gaps.append("Run and record a quarterly access review.")
    if not readiness["tested_backups"]:
        gaps.append("Run a restore test and record evidence.")
    if not readiness["baa_register"]:
        gaps.append("Complete the BAA register and review dates.")
    if not readiness["downtime_plan"]:
        gaps.append("Document downtime procedures for critical systems.")
    if not readiness["log_review_cadence"]:
        gaps.append("Set a monthly log review cadence.")
    if len(gaps) >= 5:
        return "High", gaps
    if len(gaps) >= 3:
        return "Medium", gaps
    return "Low", gaps


def table(headers: list[str], rows: list[list[str]]) -> str:
    # Security decision: unescaped pipes or newlines in profile values would shift
    # reviewer-facing table columns (e.g. making a vendor's BAA look signed).
    lines = ["| " + " | ".join(markdown_cell(header) for header in headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(markdown_cell(cell) for cell in row) + " |")
    return "\n".join(lines)


def _joined(value: object) -> str:
    if isinstance(value, list):
        return "; ".join(str(item) for item in value)
    return str(value)


def lifecycle_records(profile: dict) -> list[dict]:
    return build_evidence_lifecycle(profile, date.today())


def action_packet_rows(profile: dict) -> list[dict]:
    risk, gaps = risk_level(profile)
    return finding_entries(profile, risk, gaps)


def action_packet_table(profile: dict) -> str:
    rows = []
    for packet in action_packet_rows(profile)[:10]:
        rows.append(
            [
                packet["title"],
                packet["priority"],
                packet["plain_english_summary"],
                packet["why_it_matters"],
                packet["owner_lane"],
                packet["recommended_question"],
                _joined(packet["acceptable_evidence"]),
                _joined(packet["unsafe_inputs"]),
                packet["timeframe"],
                _joined(packet["reviewer_needed"]),
                packet["next_action"],
            ]
        )
    if not rows:
        rows.append(
            [
                "No generated major finding",
                "low",
                "No major action packet was generated.",
                "The practice should still review evidence support before relying on the packet.",
                "owner",
                "Which evidence references should be refreshed first?",
                "evidence reference ID",
                "PHI; credentials; private URLs",
                "quarterly_refresh",
                "owner",
                "Review the packet with the owner and MSP.",
            ]
        )
    return table(
        [
            "Finding",
            "Priority",
            "Plain-English summary",
            "Why it matters",
            "Owner lane",
            "Recommended question",
            "Acceptable evidence",
            "Unsafe inputs",
            "Timeframe",
            "Reviewer needed",
            "Next action",
        ],
        rows,
    )


def readiness_review(profile: dict) -> str:
    risk, _gaps = risk_level(profile)
    readiness = profile["readiness"]
    readiness_lifecycle = lifecycle_by_source(lifecycle_records(profile), "readiness")
    missing = [f"{label} — {area}" for key, label, area in READINESS_ITEMS if not readiness.get(key)]
    open_evidence = []
    for record in readiness_lifecycle.values():
        if record["closeout_state"] in {"closed", "not_applicable"}:
            continue
        open_evidence.append(
            f"{record['title']} — {record['owner']} · {closeout_label(record['closeout_state'])}. "
            f"{_joined(record['acceptable_evidence'])}."
        )
    return f"""# Readiness Review

{readiness_insight(profile)} Initial risk: **{risk}**.

## Missing

{_bullets(missing)}

## Evidence Closeout Queue

{_bullets(open_evidence)}
"""


def ephi_flow_map(profile: dict) -> str:
    mapped = build_ephi_map(profile)
    flow_lines = []
    for flow in mapped["outside_flows"]:
        baa = "BAA needed" if flow.get("baa_needed") else "no BAA flag"
        flow_lines.append(
            f"**{flow['source']} → {flow['destination']}** — {flow['ehr_lane_label']}. "
            f"{flow['outside_kind_label']}. {flow['risk']} risk. {baa}. "
            f"{flow['ephi_type']}. Evidence: {flow['evidence_needed']}."
        )
    return f"""# ePHI Flow Map

{ephi_insight(profile)}

## Patient Data Outside the EHR

{_bullets(flow_lines)}
"""


def vendor_review(profile: dict) -> str:
    attention = []
    settled = []
    for vendor in profile["vendors"]:
        ephi = "touches ePHI" if vendor.get("touches_ephi") else "no ePHI mark"
        line = (
            f"**{vendor['name']}** — {vendor['service']}. {ephi}. "
            f"BAA {vendor['baa_status']}. SOC 2 Status {vendor_soc2_status(vendor)}. "
            f"HITRUST Status {vendor_hitrust_status(vendor)}. "
            f"Incident terms: {vendor['incident_notification_terms']}. "
            f"AI/data use: {vendor['ai_training_use']}. {vendor['risk']} risk."
        )
        if vendor_needs_attention(vendor):
            attention.append(line)
        else:
            settled.append(vendor["name"])
    settled_line = (
        f"{', '.join(settled)} can wait: BAA is signed enough to review later."
        if settled
        else ""
    )
    return f"""# Vendor and BAA Review

{vendor_insight(profile)}

## Needs attention

{_bullets(attention)}

{settled_line}

## Next Evidence

- Confirm BAA review date for each vendor touching ePHI.
- Record SOC 2 and HITRUST evidence status as provided, not provided, absent, or not applicable; do not infer attestations from marketing pages.
- Record incident notification terms.
- Ask AI/data-use questions for any vendor using automation or model training.
"""


def ai_review(profile: dict) -> str:
    grouped = {"prohibited": [], "restricted": [], "allowed": []}
    allowed_names = []
    for workflow in profile["ai_workflows"]:
        decision = str(workflow.get("decision", "restricted")).lower()
        line = (
            f"**{workflow['name']}** — {workflow['proposed_use']}. "
            f"Data: {workflow['data_used']}. Evidence: {workflow['evidence_needed']}."
        )
        grouped.setdefault(decision, []).append(line)
        if decision == "allowed":
            allowed_names.append(workflow["name"])
    allowed_note = (
        f"Allowed and left in the background: {', '.join(allowed_names)}."
        if allowed_names
        else ""
    )
    return f"""# AI Workflow Review

{ai_insight(profile)}

## Prohibited

{_bullets(grouped["prohibited"])}

## Restricted

{_bullets(grouped["restricted"])}

{allowed_note}
"""


def downtime_packet(profile: dict) -> str:
    downtime = profile["downtime"]
    downtime_lifecycle = lifecycle_by_source(lifecycle_records(profile), "downtime")
    rows = [
        [
            system,
            downtime_lifecycle[system]["owner"],
            lifecycle_label(downtime_lifecycle[system]["lifecycle_status"]),
            closeout_label(downtime_lifecycle[system]["closeout_state"]),
            trace_label(downtime_lifecycle[system]),
            downtime_lifecycle[system]["closeout_rule"],
        ]
        for system in downtime["critical_systems"]
    ]
    return f"""# Downtime and Ransomware Tabletop

Downtime plan status: **{downtime['downtime_plan_status']}**

Restore test status: **{downtime['last_restore_test'] or 'not recorded'}**

Tabletop status: **{downtime['tabletop_status']}**

{table(['Critical System', 'Downtime Owner', 'Lifecycle', 'Closeout', 'Trace', 'Closeout rule'], rows)}

## Tabletop Scenario

Run a 30-minute walkthrough: EHR unavailable at 8:30 AM, phones are working, billing portal is delayed, and staff need to continue patient care safely.
"""


def _incident_profile(profile: dict) -> dict:
    incident = profile.get("incident_timeline") or {}
    if incident:
        return incident
    critical = ", ".join(profile.get("downtime", {}).get("critical_systems", [])[:3]) or "critical systems"
    return {
        "scenario_name": "Downtime or suspicious access tabletop",
        "scenario_type": "tabletop",
        "summary": f"Synthetic tabletop for a small practice where {critical} need containment, continuity, and evidence-reference decisions.",
        "sensitive_data_boundary": "Record categories, owners, timestamps, and evidence reference IDs only. Do not record PHI, patient identifiers, screenshots, raw logs, private URLs, credentials, or real incident details.",
        "timeline": [
            {
                "time": "T+00",
                "phase": "Detection",
                "event": "Staff report a suspicious access or downtime concern.",
                "systems": profile.get("downtime", {}).get("critical_systems", [])[:2] or ["Critical system"],
                "owner": profile["practice"].get("security_owner", "Practice owner"),
                "evidence_ref": "INC-PRIVATE-REFERENCE",
                "status": "needs review",
                "decision_gate": "Is there active compromise, patient-care disruption, or vendor notice?",
            },
            {
                "time": "T+30",
                "phase": "Containment",
                "event": "MSP confirms what account, device, vendor, or workflow category needs containment.",
                "systems": profile.get("downtime", {}).get("critical_systems", [])[:2] or ["Critical system"],
                "owner": profile["practice"].get("technical_owner", "MSP Lead"),
                "evidence_ref": "INC-CONTAINMENT-REFERENCE",
                "status": "open",
                "decision_gate": "Which actions can be taken now while qualified review is pending?",
            },
        ],
        "decision_gates": [
            {
                "gate": "Escalation needed?",
                "owner": profile["practice"].get("technical_owner", "MSP Lead"),
                "trigger": "Active compromise, ransomware, unauthorized access, lost device, vendor breach notice, or patient-care disruption.",
                "action": "Escalate to qualified incident response and preserve private evidence references.",
            },
            {
                "gate": "Qualified review needed?",
                "owner": "Qualified reviewer",
                "trigger": "Possible breach notification, insurance notice, contract notice, regulatory question, or formal risk-analysis decision.",
                "action": "Park the decision for counsel, compliance, insurer, or qualified security reviewer.",
            },
        ],
        "after_actions": [
            {
                "id": "INC-AA-001",
                "priority": "high",
                "owner": profile["practice"].get("technical_owner", "MSP Lead"),
                "action": "Confirm MFA, access review, backup scope, and log review evidence for affected systems.",
                "evidence_needed": "Admin settings export, access review reference, restore-test reference, and log-review cadence reference.",
                "due": "30 days",
            }
        ],
    }


def _entry_guidance(entry: dict) -> dict:
    guidance = phase_guidance_for(str(entry.get("phase") or "Detection"))
    merged = dict(guidance)
    for key in [
        "owner_lane",
        "source_alignment",
        "plain_english_goal",
        "owner_prompt",
        "staff_script",
        "do_now",
        "ask_msp_or_vendor",
        "allowed_inputs",
        "blocked_inputs",
        "evidence_required",
        "completion_criteria",
        "escalation_triggers",
    ]:
        if entry.get(key):
            merged[key] = entry[key]
    return merged


def _check(value: object) -> str:
    return "Yes" if bool(value) else "No"


def incident_evidence_timeline(profile: dict) -> str:
    incident = _incident_profile(profile)
    rows = []
    guided_rows = []
    call_sheet_rows = []
    for entry in incident.get("timeline", []):
        guidance = _entry_guidance(entry)
        rows.append(
            [
                entry.get("time", "TBD"),
                entry.get("phase", "Timeline event"),
                entry.get("event", "Sanitized event category"),
                _joined(entry.get("systems", [])),
                entry.get("owner", profile["practice"].get("security_owner", "Practice owner")),
                entry.get("evidence_ref", "private evidence reference"),
                entry.get("decision_gate", "Decision gate to confirm"),
                entry.get("status", "open"),
            ]
        )
        guided_rows.append(
            [
                entry.get("phase", "Timeline event"),
                guidance.get("owner_lane", entry.get("owner", "Owner")),
                _joined(guidance.get("source_alignment", [])),
                guidance.get("plain_english_goal", "Confirm facts and next owner."),
                _joined(guidance.get("do_now", [])),
                _joined(guidance.get("evidence_required", [])),
                _joined(guidance.get("completion_criteria", [])),
                _joined(guidance.get("escalation_triggers", [])),
                _check(entry.get("complete", False)),
            ]
        )
        call_sheet_rows.append(
            [
                entry.get("phase", "Timeline event"),
                guidance.get("owner_prompt", entry.get("decision_gate", "What decision is needed?")),
                guidance.get("staff_script", "Keep details sanitized and route private evidence to the owner."),
                _joined(guidance.get("ask_msp_or_vendor", [])),
                _joined(guidance.get("blocked_inputs", [])),
            ]
        )

    gate_rows = [
        [
            gate.get("gate", "Decision gate"),
            gate.get("owner", "Owner"),
            gate.get("trigger", "Trigger to confirm"),
            gate.get("action", "Action to take"),
        ]
        for gate in incident.get("decision_gates", [])
    ]

    return f"""# Incident Evidence Timeline

Scenario: **{incident.get('scenario_name', 'Incident tabletop')}**

Type: **{incident.get('scenario_type', 'tabletop')}**

{incident.get('summary', 'Synthetic incident evidence timeline for owner, MSP, and qualified-review handoff.')}

## Evidence Boundary

{incident.get('sensitive_data_boundary', 'Use reference IDs only. Do not include PHI, patient identifiers, screenshots, raw logs, private URLs, credentials, or real incident details.')}

## Timeline

{table(['Time', 'Phase', 'Sanitized event', 'System/workflow', 'Owner', 'Evidence ref', 'Decision gate', 'Status'], rows)}

## Guided Phase Checklist

{table(['Phase', 'Owner lane', 'Source alignment', 'Goal', 'Do now', 'Evidence required', 'Completion criteria', 'Escalation triggers', 'Complete?'], guided_rows)}

## Owner/MSP Call Sheet

{table(['Phase', 'Owner question', 'Staff script', 'Ask MSP/vendor', 'Do not record'], call_sheet_rows)}

## Decision Gates

{table(['Gate', 'Owner', 'Trigger', 'Action'], gate_rows)}

## Handoff Rules

- Separate technical containment from breach-notification, insurance, contract, regulatory, and legal/compliance decisions.
- Preserve private evidence references without copying raw evidence into the public packet.
- Escalate active compromise, ransomware, unauthorized access, lost device, vendor breach notice, or patient-care disruption to qualified incident response.
- Use this timeline to prepare the qualified-review conversation; do not use it to decide reportability.

## Source Basis

- NIST SP 800-61 Rev. 3: incident response should support preparation, detection, response, recovery, and continuous improvement across cybersecurity risk management.
- HIPAA Security Rule 45 CFR 164.308(a)(6): security incident procedures should support response, mitigation where practicable, and incident documentation.
- HHS HICP Technical Volume 1: small healthcare organizations often need practical, MSP-supported incident response workflows.
- CISA ransomware and incident playbooks: isolate impacted systems when needed, preserve evidence, coordinate response roles, and document actions.
"""


def incident_after_action_report(profile: dict) -> str:
    incident = _incident_profile(profile)
    rows = [
        [
            action.get("id", f"INC-AA-{index:03d}"),
            action.get("priority", "medium"),
            action.get("owner", "Practice owner/MSP"),
            action.get("action", "Action to complete"),
            action.get("evidence_needed", "Evidence reference needed"),
            action.get("due", "30 days"),
        ]
        for index, action in enumerate(incident.get("after_actions", []), start=1)
    ]
    if not rows:
        rows.append(
            [
                "INC-AA-001",
                "medium",
                profile["practice"].get("security_owner", "Practice owner"),
                "Review the incident timeline and assign remediation owners.",
                "Owner signoff and private evidence reference.",
                "30 days",
            ]
        )
    phase_review_rows = []
    for entry in incident.get("timeline", []):
        guidance = _entry_guidance(entry)
        phase_review_rows.append(
            [
                entry.get("phase", "Timeline event"),
                guidance.get("owner_lane", entry.get("owner", "Owner")),
                guidance.get("plain_english_goal", "Confirm facts and next owner."),
                _joined(guidance.get("completion_criteria", [])),
                entry.get("evidence_ref", "private evidence reference"),
                "Closed" if entry.get("complete") else "Needs owner review",
            ]
        )
    if not phase_review_rows:
        phase_review_rows.append(
            [
                "Tabletop review",
                "Practice owner/MSP",
                "Confirm facts, owners, and evidence references.",
                "owner assigned; evidence reference recorded; next action selected",
                "private evidence reference",
                "Needs owner review",
            ]
        )

    return f"""# Incident After-Action Report

Scenario: **{incident.get('scenario_name', 'Incident tabletop')}**

This report turns the timeline into owner/MSP follow-up work. It is an operational improvement packet, not a reportability conclusion, legal opinion, formal Security Risk Analysis, or incident-response substitute.

## What Worked

- A single owner/MSP timeline can preserve the order of events without exposing PHI or secrets.
- Evidence is tracked by reference ID, not by copying screenshots, logs, private URLs, contracts, or patient-level details into public artifacts.
- Legal/compliance, insurance, regulatory, and contract-notice questions stay parked for qualified reviewers.

## Phase Closeout Review

{table(['Phase', 'Owner lane', 'Goal', 'Completion criteria', 'Evidence reference', 'Closeout'], phase_review_rows)}

## Owner Review Agenda

- Which phase is still open, and who owns it?
- Which private evidence reference would a reviewer ask for first?
- Which MSP/vendor question is still unanswered?
- Which continuity workflow prevented unsafe data copies?
- Which improvement should be funded or completed in the next 30 days?

## Improvement Actions

{table(['ID', 'Priority', 'Owner', 'Action', 'Evidence needed', 'Due'], rows)}

## Reviewer Packet

- Incident evidence timeline.
- Private evidence reference list.
- Owner/MSP containment summary.
- Vendor notification or support-ticket reference, if applicable.
- Backup/restore and access-review evidence references for affected systems.
- List of decisions parked for counsel, compliance, insurer, vendor, or qualified incident responder.
"""


def connected_device_inventory(profile: dict) -> str:
    device_like = []
    device_keywords = ("imaging", "workstation", "phone", "device", "scanner", "lab", "x-ray", "sensor")
    critical_systems = {str(system).lower() for system in profile.get("downtime", {}).get("critical_systems", [])}
    for system in profile.get("systems", []):
        haystack = " ".join(
            str(system.get(key, "")).lower()
            for key in ["name", "category", "ephi_role", "access_method", "evidence_needed"]
        )
        if any(keyword in haystack for keyword in device_keywords) or str(system.get("name", "")).lower() in critical_systems:
            device_like.append(system)

    if not device_like:
        device_like = profile.get("systems", [])[:3]

    rows = []
    for system in device_like:
        rows.append(
            [
                system.get("name", "System or device"),
                system.get("vendor", "Unknown vendor"),
                system.get("access_method", "Network location/access path to confirm"),
                system.get("ephi_role", "PHI/ePHI role to confirm"),
                system.get("owner", profile["practice"].get("technical_owner", "MSP Lead")),
                "unknown - verify default credentials disabled",
                "manual workflow or restore path to confirm",
                "review vendor safety/security notices and patch advisories",
            ]
        )

    return f"""# Connected Device Inventory

This worksheet extends the ePHI flow map for small-practice IoMT and medical-device-adjacent systems. It is a readiness worksheet, not a live network scan, penetration test, FDA safety assessment, or compliance determination.

## Connected Device Worksheet

{table(['Device / system', 'Vendor', 'Network location or access path', 'PHI handled', 'Firmware / patch owner', 'Default credential status', 'Downtime fallback', 'Safety notice review'], rows)}

## Evidence To Request

- Current device or workstation inventory export, with owner and date observed.
- Vendor support path, remote-access method, and account owner.
- Firmware, patch, or managed endpoint status reference.
- Default credential exception review and compensating-control note.
- Backup/restore or downtime fallback for devices needed during patient care.
- Vendor safety/security notice review cadence and owner.

## Boundary

Record only reference IDs, owners, and short status summaries here. Keep serial numbers, screenshots, network diagrams, private IPs, raw logs, credentials, and patient details in the private/offline evidence binder.
"""


def portal_api_flow_review(profile: dict) -> str:
    portal_terms = ("portal", "api", "integration", "fhir", "messaging", "https", "app")
    rows = []
    for flow in profile.get("flows", []):
        haystack = " ".join(str(flow.get(key, "")).lower() for key in ["source", "destination", "vendor", "transmission", "evidence_needed"])
        if any(term in haystack for term in portal_terms):
            rows.append(
                [
                    flow.get("id", "FLOW"),
                    flow.get("source", "Source to confirm"),
                    flow.get("destination", "Destination to confirm"),
                    flow.get("vendor", "Vendor/app owner to confirm"),
                    flow.get("transmission", "Connection type to confirm"),
                    flow.get("ephi_type", "Data class to confirm"),
                    yn(bool(flow.get("baa_needed"))),
                    flow.get("evidence_needed", "Audit, access, retention, and export/delete evidence to request"),
                ]
            )

    if not rows:
        rows.append(["PORTAL-001", "Patient portal", "EHR or messaging vendor", "Vendor/app owner", "portal/API", "patient communication categories", "Yes", "Portal users, audit logs, secure messaging, retention, and export/delete evidence"])

    checklist = [
        "Portal users and role list, including inactive or shared-account exceptions.",
        "Patient identity workflow: invitation, registration, reset, proxy/delegate access, and support verification.",
        "FHIR/app/API connections: app name, vendor owner, scope, authorization path, and review date.",
        "Audit logs for portal access, secure messages, exports, failed logins, admin changes, and support access.",
        "Secure messaging settings, attachment rules, retention, and deletion/export workflow.",
        "Vendor ownership, BAA status, incident notice, subcontractors, and data-use terms.",
    ]

    return f"""# Portal And API Flow Review

This worksheet extends `ephi-flow-map.md` for portals, integrations, apps, and API/FHIR-style connections. It does not validate live APIs, prove identity controls, approve apps, or replace vendor/legal review.

## Portal And API Flows

{table(['Flow', 'Source', 'Destination', 'Vendor/app owner', 'Connection', 'Data category', 'BAA needed', 'Evidence needed'], rows)}

## Evidence Checklist

{chr(10).join(f'- [ ] {item}' for item in checklist)}

## Patient Identity Workflow

Document who can invite a patient, reset access, change contact details, approve proxy/delegate access, and handle portal support. Use reference IDs only; do not include patient examples.

## FHIR/app/API connections

For each app or integration, record owner, scope, vendor, authorization method, audit-log availability, export/delete path, and reviewer notes in the private binder.
"""


def external_evidence_precheck(profile: dict) -> str:
    precheck = external_precheck_profile(profile)
    scope = external_precheck_scope(profile)
    findings = external_precheck_findings(profile)
    scope_rows = []
    for domain in scope.get("domains", []) or []:
        scope_rows.append(["Domain", str(domain), "Public DNS/website context only"])
    for workflow in scope.get("workflows", []) or []:
        if not isinstance(workflow, dict):
            continue
        scope_rows.append(
            [
                str(workflow.get("workflow_type") or "Workflow"),
                str(workflow.get("name") or workflow.get("url_label") or "Patient-facing workflow"),
                str(workflow.get("patient_data_context") or "Data context to confirm"),
            ]
        )
    if not scope_rows:
        scope_rows.append(["Scope", "Not run", "No external pre-check scope was provided in the profile."])

    finding_rows = []
    for index, item in enumerate(findings, start=1):
        title = external_finding_title(item)
        finding_rows.append(
            [
                external_finding_id(item, index),
                external_finding_severity(item),
                str(item.get("page_label") or item.get("url_label") or "Public workflow"),
                str(item.get("observed_technology") or item.get("category") or "External observation"),
                str(item.get("network_destination") or item.get("host") or "Destination/host to confirm"),
                external_finding_recipient(item),
                str(
                    item.get("next_action")
                    or "Assign owner, request reference-only evidence, and route qualified-review questions before relying on the workflow."
                ),
            ]
        )
    if not finding_rows:
        finding_rows.append(["EXT-PRECHECK-000", "low", "Not run", "No observation", "No destination", "Owner/MSP", "Run only with authorization and reference-only evidence rules."])

    question_rows = [
        [
            "Website vendor / tag manager owner",
            "Which trackers, analytics tags, pixels, or scripts fire on appointment, intake, portal, payment, registration, or contact workflows?",
            "Tracker inventory, tag manager export, page/workflow label, date observed, and sanitized network destination summary.",
        ],
        [
            "Privacy/legal/compliance reviewer",
            "Does any tracker observation require BAA, authorization, privacy notice, contract, or formal risk-analysis review before the practice relies on the workflow?",
            "Reviewer disposition, vendor relationship status, data category summary, and decision note.",
        ],
        [
            "MSP / website host",
            "Can you confirm HTTPS redirect behavior, certificate validity, TLS posture, HSTS status, and ownership for patient-facing hosts?",
            "TLS scan summary, certificate expiry/issuer, HSTS status, covered host list, and MSP/vendor attestation.",
        ],
    ]

    source_notes = [
        "HHS/OCR tracking technology guidance says regulated entities must evaluate tracking technologies in authenticated pages and other contexts where PHI may be collected or disclosed.",
        "A June 20, 2024 federal court order vacated the portion of OCR guidance that treated an IP address plus a visit to certain unauthenticated public webpages as automatically triggering HIPAA obligations.",
        "This packet therefore flags potential privacy/security evidence questions for review. It does not declare a HIPAA violation, breach, legal conclusion, or regulatory finding.",
    ]

    return f"""# External Evidence Pre-Check

Purpose: collect safe public-site observations that can be turned into owner, MSP, website vendor, and qualified-review questions before a practice shares internal access or patient data.

Status: **{precheck.get('status', 'reference-only pre-check profile')}**

Authorization boundary: **{precheck.get('authorization', 'Run only with written authorization. Do not submit real patient data or collect sensitive payloads.')}**

## Scope Reviewed

{table(['Type', 'Target', 'Context'], scope_rows)}

## Observations

{table(['ID', 'Priority', 'Page/workflow', 'Observed item', 'Destination or host', 'Send to', 'Next action'], finding_rows)}

## Questions This Creates

{table(['Recipient', 'Question', 'Evidence to request'], question_rows)}

## Review Basis

{chr(10).join(f'- {note}' for note in source_notes)}

## Evidence Safety Boundary

- Do not submit real patient forms during public-site testing.
- Do not store patient-entered details, session cookies, private admin links, credentials, raw logs, raw contracts, or full intercepted payloads with sensitive data.
- Use page labels, timestamps, tag/script names, destination domains, certificate status, owner, and reference IDs.
- Keep screenshots or browser captures sanitized and in the private/offline evidence binder if needed.
"""


def incident_decision_log(profile: dict) -> str:
    rows = [
        ["Incident or concern", "What happened at a sanitized category level?", "Owner/MSP", "open", "Do not record patient names, screenshots, raw logs, or private URLs."],
        ["Technical containment", "What system/account/vendor path was contained or isolated?", profile["practice"].get("technical_owner", "MSP Lead"), "open", "Track actions, timestamps, and evidence reference IDs only."],
        ["Qualified legal/compliance decision", "Does this require breach-notification, contract, insurance, or regulatory analysis?", "Qualified reviewer", "parked for review", "The public packet does not decide reportability."],
        ["Owner communication", "What plain-English operational update can the owner approve?", profile["practice"].get("security_owner", "Office Manager"), "draft", "Keep incident-sensitive details out of public artifacts."],
    ]

    return f"""# Incident Decision Log

Use this as a handoff template when an outage, ransomware concern, lost device, vendor notice, misdirected message, or suspicious access question appears during the sprint. It separates technical response work from qualified breach-notification and legal/compliance decisions.

## Decision Log Template

{table(['Lane', 'Question to answer', 'Decision owner', 'Status', 'Evidence boundary'], rows)}

## Technical Containment

- Record system, account, vendor path, or workflow category affected.
- Record owner, date/time observed, action taken, and private evidence reference ID.
- Escalate to incident response if there is active compromise, ransomware, unauthorized access, lost device, or patient-care disruption.

## Qualified Legal/compliance Decision

- Park breach-notification, contractual notice, insurance, regulatory, and formal risk-analysis decisions for qualified reviewers.
- Do not use this public packet to decide whether an incident is reportable.
- Keep raw logs, patient details, screenshots, contracts, private URLs, and incident-sensitive facts outside generated public artifacts.

## Handoff Questions

- What was technically contained, by whom, and when?
- What evidence reference supports containment without exposing PHI or secrets?
- Which decisions require counsel, compliance, insurer, vendor, or incident-response review?
- What can staff safely do now while the formal decision is pending?
"""


def evidence_index(profile: dict) -> str:
    records = lifecycle_records(profile)
    rows = [
        [
            record["evidence_id"],
            record["evidence_type"],
            lifecycle_label(record["lifecycle_status"]),
            closeout_label(record["closeout_state"]),
            record["owner"],
            trace_label(record),
            _joined(record["acceptable_evidence"]),
            record["next_action"],
            _joined(record["artifact_refs"]),
        ]
        for record in records
    ]
    summary = summarize_lifecycle(records)
    return f"""# Evidence Binder Index

This is a lifecycle index for reference-only evidence. Store raw proof in the private/offline binder and keep this packet limited to owners, dates, status labels, trace context, and safe evidence references.

## Lifecycle Summary

- Total evidence rows: {summary['total']}
- Blocked: {summary['blocked']}
- Needs evidence: {summary['needs_evidence']}
- Ready for review: {summary['ready_for_review']}
- Closed: {summary['closed']}
- Traceable to ePHI flows: {summary['traceable_to_ephi']}

## Evidence Lifecycle

{table(['Evidence ID', 'Area', 'Lifecycle', 'Closeout', 'Owner', 'Trace', 'Acceptable evidence', 'Next action', 'Artifacts'], rows)}
"""


def owner_msp_handoff(profile: dict) -> str:
    risk, gaps = risk_level(profile)
    practice = profile["practice"]
    records = lifecycle_records(profile)
    closeout_rows = [
        [
            record["evidence_id"],
            closeout_label(record["closeout_state"]),
            record["owner"],
            trace_label(record),
            record["next_action"],
        ]
        for record in records
        if record["closeout_state"] in {"blocked", "needs_evidence", "ready_for_review"}
    ][:12]
    vendor_rows = []
    for vendor in profile["vendors"]:
        if vendor.get("touches_ephi") or vendor.get("risk") in {"high", "critical"}:
            vendor_rows.append(
                [
                    vendor["name"],
                    vendor["service"],
                    vendor["baa_status"],
                    vendor_soc2_status(vendor),
                    vendor_hitrust_status(vendor),
                    vendor["risk"],
                    "Practice manager",
                    "Confirm BAA scope, SOC 2/HITRUST evidence status, incident terms, subcontractors, and AI/data-use posture.",
                ]
            )
    access_actions = []
    readiness = profile["readiness"]
    if not readiness["mfa_ehr"]:
        access_actions.append("Enable or verify MFA for EHR access.")
    if not readiness["quarterly_access_review"]:
        access_actions.append("Export user lists and record a quarterly access review.")
    if not readiness["unique_accounts"]:
        access_actions.append("Remove shared accounts or document exception owners and sunset dates.")
    if not access_actions:
        access_actions.append("Keep current access controls on a quarterly review cadence.")

    return f"""# Owner/MSP Handoff

Practice: {practice['name']}

Initial risk level: **{risk}**

## Owner Decisions Needed

{chr(10).join(f'- {gap}' for gap in gaps) if gaps else '- No immediate owner decision gaps generated from the synthetic profile.'}

## Action Packet Summary

{action_packet_table(profile)}

## MSP / Technical Follow-Up

{chr(10).join(f'- {action}' for action in access_actions)}
- Confirm backup restore evidence for critical systems: {', '.join(profile['downtime']['critical_systems'])}.
- Confirm downtime owner, manual workaround, and escalation contact for each critical system.
- Return evidence references only; do not send PHI, passwords, private URLs, presigned links, or raw incident details.

## Vendor Follow-Up

{table(['Vendor', 'Service', 'BAA Status', 'SOC 2 Status', 'HITRUST Status', 'Risk', 'Owner', 'Ask'], vendor_rows) if vendor_rows else '- No vendor follow-up rows generated.'}

## Closeout Gates

{table(['Evidence', 'Closeout', 'Owner', 'Trace', 'Next action'], closeout_rows)}

## Handoff Boundary

This handoff is a coordination aid for the practice owner, MSP, and qualified reviewers. It does not issue compliance certification, provide legal advice, decide incident reporting duties, or replace a formal Security Risk Analysis.
"""


def limitations_appendix(profile: dict) -> str:
    return f"""# What This Packet Does and Does Not Prove

## What This Packet Does

- Organizes a synthetic or client-provided practice profile into a plain-English readiness packet.
- Highlights AI, vendor/BAA, ePHI-flow, access, backup, downtime, and evidence-reference gaps.
- Produces owner/MSP follow-up actions and a 30/60/90 roadmap.
- Creates reference-only evidence metadata and artifact hashes for generated packet files.

## What This Packet Does Not Prove

- It is not legal advice.
- It is not a HIPAA certification or legal opinion.
- It is not a formal HIPAA Security Risk Analysis opinion.
- It does not decide whether an incident is reportable.
- It is not penetration testing, vulnerability scanning, MDR, SOC, or incident response.
- It does not prove that a vendor, workflow, system, or AI tool is safe for PHI/ePHI.
- It does not verify real contracts, BAAs, subprocessors, access lists, backup restores, logs, or insurance requirements.

## Evidence Boundary

Use evidence references, owners, review dates, and sanitized descriptions. Do not include PHI/ePHI, patient identifiers, staff credentials, secrets, private URLs, presigned links, raw incident details, or full contract text in public packet artifacts.

## Recommended Review

Bring this packet to the practice owner, MSP/IT provider, counsel/compliance advisor, insurer, or qualified security reviewer before relying on it for operational decisions.
"""


def roadmap(profile: dict) -> str:
    risk, gaps = risk_level(profile)
    thirty = gaps[:3] or ["Review generated packet with practice owner and MSP."]
    sixty = gaps[3:6] or ["Validate evidence references and update vendor review dates."]
    ninety = [
        "Run a tabletop exercise and record lessons learned.",
        "Repeat access/vendor/backup evidence review.",
        "Prepare management signoff packet.",
    ]
    return f"""# 30-60-90 Roadmap

Initial risk level: **{risk}**

## First 30 Days

{chr(10).join(f'- {item}' for item in thirty)}

## Action Packets To Start

{action_packet_table(profile)}

## Days 31-60

{chr(10).join(f'- {item}' for item in sixty)}

## Days 61-90

{chr(10).join(f'- {item}' for item in ninety)}
"""


PACKET_KICKER = "Small Practice Security Kit"
PACKET_CSS_PATH = Path(__file__).resolve().parent / "static" / "packet.css"
PACKET_NOTICE = (
    "Not legal advice, not a certification, and not a substitute for qualified review. "
    "Do not enter PHI, secrets, or real incident details."
)
PRINT_HIDE_HEADERS = {
    "lifecycle",
    "closeout",
    "trace",
    "downstream artifacts",
    "closeout rule",
    "acceptable evidence",
    "unsafe inputs",
    "reviewer needed",
    "timeframe",
    "artifacts",
}
CHIP_CLASSES = {
    "yes": "chip-ok",
    "no": "chip-blocked",
    "high": "chip-high",
    "critical": "chip-high",
    "medium": "chip-medium",
    "low": "chip-low",
    "needs evidence": "chip-review",
    "requested": "chip-review",
    "blocked": "chip-blocked",
    "ready for review": "chip-review",
    "closed": "chip-ok",
    "provided": "chip-ok",
    "missing": "chip-blocked",
    "never touches the ehr": "chip-outside",
    "leaves or enters the ehr": "chip-crosses",
    "stays in the ehr": "chip-ok",
}


def packet_css() -> str:
    return PACKET_CSS_PATH.read_text(encoding="utf-8")


def heading_slug(title: str, used: dict[str, int]) -> str:
    base = slugify(title) or "section"
    count = used.get(base, 0) + 1
    used[base] = count
    return base if count == 1 else f"{base}_{count}"


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    return re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", escaped)


def render_status_cell(text: str) -> str:
    css = CHIP_CLASSES.get(text.strip().casefold())
    if css:
        return f'<span class="chip {css}">{inline_markdown(text)}</span>'
    return inline_markdown(text)


def _parse_table(lines: list[str]) -> list[list[str]]:
    parsed: list[list[str]] = []
    for index, line in enumerate(lines):
        cells = [cell.strip().replace("\\|", "|") for cell in re.split(r"(?<!\\)\|", line.strip("|"))]
        if index == 1 and all("-" in cell and set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        parsed.append(cells)
    return parsed


def render_finding_rows(headers: list[str], rows: list[list[str]]) -> str:
    items = []
    for row in rows:
        title = row[0] if row else "Item"
        dek_parts: list[str] = []
        ask = ""
        for header, cell in zip(headers[1:], row[1:]):
            key = header.casefold()
            if key in PRINT_HIDE_HEADERS or key in {"trace", "closeout rule"}:
                continue
            if key in {"evidence needed", "next action", "ask"}:
                ask = cell
                continue
            if cell:
                dek_parts.append(cell)
        dek = " · ".join(dek_parts)
        ask_html = f'<p class="finding-ask">{inline_markdown(ask)}</p>' if ask else ""
        items.append(
            "<li>"
            f'<p class="finding-hed">{render_status_cell(title)}</p>'
            f'<p class="finding-dek">{inline_markdown(dek)}</p>'
            f"{ask_html}"
            "</li>"
        )
    return f'<ol class="findings">{"".join(items)}</ol>'


def render_table(lines: list[str]) -> str:
    parsed = _parse_table(lines)
    if not parsed:
        return ""
    headers = parsed[0]
    keys = [header.casefold() for header in headers]
    if "trace" in keys and "closeout rule" in keys:
        return ""
    if len(headers) >= 6:
        return render_finding_rows(headers, parsed[1:])
    hide = [header.strip().casefold() in PRINT_HIDE_HEADERS for header in headers]
    rows = []
    for index, cells in enumerate(parsed):
        tag = "th" if index == 0 else "td"
        rendered = []
        for column, cell in enumerate(cells):
            extra = ' class="print-hide"' if column < len(hide) and hide[column] else ""
            content = inline_markdown(cell) if index == 0 else render_status_cell(cell)
            rendered.append(f"<{tag}{extra}>{content}</{tag}>")
        rows.append("<tr>" + "".join(rendered) + "</tr>")
    return '<div class="table-wrap"><table>' + "".join(rows) + "</table></div>"


def render_html(markdown: str, profile: dict) -> str:
    blocks: list[str] = []
    table_buffer: list[str] = []
    list_buffer: list[str] = []
    toc: list[tuple[str, str]] = []
    used_slugs: dict[str, int] = {}
    section_open = False

    def flush_table() -> None:
        nonlocal table_buffer
        if table_buffer:
            blocks.append(render_table(table_buffer))
            table_buffer = []

    def flush_list() -> None:
        nonlocal list_buffer
        if list_buffer:
            css = ' class="findings"' if any(item.startswith("**") for item in list_buffer) else ""
            blocks.append("<ul" + css + ">" + "".join(f"<li>{inline_markdown(item)}</li>" for item in list_buffer) + "</ul>")
            list_buffer = []

    def close_section() -> None:
        nonlocal section_open
        if section_open:
            blocks.append("</section>")
            section_open = False

    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            flush_list()
            table_buffer.append(stripped)
            continue
        flush_table()
        if stripped.startswith("- "):
            list_buffer.append(stripped[2:])
            continue
        flush_list()
        if not stripped or stripped == "---":
            continue
        if stripped.startswith("# "):
            close_section()
            title = stripped[2:]
            slug = heading_slug(title, used_slugs)
            primary = title in MAIN_SECTION_TITLES
            toc.append((slug, title, primary))
            css = "packet-section" if primary else "packet-section appendix"
            blocks.append(f'<section class="{css}" id="{html.escape(slug)}"><h1>{inline_markdown(title)}</h1>')
            section_open = True
        elif stripped.startswith("## "):
            blocks.append(f"<h2>{inline_markdown(stripped[3:])}</h2>")
        else:
            blocks.append(f"<p>{inline_markdown(stripped)}</p>")
    flush_table()
    flush_list()
    close_section()

    practice = profile["practice"]
    title = f"{practice['name']} Security Review Packet"
    risk, _gaps = risk_level(profile)
    week_items = joined_findings(profile)[:4]
    week_html: list[str] = []
    for item in week_items:
        if "→" in item["path"]:
            source, dest = item["path"].split("→", 1)
            path_html = (
                f"{html.escape(source.strip())} <span class=\"arrow\">→</span> "
                f"{html.escape(dest.strip())}"
            )
        else:
            path_html = html.escape(item["path"])
        week_html.append(
            "<li>"
            f'<p class="path">{path_html}</p>'
            f'<p class="why">{html.escape(item["why"])}</p>'
            f'<p class="ask">{html.escape(item["owner"])} — {html.escape(item["ask"])}</p>'
            "</li>"
        )
    if not week_html:
        week_html.append("<li><p class=\"path\">Review the packet with the owner and MSP.</p></li>")
    main_toc = "".join(
        f'<li><a href="#{html.escape(slug)}">{inline_markdown(label)}</a></li>'
        for slug, label, primary in toc
        if primary
    )
    note_toc = "".join(
        f'<li><a href="#{html.escape(slug)}">{inline_markdown(label)}</a></li>'
        for slug, label, primary in toc
        if not primary
    )
    notes_block = (
        f'<p class="toc-notes-label">Notes</p><ol class="toc-notes">{note_toc}</ol>' if note_toc else ""
    )
    body = "\n".join(blocks)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
{packet_css()}
  </style>
</head>
<body>
  <div class="print-footer">{html.escape(str(practice["name"]))} · {html.escape(str(practice["review_period"]))} · Not legal advice</div>
  <main class="shell">
    <header class="cover">
      <div class="masthead">
        <p class="kicker">{PACKET_KICKER}</p>
        <p class="issue">{html.escape(str(practice["type"]))} · {html.escape(str(practice["review_period"]))} · {html.escape(risk)} risk</p>
      </div>
      <h1>{html.escape(str(practice["name"]))}</h1>
      <p class="deck">Security review packet</p>
      <p class="verdict">{html.escape(verdict(profile))}</p>
      <div class="next-block">
        <span class="label">This week</span>
        <ol class="week">{"".join(week_html)}</ol>
      </div>
    </header>
    <p class="notice">{PACKET_NOTICE}</p>
    <nav class="toc" aria-label="Packet contents">
      <h2>In this packet</h2>
      <ol>{main_toc}</ol>
      {notes_block}
    </nav>
    {body}
  </main>
</body>
</html>
"""


def build_packet(profile_path: Path, output_root: Path = OUT, *, generated_at: str | None = None) -> Path:
    profile = load_profile(profile_path)
    sensitive_findings = blocking_findings(profile)
    if sensitive_findings:
        joined = "; ".join(f"{finding.path}: {finding.message}" for finding in sensitive_findings[:5])
        raise ValueError(f"profile contains blocked sensitive data; use references only ({joined})")
    out_dir = output_root / slugify(profile["practice"]["name"])
    out_dir.mkdir(parents=True, exist_ok=True)
    risk, gaps = risk_level(profile)
    docs = {
        "readiness-review.md": readiness_review(profile),
        "ephi-flow-map.md": ephi_flow_map(profile),
        "vendor-baa-review.md": vendor_review(profile),
        "ai-workflow-review.md": ai_review(profile),
        "downtime-ransomware-tabletop.md": downtime_packet(profile),
        "connected-device-inventory.md": connected_device_inventory(profile),
        "portal-api-flow-review.md": portal_api_flow_review(profile),
        "external-evidence-precheck.md": external_evidence_precheck(profile),
        "incident-decision-log.md": incident_decision_log(profile),
        "incident-evidence-timeline.md": incident_evidence_timeline(profile),
        "incident-after-action-report.md": incident_after_action_report(profile),
        "evidence-binder-index.md": evidence_index(profile),
        "owner-msp-handoff.md": owner_msp_handoff(profile),
        "30-60-90-roadmap.md": roadmap(profile),
        "limitations-appendix.md": limitations_appendix(profile),
    }
    for name, content in docs.items():
        (out_dir / name).write_text(content, encoding="utf-8", newline="\n")
    packet = "\n\n---\n\n".join(docs.values())
    (out_dir / "review-packet.md").write_text(packet, encoding="utf-8", newline="\n")
    (out_dir / "review-packet.html").write_text(render_html(packet, profile), encoding="utf-8", newline="\n")
    manifest = build_packet_manifest(
        profile=profile,
        profile_path=profile_path,
        out_dir=out_dir,
        artifact_names=[*docs.keys(), "review-packet.md", "review-packet.html"],
        risk=risk,
        gaps=gaps,
        generated_at=generated_at,
    )
    (out_dir / "packet-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out_dir
