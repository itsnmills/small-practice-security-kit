from __future__ import annotations

from typing import Any


OWNER_LANES = {
    "owner",
    "office_manager",
    "msp",
    "vendor",
    "legal_compliance",
    "insurer",
    "clinical_lead",
    "velari_reviewer",
    "incident_responder",
}
PRIORITIES = {"critical", "high", "medium", "low"}
TIMEFRAMES = {"this_week", "30_days", "60_days", "90_days", "quarterly_refresh"}
REVIEWER_NEEDED = {
    "owner",
    "office_manager",
    "msp",
    "vendor_owner",
    "legal_or_compliance_reviewer",
    "technical_reviewer",
    "clinical_lead",
    "velari_reviewer",
    "incident_responder",
}

SECTION_STAGE_MAP = {
    "executive_scorecard": "access_offboarding_review",
    "ai_findings": "ai_phi_review",
    "vendor_baa_exposure": "vendor_baa_review",
    "ephi_map_lite": "patient_data_outside_ehr_map",
    "access_mfa_offboarding": "access_offboarding_review",
    "downtime_ransomware": "downtime_ransomware_review",
    "evidence_index": "evidence_packet_export",
    "external_evidence_precheck": "external_evidence_precheck",
    "owner_msp_handoff": "owner_msp_handoff",
    "roadmap_30_60_90": "findings_risk_register",
}

DEFAULT_UNSAFE_INPUTS = [
    "patient names",
    "patient records",
    "credentials",
    "private portal links",
    "raw logs",
    "screenshots with sensitive data",
]


def stage_for_section(section_id: str) -> str:
    return SECTION_STAGE_MAP.get(section_id, "findings_risk_register")


def stage_for_title(title: str, section_id: str = "") -> str:
    lowered = title.lower()
    if (
        "tracker" in lowered
        or "pixel" in lowered
        or "analytics" in lowered
        or "tag manager" in lowered
        or "tls" in lowered
        or "certificate" in lowered
        or "https" in lowered
        or "scheduler" in lowered
        or "intake" in lowered
        or section_id == "external_evidence_precheck"
    ):
        return "external_evidence_precheck"
    if "backup" in lowered or "restore" in lowered or "downtime" in lowered:
        return "downtime_ransomware_review"
    if "baa" in lowered or "vendor" in lowered:
        return "vendor_baa_review"
    if "ai workflow" in lowered or "chatbot" in lowered or "scribe" in lowered or "ai " in lowered:
        return "ai_phi_review"
    if "email" in lowered or "shared drive" in lowered or "shared-drive" in lowered:
        return "patient_data_outside_ehr_map"
    if "mfa" in lowered or "access" in lowered or "account" in lowered or "log review" in lowered:
        return "access_offboarding_review"
    return stage_for_section(section_id)


def stage_for_finding(finding: dict[str, Any]) -> str:
    return stage_for_title(str(finding.get("title", "")), str(finding.get("section_id", "")))


def normalize_priority(value: str) -> str:
    lowered = value.strip().lower()
    return lowered if lowered in PRIORITIES else "medium"


def timeframe_for_priority(priority: str, stage_id: str) -> str:
    if priority == "critical":
        return "this_week"
    if priority == "high":
        return "30_days"
    if priority == "medium":
        return "60_days" if stage_id in {"access_offboarding_review", "vendor_baa_review"} else "90_days"
    return "quarterly_refresh"


def owner_lane_for_stage(stage_id: str, title: str = "") -> str:
    lowered = title.lower()
    if stage_id == "external_evidence_precheck":
        if "tls" in lowered or "certificate" in lowered or "https" in lowered:
            return "msp"
        if "tracker" in lowered or "pixel" in lowered or "analytics" in lowered or "tag manager" in lowered:
            return "office_manager"
        return "office_manager"
    if stage_id == "vendor_baa_review":
        return "vendor"
    if stage_id in {"access_offboarding_review", "downtime_ransomware_review"}:
        return "msp"
    if stage_id == "ai_phi_review":
        return "office_manager"
    if stage_id == "patient_data_outside_ehr_map":
        return "office_manager" if "email" in lowered or "shared" in lowered else "msp"
    if stage_id == "evidence_packet_export":
        return "legal_compliance"
    if stage_id == "owner_msp_handoff":
        return "owner"
    return "owner"


