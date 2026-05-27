from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path

from .brand import VELARI_CSS_VARIABLES
from .evidence_lifecycle import (
    build_evidence_lifecycle,
    closeout_label,
    lifecycle_by_source,
    lifecycle_label,
    summarize_lifecycle,
    trace_label,
)
from .manifest import build_packet_manifest, finding_entries
from .profile import load_profile, slugify
from .sensitive_data import blocking_findings
from .vendor_evidence import vendor_hitrust_status, vendor_soc2_status


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out"


def yn(value: bool) -> str:
    return "Yes" if value else "No"


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
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
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
    risk, gaps = risk_level(profile)
    readiness = profile["readiness"]
    readiness_lifecycle = lifecycle_by_source(lifecycle_records(profile), "readiness")
    rows = [
        ["Email MFA", yn(readiness["mfa_email"]), "Access"],
        ["EHR MFA", yn(readiness["mfa_ehr"]), "Access"],
        ["Unique accounts", yn(readiness["unique_accounts"]), "Access"],
        ["Quarterly access review", yn(readiness["quarterly_access_review"]), "Evidence"],
        ["Tested backups", yn(readiness["tested_backups"]), "Resilience"],
        ["Vendor inventory", yn(readiness["vendor_inventory"]), "Vendor"],
        ["BAA register", yn(readiness["baa_register"]), "Vendor"],
        ["Incident contact list", yn(readiness["incident_contact_list"]), "Incident"],
        ["Downtime plan", yn(readiness["downtime_plan"]), "Resilience"],
        ["Training current", yn(readiness["security_training_current"]), "Workforce"],
        ["Log review cadence", yn(readiness["log_review_cadence"]), "Monitoring"],
    ]
    closeout_rows = []
    for key, record in readiness_lifecycle.items():
        if key in {"mfa_email", "vendor_inventory", "incident_contact_list", "security_training_current"} and record["closeout_state"] == "closed":
            continue
        closeout_rows.append(
            [
                record["title"],
                lifecycle_label(record["lifecycle_status"]),
                closeout_label(record["closeout_state"]),
                record["owner"],
                _joined(record["acceptable_evidence"]),
                record["closeout_rule"],
            ]
        )
    return f"""# Readiness Review

Practice: {profile['practice']['name']}

Overall initial risk: **{risk}**

{table(['Item', 'Ready?', 'Area'], rows)}

## Priority Gaps

{chr(10).join(f'- {gap}' for gap in gaps) if gaps else '- No priority gaps found.'}

## Evidence Closeout Queue

{table(['Item', 'Lifecycle', 'Closeout', 'Owner', 'Acceptable evidence', 'Closeout rule'], closeout_rows)}
"""


def ephi_flow_map(profile: dict) -> str:
    flow_lifecycle = lifecycle_by_source(lifecycle_records(profile), "flow")
    system_rows = [[s["name"], s["category"], s["ephi_role"], s["vendor"], s["evidence_needed"]] for s in profile["systems"]]
    flow_rows = [
        [
            f["id"],
            f["source"],
            f["destination"],
            f["vendor"],
            f["ephi_type"],
            yn(f["baa_needed"]),
            f["risk"],
            lifecycle_label(flow_lifecycle[f["id"]]["lifecycle_status"]),
            closeout_label(flow_lifecycle[f["id"]]["closeout_state"]),
            f["evidence_needed"],
        ]
        for f in profile["flows"]
    ]
    trace_rows = [
        [
            record["source_ref"],
            trace_label(record),
            _joined(record["artifact_refs"]),
            record["closeout_rule"],
        ]
        for record in flow_lifecycle.values()
    ]
    return f"""# ePHI Flow Map

## Systems

{table(['System', 'Category', 'ePHI Role', 'Vendor', 'Evidence Needed'], system_rows)}

## Flows

{table(['Flow', 'Source', 'Destination', 'Vendor', 'ePHI Type', 'BAA Needed', 'Risk', 'Lifecycle', 'Closeout', 'Evidence Needed'], flow_rows)}

## Traceability Summary

{table(['Flow', 'Trace', 'Downstream artifacts', 'Closeout rule'], trace_rows)}
"""


