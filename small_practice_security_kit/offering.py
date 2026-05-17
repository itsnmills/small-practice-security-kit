from __future__ import annotations

from typing import Any

from .vendor_evidence import vendor_hitrust_status, vendor_soc2_status


OFFERING_NAME = "Velari Cyber Readiness Sprint for Small Healthcare Practices"

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

OFFERING_ARTIFACTS: list[dict[str, str]] = [
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
        "patient_data_outside_ehr_map": "ephi-flow-map.md",
        "ai_phi_review": "ai-workflow-review.md",
        "vendor_baa_review": "vendor-baa-ai-questionnaire.md",
        "access_offboarding_review": "msp-remediation-brief.md",
        "downtime_ransomware_review": "day-one-workshop-agenda.md",
        "findings_risk_register": "risk-register.csv",
        "evidence_packet_export": "evidence-collection-checklist.md",
        "owner_msp_handoff": "owner-action-plan.md",
    }
    return mapping.get(stage_id, "sprint-offering-readout.md")


def build_audience_lanes(profile: dict[str, Any]) -> list[dict[str, Any]]:
    practice = profile["practice"]
    return [
        {
            "id": "practice_owner",
            "label": "Practice owner / office manager",
            "value": "Plain-English priorities, first-week decisions, and scripts to send to the MSP, vendors, and reviewers.",
            "primary_owner": str(practice["security_owner"]),
            "primary_artifacts": ["sprint-offering-readout.md", "owner-action-plan.md", "evidence-collection-checklist.md"],
            "first_questions": [
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
            "primary_artifacts": ["sprint-offering-readout.md", "source-map.md", "limitations-appendix.md"],
            "first_questions": [
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
            "day": "Day 1",
            "lane": "Owner",
            "stage_id": "intake",
            "action": f"Confirm {practice['security_owner']} owns the sprint, {practice['technical_owner']} owns technical evidence, and all outputs stay reference-only.",
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
            "artifact_ref": "sprint-offering-readout.md",
        },
    ]


def build_offering_summary(profile: dict[str, Any], stages: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "name": OFFERING_NAME,
        "positioning": "A short, patient-safety-oriented readiness sprint that maps ePHI-like workflows, evidence gaps, vendor/BAA/AI questions, MSP checks, and first-week owner actions without collecting raw PHI or evidence in the public repo.",
        "audience_lanes": build_audience_lanes(profile),
        "source_anchors": SOURCE_ANCHORS,
        "stage_source_map": build_stage_source_map(stages),
        "first_7_days_actions": build_first_7_days_actions(profile),
        "top_value_outcomes": [
            "A plain-English map of where patient-data workflows create operational and trust risk outside the EHR.",
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
                "artifact_refs": list(stage.get("artifact_refs", [])) + [_artifact_for_stage(stage_id)],
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


def _top_gap_rows(risk_rows: list[dict[str, str]]) -> list[list[str]]:
    rows = []
    for risk in risk_rows[:5]:
        stage_id = risk["stage_id"]
        rows.append(
            [
                risk["title"],
                risk["priority"],
                _why_finding_matters(risk["title"], stage_id),
                risk["recommended_action"],
                _question_for_finding(risk["title"], stage_id, risk["recipient"]),
            ]
        )
    if not rows:
        rows.append(
            [
                "No generated high-priority finding",
                "low",
                "The practice should still review evidence references and owners before relying on the packet.",
                "Walk through the source map and evidence checklist with the owner and MSP.",
                "Which evidence references should be refreshed first?",
            ]
        )
    return rows


def _questions_by_lane(summary: dict[str, Any]) -> dict[str, list[str]]:
    lanes: dict[str, list[str]] = {}
    for lane in summary["offering_summary"]["audience_lanes"]:
        lanes[str(lane["label"])] = list(lane["first_questions"])
    return lanes


def render_sprint_offering_readout(
    summary: dict[str, Any],
    risk_rows: list[dict[str, str]],
    handoff_rows: list[dict[str, str]],
) -> str:
    practice = summary["practice"]
    offering = summary["offering_summary"]
    top_gap_table = markdown_table(
        ["Finding or gap", "Priority", "Why it matters", "What to do this week", "Question to ask"],
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


def render_owner_action_plan(summary: dict[str, Any], risk_rows: list[dict[str, str]]) -> str:
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
        f"- {risk['title']} ({risk['priority']}): {risk['recommended_action']}"
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


def _technical_check_for_risk(risk: dict[str, str]) -> str:
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


def _expected_proof_for_risk(risk: dict[str, str]) -> str:
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
    risk_rows: list[dict[str, str]],
    handoff_rows: list[dict[str, str]],
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
                _technical_check_for_risk(risk),
                _expected_proof_for_risk(risk),
                risk["owner"],
                risk.get("artifact_ref", "msp-remediation-brief.md"),
                _source_titles_for_stage(risk["stage_id"]),
            ]
        )
    return f"""# MSP Remediation Brief

This is a handoff brief. It does not require real system access in the public runner. The MSP should return reference-only proof, owners, dates observed, and gaps; raw screenshots/logs/contracts stay in the private/offline binder.

## Priority Technical Checks And Evidence Requests

{markdown_table(['Priority', 'Stage reference', 'Technical check', 'Expected proof', 'Owner', 'Artifact', 'Source mapping'], rows)}

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
