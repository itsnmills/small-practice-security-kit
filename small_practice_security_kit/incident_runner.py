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


def scenario_options() -> list[dict[str, Any]]:
    return [
        {
            "key": key,
            "label": scenario["label"],
            "summary": scenario["summary"],
            "phase_count": len(scenario["phases"]),
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


def scenario_template(profile: dict[str, Any], scenario_key: str) -> dict[str, Any]:
    scenario = SCENARIOS.get(scenario_key) or SCENARIOS["suspicious_login"]
    timeline = []
    for time, phase, event, decision_gate in scenario["phases"]:
        timeline.append(
            {
                "time": time,
                "phase": phase,
                "event": event,
                "systems": list(scenario["systems"]),
                "owner": _owner_for_phase(profile, phase),
                "evidence_ref": f"restricted-evidence/incidents/{scenario_key}-{phase.lower().replace(' ', '-').replace('/', '-')}",
                "status": "requested",
                "decision_gate": decision_gate,
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