def vendor_review(profile: dict) -> str:
    vendor_lifecycle = lifecycle_by_source(lifecycle_records(profile), "vendor")
    rows = [
        [
            v["name"],
            v["service"],
            yn(v["touches_ephi"]),
            v["baa_status"],
            v["ai_training_use"],
            vendor_soc2_status(v),
            vendor_hitrust_status(v),
            v["subcontractors_known"],
            v["incident_notification_terms"],
            v["risk"],
            lifecycle_label(vendor_lifecycle[v["name"]]["lifecycle_status"]),
            closeout_label(vendor_lifecycle[v["name"]]["closeout_state"]),
            trace_label(vendor_lifecycle[v["name"]]),
        ]
        for v in profile["vendors"]
    ]
    return f"""# Vendor and BAA Review

{table(['Vendor', 'Service', 'Touches ePHI?', 'BAA Status', 'AI Training Use', 'SOC 2 Status', 'HITRUST Status', 'Subcontractors', 'Incident Terms', 'Risk', 'Lifecycle', 'Closeout', 'Trace'], rows)}

## Next Evidence

- Confirm BAA review date for each vendor touching ePHI.
- Record SOC 2 and HITRUST evidence status as provided, not provided, absent, or not applicable; do not infer attestations from marketing pages.
- Record incident notification terms.
- Ask AI/data-use questions for any vendor using automation or model training.
"""


def ai_review(profile: dict) -> str:
    ai_lifecycle = lifecycle_by_source(lifecycle_records(profile), "ai_workflow")
    rows = [
        [
            w["name"],
            w["proposed_use"],
            w["data_used"],
            w["vendor"],
            w["decision"],
            lifecycle_label(ai_lifecycle[w["name"]]["lifecycle_status"]),
            closeout_label(ai_lifecycle[w["name"]]["closeout_state"]),
            trace_label(ai_lifecycle[w["name"]]),
            w["evidence_needed"],
        ]
        for w in profile["ai_workflows"]
    ]
    return f"""# AI Workflow Review

{table(['Workflow', 'Use', 'Data Used', 'Vendor', 'Decision', 'Lifecycle', 'Closeout', 'Trace', 'Evidence Needed'], rows)}

## Rules of Thumb

- Allowed: generic administrative drafting with no patient or clinical details.
- Restricted: workflows involving claim, treatment, billing, or operationally sensitive data.
- Prohibited: pasting patient-level notes or identifiers into tools without approved safeguards and a reviewed vendor relationship.
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


def incident_evidence_timeline(profile: dict) -> str:
    incident = _incident_profile(profile)
    rows = []
    for entry in incident.get("timeline", []):
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

## Decision Gates

{table(['Gate', 'Owner', 'Trigger', 'Action'], gate_rows)}

## Handoff Rules

- Separate technical containment from breach-notification, insurance, contract, regulatory, and legal/compliance decisions.
- Preserve private evidence references without copying raw evidence into the public packet.
- Escalate active compromise, ransomware, unauthorized access, lost device, vendor breach notice, or patient-care disruption to qualified incident response.
- Use this timeline to prepare the qualified-review conversation; do not use it to decide reportability.
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

    return f"""# Incident After-Action Report

Scenario: **{incident.get('scenario_name', 'Incident tabletop')}**

This report turns the timeline into owner/MSP follow-up work. It is an operational improvement packet, not a reportability conclusion, legal opinion, formal Security Risk Analysis, or incident-response substitute.

## What Worked

- A single owner/MSP timeline can preserve the order of events without exposing PHI or secrets.
- Evidence is tracked by reference ID, not by copying screenshots, logs, private URLs, contracts, or patient-level details into public artifacts.
- Legal/compliance, insurance, regulatory, and contract-notice questions stay parked for qualified reviewers.

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


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    return re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", escaped)


def render_table(lines: list[str]) -> str:
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        tag = "th" if not rows else "td"
        rows.append("<tr>" + "".join(f"<{tag}>{inline_markdown(cell)}</{tag}>" for cell in cells) + f"</tr>")
    return "<div class='table-wrap'><table>" + "".join(rows) + "</table></div>"