def secondary_owner_lane_for_stage(stage_id: str, owner_lane: str) -> str:
    if stage_id == "external_evidence_precheck":
        return "legal_compliance" if owner_lane != "legal_compliance" else "msp"
    if owner_lane == "msp":
        return "office_manager"
    if owner_lane == "vendor":
        return "office_manager"
    if stage_id == "ai_phi_review":
        return "legal_compliance"
    if stage_id == "patient_data_outside_ehr_map":
        return "msp"
    return "velari_reviewer"


def risk_area_for_stage(stage_id: str, title: str) -> str:
    lowered = title.lower()
    if stage_id == "external_evidence_precheck":
        if "tracker" in lowered or "pixel" in lowered or "analytics" in lowered or "tag manager" in lowered:
            return "Public site tracker / privacy evidence"
        if "tls" in lowered or "certificate" in lowered or "https" in lowered:
            return "Public site TLS / transmission security evidence"
        return "External evidence pre-check"
    if "mfa" in lowered:
        return "Access / MFA"
    if "access review" in lowered or "account" in lowered:
        return "Access review"
    if "backup" in lowered or "restore" in lowered:
        return "Backup / downtime"
    if "baa" in lowered or stage_id == "vendor_baa_review":
        return "Vendor / BAA"
    if "ai" in lowered or stage_id == "ai_phi_review":
        return "AI workflow review"
    if "email" in lowered or "shared" in lowered or stage_id == "patient_data_outside_ehr_map":
        return "Patient data outside the EHR"
    if "log" in lowered:
        return "Monitoring"
    return "Readiness / evidence support"


def affected_workflows_for_stage(stage_id: str, title: str) -> list[str]:
    lowered = title.lower()
    if stage_id == "external_evidence_precheck":
        if "tracker" in lowered or "pixel" in lowered or "analytics" in lowered or "tag manager" in lowered:
            return ["appointment scheduler", "patient intake", "portal registration", "public contact workflow"]
        if "tls" in lowered or "certificate" in lowered or "https" in lowered:
            return ["public website", "patient portal", "online scheduler", "payment or intake workflow"]
        return ["public website", "patient-facing workflow", "vendor handoff"]
    if "mfa" in lowered or "access" in lowered or "account" in lowered:
        return ["EHR access", "billing access", "email access", "remote access"]
    if "backup" in lowered or "restore" in lowered or "downtime" in lowered:
        return ["EHR outage", "billing downtime", "shared drive recovery", "patient-care continuity"]
    if "baa" in lowered or stage_id == "vendor_baa_review":
        return ["vendor services", "patient messaging", "billing", "AI documentation"]
    if "ai" in lowered or stage_id == "ai_phi_review":
        return ["AI drafting", "billing appeal drafting", "AI documentation", "staff guidance"]
    if "email" in lowered or "shared" in lowered or stage_id == "patient_data_outside_ehr_map":
        return ["patient messaging", "email", "shared drives", "portal exports"]
    if "log" in lowered:
        return ["EHR access", "email access", "remote access", "vendor support"]
    return ["owner/MSP handoff", "evidence collection", "workflow review"]


