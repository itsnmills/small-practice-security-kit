from __future__ import annotations

from typing import Any

from .sensitive_data import SensitiveFinding, find_sensitive_data


INCIDENT_BOUNDARY = (
    "Use categories, owners, timestamps, and evidence reference IDs only. Do not include PHI, patient identifiers, "
    "screenshots, raw logs, private URLs, credentials, vendor contracts, or real incident details."
)


SCENARIOS: dict[str, dict[str, Any]] = {
    "suspicious_login": {
        "label": "Suspicious login",
        "summary": "Staff or MSP notices an unusual login, admin alert, or account activity pattern.",
        "systems": ["Email", "Cloud EHR"],
        "phases": [
            ["T+00", "Detection", "Suspicious login category is reported by staff, owner, vendor, or MSP.", "Is there active unauthorized access or account misuse?"],
            ["T+15", "Triage", "MSP reviews affected account, admin role, MFA, session, and vendor-support categories.", "Which sessions, accounts, or vendor paths should be contained first?"],
            ["T+30", "Containment", "Owner/MSP records reference-only containment action and preserves private evidence references.", "What was contained, by whom, and when?"],
            ["T+60", "Qualified review", "Owner parks reportability, insurance, contract, and regulatory questions for qualified reviewers.", "Which facts and private evidence references are needed for qualified review?"],
            ["T+1 business day", "After-action", "Practice assigns access-review, MFA, log-review, and staff-communication improvements.", "Which improvements must close before the tabletop is complete?"],
        ],
    },
    "ehr_downtime": {
        "label": "EHR downtime",
        "summary": "EHR is unavailable during patient-care operations and staff need continuity decisions.",
        "systems": ["Cloud EHR", "Billing Portal", "Phones"],
        "phases": [
            ["T+00", "Detection", "Staff report EHR unavailability at a sanitized workflow level.", "Is patient-care continuity affected?"],
            ["T+15", "Continuity", "Practice switches to downtime workflow and records owner approval reference.", "Which manual workflow keeps care moving without unsafe data copies?"],
            ["T+30", "Vendor/MSP triage", "MSP and vendor-support categories are reviewed for outage scope and restoration path.", "Which vendor or MSP reference confirms current status?"],
            ["T+60", "Qualified review", "Owner parks insurance, contract, and regulatory questions for qualified reviewers.", "Which outage facts and private evidence references need qualified review?"],
            ["T+1 business day", "After-action", "Practice assigns restore-test, downtime workflow, and communication improvements.", "Which resilience evidence must be refreshed?"],
        ],
    },
    "ransomware_concern": {
        "label": "Ransomware concern",
        "summary": "A system, endpoint, vendor notice, or staff report raises a ransomware concern.",
        "systems": ["Cloud EHR", "Shared Drive", "Billing Portal"],
        "phases": [
            ["T+00", "Detection", "Ransomware concern is reported as a category without copying screenshots or raw indicators.", "Is there active compromise or patient-care disruption?"],
            ["T+15", "Containment", "MSP identifies affected system, account, endpoint, backup, and vendor-support categories.", "Which systems or access paths should be isolated or reviewed first?"],
            ["T+30", "Continuity", "Practice confirms downtime workflow and critical-system fallback categories.", "Can care continue safely while evidence is preserved privately?"],
            ["T+60", "Qualified review", "Owner escalates to qualified incident response, insurer, counsel, or compliance reviewer as appropriate.", "Which private evidence references must be prepared for qualified review?"],
            ["T+1 business day", "After-action", "Practice assigns backup, restore-test, MFA, access review, and staff-training improvements.", "Which high-priority fixes must close in 30 days?"],
        ],
    },
    "vendor_notice": {
        "label": "Vendor notice",
        "summary": "A vendor sends an outage, security, privacy, support-access, or incident-related notice.",
        "systems": ["Example EHR Vendor", "Billing Portal"],
        "phases": [
            ["T+00", "Detection", "Owner receives a vendor notice and records a private reference only.", "Does the notice affect ePHI, access, availability, or contract terms?"],
            ["T+15", "Scope review", "Practice identifies affected service, workflow category, BAA status, support contact, and incident terms.", "Which vendor facts are missing or need confirmation?"],
            ["T+30", "Continuity", "Owner/MSP reviews whether operations, patient messaging, billing, or EHR access are affected.", "Which operational fallback is needed now?"],
            ["T+60", "Qualified review", "Owner parks contract, privacy, insurance, regulatory, and legal/compliance questions for qualified reviewers.", "Which vendor evidence references are needed for qualified review?"],
            ["T+1 business day", "After-action", "Practice assigns vendor follow-up, BAA review, incident-term review, and evidence-refresh actions.", "Which vendor questions must be answered before closure?"],
        ],
    },
    "lost_device": {
        "label": "Lost device",
        "summary": "A workstation, laptop, phone, scanner, or removable device is reported missing or unaccounted for.",
        "systems": ["Dental Imaging Workstation", "Shared Drive", "Email"],
        "phases": [
            ["T+00", "Detection", "Lost-device concern is reported without device serials, screenshots, patient examples, or raw location data.", "Could the device access or store patient-data categories?"],
            ["T+15", "Containment", "MSP reviews encryption, remote wipe, account access, MFA, and session categories.", "Which access paths or sessions should be disabled first?"],
            ["T+30", "Evidence preservation", "Owner records reference-only evidence for device inventory, encryption, remote wipe, and access review.", "Which private evidence references support containment?"],
            ["T+60", "Qualified review", "Owner parks reportability, insurance, regulatory, and legal/compliance questions for qualified reviewers.", "Which facts require qualified review?"],
            ["T+1 business day", "After-action", "Practice assigns device inventory, encryption, access review, and staff-reporting improvements.", "Which controls must be refreshed before closure?"],
        ],
    },
    "misdirected_message": {
        "label": "Misdirected message",
        "summary": "A patient-message, email, portal, fax, or referral workflow is sent to the wrong destination category.",
        "systems": ["Patient Messaging Portal", "Email", "Cloud EHR"],
        "phases": [
            ["T+00", "Detection", "Misdirected message category is reported without patient details or message contents.", "What workflow category was affected?"],
            ["T+15", "Containment", "Owner/MSP reviews message recall, access, forwarding, portal, and staff workflow categories.", "What can be contained without copying message contents?"],
            ["T+30", "Evidence preservation", "Practice records private reference IDs for workflow, owner decision, and containment note.", "Which evidence references support the timeline?"],
            ["T+60", "Qualified review", "Owner parks privacy, reporting, contract, insurance, and regulatory questions for qualified reviewers.", "Which facts and evidence references need qualified review?"],
            ["T+1 business day", "After-action", "Practice assigns staff guidance, secure-message workflow, forwarding review, and training updates.", "Which process improvements prevent recurrence?"],
        ],
    },
}


