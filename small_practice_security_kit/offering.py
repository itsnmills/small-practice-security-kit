from __future__ import annotations

import html
from typing import Any

from .vendor_evidence import vendor_hitrust_status, vendor_soc2_status


OFFERING_NAME = "Velari Practice Assurance Packet for Small Dental Practices"
OFFERING_TAGLINE = "A plain-English security and vendor evidence report for small dental practices."

SOURCE_ANCHORS: list[dict[str, Any]] = [
    {
        "id": "hhs_cyber_gateway",
        "title": "HHS Cyber Gateway",
        "urls": ["https://hhscyber.hhs.gov/"],
        "why_it_matters": "Frames healthcare cybersecurity as patient-safety work, not only IT hygiene.",
        "how_this_changes_the_sprint": "Every finding is translated into patient-care continuity, trust, and owner/MSP action language.",
    },
    {
        "id": "hhs_405d_hicp",
        "title": "HHS 405(d) HICP",
        "urls": ["https://405d.hhs.gov/cornerstone/hicp"],
        "why_it_matters": "Prioritizes common healthcare threats and the mitigating practices small organizations can discuss with IT partners.",
        "how_this_changes_the_sprint": "The packet asks about social engineering, ransomware, lost equipment or data, insider data loss, connected devices, identity, endpoint, data protection, asset, network, vulnerability, response, and governance evidence.",
    },
    {
        "id": "cisa_cpgs",
        "title": "CISA Cybersecurity Performance Goals",
        "urls": [
            "https://www.cisa.gov/cybersecurity-performance-goals-2-0-cpg-2-0",
            "https://www.cisa.gov/cybersecurity-performance-goals-cpgs",
        ],
        "why_it_matters": "Provides voluntary, high-impact baseline practices that help small teams prioritize without pretending the list is comprehensive.",
        "how_this_changes_the_sprint": "The packet turns asset inventory, accountable ownership, third-party notification, known exploited vulnerability handling, backups, MFA, incident response, and secure defaults into concrete evidence requests.",
    },
    {
        "id": "onc_ocr_sra_tool",
        "title": "ONC/OCR Security Risk Assessment Tool",
        "urls": ["https://healthit.gov/privacy-security/security-risk-assessment-tool/"],
        "why_it_matters": "Supports small and medium providers conducting HIPAA Security Rule risk assessments while keeping entries local to the user's computer.",
        "how_this_changes_the_sprint": "The public runner stays local-first and reference-only, and it points practices toward qualified review for formal risk assessment decisions.",
    },
    {
        "id": "hhs_ocr_tracking_tech",
        "title": "HHS/OCR Online Tracking Technologies Guidance",
        "urls": ["https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/hipaa-online-tracking/index.html"],
        "why_it_matters": "Patient-facing websites, portals, schedulers, and apps can create privacy and vendor-review questions when tracking technologies collect or disclose regulated information.",
        "how_this_changes_the_sprint": "The packet treats tracker observations as potential privacy/security evidence questions for website vendors and qualified reviewers, not automatic legal conclusions.",
    },
    {
        "id": "hhs_security_rule",
        "title": "HHS HIPAA Security Rule Summary",
        "urls": ["https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html"],
        "why_it_matters": "The Security Rule is technology-neutral and focuses on reasonable safeguards for electronic protected health information, including technical safeguards and transmission security.",
        "how_this_changes_the_sprint": "The external pre-check turns TLS, certificate, redirect, portal, and public-host observations into MSP evidence questions without claiming a compliance determination.",
    },
    {
        "id": "hhs_security_rule_nprm",
        "title": "HHS HIPAA Security Rule NPRM Fact Sheet",
        "urls": ["https://www.hhs.gov/hipaa/for-professionals/security/hipaa-security-rule-nprm/factsheet/index.html"],
        "why_it_matters": "Flags proposed modernization items while the current Security Rule remains in effect during rulemaking.",
        "how_this_changes_the_sprint": "Modernization items such as asset inventory, network maps, MFA, encryption, vulnerability scanning, segmentation, backups, incident response, and BA verification are tracked as watchlist deltas, not guaranteed current obligations.",
    },
    {
        "id": "fda_medical_device_cybersecurity",
        "title": "FDA Medical Device Cybersecurity Guidance",
        "urls": ["https://www.fda.gov/medical-devices/digital-health-center-excellence/cybersecurity"],
        "why_it_matters": "Connected clinical devices can affect patient safety and need owner, patch, support-access, and safety-notice review.",
        "how_this_changes_the_sprint": "The packet adds a connected-device worksheet for device/vendor ownership, patch evidence, default credential status, downtime fallback, and safety/security notice review.",
    },
]

STAGE_SOURCE_MAP: dict[str, dict[str, Any]] = {
    "intake": {
        "control_theme": "Scope, safety boundary, accountable owner",
        "source_ids": ["hhs_cyber_gateway", "onc_ocr_sra_tool"],
        "how_this_source_changes_what_we_ask": "Confirm the practice owner, technical owner, review period, and no-PHI/no-secret input rule before discussing evidence.",
    },
    "external_evidence_precheck": {
        "control_theme": "Public-site tracker, patient-facing workflow, and transmission evidence",
        "source_ids": ["hhs_ocr_tracking_tech", "hhs_security_rule", "cisa_cpgs"],
        "how_this_source_changes_what_we_ask": "Check public patient-facing workflows for tracker, scheduler, portal, TLS, certificate, redirect, and ownership observations that should be routed to the website vendor, MSP, or qualified reviewer.",
    },
    "patient_data_outside_ehr_map": {
        "control_theme": "ePHI-like workflow visibility, asset inventory, data protection",
        "source_ids": ["hhs_405d_hicp", "cisa_cpgs", "hhs_security_rule_nprm", "fda_medical_device_cybersecurity"],
        "how_this_source_changes_what_we_ask": "Ask where patient data leaves the EHR, which vendor or system handles it, whether a BAA may be needed, what connected devices, portals, apps, or integrations touch the workflow, and what evidence reference proves the control.",
    },
    "ai_phi_review": {
        "control_theme": "AI data-use boundary, data protection, governance",
        "source_ids": ["hhs_405d_hicp", "cisa_cpgs"],
        "how_this_source_changes_what_we_ask": "Separate no-PHI administrative drafting from workflows that need vendor, retention, training-use, and human-review scrutiny.",
    },
    "vendor_baa_review": {
        "control_theme": "Third-party risk, BAA posture, subcontractors, incident notice",
        "source_ids": ["hhs_405d_hicp", "cisa_cpgs"],
        "how_this_source_changes_what_we_ask": "Ask vendors for BAA scope, SOC 2/HITRUST evidence status, security contact, subcontractor posture, incident notification terms, retention/deletion, AI training-use, and export/delete options.",
    },
    "access_offboarding_review": {
        "control_theme": "Identity, access management, MFA, unique accounts",
        "source_ids": ["hhs_405d_hicp", "cisa_cpgs"],
        "how_this_source_changes_what_we_ask": "Ask the MSP for proof of MFA enforcement, user list exports, admin role review, shared-account exceptions, and offboarding cadence.",
    },
    "downtime_ransomware_review": {
        "control_theme": "Ransomware resilience, backups, restore testing, downtime operations",
        "source_ids": ["hhs_cyber_gateway", "hhs_405d_hicp", "cisa_cpgs"],
        "how_this_source_changes_what_we_ask": "Ask for backup scope, restore-test notes, tabletop lessons, critical-system owners, and downtime workflow continuity.",
    },
    "findings_risk_register": {
        "control_theme": "Prioritized readiness gaps and fix sequencing",
        "source_ids": ["hhs_405d_hicp", "cisa_cpgs"],
        "how_this_source_changes_what_we_ask": "Sort gaps by likely patient-safety and operational impact, then assign owners and a 30/60/90 evidence path.",
    },
    "evidence_packet_export": {
        "control_theme": "Reference-only evidence index and reviewer packet",
        "source_ids": ["onc_ocr_sra_tool", "cisa_cpgs"],
        "how_this_source_changes_what_we_ask": "Collect evidence references and review status locally; do not upload raw evidence, PHI, secrets, contracts, logs, or private links to this public repo.",
    },
    "owner_msp_handoff": {
        "control_theme": "Governance, accountable cyber owner, MSP/vendor/legal lanes",
        "source_ids": ["hhs_cyber_gateway", "hhs_405d_hicp", "cisa_cpgs", "onc_ocr_sra_tool"],
        "how_this_source_changes_what_we_ask": "Turn every gap into a lane-specific question so the owner, MSP, vendor, and legal/compliance reviewer each know what to answer next.",
    },
}

BOUNDARY_STATEMENTS = [
    "Use synthetic or client-supplied reference metadata only.",
    "Do not upload, paste, or send PHI, patient identifiers, credentials, secrets, private URLs, presigned links, raw contracts, raw logs, screenshots with sensitive data, or incident-sensitive details to this public tool.",
    "The packet is a readiness and evidence-gap organizer; it does not establish legal, regulatory, cyber-insurance, vendor, or AI production-use acceptance.",
    "Formal Security Risk Analysis, legal/compliance review, incident reporting decisions, and contract interpretation stay with qualified reviewers.",
]

ESCALATION_TRIGGERS = [
    "A vendor touching ePHI cannot produce a BAA status, SOC 2/HITRUST evidence status, security contact, retention/deletion answer, or incident-notification terms.",
    "MFA is not technically enforced for EHR, billing, email, remote access, administrator, or vendor-support accounts.",
    "Backup scope or restore-test evidence is missing for systems needed to continue patient care.",
    "Staff are using AI tools with patient-level, billing, clinical, credential, or raw evidence details before vendor and policy review.",
    "There is a suspected incident, ransomware event, lost device, unauthorized disclosure, or urgent insurance/legal question.",
]


def build_simple_intake_steps(profile: dict[str, Any]) -> list[dict[str, str]]:
    practice = profile["practice"]
    return [
        {
            "id": "practice_scope",
            "label": "Practice and owners",
            "owner": "Practice owner / office manager",
            "question": f"Confirm the practice name, review period, {practice['security_owner']} as security owner, and {practice['technical_owner']} as technical owner.",
            "evidence_format": "Owner names, review period, location count, staff count, and a no-PHI/no-secret signoff note.",
            "unsafe_inputs": "PHI, patient identifiers, credentials, private admin links, raw logs, raw contracts.",
            "artifact_ref": "practice-assurance-packet.html",
            "status": "Ready to ask",
        },
        {
            "id": "vendor_inventory",
            "label": "Key vendors",
            "owner": "Office manager",
            "question": "List the EHR, billing, email, fax, cloud storage, telehealth, backup, imaging, website, scheduler, portal, AI, and MSP vendors.",
            "evidence_format": "Vendor names, owner, workflow touched, BAA status label, security evidence status label, and review date if known.",
            "unsafe_inputs": "Full contracts, patient screenshots, claim details, credentials, private vendor portal links.",
            "artifact_ref": "vendor-baa-ai-questionnaire.md",
            "status": "Ready to ask",
        },
        {
            "id": "patient_facing_urls",
            "label": "Patient-facing URLs",
            "owner": "Website owner / MSP",
            "question": "Identify the public website, scheduler, new patient intake, portal login, payment, registration, and contact workflows to review.",
            "evidence_format": "Public URL labels, page/workflow names, owner, date observed, tracker/tag summary, TLS/certificate summary.",
            "unsafe_inputs": "Real patient form submissions, session cookies, full intercepted payloads, private portal links.",
            "artifact_ref": "external-evidence-precheck.md",
            "status": "Ready to ask",
        },
        {
            "id": "ai_workflows",
            "label": "AI use",
            "owner": "Practice owner / department lead",
            "question": "Name AI tools being used or considered, what staff want to use them for, and whether any workflow could include patient, billing, clinical, credential, or raw evidence details.",
            "evidence_format": "Tool name, proposed use, data category, vendor, decision label, policy or training reference.",
            "unsafe_inputs": "Patient notes, transcripts, images, claims, clinical narratives, credentials, raw evidence, prompts with patient details.",
            "artifact_ref": "ai-workflow-review.md",
            "status": "Ready to ask",
        },
        {
            "id": "msp_evidence",
            "label": "MSP evidence status",
            "owner": "MSP / technical owner",
            "question": "Mark each proof area as have it, need MSP, need vendor, needs reviewer, or unknown.",
            "evidence_format": "MFA status, access review date, backup scope, restore-test date, remote support method, log review cadence, patch/vulnerability process.",
            "unsafe_inputs": "Raw logs, credentials, private URLs, sensitive screenshots, patient data, full network captures.",
            "artifact_ref": "msp-remediation-brief.md",
            "status": "Ready to ask",
        },
    ]