def plain_summary_for_finding(title: str, stage_id: str) -> str:
    lowered = title.lower()
    if stage_id == "external_evidence_precheck":
        if "tracker" in lowered or "pixel" in lowered or "analytics" in lowered or "tag manager" in lowered:
            return "A third-party tracker or analytics tag was observed on a patient-facing workflow and needs vendor/privacy review before the practice relies on it."
        if "tls" in lowered or "certificate" in lowered or "https" in lowered:
            return "A public website or portal encryption signal needs MSP review before the practice relies on the workflow for patient-facing communication."
        return "A public patient-facing workflow produced an external evidence observation that needs owner, MSP, vendor, or qualified-review follow-up."
    if "mfa" in lowered:
        return "MFA evidence for an EHR or remote-access workflow is missing or not recorded."
    if "access review" in lowered or "quarterly access" in lowered:
        return "The practice does not have current evidence that user access was reviewed."
    if "backup" in lowered or "restore" in lowered:
        return "Backup restore evidence is missing or stale for systems needed during patient care."
    if "baa" in lowered or stage_id == "vendor_baa_review":
        return "A vendor appears to support a workflow involving patient data, but BAA status or review evidence is missing."
    if "ai" in lowered or stage_id == "ai_phi_review":
        return "An AI workflow needs clearer data-use, vendor, and human-review boundaries before staff rely on it."
    if "email" in lowered or "shared" in lowered or stage_id == "patient_data_outside_ehr_map":
        return "A patient-data workflow outside the EHR needs an owner, evidence support, and safe handling boundaries."
    if "downtime" in lowered:
        return "Downtime workflow evidence is missing for a system the practice may need during patient care."
    if "log" in lowered:
        return "Log review cadence evidence is missing or not recorded for systems that support patient-data workflows."
    return "This readiness item needs an owner, evidence support, and a next action before closeout."


def why_it_matters_for_finding(title: str, stage_id: str) -> str:
    lowered = title.lower()
    if stage_id == "external_evidence_precheck":
        if "tracker" in lowered or "pixel" in lowered or "analytics" in lowered or "tag manager" in lowered:
            return "Tracking technologies on intake, scheduler, portal, payment, or registration workflows can create privacy, vendor-contract, authorization, and evidence questions that a small practice should not have to decode alone."
        if "tls" in lowered or "certificate" in lowered or "https" in lowered:
            return "Weak or unclear public-site encryption evidence can reduce trust in patient-facing workflows and create transmission-security questions for the MSP to confirm."
        return "External observations give the owner a concrete starting point without requiring access to private systems or patient data."
    if "mfa" in lowered or "account" in lowered or "access" in lowered:
        return "Weak access proof makes it harder to show who can reach systems that support patient care and patient-data workflows."
    if "backup" in lowered or "restore" in lowered or "downtime" in lowered:
        return "Unproven recovery can turn a ransomware or outage event into patient-care disruption and billing downtime."
    if "baa" in lowered or "vendor" in lowered or stage_id == "vendor_baa_review":
        return "Vendor uncertainty leaves the practice without clear privacy, incident notice, retention, deletion, and subcontractor answers."
    if "ai" in lowered or stage_id == "ai_phi_review":
        return "AI workflows need explicit data boundaries so staff do not enter patient, billing, clinical, credential, or raw evidence details into the wrong tool."
    if "email" in lowered or "shared" in lowered or stage_id == "patient_data_outside_ehr_map":
        return "Patient-data workflows outside the EHR are where evidence, owner, retention, and vendor assumptions most often get lost."
    if "log" in lowered:
        return "Missing log review evidence reduces risk visibility when suspicious access, vendor support, or account misuse questions arise."
    return "The gap needs an owner, evidence reference, and review path before it can support a credible readiness conversation."