PHASE_GUIDANCE: dict[str, dict[str, list[str] | str]] = {
    "detection": {
        "owner_lane": "Owner/MSP",
        "source_alignment": [
            "NIST CSF 2.0 Detect: find and analyze possible attacks or compromises",
            "HIPAA Security Rule 45 CFR 164.308(a)(6): identify and respond to suspected or known incidents",
            "CISA playbook pattern: collect and preserve enough data to verify, categorize, prioritize, and report internally",
        ],
        "plain_english_goal": "Confirm whether the concern is a normal operational issue, a security event, or something that needs immediate containment without copying sensitive evidence into the kit.",
        "owner_prompt": "What did we notice, who owns the next decision, and where is the private evidence reference?",
        "staff_script": "Thanks for reporting this. Do not forward screenshots or patient details. Tell the owner which system or workflow category is affected and when you noticed it.",
        "do_now": [
            "Record the concern category, reporter role, time observed, and affected system category.",
            "Assign a practice owner and technical owner before anyone starts changing systems.",
            "Create a private evidence reference outside the public packet for screenshots, alerts, or logs.",
            "Check whether patient-care operations, admin access, backups, or vendor access are affected.",
        ],
        "ask_msp_or_vendor": [
            "Can you confirm whether this is active unauthorized access, service outage, malware, or a false alarm?",
            "Which systems, accounts, devices, integrations, or vendor-support paths should be reviewed first?",
            "What private ticket or evidence reference should the practice record?",
        ],
        "allowed_inputs": [
            "what category of concern was noticed",
            "which system or workflow category is affected",
            "who noticed it",
            "when it was observed",
            "private evidence reference ID",
        ],
        "blocked_inputs": [
            "patient names or identifiers",
            "screenshots",
            "raw logs",
            "credentials or MFA codes",
            "private URLs",
        ],
        "evidence_required": [
            "private detection note reference",
            "owner or MSP observation reference",
            "affected system category",
        ],
        "completion_criteria": [
            "concern category recorded",
            "initial owner assigned",
            "private evidence reference created",
            "escalation trigger reviewed",
        ],
        "escalation_triggers": [
            "active unauthorized access",
            "ransomware indicator",
            "patient-care disruption",
            "lost device with patient-data access",
            "vendor breach/security notice",
        ],
    },
    "continuity": {
        "owner_lane": "Practice owner/Office manager",
        "source_alignment": [
            "NIST CSF 2.0 Recover: restore assets and operations affected by an incident",
            "HIPAA Security Rule contingency planning: continue critical business processes while protecting ePHI",
            "HICP small-organization reality: small practices often rely on simple downtime workflows and outsourced IT",
        ],
        "plain_english_goal": "Keep care and core operations moving with the least risky manual workflow while the technical owner investigates.",
        "owner_prompt": "Can the practice continue safely, and which workflow is approved until systems return?",
        "staff_script": "Use the approved downtime workflow only. Do not create new spreadsheets, photos, exports, or message threads unless the owner has approved the method.",
        "do_now": [
            "Name the critical workflow affected: scheduling, chart access, billing, phones, imaging, prescribing, or patient messaging.",
            "Choose the approved manual workaround and owner.",
            "Record where the downtime workflow lives by reference ID, not by copying patient-level data.",
            "Set a check-in time for the owner and MSP to reassess continuity risk.",
        ],
        "ask_msp_or_vendor": [
            "Which services are degraded, unavailable, or still safe to use?",
            "What restoration estimate or vendor-status reference can be shared with the owner?",
            "What should staff avoid doing until restoration is confirmed?",
        ],
        "allowed_inputs": [
            "manual workflow category",
            "critical system category",
            "staff role owner",
            "downtime form or packet reference",
            "owner approval reference",
        ],
        "blocked_inputs": [
            "patient schedule details",
            "patient message contents",
            "clinical note text",
            "billing claim details",
        ],
        "evidence_required": [
            "downtime workflow reference",
            "critical-system owner",
            "patient-care continuity decision reference",
        ],
        "completion_criteria": [
            "manual workflow selected",
            "critical systems listed",
            "owner approval reference recorded",
            "unsafe data-copy risk reviewed",
        ],
        "escalation_triggers": [
            "care cannot continue safely",
            "communications unavailable",
            "backup or restore path unknown",
            "multiple critical systems unavailable",
        ],
    },
    "containment": {
        "owner_lane": "MSP/technical owner",
        "source_alignment": [
            "NIST CSF 2.0 Respond: take action regarding a detected incident",
            "CISA ransomware response guidance: determine impacted systems and isolate them when needed",
            "CISA playbook containment: reduce immediate impact while considering evidence preservation",
        ],
        "plain_english_goal": "Limit further harm while preserving the facts a qualified responder, insurer, vendor, or reviewer may need later.",
        "owner_prompt": "What can be isolated, disabled, reset, or monitored now without destroying evidence or disrupting care unnecessarily?",
        "staff_script": "Stop using the affected system or account if the owner or MSP says to. Do not wipe devices, reinstall software, delete messages, or clear alerts.",
        "do_now": [
            "Assign the technical owner and record the containment action category.",
            "Confirm whether the suspected path is account, endpoint, email, EHR, vendor-support, network, backup, or shared-drive related.",
            "Record any isolation or access action by ticket/reference ID.",
            "Preserve private evidence before destructive remediation whenever qualified guidance is needed.",
        ],
        "ask_msp_or_vendor": [
            "Which systems or accounts are believed impacted, and which are confirmed clean enough to keep operating?",
            "Should any system be isolated from the network, have sessions revoked, or have privileged access rotated?",
            "Should forensic images, memory capture, log export, or vendor evidence be preserved by a qualified party before rebuilding?",
        ],
        "allowed_inputs": [
            "account category",
            "device category",
            "vendor support path",
            "session/access action category",
            "ticket or action reference",
        ],
        "blocked_inputs": [
            "user passwords",
            "session tokens",
            "raw firewall logs",
            "endpoint screenshots",
            "private IPs or admin URLs",
        ],
        "evidence_required": [
            "containment action reference",
            "affected account/system category",
            "MSP or vendor ticket reference",
        ],
        "completion_criteria": [
            "technical owner assigned",
            "containment action category recorded",
            "private evidence reference recorded",
            "qualified-review need assessed",
        ],
        "escalation_triggers": [
            "active compromise continues",
            "ransomware spreads",
            "admin account suspected",
            "backup system affected",
            "vendor support path uncertain",
        ],
    },
    "triage": {
        "owner_lane": "MSP/technical owner",
        "source_alignment": [
            "NIST CSF 2.0 Detect and Respond: analyze, prioritize, and manage the incident",
            "NIST SP 800-61 Rev. 3: many internal and external roles may participate in response",
            "HICP Technical Volume 1: small organizations often need MSP/vendor help for IT and security tasks",
        ],
        "plain_english_goal": "Separate confirmed facts from open questions so the practice does not overreact, underreact, or lose the trail.",
        "owner_prompt": "What do we know, what is still unknown, and who owns the next fact-finding step?",
        "staff_script": "Share only the affected workflow category and when it started. Route technical details to the MSP and private evidence store.",
        "do_now": [
            "Record scope as confirmed, suspected, unknown, or not affected for each critical system category.",
            "Capture the vendor or MSP ticket reference.",
            "Assign one owner to decide whether to move into containment, continuity, or qualified review.",
            "List missing facts as questions instead of filling gaps with assumptions.",
        ],
        "ask_msp_or_vendor": [
            "Which evidence sources have been checked: admin audit logs, sign-in logs, endpoint alerts, vendor status, or EHR support?",
            "Are there signs of spread, privilege misuse, data access, or patient-care disruption?",
            "What is the next safest technical step and what evidence should be preserved first?",
        ],
        "allowed_inputs": [
            "scope category",
            "affected service category",
            "vendor status reference",
            "ticket reference",
            "owner decision reference",
        ],
        "blocked_inputs": [
            "raw logs",
            "patient examples",
            "credentials",
            "private portal links",
        ],
        "evidence_required": [
            "scope review reference",
            "affected system or vendor category",
            "status owner",
        ],
        "completion_criteria": [
            "scope category recorded",
            "owner assigned",
            "next technical action identified",
            "private evidence reference recorded",
        ],
        "escalation_triggers": [
            "scope cannot be determined",
            "vendor cannot confirm status",
            "critical system unavailable",
            "possible unauthorized access",
        ],
    },
    "evidence": {
        "owner_lane": "Owner/MSP",
        "source_alignment": [
            "HIPAA Security Rule 45 CFR 164.308(a)(6): document incidents and outcomes",
            "CISA playbook pattern: preserve logs, images, and evidence according to applicable procedures",
            "NIST CSF 2.0 Identify Improvement: use lessons and evidence to improve response practices",
        ],
        "plain_english_goal": "Make evidence findable and reviewable without putting raw logs, screenshots, patient details, or secrets into the public packet.",
        "owner_prompt": "Which private evidence references prove the timeline, and who controls access to them?",
        "staff_script": "Do not paste screenshots, patient messages, contracts, log lines, URLs, or passwords here. Use a reference ID and tell the owner where the private evidence is stored.",
        "do_now": [
            "Create or confirm one private evidence index entry per artifact category.",
            "Record owner, date observed, source system category, and retention location reference.",
            "Check that raw evidence is not copied into public artifacts.",
            "List which reviewer needs the evidence: MSP, insurer, counsel, compliance, vendor, or incident responder.",
        ],
        "ask_msp_or_vendor": [
            "Which logs or admin exports are time-sensitive and may rotate soon?",
            "Who can preserve evidence without modifying the affected system?",
            "What reference can the practice cite without exposing the artifact itself?",
        ],
        "allowed_inputs": [
            "private evidence reference ID",
            "owner",
            "date observed",
            "artifact category",
            "storage location reference",
        ],
        "blocked_inputs": [
            "raw logs",
            "screenshots with patient or account details",
            "full contracts",
            "patient messages",
            "credentials",
        ],
        "evidence_required": [
            "private evidence index entry",
            "owner",
            "date observed",
            "artifact category",
        ],
        "completion_criteria": [
            "private evidence references listed",
            "no raw evidence copied into packet",
            "owners assigned",
            "reviewer questions listed",
        ],
        "escalation_triggers": [
            "evidence may be overwritten",
            "forensics or insurer involvement likely",
            "staff unsure what to preserve",
            "vendor notice references missing",
        ],
    },
    "qualified": {
        "owner_lane": "Qualified reviewer",
        "source_alignment": [
            "HIPAA Security Rule: respond, mitigate where practicable, and document outcomes",
            "NIST SP 800-61 Rev. 3: legal, privacy, technology, leadership, and third parties may all have response roles",
            "HHS Security Rule summary: safeguards are scalable and should fit size, capabilities, cost, and risk",
        ],
        "plain_english_goal": "Park legal, regulatory, insurance, contract, and formal reporting questions for qualified reviewers while the practice keeps the fact packet clean.",
        "owner_prompt": "Which decisions are outside the practice owner's lane, and what facts must be handed to the reviewer?",
        "staff_script": "Do not tell patients, vendors, or public channels anything beyond an owner-approved operational update. Route formal notice questions to the assigned reviewer.",
        "do_now": [
            "Name the reviewer lane: counsel, compliance, insurer, incident responder, vendor, or regulator support.",
            "List decision questions without answering them inside the kit.",
            "Prepare private evidence references and the sanitized timeline.",
            "Record who is allowed to communicate externally and what boundary they must follow.",
        ],
        "ask_msp_or_vendor": [
            "Which facts are confirmed versus suspected?",
            "Which private evidence references support system access, availability, containment, and recovery?",
            "What vendor, contract, or insurance notice terms may affect the review path?",
        ],
        "allowed_inputs": [
            "decision category",
            "reviewer role",
            "private evidence reference",
            "contract or insurance question category",
            "status",
        ],
        "blocked_inputs": [
            "legal conclusions",
            "reportability conclusions",
            "patient details",
            "raw incident evidence",
        ],
        "evidence_required": [
            "qualified-review queue reference",
            "decision category",
            "reviewer owner",
            "private evidence reference list",
        ],
        "completion_criteria": [
            "qualified reviewer identified",
            "parked decisions listed",
            "private evidence references ready",
            "owner communication boundary confirmed",
        ],
        "escalation_triggers": [
            "possible reportability question",
            "insurance notice question",
            "contract notice question",
            "vendor or regulator communication needed",
        ],
    },
    "after": {
        "owner_lane": "Practice owner/MSP",
        "source_alignment": [
            "NIST CSF 2.0 Identify Improvement: feed lessons into future governance, protection, detection, response, and recovery",
            "NIST CSF 2.0 Recover: complete documentation and confirm return to normal operations based on criteria",
            "HICP Technical Volume 1: practical, low-cost cyber hygiene and MSP-supported improvements matter for small practices",
        ],
        "plain_english_goal": "Convert the incident or tabletop into closed owners, due dates, and evidence refreshes instead of vague lessons.",
        "owner_prompt": "What has to change before we can say this practice is safer than before the scenario?",
        "staff_script": "The goal is to fix workflows, training, vendor terms, and evidence gaps. Do not blame individuals in the packet.",
        "do_now": [
            "Assign no more than five high-value improvements with owners and dates.",
            "Tie each improvement to an evidence reference needed for closeout.",
            "Schedule a follow-up review and tabletop refresh.",
            "Update staff guidance, vendor questions, access review, backup proof, or downtime workflow as needed.",
        ],
        "ask_msp_or_vendor": [
            "Which control would have reduced the incident fastest: MFA, access review, backup test, log alert, endpoint control, vendor terms, or downtime process?",
            "Which evidence can be refreshed in the next 30 days?",
            "Which issue needs budget, vendor change, or owner approval?",
        ],
        "allowed_inputs": [
            "remediation action",
            "owner",
            "due date",
            "evidence needed",
            "closure status",
        ],
        "blocked_inputs": [
            "patient examples",
            "raw logs",
            "credential details",
            "legal conclusions",
        ],
        "evidence_required": [
            "after-action owner",
            "priority",
            "due date",
            "closure evidence reference",
        ],
        "completion_criteria": [
            "top fixes assigned",
            "evidence needed for closure listed",
            "owner review scheduled",
            "next tabletop improvement identified",
        ],
        "escalation_triggers": [
            "high-priority fix has no owner",
            "restore evidence missing",
            "access review missing",
            "vendor terms unresolved",
        ],
    },
}