OFFERING_ARTIFACTS: list[dict[str, str]] = [
    {
        "path": "practice-assurance-packet.html",
        "purpose": "Polished buyer-facing report that summarizes the practice, top risks, evidence requests, audience handoffs, and safety boundary.",
        "audience": "practice_owner_msp",
    },
    {
        "path": "practice-assurance-packet.md",
        "purpose": "Plain Markdown copy of the Practice Assurance Packet for quick review or text export.",
        "audience": "practice_owner_msp",
    },
    {
        "path": "external-evidence-precheck.md",
        "purpose": "Reference-only public-site observation report for tracker, scheduler, portal, TLS, certificate, and vendor/MSP/reviewer follow-up questions.",
        "audience": "practice_owner_msp_legal",
    },
    {
        "path": "sprint-offering-readout.md",
        "purpose": "Client-ready plain-English readout of what was reviewed, why it matters, top gaps, next questions, and boundaries.",
        "audience": "owner_msp_legal",
    },
    {
        "path": "owner-action-plan.md",
        "purpose": "First-week office-manager plan with scripts for MSP, vendor, and legal/compliance follow-up.",
        "audience": "practice_owner",
    },
    {
        "path": "msp-remediation-brief.md",
        "purpose": "Technical handoff that converts gaps into checks, expected proof, owners, stages, and source mapping.",
        "audience": "msp",
    },
    {
        "path": "vendor-baa-ai-questionnaire.md",
        "purpose": "BAA, SOC 2/HITRUST evidence status, subcontractor, incident notice, retention/deletion, AI training-use, access, audit-log, and export/delete questions.",
        "audience": "vendor_baa_ai_reviewer",
    },
    {
        "path": "evidence-collection-checklist.md",
        "purpose": "Reference-only list of screenshots, exports, policy pages, and notes to gather in the private/offline evidence binder.",
        "audience": "owner_msp",
    },
    {
        "path": "day-one-workshop-agenda.md",
        "purpose": "Consultative first-session agenda with discovery questions, evidence safety boundaries, lanes, and expected outputs.",
        "audience": "delivery_team",
    },
    {
        "path": "source-map.md",
        "purpose": "Stage-to-source map showing how HHS, HICP, CISA, and ONC/OCR anchors change the packet questions.",
        "audience": "reviewer",
    },
    {
        "path": "connected-device-inventory.md",
        "purpose": "IoMT/medical-device worksheet for vendor, network/access path, PHI handled, patch owner, default credentials, downtime fallback, and safety notice review.",
        "audience": "msp",
    },
    {
        "path": "portal-api-flow-review.md",
        "purpose": "Portal, API, app, and FHIR-style flow worksheet covering patient identity workflow, audit logs, secure messaging, ownership, and export/delete evidence.",
        "audience": "owner_msp_vendor",
    },
    {
        "path": "incident-decision-log.md",
        "purpose": "Decision-log template separating technical containment from qualified legal/compliance breach-notification decisions.",
        "audience": "owner_msp_legal",
    },
]


def _source_title_by_id() -> dict[str, str]:
    return {source["id"]: source["title"] for source in SOURCE_ANCHORS}


def _stage_name_by_id(stages: list[dict[str, Any]]) -> dict[str, str]:
    return {str(stage["id"]): str(stage["name"]) for stage in stages}


def _artifact_for_stage(stage_id: str) -> str:
    mapping = {
        "intake": "sprint-summary.json",
        "external_evidence_precheck": "external-evidence-precheck.md",
        "patient_data_outside_ehr_map": "ephi-flow-map.md",
        "ai_phi_review": "ai-workflow-review.md",
        "vendor_baa_review": "vendor-baa-ai-questionnaire.md",
        "access_offboarding_review": "msp-remediation-brief.md",
        "downtime_ransomware_review": "day-one-workshop-agenda.md",
        "findings_risk_register": "risk-register.csv",
        "evidence_packet_export": "evidence-collection-checklist.md",
        "owner_msp_handoff": "owner-action-plan.md",
    }
    return mapping.get(stage_id, "practice-assurance-packet.html")


def build_audience_lanes(profile: dict[str, Any]) -> list[dict[str, Any]]:
    practice = profile["practice"]
    return [
        {
            "id": "practice_owner",
            "label": "Practice owner / office manager",
            "value": "Plain-English priorities, first-week decisions, and scripts to send to the MSP, vendors, and reviewers.",
            "primary_owner": str(practice["security_owner"]),
            "primary_artifacts": ["practice-assurance-packet.html", "external-evidence-precheck.md", "owner-action-plan.md", "evidence-collection-checklist.md"],
            "first_questions": [
                "What did the external pre-check observe on the public patient-facing website, scheduler, portal, or intake workflow?",
                "Which patient-data workflows create the most urgent evidence gaps?",
                "Which vendor or MSP answers do we need this week?",
                "Which decisions require a qualified legal/compliance reviewer?",
            ],
        },
        {
            "id": "msp",
            "label": "MSP / IT partner",
            "value": "Technical checks, proof requested, owner lane, stage reference, and remediation sequence without needing direct system access in the public runner.",
            "primary_owner": str(practice["technical_owner"]),
            "primary_artifacts": ["msp-remediation-brief.md", "risk-register.csv", "handoff-actions.csv"],
            "first_questions": [
                "Which public hosts, portals, redirects, certificates, and TLS settings need verification?",
                "Which accounts have MFA enforced, and which systems still need review?",
                "Which systems are in backup scope, and when was restore last tested?",
                "Which logs, admin roles, remote support methods, and known-exploited-vulnerability processes can be evidenced?",
            ],
        },
        {
            "id": "vendor_baa_ai_reviewer",
            "label": "Vendor / BAA / AI reviewer",
            "value": "Answerable vendor questions for BAA scope, SOC 2/HITRUST evidence status, subcontractors, incident notice, retention/deletion, AI training-use, access controls, logs, and export/delete capability.",
            "primary_owner": "Vendor owner / practice manager",
            "primary_artifacts": ["vendor-baa-ai-questionnaire.md", "vendor-baa-review.md"],
            "first_questions": [
                "Does the vendor touch ePHI or support a workflow that could later receive ePHI?",
                "What are the BAA, SOC 2/HITRUST evidence status, subcontractor, incident notice, retention, deletion, and AI training-use answers?",
                "Can the practice export or delete its data, and can audit logs be reviewed?",
            ],
        },
        {
            "id": "legal_compliance_reviewer",
            "label": "Legal / compliance reviewer",
            "value": "Bounded review notes, escalation triggers, and clear separation between readiness prompts and professional determinations.",
            "primary_owner": "Qualified reviewer",
            "primary_artifacts": ["practice-assurance-packet.html", "source-map.md", "limitations-appendix.md"],
            "first_questions": [
                "Which tracker, scheduler, portal, or intake observations need privacy/legal/compliance review before the owner acts?",
                "Which questions require contract interpretation or formal risk assessment work?",
                "Which vendor, AI, incident, or insurance answers should be reviewed before the owner acts?",
                "Which evidence references are enough for planning, and which require private review?",
            ],
        },
    ]


def build_first_7_days_actions(profile: dict[str, Any]) -> list[dict[str, str]]:
    practice = profile["practice"]
    critical_systems = ", ".join(profile.get("downtime", {}).get("critical_systems", [])[:4]) or "critical systems"
    ephi_vendors = [vendor["name"] for vendor in profile.get("vendors", []) if vendor.get("touches_ephi")]
    vendor_text = ", ".join(ephi_vendors[:4]) if ephi_vendors else "vendors touching ePHI-like workflows"
    restricted_ai = [
        workflow["name"]
        for workflow in profile.get("ai_workflows", [])
        if str(workflow.get("decision", "")).lower() != "allowed"
    ]
    ai_text = ", ".join(restricted_ai[:3]) if restricted_ai else "any AI workflow that could receive patient, billing, clinical, credential, or raw evidence details"
    return [
        {
            "day": "Day 0-1",
            "lane": "Owner/MSP/vendor reviewer",
            "stage_id": "external_evidence_precheck",
            "action": "Review public-site tracker, scheduler, portal, intake, TLS, and certificate observations before relying on patient-facing workflows.",
            "evidence_request": "Tracker inventory, tag manager export, sanitized network destination summary, TLS scan summary, certificate status, website owner, and qualified-review disposition.",
            "artifact_ref": "external-evidence-precheck.md",
        },
        {
            "day": "Day 1",
            "lane": "Owner",
            "stage_id": "intake",
            "action": f"Confirm {practice['security_owner']} owns the packet, {practice['technical_owner']} owns technical evidence, and all outputs stay reference-only.",
            "evidence_request": "Owner signoff note that the public runner contains no PHI, secrets, private URLs, raw contracts, or raw logs.",
            "artifact_ref": "owner-action-plan.md",
        },
        {
            "day": "Days 1-2",
            "lane": "MSP",
            "stage_id": "access_offboarding_review",
            "action": "Request MFA enforcement status and user-list exports for EHR, billing, imaging, email, remote access, administrator, and vendor-support accounts.",
            "evidence_request": "MFA status screenshot or admin export, user list export, admin role list, shared-account exception list, and owner access-review signoff.",
            "artifact_ref": "msp-remediation-brief.md",
        },
        {
            "day": "Days 2-3",
            "lane": "MSP",
            "stage_id": "downtime_ransomware_review",
            "action": f"Confirm backup scope and last restore-test evidence for {critical_systems}.",
            "evidence_request": "Backup scope summary, restore-test note, recovery owner, date observed, and private binder reference ID.",
            "artifact_ref": "evidence-collection-checklist.md",
        },
        {
            "day": "Days 3-4",
            "lane": "Vendor",
            "stage_id": "vendor_baa_review",
            "action": f"Send BAA, SOC 2/HITRUST evidence status, subcontractor, incident notice, retention/deletion, AI training-use, access control, audit-log, and export/delete questions to {vendor_text}.",
            "evidence_request": "Vendor written answers, BAA status/link label, SOC 2/HITRUST status label, security contact, incident notice terms, and reviewer notes kept outside the public repo.",
            "artifact_ref": "vendor-baa-ai-questionnaire.md",
        },
        {
            "day": "Days 4-5",
            "lane": "Owner",
            "stage_id": "ai_phi_review",
            "action": f"Decide interim AI rules for {ai_text} and issue no-PHI staff guidance before any rollout.",
            "evidence_request": "AI acceptable-use page, staff acknowledgement reference, vendor terms review status, and human-review owner.",
            "artifact_ref": "owner-action-plan.md",
        },
        {
            "day": "Days 5-7",
            "lane": "Owner/MSP",
            "stage_id": "downtime_ransomware_review",
            "action": "Run a 30-minute downtime/ransomware tabletop for an EHR outage during patient care and record lessons learned.",
            "evidence_request": "Tabletop agenda, participant roles, manual workflow decisions, communications owner, and private binder reference ID.",
            "artifact_ref": "day-one-workshop-agenda.md",
        },
        {
            "day": "Day 7",
            "lane": "Legal/compliance reviewer",
            "stage_id": "evidence_packet_export",
            "action": "Escalate BAA, AI, incident, insurance, and formal risk-assessment questions that require qualified review.",
            "evidence_request": "Question list with artifact references only; no PHI, secrets, raw contracts, raw logs, or incident-sensitive details.",
            "artifact_ref": "practice-assurance-packet.html",
        },
    ]