def recommended_question_for_finding(title: str, stage_id: str, recipient: str = "") -> str:
    lowered = title.lower()
    if stage_id == "external_evidence_precheck":
        if "tracker" in lowered or "pixel" in lowered or "analytics" in lowered or "tag manager" in lowered:
            return "Can the website/vendor confirm which trackers fire on patient-facing scheduler, intake, portal, payment, or registration workflows, what data is sent, and whether BAA, authorization, or qualified privacy review is needed?"
        if "tls" in lowered or "certificate" in lowered or "https" in lowered:
            return "Can the MSP confirm certificate validity, HTTPS redirect behavior, TLS posture, HSTS status, and ownership for the public patient-facing workflow?"
        return "Who owns this public-site observation, what evidence confirms the current state, and which vendor/MSP/reviewer should answer next?"
    if "mfa" in lowered:
        return "Can you provide an MFA enforcement export or screenshot for EHR, billing, email, remote access, admin, and vendor-support accounts?"
    if "access review" in lowered or "account" in lowered:
        return "Can you provide user list exports, admin role lists, shared-account exceptions, and owner signoff for access review?"
    if "backup" in lowered or "restore" in lowered:
        return "Can you provide backup scope, last restore-test date, recovery owner, and a private binder reference ID?"
    if "baa" in lowered or stage_id == "vendor_baa_review" or recipient == "Vendor":
        return "Can you confirm whether this vendor stores, processes, transmits, or accesses PHI, whether a BAA is in place, and when it was last reviewed?"
    if "ai" in lowered or stage_id == "ai_phi_review":
        return "Should this workflow remain no-PHI, restricted, or paused until vendor terms, retention, model-training use, and human-review controls are reviewed?"
    if "email" in lowered or "shared" in lowered or stage_id == "patient_data_outside_ehr_map":
        return "Which email, shared-drive, portal, or export workflows handle patient data, who owns them, and what evidence shows access, retention, and secure sharing controls?"
    if "log" in lowered:
        return "Can you provide the log sources, review cadence, alert owner, escalation path, and date last reviewed?"
    if stage_id == "evidence_packet_export":
        return "Which evidence references are enough for planning, and which require private professional review before the owner acts?"
    return "Does this item require owner signoff, MSP evidence, vendor clarification, or professional review before action?"


def acceptable_evidence_for_finding(title: str, stage_id: str) -> list[str]:
    lowered = title.lower()
    if stage_id == "external_evidence_precheck":
        if "tracker" in lowered or "pixel" in lowered or "analytics" in lowered or "tag manager" in lowered:
            return ["tracker inventory", "tag manager export", "sanitized network request summary", "page/workflow label", "vendor BAA or authorization review note", "privacy reviewer disposition"]
        if "tls" in lowered or "certificate" in lowered or "https" in lowered:
            return ["TLS scan summary", "certificate expiry and issuer", "HTTPS redirect evidence", "HSTS status", "covered host list", "MSP attestation"]
        return ["public observation summary", "page/workflow label", "date observed", "owner", "vendor/MSP/reviewer note"]
    if "mfa" in lowered:
        return ["MFA policy export", "admin screenshot with date observed", "covered groups", "exception list", "MSP attestation"]
    if "access review" in lowered or "account" in lowered:
        return ["user list export", "admin role list", "owner access-review signoff", "removed-account notes", "exception sunset dates"]
    if "backup" in lowered or "restore" in lowered:
        return ["backup scope summary", "restore-test note", "date observed", "recovery owner", "systems excluded from backup"]
    if "baa" in lowered or stage_id == "vendor_baa_review":
        return ["BAA status", "BAA review date", "vendor security page", "SOC 2 or HITRUST status", "incident notification terms", "retention/deletion terms"]
    if "ai" in lowered or stage_id == "ai_phi_review":
        return ["AI acceptable-use guidance", "vendor terms summary", "model-training setting", "retention/deletion terms", "staff acknowledgement"]
    if "email" in lowered or "shared" in lowered or stage_id == "patient_data_outside_ehr_map":
        return ["workflow map", "secure email policy", "shared-drive access review", "retention summary", "staff guidance"]
    if "log" in lowered:
        return ["log source list", "review cadence record", "alert owner", "escalation path", "date observed"]
    return ["owner signoff", "evidence reference ID", "date observed", "workflow owner", "review note"]