def render_html(markdown: str, profile: dict) -> str:
    blocks: list[str] = []
    table_buffer: list[str] = []
    list_buffer: list[str] = []

    def flush_table() -> None:
        nonlocal table_buffer
        if table_buffer:
            blocks.append(render_table(table_buffer))
            table_buffer = []

    def flush_list() -> None:
        nonlocal list_buffer
        if list_buffer:
            blocks.append("<ul>" + "".join(f"<li>{inline_markdown(item)}</li>" for item in list_buffer) + "</ul>")
            list_buffer = []

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
        if not stripped:
            continue
        if stripped == "---":
            blocks.append("<hr>")
        elif stripped.startswith("# "):
            blocks.append(f"<section class='packet-section'><h1>{inline_markdown(stripped[2:])}</h1>")
        elif stripped.startswith("## "):
            blocks.append(f"<h2>{inline_markdown(stripped[3:])}</h2>")
        else:
            blocks.append(f"<p>{inline_markdown(stripped)}</p>")
    flush_table()
    flush_list()
    practice = profile["practice"]
    title = f"{practice['name']} Security Review Packet"
    body = "\n".join(blocks)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{ {VELARI_CSS_VARIABLES} }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--paper); color: var(--ink); font-family: Inter, Avenir Next, "Segoe UI", Arial, sans-serif; line-height: 1.55; }}
    .shell {{ max-width: 1120px; margin: 0 auto; padding: 32px 22px 56px; }}
    .cover {{ background: var(--app-bg); color: var(--text-on-dark); border-top: 8px solid var(--gold); border-radius: var(--radius); padding: 34px; display: grid; gap: 8px; box-shadow: var(--shadow); }}
    .kicker {{ color: var(--gold-soft); font-weight: 800; text-transform: uppercase; font-size: 12px; }}
    h1, h2 {{ line-height: 1.12; letter-spacing: 0; }}
    .cover h1 {{ font-size: clamp(34px, 5vw, 54px); margin: 0; max-width: 900px; }}
    .meta {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; margin-top: 18px; }}
    .meta div {{ border: 1px solid var(--line-strong); padding: 10px; background: var(--elevated); }}
    .meta strong {{ display: block; font-size: 12px; color: var(--muted-inverse); margin-bottom: 3px; }}
    .notice {{ background: var(--surface); border-left: 4px solid var(--gold); border-radius: var(--radius); box-shadow: var(--shadow); padding: 12px 14px; margin: 18px 0; font-size: 14px; }}
    .packet-section {{ display: block; padding: 24px; margin: 16px 0; border: 1px solid var(--line); border-radius: var(--radius); background: var(--surface); box-shadow: var(--shadow); }}
    .packet-section h1 {{ font-size: 30px; margin: 0 0 12px; }}
    h2 {{ font-size: 20px; margin: 22px 0 10px; color: var(--primary); }}
    p, li {{ font-size: 15px; }}
    .table-wrap {{ overflow-x: auto; margin: 12px 0 20px; border: 1px solid var(--line); background: var(--surface); }}
    table {{ width: 100%; border-collapse: collapse; min-width: 760px; font-size: 13px; }}
    th {{ text-align: left; background: var(--accent-soft); color: var(--primary); }}
    th, td {{ border-bottom: 1px solid var(--line); padding: 9px 10px; vertical-align: top; }}
    tr:last-child td {{ border-bottom: 0; }}
    hr {{ border: 0; border-top: 1px solid var(--line); margin: 28px 0; }}
    @media print {{
      :root {{ --bg: #e9f0f7; --paper: #e9f0f7; --surface: #f8fafc; --surface-strong: #f8fafc; --panel: #f8fafc; --elevated: #e9f0f7; --ink: #050a10; --muted: #64748b; --line: #94a3b8; --primary-soft: #e9f0f7; --blue-soft: #e9f0f7; }}
      body {{ background: var(--paper); color: var(--ink); }}
      .shell {{ max-width: none; padding: 0.4in; }}
      .table-wrap {{ overflow: visible; }}
      table {{ min-width: 0; font-size: 10px; }}
      .packet-section {{ page-break-inside: avoid; }}
    }}
    @media (max-width: 760px) {{ .meta {{ grid-template-columns: 1fr; }} .cover h1 {{ font-size: 34px; }} }}
  </style>
</head>
<body>
  <main class="shell">
    <header class="cover">
      <div class="kicker">Velari Security Kit</div>
      <h1>{html.escape(title)}</h1>
      <div class="meta">
        <div><strong>Practice Type</strong>{html.escape(str(practice['type']))}</div>
        <div><strong>Review Period</strong>{html.escape(str(practice['review_period']))}</div>
        <div><strong>Security Owner</strong>{html.escape(str(practice['security_owner']))}</div>
        <div><strong>Technical Owner</strong>{html.escape(str(practice['technical_owner']))}</div>
      </div>
    </header>
    <div class="notice">This packet is an operational planning aid. It is not legal advice, does not establish legal or regulatory status, does not decide incident reporting duties, and is not a substitute for qualified review. Do not include PHI, secrets, credentials, or real incident details.</div>
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