def build_offering_summary(profile: dict[str, Any], stages: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "name": OFFERING_NAME,
        "positioning": f"{OFFERING_TAGLINE} It maps patient-data workflows outside the EHR, evidence gaps, vendor/BAA/AI questions, MSP checks, and first-week owner actions without collecting raw PHI or evidence in the public repo.",
        "audience_lanes": build_audience_lanes(profile),
        "simple_intake_steps": build_simple_intake_steps(profile),
        "source_anchors": SOURCE_ANCHORS,
        "stage_source_map": build_stage_source_map(stages),
        "first_7_days_actions": build_first_7_days_actions(profile),
        "top_value_outcomes": [
            "A plain-English report a practice owner can read without operating another security dashboard.",
            "A public-site External Evidence Pre-Check that turns tracker, scheduler, portal, TLS, and certificate observations into safe owner/MSP/vendor/reviewer questions before internal access is needed.",
            "A map of where patient-data workflows create operational and trust risk outside the EHR.",
            "A first-week action plan the office manager can actually send to the MSP, vendors, and reviewers.",
            "A technical remediation brief that asks for specific proof instead of broad security promises.",
            "A vendor/BAA/AI questionnaire that makes contract, SOC 2/HITRUST evidence status, retention, incident notice, subcontractor, and model-training questions visible.",
            "A reference-only evidence checklist ready for a private/offline binder without moving PHI or raw restricted evidence into this repo.",
            "A source map that shows why each stage exists and which federal healthcare/cross-sector guidance shaped the questions.",
        ],
        "artifact_list": OFFERING_ARTIFACTS,
        "boundary_statements": BOUNDARY_STATEMENTS,
        "escalation_triggers": ESCALATION_TRIGGERS,
        "private_app_import": {
            "contract_key": "offering_summary",
            "import_use": "Seed private Sprint Mode lanes, first-week tasks, source mappings, artifact checklist, and boundary warnings before any reviewed evidence import.",
            "review_before_import": True,
        },
    }