def unsafe_inputs_for_finding(title: str, stage_id: str) -> list[str]:
    lowered = title.lower()
    unsafe = list(DEFAULT_UNSAFE_INPUTS)
    if stage_id == "external_evidence_precheck":
        unsafe.extend(["real form submissions", "patient-entered details", "full intercepted payloads with sensitive data", "session cookies", "private admin links"])
    if "baa" in lowered or stage_id == "vendor_baa_review":
        unsafe.append("raw contracts with sensitive details")
    if "ai" in lowered or stage_id == "ai_phi_review":
        unsafe.extend(["patient notes", "claim narratives", "raw contracts"])
    if "backup" in lowered or "restore" in lowered:
        unsafe.extend(["raw backup data", "private console links"])
    if "email" in lowered or "shared" in lowered or stage_id == "patient_data_outside_ehr_map":
        unsafe.extend(["clinical notes", "claim narratives", "shared-drive private URLs"])
    return list(dict.fromkeys(unsafe))


def next_action_for_finding(title: str, stage_id: str) -> str:
    lowered = title.lower()
    if stage_id == "external_evidence_precheck":
        if "tracker" in lowered or "pixel" in lowered or "analytics" in lowered or "tag manager" in lowered:
            return "Send the observation to the website vendor and qualified privacy reviewer, confirm tracker purpose and data flow, and decide whether the tag should be removed or restricted on patient-facing workflows."
        if "tls" in lowered or "certificate" in lowered or "https" in lowered:
            return "Ask the MSP or website vendor to confirm TLS/certificate posture and record a reference-only remediation or acceptance note."
        return "Assign the observation to the right owner and collect reference-only evidence before relying on the public workflow."
    if "mfa" in lowered:
        return "Request MFA proof, document exceptions, and assign an owner for any missing enforcement."
    if "access review" in lowered or "account" in lowered:
        return "Run the access review, remove or document exceptions, and store evidence references."
    if "backup" in lowered or "restore" in lowered:
        return "Run or schedule a restore test and record reference-only evidence."
    if "baa" in lowered or stage_id == "vendor_baa_review":
        return "Add the vendor to the register, confirm PHI access level, and request BAA/evidence status."
    if "ai" in lowered or stage_id == "ai_phi_review":
        return "Keep the workflow no-PHI or restricted, collect gated proof, and route terms to professional review if needed."
    if "email" in lowered or "shared" in lowered or stage_id == "patient_data_outside_ehr_map":
        return "Map the workflow, confirm the owner/MSP handoff, and collect reference-only evidence."
    if "log" in lowered:
        return "Assign a log review owner, record cadence evidence, and define escalation for suspicious access."
    if stage_id == "evidence_packet_export":
        return "Separate public evidence references from gated proof and route private items to professional review."
    return "Assign an owner, collect reference-only evidence, and update the action packet."


def reviewers_for_stage(stage_id: str, title: str) -> list[str]:
    lowered = title.lower()
    if stage_id == "external_evidence_precheck":
        if "tracker" in lowered or "pixel" in lowered or "analytics" in lowered or "tag manager" in lowered:
            return ["office_manager", "vendor_owner", "legal_or_compliance_reviewer", "technical_reviewer"]
        return ["msp", "office_manager", "technical_reviewer"]
    if "baa" in lowered or stage_id == "vendor_baa_review":
        return ["vendor_owner", "legal_or_compliance_reviewer"]
    if "ai" in lowered or stage_id == "ai_phi_review":
        return ["office_manager", "legal_or_compliance_reviewer", "technical_reviewer"]
    if "backup" in lowered or "restore" in lowered or "downtime" in lowered:
        return ["msp", "office_manager"]
    if "mfa" in lowered or "access" in lowered or "account" in lowered or "log" in lowered:
        return ["msp", "office_manager"]
    if stage_id == "patient_data_outside_ehr_map":
        return ["office_manager", "msp", "legal_or_compliance_reviewer"]
    if stage_id == "evidence_packet_export":
        return ["legal_or_compliance_reviewer", "velari_reviewer"]
    return ["owner", "velari_reviewer"]


