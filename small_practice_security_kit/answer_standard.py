from __future__ import annotations

from typing import Any


STANDARD_NAME = "Velari Answer Standard"
UNSAFE_INPUTS = (
    "Do not request or paste PHI, credentials, private URLs, raw logs, patient screenshots, "
    "raw contracts, patient examples, claim details, clinical notes, secrets, or incident-sensitive details. "
    "Use reference IDs, dates observed, owner roles, safe summaries, and private/offline evidence locations."
)

ANSWER_STANDARD_FIELDS = [
    "plain_english_summary",
    "why_it_matters",
    "owner_lane",
    "recommended_question",
    "acceptable_evidence",
    "unsafe_inputs",
    "priority",
    "timeframe",
    "reviewer_needed",
    "next_action",
    "owner_view",
    "msp_view",
    "vendor_view",
    "legal_compliance_view",
]

ANSWER_STANDARD_EXTRA_FIELDS = [
    field for field in ANSWER_STANDARD_FIELDS if field not in {"priority", "next_action"}
]


def fields_with_answer_standard(base_fields: list[str]) -> list[str]:
    fields = list(base_fields)
    for field in ANSWER_STANDARD_FIELDS:
        if field not in fields:
            fields.append(field)
    return fields


def timeframe_for_bucket(bucket: str) -> str:
    if bucket == "30_days":
        return "0-30 days"
    if bucket == "60_days":
        return "31-60 days"
    return "61-90 days"


def reviewer_needed(stage_id: str, priority: str, recipient: str) -> str:
    if priority in {"critical", "high"}:
        return "yes"
    if stage_id in {"vendor_baa_review", "ai_phi_review", "evidence_packet_export", "owner_msp_handoff"}:
        return "yes"
    if "legal" in recipient.lower() or "compliance" in recipient.lower():
        return "yes"
    return "no"


def owner_lane(stage_id: str, recipient: str) -> str:
    mapping = {
        "intake": "Practice owner",
        "patient_data_outside_ehr_map": "Shared: practice owner and MSP",
        "ai_phi_review": "Practice owner and qualified reviewer",
        "vendor_baa_review": "Practice owner, vendor, and qualified reviewer",
        "access_offboarding_review": "MSP with practice owner signoff",
        "downtime_ransomware_review": "Shared: practice owner and MSP",
        "findings_risk_register": "Practice owner and MSP",
        "evidence_packet_export": "Practice owner and qualified reviewer",
        "owner_msp_handoff": "Owner/MSP/vendor/reviewer lane",
    }
    return mapping.get(stage_id, recipient or "Practice owner/MSP")


def why_it_matters(title: str, stage_id: str) -> str:
    lowered = title.lower()
    if stage_id == "patient_data_outside_ehr_map":
        return "Patient-data workflow uncertainty should become an owner, MSP, or vendor action tied to safe evidence references."
    if "mfa" in lowered or "account" in lowered or "access" in lowered:
        return "Access uncertainty should become a clear MSP verification task before the practice relies on the control."
    if "backup" in lowered or "restore" in lowered or "downtime" in lowered:
        return "Recovery uncertainty should become a restore-test or downtime-owner action before an outage or ransomware event."
    if "baa" in lowered or "vendor" in lowered:
        return "Vendor uncertainty should become a direct BAA, incident-term, subprocessor, and AI/data-use question."
    if "ai" in lowered or stage_id == "ai_phi_review":
        return "AI uncertainty should become a staff rule, vendor/data-use question, or reviewer handoff before staff use the workflow."
    return "The item needs an owner, evidence reference, and review path before it can support a credible readiness conversation."


def recommended_question(title: str, stage_id: str, recipient: str) -> str:
    lowered = title.lower()
    if stage_id == "patient_data_outside_ehr_map":
        return "Who owns this patient-data flow, what minimum data moves, and what safe evidence shows the access path, vendor role, and control owner?"
    if "mfa" in lowered:
        return "Can the MSP confirm MFA is enforced for the relevant users, admins, remote access paths, and vendor-support accounts?"
    if "access" in lowered or "account" in lowered:
        return "Who reviewed the current users, admin roles, exceptions, and offboarding evidence, and what changed?"
    if "backup" in lowered or "restore" in lowered:
        return "Which systems were restore-tested, when, by whom, and what blockers or exclusions remain?"
    if "baa" in lowered or stage_id == "vendor_baa_review":
        return "Can the vendor or vendor owner confirm BAA status, review date, incident terms, subcontractors, retention/deletion, and AI/customer-data handling?"
    if stage_id == "ai_phi_review":
        return "What data is allowed in this AI workflow, what is prohibited, and what vendor or reviewer evidence is needed before use?"
    if "legal" in recipient.lower() or "compliance" in recipient.lower():
        return "Does this item need qualified legal/compliance review before the owner treats the evidence as adequate?"
    return "Who owns the next action, what safe evidence is acceptable, and when should the owner review the answer?"