def scenario_options() -> list[dict[str, Any]]:
    return [
        {
            "key": key,
            "label": scenario["label"],
            "summary": scenario["summary"],
            "phase_count": len(scenario["phases"]),
            "systems": list(scenario["systems"]),
        }
        for key, scenario in SCENARIOS.items()
    ]


def _owner_for_phase(profile: dict[str, Any], phase: str) -> str:
    lowered = phase.lower()
    if "containment" in lowered or "triage" in lowered or "vendor/msp" in lowered:
        return str(profile.get("practice", {}).get("technical_owner") or "MSP Lead")
    if "qualified" in lowered:
        return "Qualified reviewer"
    if "after-action" in lowered:
        return str(profile.get("practice", {}).get("security_owner") or "Practice owner")
    return str(profile.get("practice", {}).get("security_owner") or "Practice owner")


def _phase_guidance(phase: str) -> dict[str, Any]:
    lowered = phase.lower()
    if "qualified" in lowered:
        key = "qualified"
    elif "after" in lowered:
        key = "after"
    elif "evidence" in lowered or "preservation" in lowered:
        key = "evidence"
    elif "containment" in lowered:
        key = "containment"
    elif "triage" in lowered or "scope" in lowered or "vendor/msp" in lowered:
        key = "triage"
    elif "continuity" in lowered:
        key = "continuity"
    else:
        key = "detection"
    return PHASE_GUIDANCE[key]