def output_views_for_packet(
    *,
    plain_english_summary: str,
    why_it_matters: str,
    recommended_question: str,
    next_action: str,
    owner_lane: str,
    risk_area: str,
) -> dict[str, str]:
    return {
        "owner_summary": f"{plain_english_summary} Next action: {next_action}",
        "msp_task": (
            f"Support the {risk_area} workflow review with reference-only evidence, dates observed, owners, "
            "and any missing or stale evidence."
        ),
        "vendor_question": recommended_question if owner_lane == "vendor" else "No direct vendor ask unless this workflow depends on a vendor answer.",
        "legal_compliance_note": (
            f"Professional review recommended for contract, formal risk assessment, incident, insurance, or regulatory questions. {why_it_matters}"
        ),
        "technical_reviewer_note": (
            f"Review the control evidence, unsafe inputs, and owner/MSP handoff before relying on this action packet."
        ),
    }


def build_action_packet(
    *,
    finding_id: str,
    title: str,
    section_id: str = "",
    stage_id: str | None = None,
    severity: str = "medium",
    owner: str = "",
    evidence_refs: list[str] | None = None,
    service_context: str = "",
    recipient: str = "",
    next_action_override: str = "",
) -> dict[str, Any]:
    resolved_stage = stage_id or stage_for_title(title, section_id)
    priority = normalize_priority(severity)
    owner_lane = owner_lane_for_stage(resolved_stage, title)
    secondary_owner_lane = secondary_owner_lane_for_stage(resolved_stage, owner_lane)
    plain_summary = plain_summary_for_finding(title, resolved_stage)
    why_it_matters = why_it_matters_for_finding(title, resolved_stage)
    risk_area = risk_area_for_stage(resolved_stage, title)
    recommended_question = recommended_question_for_finding(title, resolved_stage, recipient)
    next_action = next_action_override or next_action_for_finding(title, resolved_stage)
    packet = {
        "finding_id": finding_id,
        "title": title,
        "plain_english_summary": plain_summary,
        "why_it_matters": why_it_matters,
        "risk_area": risk_area,
        "affected_workflows": affected_workflows_for_stage(resolved_stage, title),
        "owner_lane": owner_lane,
        "secondary_owner_lane": secondary_owner_lane,
        "priority": priority,
        "timeframe": timeframe_for_priority(priority, resolved_stage),
        "recommended_question": recommended_question,
        "acceptable_evidence": acceptable_evidence_for_finding(title, resolved_stage),
        "unsafe_inputs": unsafe_inputs_for_finding(title, resolved_stage),
        "next_action": next_action,
        "reviewer_needed": reviewers_for_stage(resolved_stage, title),
        "service_context": service_context or resolved_stage.replace("_", " ").title(),
        "output_views": output_views_for_packet(
            plain_english_summary=plain_summary,
            why_it_matters=why_it_matters,
            recommended_question=recommended_question,
            next_action=next_action,
            owner_lane=owner_lane,
            risk_area=risk_area,
        ),
    }
    if owner:
        packet["owner"] = owner
    if evidence_refs is not None:
        packet["evidence_refs"] = evidence_refs
    return packet


def flattened_output_views(packet: dict[str, Any]) -> dict[str, str]:
    views = packet.get("output_views", {})
    return {
        "owner_view": str(views.get("owner_summary", "")),
        "msp_view": str(views.get("msp_task", "")),
        "vendor_view": str(views.get("vendor_question", "")),
        "legal_compliance_view": str(views.get("legal_compliance_note", "")),
        "technical_reviewer_view": str(views.get("technical_reviewer_note", "")),
    }