def build_stage_source_map(stages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_titles = _source_title_by_id()
    stage_names = _stage_name_by_id(stages)
    rows = []
    for stage in stages:
        stage_id = str(stage["id"])
        mapping = STAGE_SOURCE_MAP[stage_id]
        source_ids = list(mapping["source_ids"])
        rows.append(
            {
                "stage_id": stage_id,
                "stage_name": stage_names[stage_id],
                "control_theme": str(mapping["control_theme"]),
                "source_ids": source_ids,
                "source_titles": [source_titles[source_id] for source_id in source_ids],
                "how_this_source_changes_what_we_ask": str(mapping["how_this_source_changes_what_we_ask"]),
                "artifact_refs": list(dict.fromkeys([*stage.get("artifact_refs", []), _artifact_for_stage(stage_id)])),
            }
        )
    return rows


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |")
    return "\n".join(lines)


def _source_titles_for_stage(stage_id: str) -> str:
    titles = _source_title_by_id()
    source_ids = STAGE_SOURCE_MAP.get(stage_id, STAGE_SOURCE_MAP["findings_risk_register"])["source_ids"]
    return ", ".join(titles[source_id] for source_id in source_ids)


def _why_finding_matters(title: str, stage_id: str) -> str:
    lowered = title.lower()
    if "mfa" in lowered or "account" in lowered or "access" in lowered:
        return "Weak access proof makes it harder to show who can reach systems that support patient care and ePHI workflows."
    if "backup" in lowered or "restore" in lowered or "downtime" in lowered:
        return "Unproven recovery can turn a ransomware or outage event into care disruption and billing downtime."
    if "baa" in lowered or "vendor" in lowered:
        return "Vendor uncertainty leaves the practice without clear privacy, incident notice, retention, and subcontractor answers."
    if "ai" in lowered or stage_id == "ai_phi_review":
        return "AI workflows need explicit data boundaries so staff do not enter patient, billing, clinical, credential, or raw evidence details into the wrong tool."
    if stage_id == "patient_data_outside_ehr_map":
        return "Patient-data workflows outside the EHR are where evidence, owner, and vendor assumptions most often get lost."
    return "The gap needs an owner, evidence reference, and review path before it can support a credible readiness conversation."


def _question_for_finding(title: str, stage_id: str, recipient: str) -> str:
    lowered = title.lower()
    if recipient == "MSP" or stage_id in {"access_offboarding_review", "downtime_ransomware_review"}:
        if "mfa" in lowered:
            return "Can you provide an MFA enforcement export or screenshot for EHR, billing, email, remote access, admin, and vendor-support accounts?"
        if "backup" in lowered or "restore" in lowered:
            return "Can you provide backup scope, last restore-test date, recovery owner, and a private binder reference ID?"
        return "Can you provide the technical proof, date observed, owner, and remediation sequence for this stage?"
    if recipient == "Vendor" or stage_id == "vendor_baa_review":
        return "Can you answer BAA scope, SOC 2/HITRUST evidence status, subcontractor, incident notice, retention/deletion, AI training-use, access-control, audit-log, and export/delete questions?"
    if stage_id == "ai_phi_review":
        return "Should this workflow remain no-PHI, restricted, or paused until vendor terms and human-review controls are reviewed?"
    return "Does this item require legal/compliance review, owner signoff, or a private evidence review before action?"


def _joined(value: Any) -> str:
    if isinstance(value, list):
        return "; ".join(str(item) for item in value)
    return str(value)


def _html(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _slug_class(value: Any) -> str:
    text = str(value).lower().replace("_", "-").replace(" ", "-")
    return "".join(character for character in text if character.isalnum() or character == "-") or "unknown"


def _artifact_anchor(path: str) -> str:
    escaped = _html(path)
    return f'<a href="{escaped}">{escaped}</a>'


def _top_gap_rows(risk_rows: list[dict[str, Any]]) -> list[list[str]]:
    rows = []
    for risk in risk_rows[:5]:
        stage_id = risk["stage_id"]
        rows.append(
            [
                risk["title"],
                risk["priority"],
                risk.get("plain_english_summary", ""),
                risk.get("why_it_matters") or _why_finding_matters(risk["title"], stage_id),
                risk.get("owner_lane", ""),
                risk.get("recommended_question") or _question_for_finding(risk["title"], stage_id, risk["recipient"]),
                _joined(risk.get("acceptable_evidence", "")),
                _joined(risk.get("unsafe_inputs", "")),
                risk.get("timeframe", ""),
                _joined(risk.get("reviewer_needed", "")),
                risk.get("next_action") or risk["recommended_action"],
            ]
        )
    if not rows:
        rows.append(
            [
                "No generated high-priority finding",
                "low",
                "No major gap was generated.",
                "The practice should still review evidence references and owners before relying on the packet.",
                "owner",
                "Which evidence references should be refreshed first?",
                "evidence reference ID",
                "PHI; credentials; private URLs",
                "quarterly_refresh",
                "owner",
                "Walk through the source map and evidence checklist with the owner and MSP.",
            ]
        )
    return rows


def _questions_by_lane(summary: dict[str, Any]) -> dict[str, list[str]]:
    lanes: dict[str, list[str]] = {}
    for lane in summary["offering_summary"]["audience_lanes"]:
        lanes[str(lane["label"])] = list(lane["first_questions"])
    return lanes


def _looks_generic_evidence(value: Any) -> bool:
    text = _joined(value).lower()
    generic_markers = [
        "owner signoff",
        "evidence reference id",
        "date observed",
        "workflow owner",
        "review note",
    ]
    return sum(1 for marker in generic_markers if marker in text) >= 3


def _frontdoor_evidence_for_item(item: dict[str, Any]) -> str:
    current = _joined(item.get("acceptable_evidence", "")).strip()
    if current and not _looks_generic_evidence(current):
        return current
    risk_like = dict(item)
    risk_like.setdefault("title", item.get("title") or item.get("action") or "")
    risk_like.setdefault("stage_id", item.get("stage_id", "findings_risk_register"))
    return _expected_proof_for_risk(risk_like)


def _simple_intake_rows(summary: dict[str, Any]) -> list[list[str]]:
    rows = []
    for step in summary["offering_summary"].get("simple_intake_steps", []):
        rows.append(
            [
                str(step.get("label", "")),
                str(step.get("owner", "")),
                str(step.get("question", "")),
                str(step.get("evidence_format", "")),
                str(step.get("unsafe_inputs", "")),
                str(step.get("artifact_ref", "")),
            ]
        )
    return rows


def _decision_queue_rows(risk_rows: list[dict[str, Any]]) -> list[list[str]]:
    rows = []
    for risk in risk_rows[:5]:
        rows.append(
            [
                str(risk.get("title", "Evidence question")),
                str(risk.get("recipient", "Owner/MSP")),
                _owner_takeaway_for_risk(risk),
                str(risk.get("recommended_question", "")),
                _frontdoor_evidence_for_item(risk),
                _joined(risk.get("unsafe_inputs", "")),
                str(risk.get("artifact_ref", "practice-assurance-packet.html")),
            ]
        )
    if not rows:
        rows.append(
            [
                "No generated high-priority finding",
                "Owner/MSP",
                "Assign an owner and collect a reference-only evidence note.",
                "Which evidence references should be refreshed first?",
                "Evidence reference ID, owner, date observed, and short status note.",
                "PHI; credentials; private URLs; raw logs; raw contracts.",
                "practice-assurance-packet.html",
            ]
        )
    return rows


def _owner_takeaway_for_risk(risk: dict[str, Any]) -> str:
    title = str(risk.get("title", "")).lower()
    stage_id = str(risk.get("stage_id", ""))
    recipient = str(risk.get("recipient", "")).lower()
    if stage_id == "external_evidence_precheck":
        if "tracker" in title or "pixel" in title or "analytics" in title or "tag manager" in title:
            return "Ask the website vendor and privacy reviewer what data the tracker receives on patient-facing pages."
        if "tls" in title or "certificate" in title or "https" in title:
            return "Ask the MSP or website vendor to confirm TLS, certificate, redirect, and HSTS evidence."
        return "Assign the public-site observation to an owner before relying on the workflow."
    if "mfa" in title:
        return "Ask the MSP for MFA proof and any exception list."
    if "backup" in title or "restore" in title:
        return "Ask the MSP for backup scope and restore-test evidence."
    if "downtime" in title or stage_id == "downtime_ransomware_review":
        return "Assign a downtime owner and record tabletop or manual-workflow evidence."
    if "baa" in title or "vendor" in title or recipient == "vendor" or stage_id == "vendor_baa_review":
        return "Ask the vendor for BAA status, security evidence status, and incident terms."
    if "ai" in title or stage_id == "ai_phi_review":
        return "Keep the workflow no-PHI or restricted until terms and staff guidance are reviewed."
    if "access" in title or "account" in title or stage_id == "access_offboarding_review":
        return "Ask the MSP for user, admin-role, and offboarding evidence."
    return "Assign an owner and collect a reference-only evidence note."


def _ready_to_send_messages(summary: dict[str, Any]) -> list[tuple[str, str]]:
    practice = summary["practice"]
    label = str(practice["label"])
    review_period = str(practice["review_period"])
    return [
        (
            "Email to MSP",
            f"""Subject: Quick evidence request for {label} - Velari packet

Hi [MSP Contact],

We are using a Velari Practice Assurance Packet for our {review_period} review. It highlights a few high-priority items where we need reference-only evidence this week:

- MFA enforcement status and user/admin list exports for EHR, billing, email, remote access, and administrator accounts
- Backup scope and last restore-test evidence for critical practice systems
- Downtime workflow or tabletop notes for systems needed during patient care

Please reply with evidence reference IDs, dates observed, owners, scope covered, and any gaps we need to decide on. Keep raw files, screenshots, logs, private URLs, credentials, and sensitive details in our private binder.

Can you send what you have by [date], or suggest a short call if that is easier?

Thanks,
[Your Name]""",
        ),
        (
            "Email to Vendor",
            f"""Subject: BAA and security evidence request - {label}

Hi [Vendor Contact],

As part of our {review_period} practice security and vendor review, we need to confirm a few reference-only items for [Vendor Name].

Can you please provide:

- Current BAA status and last review date
- SOC 2, HITRUST, or equivalent security evidence status
- Security contact and incident-notification terms
- Retention/deletion terms and subprocessors or subcontractors
- AI data-use or model-training terms, if applicable

We only need status labels, public/gated proof references, or a short written response. Please do not send PHI, credentials, raw contracts, raw logs, patient screenshots, or private admin links in this thread.

Thank you,
[Your Name] / {label}""",
        ),
        (
            "Internal Note to Practice Owner",
            f"""Subject: First actions from the Velari packet

The Velari packet is ready for {label}. The fastest next step is to send the MSP and vendor requests, then track responses by reference ID instead of moving sensitive files around.

This week I recommend we:

- Ask the MSP for MFA, access, backup, restore-test, and downtime evidence
- Ask key vendors for BAA, security evidence status, incident, retention/deletion, and AI data-use answers
- Keep PHI, passwords, raw logs, raw contracts, patient screenshots, and private links out of email and public tools
- Escalate legal/compliance, insurance, incident, or formal risk-assessment questions to the right reviewer

I can send the first requests and collect responses into the evidence tracker.""",
        ),
        (
            "Optional Note to Reviewer",
            f"""Subject: Reference-only packet for qualified review - {label}

Hi [Reviewer],

We have a Velari Practice Assurance Packet for {label}'s {review_period} review. It is a readiness and evidence-handoff packet, not a formal Security Risk Analysis, audit opinion, legal advice, or insurance advice.

Can you review the packet and flag which vendor, AI, incident, insurance, contract, or formal risk-assessment questions need qualified review before the practice relies on them?

We are keeping raw evidence in a private/offline binder and using reference IDs in the packet. Please do not request PHI, credentials, raw logs, raw contracts, private admin links, or incident-sensitive details in public tools.""",
        ),
    ]


def _ready_to_send_messages_markdown(summary: dict[str, Any]) -> str:
    blocks = []
    for title, body in _ready_to_send_messages(summary):
        blocks.append(f"### {title}\n\n```text\n{body}\n```")
    return "\n\n".join(blocks)


def render_sprint_offering_readout(
    summary: dict[str, Any],
    risk_rows: list[dict[str, Any]],
    handoff_rows: list[dict[str, Any]],
) -> str:
    practice = summary["practice"]
    offering = summary["offering_summary"]
    top_gap_table = markdown_table(
        [
            "Finding or gap",
            "Priority",
            "Plain-English summary",
            "Why it matters",
            "Owner lane",
            "Question to ask",
            "Evidence to collect",
            "Unsafe inputs",
            "Timeframe",
            "Reviewer needed",
            "Next action",
        ],
        _top_gap_rows(risk_rows),
    )
    reviewed = [
        f"- {stage['name']}: {', '.join(stage['artifact_refs'])}"
        for stage in summary["stage_statuses"]
    ]
    first_week = [
        f"- **{action['day']} - {action['lane']}**: {action['action']} Evidence to request: {action['evidence_request']} (`{action['artifact_ref']}`)"
        for action in offering["first_7_days_actions"]
    ]
    questions_by_lane = _questions_by_lane(summary)
    question_lines = []
    for lane, questions in questions_by_lane.items():
        question_lines.append(f"### {lane}")
        question_lines.extend(f"- {question}" for question in questions)
    source_lines = [
        f"- {source['title']}: {', '.join(source['urls'])}. {source['how_this_changes_the_sprint']}"
        for source in offering["source_anchors"]
    ]
    handoff_preview = [
        f"- {row['recipient']}: {row['action']} (`{row['artifact_ref']}`)"
        for row in handoff_rows[:6]
    ]
    return f"""# {offering['name']}

Practice: **{practice['label']}**

Review period: **{practice['review_period']}**

Readiness signal: **{summary['readiness_signal']['label']}**

## What We Reviewed

{chr(10).join(reviewed)}

## 10-Minute Intake

Use this as the first call checklist. Unknown is acceptable; unknowns become MSP, vendor, or qualified-review questions.

{markdown_table(['Step', 'Owner', 'Question', 'Evidence format', 'Do not send', 'Artifact'], _simple_intake_rows(summary))}

## What This Means For Patient Safety And Client Trust

HHS Cyber Gateway frames the work plainly: cyber safety is patient safety. For a small practice, that means the sprint focuses on whether patient-data workflows, vendors, access, AI use, and downtime plans are understandable enough for the owner and MSP to act this week. The packet turns guidance from HHS 405(d) HICP, CISA Cybersecurity Performance Goals, and the ONC/OCR SRA Tool into practical questions and evidence requests.

## Top 5 Findings Or Gaps

{top_gap_table}

## First 7 Days

{chr(10).join(first_week)}

## Questions To Send

{chr(10).join(question_lines)}

## Immediate Handoff Preview

{chr(10).join(handoff_preview) if handoff_preview else '- Review `handoff-actions.csv` with the owner and MSP.'}

## Source Anchors

{chr(10).join(source_lines)}

## What This Does Not Prove

- It does not establish legal, regulatory, cyber-insurance, vendor, or AI production-use acceptance.
- It does not replace a formal Security Risk Analysis, legal/compliance review, incident reporting decision, penetration test, vulnerability scan, MDR, SOC, or contract review.
- It does not verify live systems, contracts, backups, logs, user lists, vendor claims, AI terms, or insurance answers.
- It does not permit PHI, patient identifiers, credentials, secrets, private URLs, raw contracts, raw logs, or incident-sensitive details in this public repo.
"""


def render_practice_assurance_packet(
    summary: dict[str, Any],
    risk_rows: list[dict[str, Any]],
    handoff_rows: list[dict[str, Any]],
) -> str:
    practice = summary["practice"]
    top_rows = []
    for risk in risk_rows[:5]:
        top_rows.append(
            [
                risk["title"],
                risk["priority"],
                risk.get("recipient", ""),
                _owner_takeaway_for_risk(risk),
                risk.get("plain_english_summary", ""),
                risk.get("recommended_question", ""),
                _frontdoor_evidence_for_item(risk),
                _joined(risk.get("unsafe_inputs", "")),
            ]
        )
    if not top_rows:
        top_rows.append(
            [
                "No generated high-priority finding",
                "low",
                "Owner/MSP",
                "Assign an owner and collect a reference-only evidence note.",
                "No major gap was generated, but evidence references should still be reviewed.",
                "Which evidence references should be refreshed first?",
                "Evidence reference ID, owner, date observed, and short status note.",
                "PHI, patient identifiers, credentials, secrets, private URLs, raw contracts, raw logs.",
            ]
        )

    external_rows = []
    for risk in risk_rows:
        if str(risk.get("stage_id", "")) == "external_evidence_precheck":
            external_rows.append(
                [
                    risk["title"],
                    risk["priority"],
                    risk.get("recipient", "Owner/MSP"),
                    _owner_takeaway_for_risk(risk),
                    risk.get("recommended_question", ""),
                    _frontdoor_evidence_for_item(risk),
                ]
            )
    external_section = ""
    if external_rows:
        external_section = f"""
## External Evidence Pre-Check

These are public-site observations from patient-facing workflows such as the website, scheduler, portal, intake, payment, or registration path. They are evidence questions for the practice, MSP, website vendor, and qualified reviewer. They are not HIPAA violation, breach, legal, or compliance determinations.

{markdown_table(['Observation', 'Priority', 'Send to', 'Owner takeaway', 'Question to ask', 'Evidence to request'], external_rows)}
"""

    handoff_preview = []
    for row in handoff_rows[:8]:
        handoff_preview.append(
            [
                row.get("recipient", ""),
                row.get("priority", ""),
                row.get("action", ""),
                _frontdoor_evidence_for_item(row),
                row.get("artifact_ref", ""),
            ]
        )
    if not handoff_preview:
        handoff_preview.append(["Owner/MSP", "medium", "Review the packet together.", "Evidence reference IDs and owner notes.", "sprint-index.md"])

    audience_rows = [
        [
            "Practice owner / office manager",
            "`practice-assurance-packet.html`, `owner-action-plan.md`, `sprint-client-readout.md`",
            "What matters first, who to ask, and what can be handled this week.",
        ],
        [
            "MSP / IT partner",
            "`msp-evidence-request.md`, `msp-remediation-brief.md`, `control-evidence-matrix.csv`",
            "Which technical proof is needed for access, MFA, backups, restore testing, logs, and remediation sequencing.",
        ],
        [
            "Vendors / BAA / AI reviewers",
            "`vendor-evidence-request.md`, `vendor-baa-ai-questionnaire.md`, `vendor-baa-review.md`",
            "Which contract, incident-notice, subcontractor, retention, deletion, audit-log, and AI data-use answers are still unclear.",
        ],
        [
            "Insurance / legal / compliance reviewer",
            "`insurance-evidence-packet.md`, `limitations-appendix.md`, `source-map.md`",
            "Which evidence references support planning and which questions need qualified review.",
        ],
    ]

    return f"""# Velari Practice Assurance Packet

{OFFERING_TAGLINE}

Practice: **{practice['label']}**

Practice type: **{practice['type']}**

Review period: **{practice['review_period']}**

Readiness signal: **{summary['readiness_signal']['label']}**

Target delivery signal: **{summary['target_delivery_signal']['status'].replace('_', ' ')}**

Review basis: questions are informed by HHS/ONC/OCR SRA guidance, CISA baseline goals, healthcare cybersecurity guidance, and dental ransomware risk guidance. This packet can support preparation for a formal Security Risk Analysis, but it is not itself a formal SRA.

## What This Packet Is For

This packet helps a small dental practice understand what security and vendor evidence it already has, what is missing, and what the owner should ask the MSP, vendors, and qualified reviewers next. It is designed as a report and handoff packet, not another dashboard the practice has to manage.

It focuses on the common places evidence gets scattered: EHR, billing, email, fax, shared drives, telehealth, backup, remote support, patient messaging, imaging, AI tools, vendor contracts, and MSP tickets.

## 10-Minute Intake

Use this as the first call checklist. The owner or office manager should be able to answer these without finding raw files or handling PHI. Unknown is acceptable; the packet turns unknowns into MSP, vendor, or reviewer questions.

{markdown_table(['Step', 'Owner', 'Question', 'Evidence format', 'Do not send', 'Artifact'], _simple_intake_rows(summary))}

## Executive Snapshot

- Stages needing evidence: {summary['counts']['stages_needing_evidence']} of {summary['counts']['stages']}
- High or critical findings: {summary['counts']['high_or_critical_findings']}
- Evidence references needing attention: {summary['evidence_gap_summary']['needs_attention']}
- Control evidence rows needing attention: {summary['counts']['control_evidence_needing_attention']}
- Handoff actions: {summary['counts']['handoff_actions']}
- Connector evidence items reviewed: {summary['counts']['connector_evidence_items']}

{external_section}

## What Needs Action First

{markdown_table(['Risk or question', 'Priority', 'Send to', 'Owner takeaway', 'Plain-English reason', 'Question to ask', 'Evidence to request', 'Do not send'], top_rows)}

## Owner Decision Queue

These are the decisions or approvals the practice owner should not leave buried in an MSP ticket. Each row separates the owner takeaway from the proof request.

{markdown_table(['Decision', 'Send to', 'Owner takeaway', 'Question to ask', 'Evidence format', 'Do not send', 'Artifact'], _decision_queue_rows(risk_rows))}

## What To Hand To Whom

{markdown_table(['Audience', 'Give them', 'Why it helps'], audience_rows)}

## Evidence Requests To Start This Week

{markdown_table(['Recipient', 'Priority', 'Ask', 'Evidence format', 'Artifact'], handoff_preview)}

## Ready-To-Send Messages

Copy, paste, and adapt. All requests are reference-only. No PHI, credentials, or raw files needed.

{_ready_to_send_messages_markdown(summary)}

## Why This Helps The MSP

- The MSP gets scoped proof requests instead of a vague "are we secure?" conversation.
- Access, MFA, backup, restore-test, logging, remote-support, and remediation questions are separated from contract and legal/compliance questions.
- Evidence can be returned as reference IDs, dates observed, owner roles, and short status notes without sending PHI, credentials, private URLs, raw contracts, raw logs, or sensitive screenshots.

## Next Step With Velari

If this packet surfaces gaps the practice wants help closing, the fastest path is a short evidence call plus an updated packet.

- Walk through the top findings in a 30-45 minute evidence call.
- Send or customize the ready-to-send MSP and vendor messages above.
- Collect reference-only responses, owners, dates observed, and open questions.
- Deliver an updated packet with answers incorporated and a clear 30-day owner/MSP/reviewer plan.
- No PHI, patient data, credentials, passwords, raw logs, full contracts, or private admin links are needed.

This is a one-time packet service, not a dashboard or ongoing subscription. The goal is clarity and handoff in one week, not another tool to manage.

## What This Does Not Do

- It is not an audit opinion, legal advice, cyber-insurance advice, penetration test, vulnerability scan, MDR/SOC service, forensic review, or formal Security Risk Analysis.
- It can support preparation for a formal Security Risk Analysis, but it is not itself a formal SRA.
- It does not prove that a practice, vendor, system, AI workflow, policy, backup, or evidence binder satisfies a legal or regulatory requirement.
- It does not verify live systems, contracts, logs, backups, user lists, vendor claims, AI terms, insurance answers, or incident facts.
- It does not replace the MSP. It gives the practice and MSP a clearer evidence request list and owner handoff.

## Evidence Safety Boundary

Do not put PHI, patient identifiers, credentials, secrets, private URLs, presigned links, raw contracts, raw logs, screenshots with sensitive data, or incident-sensitive details into this public repo or public runner. Keep raw evidence in a private/offline binder and use reference IDs in generated artifacts.
"""


def render_practice_assurance_packet_html(
    summary: dict[str, Any],
    risk_rows: list[dict[str, Any]],
    handoff_rows: list[dict[str, Any]],
) -> str:
    practice = summary["practice"]
    generated_at = summary["generated_at"]
    delivery_label = str(summary["target_delivery_signal"]["status"]).replace("_", " ")
    top_risks = risk_rows[:5]
    if not top_risks:
        top_risks = [
            {
                "title": "No generated high-priority finding",
                "priority": "low",
                "recipient": "Owner/MSP",
                "plain_english_summary": "No major gap was generated, but evidence references should still be reviewed.",
                "recommended_question": "Which evidence references should be refreshed first?",
                "acceptable_evidence": ["Evidence reference ID", "owner", "date observed", "short status note"],
                "unsafe_inputs": ["PHI", "patient identifiers", "credentials", "private URLs", "raw contracts", "raw logs"],
            }
        ]

    risk_cards = []
    for index, risk in enumerate(top_risks, start=1):
        priority = str(risk.get("priority", "medium"))
        risk_cards.append(
            f"""
            <article class="risk-card priority-{_slug_class(priority)}">
              <div class="risk-head">
                <span class="risk-number">{index}</span>
                <span class="chip priority-{_slug_class(priority)}">{_html(priority)}</span>
                <span class="chip neutral">{_html(risk.get('recipient', 'Owner/MSP'))}</span>
              </div>
              <h3>{_html(risk.get('title', 'Evidence question'))}</h3>
              <p class="takeaway"><strong>Owner takeaway:</strong> {_html(_owner_takeaway_for_risk(risk))}</p>
              <p>{_html(risk.get('plain_english_summary', 'Review this item with the owner and MSP.'))}</p>
              <dl>
                <dt>Question to ask</dt>
                <dd>{_html(risk.get('recommended_question', 'Which evidence should be reviewed first?'))}</dd>
                <dt>Evidence to request</dt>
                <dd>{_html(_frontdoor_evidence_for_item(risk))}</dd>
                <dt>Do not send</dt>
                <dd>{_html(_joined(risk.get('unsafe_inputs', 'PHI; credentials; private URLs')))}</dd>
              </dl>
            </article>
            """
        )

    handoff_rows_html = []
    for row in handoff_rows[:8]:
        priority = str(row.get("priority", "medium"))
        handoff_rows_html.append(
            f"""
            <tr>
              <td><span class="chip priority-{_slug_class(priority)}">{_html(priority)}</span></td>
              <td><strong>{_html(row.get('recipient', 'Owner/MSP'))}</strong></td>
              <td>{_html(row.get('action', 'Review packet with owner and MSP.'))}</td>
              <td>{_html(_frontdoor_evidence_for_item(row))}</td>
              <td>{_artifact_anchor(str(row.get('artifact_ref', 'sprint-index.md')))}</td>
            </tr>
            """
        )
    if not handoff_rows_html:
        handoff_rows_html.append(
            """
            <tr>
              <td><span class="chip priority-medium">medium</span></td>
              <td><strong>Owner/MSP</strong></td>
              <td>Review the packet together.</td>
              <td>Evidence reference IDs and owner notes.</td>
              <td><a href="sprint-index.md">sprint-index.md</a></td>
            </tr>
            """
        )

    audience_cards = [
        (
            "Practice owner / office manager",
            "What matters first, who to ask, and what can move this week.",
            ["practice-assurance-packet.html", "owner-action-plan.md", "sprint-client-readout.md"],
        ),
        (
            "MSP / IT partner",
            "Specific proof requests for access, MFA, backups, restore testing, logs, and remediation sequence.",
            ["msp-evidence-request.md", "msp-remediation-brief.md", "control-evidence-matrix.csv"],
        ),
        (
            "Vendors / BAA / AI reviewers",
            "Contract, incident-notice, subcontractor, retention, deletion, audit-log, and AI data-use questions.",
            ["vendor-evidence-request.md", "vendor-baa-ai-questionnaire.md", "vendor-baa-review.md"],
        ),
        (
            "Insurance / legal / compliance reviewer",
            "Evidence references for planning plus questions that need qualified review.",
            ["insurance-evidence-packet.md", "limitations-appendix.md", "source-map.md"],
        ),
    ]
    audience_cards_html = []
    for label, value, artifacts in audience_cards:
        audience_cards_html.append(
            f"""
            <article class="audience-card">
              <h3>{_html(label)}</h3>
              <p>{_html(value)}</p>
              <ul>{''.join(f'<li>{_artifact_anchor(path)}</li>' for path in artifacts)}</ul>
            </article>
            """
        )

    first_week_items = []
    for action in summary["offering_summary"]["first_7_days_actions"][:7]:
        first_week_items.append(
            f"""
            <li>
              <span>{_html(action['day'])}</span>
              <strong>{_html(action['lane'])}</strong>
              <p>{_html(action['action'])}</p>
            </li>
            """
        )

    source_items = []
    for source in summary["offering_summary"]["source_anchors"][:4]:
        source_items.append(
            f"""
            <li>
              <strong>{_html(source['title'])}</strong>
              <span>{_html(source['why_it_matters'])}</span>
            </li>
            """
        )

    ready_messages_html = []
    for title, body in _ready_to_send_messages(summary):
        ready_messages_html.append(
            f"""
            <article class="message-block">
              <h3>{_html(title)}</h3>
              <pre><code>{_html(body)}</code></pre>
            </article>
            """
        )

    intake_items_html = []
    for index, step in enumerate(summary["offering_summary"].get("simple_intake_steps", []), start=1):
        intake_items_html.append(
            f"""
            <li>
              <span class="task-number">{index}</span>
              <div>
                <div class="task-top">
                  <h3>{_html(step.get('label', 'Intake step'))}</h3>
                  <span class="chip neutral">{_html(step.get('status', 'Ready to ask'))}</span>
                </div>
                <p>{_html(step.get('question', 'Confirm this item before the packet is updated.'))}</p>
                <dl>
                  <dt>Evidence format</dt>
                  <dd>{_html(step.get('evidence_format', 'Reference-only status note.'))}</dd>
                  <dt>Do not send</dt>
                  <dd>{_html(step.get('unsafe_inputs', 'PHI; credentials; private URLs.'))}</dd>
                  <dt>Artifact</dt>
                  <dd>{_artifact_anchor(str(step.get('artifact_ref', 'practice-assurance-packet.html')))}</dd>
                </dl>
              </div>
            </li>
            """
        )

    decision_rows_html = []
    for row in _decision_queue_rows(risk_rows):
        decision_rows_html.append(
            f"""
            <tr>
              <td><strong>{_html(row[0])}</strong></td>
              <td>{_html(row[1])}</td>
              <td>{_html(row[2])}</td>
              <td>{_html(row[3])}</td>
              <td>{_html(row[4])}</td>
              <td>{_html(row[5])}</td>
              <td>{_artifact_anchor(row[6])}</td>
            </tr>
            """
        )

    external_risks = [risk for risk in risk_rows if str(risk.get("stage_id", "")) == "external_evidence_precheck"]
    external_precheck_html = ""
    if external_risks:
        external_items = []
        for risk in external_risks[:4]:
            external_items.append(
                f"""
                <li>
                  <strong>{_html(risk.get('title', 'External observation'))}</strong>
                  <span>{_html(risk.get('priority', 'medium'))} &middot; {_html(risk.get('recipient', 'Owner/MSP'))}</span>
                  <p>{_html(_owner_takeaway_for_risk(risk))}</p>
                </li>
                """
            )
        external_precheck_html = f"""
    <section class="panel external-precheck">
      <div class="eyebrow">External Evidence Pre-Check</div>
      <h2>Public Patient-Facing Workflow Signals</h2>
      <p>These are public-site observations from patient-facing workflows such as the website, scheduler, portal, intake, payment, or registration path. They create evidence questions for the practice, MSP, website vendor, and qualified reviewer. They are not HIPAA violation, breach, legal, or compliance determinations.</p>
      <ul class="signal-list">{''.join(external_items)}</ul>
      <p class="small-note">Use {_artifact_anchor('external-evidence-precheck.md')} for the reference-only observation table and evidence questions. Do not submit real patient forms or store sensitive intercepted payloads.</p>
    </section>
"""

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{_html(practice['label'])} Practice Assurance Packet</title>
  <style>
    :root {{
      --paper: #eef3f7;
      --sheet: #ffffff;
      --ink: #17212b;
      --muted: #5f6f7e;
      --quiet: #8191a0;
      --line: #d7e0e7;
      --line-strong: #afbfca;
      --navy: #102637;
      --navy-soft: #e8f1f6;
      --teal: #0f766e;
      --teal-soft: #e6f4f2;
      --gold: #b58b2b;
      --gold-soft: #fbf2d6;
      --red: #b42318;
      --red-soft: #fde8e4;
      --amber: #b7791f;
      --amber-soft: #fff3d6;
      --green: #14745b;
      --green-soft: #e4f5ee;
      --shadow: 0 22px 52px rgba(16, 38, 55, 0.12);
      --radius: 8px;
    }}
    * {{ box-sizing: border-box; }}
    html {{ background: var(--paper); }}
    body {{
      margin: 0;
      color: var(--ink);
      background: var(--paper);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}
    a {{ color: var(--navy); text-decoration: none; border-bottom: 1px solid rgba(16, 38, 55, 0.28); }}
    a:focus-visible {{ outline: 3px solid var(--gold); outline-offset: 3px; }}
    .page {{ max-width: 1180px; margin: 0 auto; padding: 30px 22px 56px; }}
    .cover {{
      background: var(--sheet);
      border: 1px solid var(--line);
      border-top: 8px solid var(--navy);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow: hidden;
    }}
    .cover-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1.42fr) minmax(310px, 0.58fr);
      min-height: 360px;
    }}
    .cover-main {{ padding: 38px 40px 34px; }}
    .cover-side {{
      background: var(--navy);
      color: #fff;
      padding: 32px;
      display: grid;
      align-content: space-between;
      gap: 28px;
    }}
    .eyebrow {{
      color: var(--gold);
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0;
      text-transform: uppercase;
      margin-bottom: 14px;
    }}
    h1, h2, h3, p {{ margin-top: 0; }}
    h1 {{ max-width: 760px; margin-bottom: 18px; font-size: 50px; line-height: 1.02; letter-spacing: 0; overflow-wrap: anywhere; }}
    h2 {{ margin-bottom: 16px; font-size: 24px; line-height: 1.18; letter-spacing: 0; }}
    h3 {{ margin-bottom: 8px; font-size: 17px; line-height: 1.25; letter-spacing: 0; }}
    .subtitle {{ max-width: 700px; color: var(--muted); font-size: 18px; }}
    .practice-meta {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
      margin-top: 30px;
    }}
    .meta-item {{ border-top: 1px solid var(--line); padding-top: 12px; }}
    .meta-item span, .side-label {{ display: block; color: var(--quiet); font-size: 12px; font-weight: 800; text-transform: uppercase; }}
    .meta-item strong {{ display: block; margin-top: 4px; font-size: 15px; overflow-wrap: anywhere; }}
    .side-title {{ color: #c6d6df; font-size: 13px; font-weight: 800; text-transform: uppercase; }}
    .signal {{ display: grid; gap: 12px; }}
    .signal strong {{ display: block; color: #fff; font-size: 34px; line-height: 1; text-transform: capitalize; }}
    .signal p {{ color: #c6d6df; margin: 0; }}
    .boundary {{
      border: 1px solid rgba(255, 255, 255, 0.16);
      border-left: 4px solid var(--gold);
      border-radius: var(--radius);
      padding: 14px;
      color: #e5edf2;
      font-size: 13px;
    }}
    .snapshot {{
      display: grid;
      grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 10px;
      margin: 18px 0 0;
    }}
    .stat {{
      background: var(--sheet);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 16px;
      min-height: 116px;
    }}
    .stat span {{ display: block; color: var(--muted); font-size: 12px; font-weight: 800; }}
    .stat strong {{ display: block; margin-top: 12px; color: var(--navy); font-size: 30px; line-height: 1; }}
    section {{ margin-top: 26px; }}
    .section-head {{ display: flex; justify-content: space-between; gap: 20px; align-items: end; margin-bottom: 12px; }}
    .section-head p {{ max-width: 620px; margin: 0; color: var(--muted); }}
    .section-note {{ max-width: 720px; color: var(--muted); margin-bottom: 14px; }}
    .review-basis {{
      background: var(--sheet);
      border: 1px solid var(--line);
      border-left: 5px solid var(--teal);
      border-radius: var(--radius);
      padding: 16px 18px;
      color: var(--muted);
    }}
    .review-basis strong {{ color: var(--navy); }}
    .task-list {{
      margin: 0;
      padding: 0;
      list-style: none;
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }}
    .task-list li {{
      display: grid;
      grid-template-columns: 34px minmax(0, 1fr);
      gap: 12px;
      min-height: 240px;
      background: var(--sheet);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 16px;
    }}
    .task-number {{
      width: 34px;
      height: 34px;
      border-radius: 999px;
      display: grid;
      place-items: center;
      background: var(--teal-soft);
      color: var(--teal);
      font-size: 13px;
      font-weight: 900;
    }}
    .task-top {{ display: flex; align-items: start; justify-content: space-between; gap: 10px; }}
    .task-top h3 {{ margin-bottom: 6px; }}
    .task-list p {{ color: var(--muted); font-size: 14px; }}
    .risk-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
    .risk-card {{
      background: var(--sheet);
      border: 1px solid var(--line);
      border-top: 5px solid var(--amber);
      border-radius: var(--radius);
      padding: 16px;
      min-height: 280px;
      box-shadow: 0 10px 24px rgba(16, 38, 55, 0.06);
    }}
    .risk-card:first-child {{ grid-column: 1 / -1; min-height: 240px; }}
    .risk-card.priority-high, .risk-card.priority-critical {{ border-top-color: var(--red); }}
    .risk-card.priority-low {{ border-top-color: var(--green); }}
    .risk-head {{ display: flex; flex-wrap: wrap; align-items: center; gap: 7px; margin-bottom: 12px; }}
    .risk-number {{
      width: 28px;
      height: 28px;
      border-radius: 999px;
      display: grid;
      place-items: center;
      background: var(--navy);
      color: #fff;
      font-size: 12px;
      font-weight: 800;
    }}
    .chip {{
      display: inline-flex;
      align-items: center;
      min-height: 26px;
      border-radius: 999px;
      padding: 4px 9px;
      font-size: 12px;
      font-weight: 800;
      color: var(--navy);
      background: var(--navy-soft);
    }}
    .chip.priority-high, .chip.priority-critical {{ color: var(--red); background: var(--red-soft); }}
    .chip.priority-medium {{ color: var(--amber); background: var(--amber-soft); }}
    .chip.priority-low {{ color: var(--green); background: var(--green-soft); }}
    .chip.neutral {{ color: var(--muted); background: #f1f5f8; }}
    .risk-card p {{ color: var(--muted); font-size: 14px; }}
    .risk-card .takeaway {{
      margin-bottom: 10px;
      color: var(--navy);
      background: var(--navy-soft);
      border-radius: var(--radius);
      padding: 10px 12px;
      font-size: 14px;
    }}
    dl {{ margin: 14px 0 0; }}
    dt {{ margin-top: 12px; color: var(--navy); font-size: 12px; font-weight: 900; text-transform: uppercase; }}
    dd {{ margin: 3px 0 0; color: var(--muted); font-size: 13px; }}
    .audience-grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; }}
    .audience-card {{
      background: var(--sheet);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 17px;
      min-height: 230px;
    }}
    .audience-card p {{ color: var(--muted); font-size: 14px; }}
    .audience-card ul, .source-list {{ margin: 14px 0 0; padding: 0; list-style: none; }}
    .audience-card li {{ margin-top: 7px; font-size: 13px; }}
    .table-panel {{
      overflow-x: auto;
      background: var(--sheet);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: 0 10px 24px rgba(16, 38, 55, 0.05);
    }}
    .decision-panel table {{ min-width: 1080px; }}
    table {{ width: 100%; min-width: 920px; border-collapse: collapse; font-size: 14px; }}
    th, td {{ padding: 13px 14px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ color: var(--navy); background: var(--navy-soft); font-size: 12px; text-transform: uppercase; }}
    tr:last-child td {{ border-bottom: 0; }}
    .two-col {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(320px, 0.78fr); gap: 16px; }}
    .panel {{
      background: var(--sheet);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 19px;
    }}
    .message-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
    .message-block {{
      background: var(--sheet);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 17px;
      min-width: 0;
    }}
    .message-block pre {{
      margin: 12px 0 0;
      overflow-x: auto;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      background: #f7fafc;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 13px;
      color: var(--ink);
      font: 13px/1.48 ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
    }}
    .message-block code {{ font: inherit; }}
    .plain-list {{ margin: 0; padding-left: 20px; color: var(--muted); }}
    .plain-list li {{ margin-top: 7px; }}
    .signal-list {{ margin: 0; padding: 0; list-style: none; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
    .signal-list li {{
      border: 1px solid var(--line);
      border-left: 4px solid var(--teal);
      border-radius: var(--radius);
      padding: 12px;
      background: #f7fafc;
    }}
    .signal-list strong {{ display: block; color: var(--navy); }}
    .signal-list span {{ display: block; margin-top: 4px; color: var(--muted); font-size: 12px; font-weight: 800; }}
    .signal-list p {{ margin: 8px 0 0; color: var(--muted); font-size: 13px; }}
    .next-step-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }}
    .next-step h3 {{ margin-top: 0; }}
    .small-note {{ color: var(--muted); font-size: 13px; }}
    .cta-line {{
      margin: 18px 0 0;
      border-top: 1px solid var(--line);
      padding-top: 14px;
      color: var(--navy);
      font-weight: 800;
    }}
    .week-list {{ margin: 0; padding: 0; list-style: none; }}
    .week-list li {{
      display: grid;
      grid-template-columns: 70px 110px minmax(0, 1fr);
      gap: 12px;
      padding: 11px 0;
      border-bottom: 1px solid var(--line);
    }}
    .week-list li:last-child {{ border-bottom: 0; }}
    .week-list span {{ color: var(--gold); font-size: 12px; font-weight: 900; }}
    .week-list strong {{ color: var(--navy); font-size: 13px; }}
    .week-list p {{ margin: 0; color: var(--muted); font-size: 13px; }}
    .source-list li {{ margin-bottom: 12px; padding-left: 12px; border-left: 3px solid var(--line); }}
    .source-list strong {{ display: block; color: var(--navy); }}
    .source-list span {{ color: var(--muted); font-size: 13px; }}
    .footer {{
      margin-top: 28px;
      color: var(--muted);
      font-size: 12px;
      display: flex;
      justify-content: space-between;
      gap: 18px;
      border-top: 1px solid var(--line);
      padding-top: 16px;
    }}
    @media (max-width: 1120px) {{
      .snapshot {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
      .audience-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
    @media (max-width: 820px) {{
      .page {{ padding: 22px 14px 44px; }}
      .cover-grid, .two-col {{ grid-template-columns: 1fr; }}
      .cover-main, .cover-side {{ padding: 26px; }}
      h1 {{ font-size: 32px; line-height: 1.08; }}
      .subtitle {{ font-size: 16px; }}
      .practice-meta, .snapshot, .task-list, .risk-grid, .audience-grid, .message-grid, .next-step-grid, .signal-list {{ grid-template-columns: 1fr; }}
      .risk-card:first-child {{ grid-column: auto; }}
      .section-head {{ display: block; }}
      .week-list li {{ grid-template-columns: 1fr; gap: 2px; }}
      .footer {{ display: block; }}
    }}
    @media print {{
      body {{ background: #fff; }}
      .page {{ max-width: none; padding: 0; }}
      .cover, .stat, .risk-card, .audience-card, .panel, .table-panel {{ box-shadow: none; break-inside: avoid; }}
      a {{ border-bottom: 0; }}
      section {{ break-inside: avoid; }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <header class="cover">
      <div class="cover-grid">
        <div class="cover-main">
          <div class="eyebrow">Velari Practice Assurance Packet</div>
          <h1>{_html(practice['label'])}</h1>
          <p class="subtitle">{_html(OFFERING_TAGLINE)} Built to show what the practice has, what is missing, and what the owner should ask the MSP, vendors, and qualified reviewers next.</p>
          <div class="practice-meta" aria-label="Practice summary">
            <div class="meta-item"><span>Practice type</span><strong>{_html(practice['type'])}</strong></div>
            <div class="meta-item"><span>Review period</span><strong>{_html(practice['review_period'])}</strong></div>
            <div class="meta-item"><span>Locations / staff</span><strong>{int(practice['locations'])} / {int(practice['staff_count'])}</strong></div>
          </div>
        </div>
        <aside class="cover-side">
          <div class="signal">
            <span class="side-title">Readiness signal</span>
            <strong>{_html(summary['readiness_signal']['label'])}</strong>
            <p>{_html(delivery_label)}</p>
          </div>
          <div class="boundary">
            Reference-only boundary: no PHI, patient identifiers, credentials, secrets, private URLs, raw contracts, raw logs, or incident-sensitive details.
          </div>
        </aside>
      </div>
    </header>

    <section class="snapshot" aria-label="Executive snapshot">
      <div class="stat"><span>Stages needing evidence</span><strong>{summary['counts']['stages_needing_evidence']}/{summary['counts']['stages']}</strong></div>
      <div class="stat"><span>High or critical findings</span><strong>{summary['counts']['high_or_critical_findings']}</strong></div>
      <div class="stat"><span>Evidence refs needing attention</span><strong>{summary['evidence_gap_summary']['needs_attention']}</strong></div>
      <div class="stat"><span>Control evidence rows</span><strong>{summary['counts']['control_evidence_rows']}</strong></div>
      <div class="stat"><span>Control rows needing attention</span><strong>{summary['counts']['control_evidence_needing_attention']}</strong></div>
      <div class="stat"><span>Handoff actions</span><strong>{summary['counts']['handoff_actions']}</strong></div>
    </section>

    <section class="review-basis" aria-label="Review basis">
      <strong>Review basis:</strong>
      Questions are informed by HHS/ONC/OCR SRA guidance, CISA baseline goals, healthcare cybersecurity guidance, and dental ransomware risk guidance. This packet can support preparation for a formal Security Risk Analysis, but it is not itself a formal SRA.
    </section>

    <section>
      <div class="section-head">
        <div>
          <div class="eyebrow">Simple Start</div>
          <h2>10-Minute Intake</h2>
        </div>
        <p>Use this as the first call checklist. Unknown is acceptable; the packet turns unknowns into MSP, vendor, or reviewer questions.</p>
      </div>
      <ol class="task-list">{''.join(intake_items_html)}</ol>
    </section>

{external_precheck_html}

    <section>
      <div class="section-head">
        <div>
          <div class="eyebrow">Priority Review</div>
          <h2>What Needs Action First</h2>
        </div>
        <p>These are the first questions to settle before the practice relies on vendor, MSP, AI, downtime, or evidence assumptions.</p>
      </div>
      <div class="risk-grid">{''.join(risk_cards)}</div>
    </section>

    <section>
      <div class="section-head">
        <div>
          <div class="eyebrow">Owner Decisions</div>
          <h2>Owner Decision Queue</h2>
        </div>
        <p>These are the decisions or approvals the practice owner should not leave buried in an MSP ticket.</p>
      </div>
      <div class="table-panel decision-panel">
        <table>
          <thead><tr><th>Decision</th><th>Send to</th><th>Owner takeaway</th><th>Question</th><th>Evidence format</th><th>Do not send</th><th>Artifact</th></tr></thead>
          <tbody>{''.join(decision_rows_html)}</tbody>
        </table>
      </div>
    </section>

    <section>
      <div class="section-head">
        <div>
          <div class="eyebrow">Handoff Map</div>
          <h2>What To Hand To Whom</h2>
        </div>
        <p>The packet separates owner decisions, MSP proof, vendor answers, and qualified-review questions so everyone gets a clear lane.</p>
      </div>
      <div class="audience-grid">{''.join(audience_cards_html)}</div>
    </section>

    <section class="panel">
      <div class="eyebrow">MSP Collaboration</div>
      <h2>Why This Helps The MSP</h2>
      <ul class="plain-list">
        <li>Scoped proof requests replace a vague "are we secure?" conversation.</li>
        <li>Owner, vendor, legal/compliance, and technical questions stay in separate lanes.</li>
        <li>The MSP can respond with reference IDs, dates observed, owners, scope covered, and short status notes.</li>
        <li>Raw screenshots, logs, contracts, private URLs, PHI, and credentials stay in the private/offline binder.</li>
      </ul>
    </section>

    <section>
      <div class="section-head">
        <div>
          <div class="eyebrow">This Week</div>
          <h2>Evidence Requests To Start</h2>
        </div>
        <p>Request reference IDs, dates observed, owner roles, and short status notes. Keep raw proof in the private/offline binder.</p>
      </div>
      <div class="table-panel">
        <table>
          <thead><tr><th>Priority</th><th>Recipient</th><th>Ask</th><th>Evidence format</th><th>Artifact</th></tr></thead>
          <tbody>{''.join(handoff_rows_html)}</tbody>
        </table>
      </div>
    </section>

    <section>
      <div class="section-head">
        <div>
          <div class="eyebrow">Copy And Send</div>
          <h2>Ready-To-Send Messages</h2>
        </div>
        <p>Copy, paste, and adapt. All requests are reference-only. No PHI, credentials, raw contracts, raw logs, or private admin links needed.</p>
      </div>
      <div class="message-grid">{''.join(ready_messages_html)}</div>
    </section>

    <section class="two-col">
      <div class="panel">
        <div class="eyebrow">Delivery Plan</div>
        <h2>First 7 Days</h2>
        <ol class="week-list">{''.join(first_week_items)}</ol>
      </div>
      <aside class="panel">
        <div class="eyebrow">Why These Questions</div>
        <h2>Source Anchors</h2>
        <ul class="source-list">{''.join(source_items)}</ul>
      </aside>
    </section>

    <section class="panel next-step">
      <div class="eyebrow">Service Close</div>
      <h2>Next Step With Velari</h2>
      <p>If this packet surfaces gaps the practice wants help closing, the fastest path is a short evidence call plus an updated packet.</p>
      <div class="next-step-grid">
        <div>
          <h3>What we do together</h3>
          <ul class="plain-list">
            <li>Walk through the top findings in a 30-45 minute evidence call.</li>
            <li>Customize or send the ready-to-send MSP and vendor messages.</li>
            <li>Collect reference-only responses, owners, dates observed, and open questions.</li>
            <li>Deliver an updated packet with answers incorporated and a clear 30-day owner/MSP/reviewer plan.</li>
          </ul>
        </div>
        <div>
          <h3>What we need from you</h3>
          <ul class="plain-list">
            <li>Practice owner, office manager, MSP contact, and review-period confirmation.</li>
            <li>Names of key EHR, billing, email, fax, cloud storage, telehealth, AI, backup, and imaging vendors.</li>
            <li>Existing evidence references or private-binder locations if they already exist.</li>
          </ul>
          <p class="small-note"><strong>We do not need:</strong> PHI, patient data, credentials, passwords, raw logs, full contracts, patient screenshots, or private admin links.</p>
        </div>
      </div>
      <p class="cta-line">Founding-client packet plus evidence call: one-time, reference-only review with a clear handoff in one week. This is not another dashboard or ongoing subscription.</p>
    </section>

    <section class="panel">
      <div class="eyebrow">Boundary</div>
      <h2>What This Does Not Do</h2>
      <p>This is not an audit opinion, legal advice, cyber-insurance advice, penetration test, vulnerability scan, MDR/SOC service, forensic review, or formal Security Risk Analysis. It can support preparation for a formal Security Risk Analysis, but it is not itself a formal SRA. It does not prove that a practice, vendor, system, AI workflow, policy, backup, or evidence binder satisfies a legal or regulatory requirement. It does not replace the MSP; it gives the practice and MSP a clearer evidence request list and owner handoff.</p>
    </section>

    <footer class="footer">
      <span>Generated at {_html(generated_at)}. Source profile hash is tracked in sprint-summary.json and packet-manifest.json.</span>
      <span>{_html(practice['label'])} / {_html(practice['review_period'])}</span>
    </footer>
  </main>
</body>
</html>
"""


def render_owner_action_plan(summary: dict[str, Any], risk_rows: list[dict[str, Any]]) -> str:
    practice = summary["practice"]
    offering = summary["offering_summary"]
    first_week = [
        f"- **{action['day']} ({action['lane']})**: {action['action']} Expected reference: {action['evidence_request']}"
        for action in offering["first_7_days_actions"]
    ]
    msp_questions = [
        "Can you confirm MFA enforcement for EHR, billing, imaging, email, remote access, administrator, and vendor-support accounts?",
        "Can you send a user list export and admin role list for each system using reference IDs only?",
        "Can you document backup scope, last restore test, recovery owner, and any system not covered?",
        "Can you identify remote support methods, vendor accounts, log review cadence, and known exploited vulnerability handling?",
    ]
    vendor_questions = [
        "Do we have a BAA for this service, and what workflow or data does it cover?",
        "What SOC 2 or HITRUST evidence status should we record: provided, not provided, absent, or not applicable?",
        "Who is the security contact, and what are the incident-notification terms?",
        "Which subcontractors may access or process our data?",
        "What are the retention, deletion, export, audit-log, and AI training-use terms?",
    ]
    reviewer_questions = [
        "Which vendor or AI answers need contract interpretation before use?",
        "Which incident, lost-device, insurance, or formal risk-assessment questions require qualified review?",
        "Which evidence should stay in the private/offline binder instead of public artifacts?",
    ]
    priority_lines = [
        f"- {risk['title']} ({risk['priority']}, {risk.get('owner_lane', 'owner')}): "
        f"{risk.get('plain_english_summary', '')} Question: {risk.get('recommended_question', '')} "
        f"Evidence: {_joined(risk.get('acceptable_evidence', ''))}. Next action: {risk.get('next_action') or risk['recommended_action']}"
        for risk in risk_rows[:5]
    ]
    if not priority_lines:
        priority_lines = ["- Review the evidence checklist and source map with the owner and MSP."]
    return f"""# Owner Action Plan

Practice: **{practice['label']}**

Owner lane: **practice owner / office manager**

## Do Not Upload Or Send PHI To This Public Tool

Do not upload, paste, email into, or store PHI, patient identifiers, credentials, secrets, private URLs, presigned links, raw contracts, raw logs, screenshots with sensitive data, or incident-sensitive details in this public repo or public runner. Use evidence reference IDs and keep raw evidence in the private/offline binder.

## First 7 Days

{chr(10).join(first_week)}

## Top Priorities

{chr(10).join(priority_lines)}

## Questions To Send To The MSP

{chr(10).join(f'- {question}' for question in msp_questions)}

## Questions To Send To Vendors

{chr(10).join(f'- {question}' for question in vendor_questions)}

## Questions For Legal Or Compliance Reviewer

{chr(10).join(f'- {question}' for question in reviewer_questions)}

## Owner Script For This Week

Please review the attached reference-only packet. We are not sending PHI, passwords, private URLs, raw logs, raw contracts, or incident details. We need evidence references, dates observed, owners, and any gaps you need us to decide on. Start with MFA/user access, backup restore evidence, vendor/BAA answers, AI data-use boundaries, and downtime workflow questions.
"""


def _technical_check_for_risk(risk: dict[str, Any]) -> str:
    title = risk["title"].lower()
    stage_id = risk["stage_id"]
    if "mfa" in title:
        return "Verify MFA is technically enforced for EHR, billing, email, imaging, remote access, administrator, and vendor-support accounts."
    if "access" in title or "account" in title:
        return "Export user lists, admin roles, shared-account exceptions, and offboarding evidence for owner review."
    if "backup" in title or "restore" in title:
        return "Confirm backup scope, restore-test date, recovery owner, recovery notes, and systems excluded from backups."
    if "log" in title:
        return "Document log sources, monthly review cadence, alert owner, and escalation path."
    if "baa" in title or stage_id == "vendor_baa_review":
        return "Confirm vendor security contact, support access method, incident notice terms, BAA status, and SOC 2/HITRUST evidence status reference."
    if stage_id == "ai_phi_review":
        return "Confirm AI tool access, approved data classes, admin settings, retention/model-training terms, and staff guidance reference."
    if stage_id == "downtime_ransomware_review":
        return "Map critical systems to downtime owner, manual workaround, communications owner, and tabletop evidence."
    return "Provide current control status, owner, date observed, gap, remediation sequence, and private evidence reference ID."


def _expected_proof_for_risk(risk: dict[str, Any]) -> str:
    title = risk["title"].lower()
    if "mfa" in title:
        return "Admin export or screenshot showing MFA policy status, covered groups, exception list, and date observed."
    if "access" in title or "account" in title:
        return "User list export, admin role list, owner signoff, removed-account notes, and exception sunset dates."
    if "backup" in title or "restore" in title:
        return "Backup scope summary, restore-test note, recovery owner, date observed, and systems not covered."
    if "baa" in title or risk["stage_id"] == "vendor_baa_review":
        return "BAA status label, SOC 2/HITRUST status label, security contact, incident notice clause summary, subcontractor answer, and reviewer note."
    if risk["stage_id"] == "ai_phi_review":
        return "AI acceptable-use policy page, admin setting screenshot, vendor terms summary, and staff acknowledgement reference."
    return "Reference-only screenshot/export/note in the private binder with owner, date observed, and no PHI or secrets."


def render_msp_remediation_brief(
    summary: dict[str, Any],
    risk_rows: list[dict[str, Any]],
    handoff_rows: list[dict[str, Any]],
) -> str:
    candidate_rows = risk_rows[:10]
    if not candidate_rows:
        candidate_rows = [
            {
                "priority": row["priority"],
                "stage_id": row["stage_id"],
                "title": row["action"],
                "owner": row["owner"],
                "recommended_action": row["action"],
                "artifact_ref": row["artifact_ref"],
            }
            for row in handoff_rows[:8]
        ]
    rows = []
    for risk in candidate_rows:
        rows.append(
            [
                risk["priority"],
                risk["stage_id"],
                risk.get("plain_english_summary", risk["title"]),
                risk.get("why_it_matters", ""),
                _technical_check_for_risk(risk),
                _expected_proof_for_risk(risk),
                risk.get("recommended_question", ""),
                _joined(risk.get("acceptable_evidence", "")),
                _joined(risk.get("unsafe_inputs", "")),
                risk.get("timeframe", ""),
                _joined(risk.get("reviewer_needed", "")),
                risk["owner"],
                risk.get("artifact_ref", "msp-remediation-brief.md"),
                _source_titles_for_stage(risk["stage_id"]),
            ]
        )
    return f"""# MSP Remediation Brief

This is a handoff brief. It does not require real system access in the public runner. The MSP should return reference-only proof, owners, dates observed, and gaps; raw screenshots/logs/contracts stay in the private/offline binder.

## Priority Technical Checks And Evidence Requests

{markdown_table(['Priority', 'Stage reference', 'Plain-English summary', 'Why it matters', 'Technical check', 'Expected proof', 'Recommended question', 'Acceptable evidence', 'Unsafe inputs', 'Timeframe', 'Reviewer needed', 'Owner', 'Artifact', 'Source mapping'], rows)}

## Proof Rules

- Return evidence reference IDs, dates observed, owner names or roles, and short control summaries.
- Do not send PHI, credentials, secrets, private URLs, presigned links, raw contracts, raw logs, or incident-sensitive details.
- Flag anything that needs practice-owner decision, vendor clarification, legal/compliance review, or emergency incident handling.
"""


def render_vendor_baa_ai_questionnaire(profile: dict[str, Any], summary: dict[str, Any]) -> str:
    vendor_rows = []
    for vendor in profile.get("vendors", []):
        vendor_rows.append(
            [
                vendor["name"],
                vendor["service"],
                "yes" if vendor.get("touches_ephi") else "no",
                vendor.get("baa_status", "unknown"),
                vendor_soc2_status(vendor),
                vendor_hitrust_status(vendor),
                vendor.get("ai_training_use", "unknown"),
                vendor.get("risk", "medium"),
            ]
        )
    workflow_rows = []
    for workflow in profile.get("ai_workflows", []):
        workflow_rows.append(
            [
                workflow["name"],
                workflow["decision"],
                workflow["data_used"],
                workflow["vendor"],
                workflow["evidence_needed"],
            ]
        )
    questions = [
        "Is a BAA available for the service and the workflow we use?",
        "Can you provide SOC 2 or HITRUST evidence for private review, or should the status be recorded as not provided, absent, or not applicable?",
        "Which legal entity provides the service, and who is the security or privacy contact?",
        "Which subcontractors or subprocessors may access, store, support, or process the data?",
        "What incident-notification terms apply, including timing, contact path, and required customer action?",
        "What are the retention, deletion, backup, export, and account-closure terms?",
        "Is customer data used for AI model training, product improvement, human review, analytics, or benchmarking?",
        "Can customer data be excluded from AI training or human review, and is the setting on by default or configurable?",
        "Which access controls are available: MFA, SSO, role-based access, admin roles, support access approval, and offboarding?",
        "Are audit logs available for user activity, admin changes, support access, exports, deletions, and failed logins?",
        "Can the practice export all needed data and delete data on request or at termination?",
        "What security documentation can be reviewed by the practice or qualified reviewer without exposing PHI?",
    ]
    return f"""# Vendor, BAA, And AI Questionnaire

Use this as a source-backed question list, not as legal advice or vendor approval. Keep answers, contracts, screenshots, and links in the private/offline binder; enter only reference IDs and short status summaries in public artifacts.

## Vendors In Scope

{markdown_table(['Vendor', 'Service', 'Touches ePHI-like workflow?', 'BAA status', 'SOC 2 status', 'HITRUST status', 'AI training/use', 'Risk'], vendor_rows)}

## AI Workflows In Scope

{markdown_table(['Workflow', 'Decision', 'Data used', 'Vendor', 'Evidence needed'], workflow_rows)}

## Questions To Ask

{chr(10).join(f'- {question}' for question in questions)}

## Reviewer Notes

- If a vendor touches ePHI-like workflows or could receive patient, billing, clinical, credential, or raw evidence details later, escalate unanswered BAA, SOC 2/HITRUST evidence status, subcontractor, incident notice, retention/deletion, and AI training-use questions.
- Do not treat a vendor marketing page as enough by itself. Ask for the contract lane, security contact, and evidence reference a qualified reviewer can inspect privately.
- Do not paste patient examples, chart content, claim details, credentials, logs, raw contracts, or private links into vendor questionnaires generated from this public repo.
"""


def render_evidence_collection_checklist(
    profile: dict[str, Any],
    summary: dict[str, Any],
    evidence_index: dict[str, Any],
) -> str:
    rows = []
    for item in evidence_index.get("evidence_references", [])[:14]:
        rows.append(
            [
                item.get("evidence_id", ""),
                item.get("title", ""),
                item.get("owner", "Practice owner/MSP"),
                item.get("status", "requested"),
                ", ".join(item.get("artifact_refs", [])),
            ]
        )
    exact_items = [
        "MFA status screenshot or admin export for EHR, billing, email, imaging, remote access, administrator, and vendor-support accounts.",
        "User list export and admin role list for EHR, billing, imaging, email, shared drive, and remote support.",
        "Quarterly access review signoff with removed accounts, exception owners, and dates observed.",
        "Backup scope summary and backup restore test note for EHR exports, billing data, shared drive, imaging workstation, and key endpoints.",
        "Downtime tabletop agenda, participant list by role, manual workflow decisions, and lessons learned.",
        "BAA link/status label, SOC 2/HITRUST status label, vendor security contact, incident notice terms, subcontractor answer, and review date.",
        "AI tool policy page, admin settings, retention/model-training terms, staff no-PHI guidance, and acknowledgement reference.",
        "Cyber insurance questionnaire evidence references for MFA, backups, incident response, vendor access, training, and endpoint controls.",
        "Security awareness training completion summary and phishing/social-engineering reminder reference.",
        "Asset list for critical systems, owner, vendor, access method, and patch/vulnerability owner.",
        "Log review cadence note showing source systems, reviewer, escalation path, and last review date.",
        "Secure email or messaging settings for referral attachments and patient communications.",
    ]
    return f"""# Evidence Collection Checklist

Reference-only rule: do not gather or store raw evidence in this public repo. Collect screenshots, exports, notes, policy pages, contract excerpts, and logs only in the private/offline evidence binder. In public outputs, use evidence IDs, dates observed, owners, short status summaries, and artifact references.

## Existing Evidence References

{markdown_table(['Evidence ID', 'Evidence needed', 'Owner', 'Status', 'Artifact refs'], rows)}

## Exact Checklist For The Private Binder

{chr(10).join(f'- [ ] {item}' for item in exact_items)}

## What To Record In Public Artifacts

- Evidence ID or ticket/reference label.
- Owner role and date observed.
- Status: missing, requested, partial, reviewed, outdated, or not applicable.
- Short note about what is needed next.
- No PHI, patient identifiers, credentials, secrets, private URLs, presigned links, raw contracts, raw logs, screenshots with sensitive data, or incident-sensitive details.
"""


def render_day_one_workshop_agenda(summary: dict[str, Any], profile: dict[str, Any]) -> str:
    agenda_rows = [
        ["0-10 min", "Owner framing", "Confirm patient-safety priority, sprint scope, owner/MSP/legal lanes, and no-PHI evidence boundary."],
        ["10-25 min", "Practice workflow discovery", "Walk through intake, EHR, billing, referrals, messaging, shared drive, imaging, remote support, and AI-adjacent workflows."],
        ["25-40 min", "Evidence safety check", "Decide where private evidence lives, how references will be named, and who can access raw evidence outside the public repo."],
        ["40-60 min", "MSP technical lane", "Review MFA, user lists, admin roles, backup scope, restore testing, logs, remote support, and vulnerability handling."],
        ["60-75 min", "Vendor/BAA/AI lane", "Review vendors touching ePHI-like workflows, AI tools, BAA status, SOC 2/HITRUST evidence status, retention/deletion, subcontractors, and incident notice questions."],
        ["75-85 min", "Legal/compliance reviewer lane", "Park contract, incident, insurance, and formal risk-assessment questions for qualified review."],
        ["85-90 min", "Closeout", "Assign first-week actions, evidence owners, and the next review checkpoint."],
    ]
    discovery_questions = [
        "Where does patient information leave the EHR during normal work?",
        "Which workflow would hurt patient care fastest if the EHR, billing portal, phones, or shared drive were unavailable?",
        "Which vendors can support staff access, remote sessions, exports, backups, messaging, billing, imaging, or AI workflows?",
        "Which evidence already exists but lives in email, vendor portals, screenshots, spreadsheets, tickets, or memory?",
        "Which AI use is clearly no-PHI administrative drafting, and which use needs vendor and policy review first?",
    ]
    outputs = [artifact["path"] for artifact in summary["offering_summary"]["artifact_list"]]
    return f"""# Day-One Workshop Agenda

Practice: **{summary['practice']['label']}**

## Agenda

{markdown_table(['Time', 'Segment', 'What to decide'], agenda_rows)}

## Discovery Questions

{chr(10).join(f'- {question}' for question in discovery_questions)}

## Evidence Safety Boundaries

{chr(10).join(f'- {statement}' for statement in summary['offering_summary']['boundary_statements'])}

## Lanes

- Owner / office manager: priorities, vendor asks, staff guidance, evidence owner decisions.
- MSP / IT partner: technical checks, proof, remediation sequence, recovery readiness.
- Vendor / BAA / AI reviewer: contract, SOC 2/HITRUST evidence status, data-use, retention, incident notice, subcontractor, access, log, and export/delete answers.
- Legal / compliance reviewer: formal risk-assessment, contract, insurance, incident, and reporting questions.

## Expected Outputs

{chr(10).join(f'- `{name}`' for name in outputs)}
"""


def render_source_map(summary: dict[str, Any]) -> str:
    offering = summary["offering_summary"]
    anchor_lines = []
    for source in offering["source_anchors"]:
        anchor_lines.append(f"## {source['title']}")
        anchor_lines.append("")
        anchor_lines.append(f"URL: {', '.join(source['urls'])}")
        anchor_lines.append("")
        anchor_lines.append(f"Why it matters: {source['why_it_matters']}")
        anchor_lines.append("")
        anchor_lines.append(f"How this changes the sprint: {source['how_this_changes_the_sprint']}")
        anchor_lines.append("")
    stage_rows = []
    for stage in offering["stage_source_map"]:
        stage_rows.append(
            [
                stage["stage_name"],
                stage["control_theme"],
                ", ".join(stage["source_titles"]),
                stage["how_this_source_changes_what_we_ask"],
                ", ".join(stage["artifact_refs"]),
            ]
        )
    return f"""# Source Map

This map explains how source anchors shape Sprint Mode questions. The CISA CPGs are treated as voluntary high-impact baseline practices, not a comprehensive control framework. The ONC/OCR SRA Tool anchor reinforces local-first handling and qualified review for formal risk assessment work.

{chr(10).join(anchor_lines)}
## Stage-To-Source Map

{markdown_table(['Sprint stage / control theme', 'Control theme', 'Source anchors', 'How this source changes what we ask', 'Artifacts'], stage_rows)}
"""