def acceptable_evidence(stage_id: str, evidence_refs: str = "") -> str:
    base = {
        "patient_data_outside_ehr_map": "Flow owner signoff, system/vendor role, BAA/status reference when needed, access-path summary, and transmission-control reference.",
        "ai_phi_review": "Staff-facing AI rule, approved/prohibited data examples, owner approval, vendor data-use answer, and reviewer note when restricted.",
        "vendor_baa_review": "BAA status or review-date reference, vendor security contact, incident-term summary, subprocessor answer, retention/deletion terms, and AI/data-use response.",
        "access_offboarding_review": "Dated user/admin role summary, MFA policy status, exception list, removed-account notes, and owner signoff.",
        "downtime_ransomware_review": "Restore-test summary, downtime owner list, manual workaround, tabletop notes, recovery blockers, and date observed.",
        "evidence_packet_export": "Private/offline binder reference IDs, owner roles, dates observed, statuses, and reviewer notes.",
        "owner_msp_handoff": "Owner, MSP, vendor, or reviewer response with evidence reference IDs and no sensitive source data.",
    }.get(stage_id, "Reference-only evidence ID, owner role, date observed, status, artifact reference, and short safe summary.")
    if evidence_refs:
        return f"{base} Existing evidence refs: {evidence_refs}."
    return base


def owner_view(stage_id: str) -> str:
    if stage_id == "vendor_baa_review":
        return "Own the vendor register, mark missing answers, and decide which responses need qualified review."
    if stage_id == "ai_phi_review":
        return "Turn the decision into a staff rule and route restricted/prohibited use for review before use."
    if stage_id == "downtime_ransomware_review":
        return "Assign business owners for manual workflows, communications, and patient-care continuity decisions."
    if stage_id == "access_offboarding_review":
        return "Review the MSP-provided access evidence and sign off on removals, exceptions, and next review date."
    return "Assign the accountable owner, request safe evidence references, and track the next action in the sprint packet."


def msp_view(stage_id: str) -> str:
    if stage_id == "vendor_baa_review":
        return "Identify vendor-managed systems, integrations, support access, logs, and configuration dependencies."
    if stage_id == "ai_phi_review":
        return "Help enforce approved-tool access, data-loss boundaries, and technical guardrails where possible."
    if stage_id == "downtime_ransomware_review":
        return "Verify recovery sequence, backups, restore testing, escalation routes, and technical recovery blockers."
    if stage_id == "access_offboarding_review":
        return "Provide metadata-only user/admin/MFA evidence, exception notes, and remediation sequencing."
    return "Provide technical status, safe evidence references, dates observed, and remediation sequence without raw logs or secrets."


def vendor_view(stage_id: str) -> str:
    if stage_id == "vendor_baa_review":
        return "Answer BAA, incident notification, subprocessor, retention/deletion, access, audit-log, export/delete, and AI/customer-data-use questions."
    if stage_id == "ai_phi_review":
        return "Answer retention, training, human-review, subprocessor, and customer-data-use questions before restricted use."
    if stage_id == "patient_data_outside_ehr_map":
        return "Confirm vendor-managed workflow controls, support access, incident contacts, and safe evidence options."
    if stage_id == "downtime_ransomware_review":
        return "Provide outage contacts, recovery responsibility, support escalation, and restore responsibility where vendor-managed."
    return "Vendor follow-up is only applicable if the item depends on a vendor-managed workflow, contract, data-use term, or support path."


def legal_compliance_view(stage_id: str) -> str:
    if stage_id in {"vendor_baa_review", "ai_phi_review", "evidence_packet_export", "owner_msp_handoff"}:
        return "A qualified reviewer can assess contract, AI-use, incident, insurance, or formal risk-assessment implications. This tool does not determine legal compliance or HIPAA status."
    return "A qualified reviewer can decide whether the evidence and workflow language are adequate. This tool does not determine legal compliance or HIPAA status."


def answer_standard_fields(
    *,
    title: str,
    stage_id: str,
    priority: str,
    next_action: str,
    recipient: str,
    roadmap_bucket: str,
    evidence_refs: str = "",
) -> dict[str, str]:
    return {
        "plain_english_summary": title.strip() or "Review item needs an accountable owner and safe evidence reference.",
        "why_it_matters": why_it_matters(title, stage_id),
        "owner_lane": owner_lane(stage_id, recipient),
        "recommended_question": recommended_question(title, stage_id, recipient),
        "acceptable_evidence": acceptable_evidence(stage_id, evidence_refs),
        "unsafe_inputs": UNSAFE_INPUTS,
        "priority": priority,
        "timeframe": timeframe_for_bucket(roadmap_bucket),
        "reviewer_needed": reviewer_needed(stage_id, priority, recipient),
        "next_action": next_action.strip() or "Assign an owner, collect safe evidence, and update the sprint packet.",
        "owner_view": owner_view(stage_id),
        "msp_view": msp_view(stage_id),
        "vendor_view": vendor_view(stage_id),
        "legal_compliance_view": legal_compliance_view(stage_id),
    }


def answer_standard_contract() -> dict[str, Any]:
    return {
        "name": STANDARD_NAME,
        "purpose": "Convert every material uncertainty into a clear owner, MSP, vendor, or qualified-review action.",
        "fields": ANSWER_STANDARD_FIELDS,
        "unsafe_inputs": UNSAFE_INPUTS,
        "claims_boundary": "Readiness, evidence, and workflow support only. No legal compliance or HIPAA certification claim.",
    }