def phase_guidance_for(phase: str) -> dict[str, Any]:
    return dict(_phase_guidance(phase))


def enrich_incident_timeline(profile: dict[str, Any], incident_timeline: dict[str, Any]) -> dict[str, Any]:
    incident = dict(incident_timeline)
    incident.setdefault("scenario_type", "tabletop")
    incident.setdefault("scenario_name", "Incident tabletop")
    incident.setdefault("summary", "Sanitized incident timeline for owner, MSP, and qualified-review handoff.")
    incident.setdefault("sensitive_data_boundary", INCIDENT_BOUNDARY)
    enriched_timeline = []
    for entry in incident.get("timeline", []):
        if not isinstance(entry, dict):
            continue
        enriched = dict(entry)
        guidance = _phase_guidance(str(enriched.get("phase") or "Detection"))
        enriched.setdefault("owner", _owner_for_phase(profile, str(enriched.get("phase") or "Detection")))
        enriched.setdefault("owner_lane", guidance["owner_lane"])
        enriched.setdefault("source_alignment", list(guidance["source_alignment"]))
        enriched.setdefault("plain_english_goal", guidance["plain_english_goal"])
        enriched.setdefault("owner_prompt", guidance["owner_prompt"])
        enriched.setdefault("staff_script", guidance["staff_script"])
        enriched.setdefault("do_now", list(guidance["do_now"]))
        enriched.setdefault("ask_msp_or_vendor", list(guidance["ask_msp_or_vendor"]))
        enriched.setdefault("allowed_inputs", list(guidance["allowed_inputs"]))
        enriched.setdefault("blocked_inputs", list(guidance["blocked_inputs"]))
        enriched.setdefault("evidence_required", list(guidance["evidence_required"]))
        enriched.setdefault("completion_criteria", list(guidance["completion_criteria"]))
        enriched.setdefault("escalation_triggers", list(guidance["escalation_triggers"]))
        enriched.setdefault("primary_question", enriched.get("decision_gate") or guidance["owner_prompt"])
        enriched.setdefault("complete", False)
        enriched_timeline.append(enriched)
    incident["timeline"] = enriched_timeline
    incident.setdefault("after_actions", [])
    incident.setdefault("decision_gates", [])
    return incident


def scenario_template(profile: dict[str, Any], scenario_key: str) -> dict[str, Any]:
    scenario = SCENARIOS.get(scenario_key) or SCENARIOS["suspicious_login"]
    timeline = []
    for time, phase, event, decision_gate in scenario["phases"]:
        guidance = _phase_guidance(phase)
        timeline.append(
            {
                "time": time,
                "phase": phase,
                "event": event,
                "systems": list(scenario["systems"]),
                "owner": _owner_for_phase(profile, phase),
                "owner_lane": guidance["owner_lane"],
                "source_alignment": list(guidance["source_alignment"]),
                "plain_english_goal": guidance["plain_english_goal"],
                "owner_prompt": guidance["owner_prompt"],
                "staff_script": guidance["staff_script"],
                "do_now": list(guidance["do_now"]),
                "ask_msp_or_vendor": list(guidance["ask_msp_or_vendor"]),
                "evidence_ref": f"restricted-evidence/incidents/{scenario_key}-{phase.lower().replace(' ', '-').replace('/', '-')}",
                "status": "requested",
                "complete": False,
                "primary_question": decision_gate,
                "decision_gate": decision_gate,
                "allowed_inputs": list(guidance["allowed_inputs"]),
                "blocked_inputs": list(guidance["blocked_inputs"]),
                "evidence_required": list(guidance["evidence_required"]),
                "completion_criteria": list(guidance["completion_criteria"]),
                "escalation_triggers": list(guidance["escalation_triggers"]),
            }
        )
    practice = profile.get("practice", {})
    return {
        "scenario_name": scenario["label"],
        "scenario_key": scenario_key,
        "scenario_type": "tabletop",
        "summary": scenario["summary"],
        "sensitive_data_boundary": INCIDENT_BOUNDARY,
        "timeline": timeline,
        "decision_gates": [
            {
                "gate": "Active compromise or patient-care disruption",
                "owner": str(practice.get("technical_owner") or "MSP Lead"),
                "trigger": "Active unauthorized access, ransomware concern, lost device, vendor notice, or patient-care disruption.",
                "action": "Escalate to qualified incident response and preserve private evidence references.",
            },
            {
                "gate": "Qualified reportability or notice review",
                "owner": "Qualified reviewer",
                "trigger": "Possible insurance, contract, regulatory, legal/compliance, or reportability question.",
                "action": "Park the decision for counsel, compliance, insurer, vendor, or qualified security reviewer.",
            },
        ],
        "after_actions": [
            {
                "id": "INC-AA-001",
                "priority": "high",
                "owner": str(practice.get("technical_owner") or "MSP Lead"),
                "action": "Confirm access, MFA, logs, backup, and containment evidence for affected systems.",
                "evidence_needed": "Reference-only admin export, access review, log-review note, restore-test note, or ticket reference.",
                "due": "30 days",
            },
            {
                "id": "INC-AA-002",
                "priority": "medium",
                "owner": str(practice.get("security_owner") or "Practice owner"),
                "action": "Update staff workflow, owner communication, and tabletop lesson notes.",
                "evidence_needed": "Owner signoff, staff acknowledgement, tabletop attendance, and lesson-reference ID.",
                "due": "60 days",
            },
        ],
    }


def safety_findings(incident_timeline: dict[str, Any]) -> list[SensitiveFinding]:
    return find_sensitive_data(incident_timeline)
