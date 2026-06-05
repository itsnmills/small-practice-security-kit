# Source Map

This map explains how source anchors shape Sprint Mode questions. The CISA CPGs are treated as voluntary high-impact baseline practices, not a comprehensive control framework. The ONC/OCR SRA Tool anchor reinforces local-first handling and qualified review for formal risk assessment work.

## HHS Cyber Gateway

URL: https://hhscyber.hhs.gov/

Why it matters: Frames healthcare cybersecurity as patient-safety work, not only IT hygiene.

How this changes the sprint: Every finding is translated into patient-care continuity, trust, and owner/MSP action language.

## HHS 405(d) HICP

URL: https://405d.hhs.gov/cornerstone/hicp

Why it matters: Prioritizes common healthcare threats and the mitigating practices small organizations can discuss with IT partners.

How this changes the sprint: The packet asks about social engineering, ransomware, lost equipment or data, insider data loss, connected devices, identity, endpoint, data protection, asset, network, vulnerability, response, and governance evidence.

## CISA Cybersecurity Performance Goals

URL: https://www.cisa.gov/cybersecurity-performance-goals-2-0-cpg-2-0, https://www.cisa.gov/cybersecurity-performance-goals-cpgs

Why it matters: Provides voluntary, high-impact baseline practices that help small teams prioritize without pretending the list is comprehensive.

How this changes the sprint: The packet turns asset inventory, accountable ownership, third-party notification, known exploited vulnerability handling, backups, MFA, incident response, and secure defaults into concrete evidence requests.

## ONC/OCR Security Risk Assessment Tool

URL: https://healthit.gov/privacy-security/security-risk-assessment-tool/

Why it matters: Supports small and medium providers conducting HIPAA Security Rule risk assessments while keeping entries local to the user's computer.

How this changes the sprint: The public runner stays local-first and reference-only, and it points practices toward qualified review for formal risk assessment decisions.

## HHS/OCR Online Tracking Technologies Guidance

URL: https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/hipaa-online-tracking/index.html

Why it matters: Patient-facing websites, portals, schedulers, and apps can create privacy and vendor-review questions when tracking technologies collect or disclose regulated information.

How this changes the sprint: The packet treats tracker observations as potential privacy/security evidence questions for website vendors and qualified reviewers, not automatic legal conclusions.

## HHS HIPAA Security Rule Summary

URL: https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html

Why it matters: The Security Rule is technology-neutral and focuses on reasonable safeguards for electronic protected health information, including technical safeguards and transmission security.

How this changes the sprint: The external pre-check turns TLS, certificate, redirect, portal, and public-host observations into MSP evidence questions without claiming a compliance determination.

## HHS HIPAA Security Rule NPRM Fact Sheet

URL: https://www.hhs.gov/hipaa/for-professionals/security/hipaa-security-rule-nprm/factsheet/index.html

Why it matters: Flags proposed modernization items while the current Security Rule remains in effect during rulemaking.

How this changes the sprint: Modernization items such as asset inventory, network maps, MFA, encryption, vulnerability scanning, segmentation, backups, incident response, and BA verification are tracked as watchlist deltas, not guaranteed current obligations.

## FDA Medical Device Cybersecurity Guidance

URL: https://www.fda.gov/medical-devices/digital-health-center-excellence/cybersecurity

Why it matters: Connected clinical devices can affect patient safety and need owner, patch, support-access, and safety-notice review.

How this changes the sprint: The packet adds a connected-device worksheet for device/vendor ownership, patch evidence, default credential status, downtime fallback, and safety/security notice review.

## Stage-To-Source Map

| Sprint stage / control theme | Control theme | Source anchors | How this source changes what we ask | Artifacts |
| --- | --- | --- | --- | --- |
| Intake | Scope, safety boundary, accountable owner | HHS Cyber Gateway, ONC/OCR Security Risk Assessment Tool | Confirm the practice owner, technical owner, review period, and no-PHI/no-secret input rule before discussing evidence. | packet-manifest.json, sprint-summary.json |
| External evidence pre-check | Public-site tracker, patient-facing workflow, and transmission evidence | HHS/OCR Online Tracking Technologies Guidance, HHS HIPAA Security Rule Summary, CISA Cybersecurity Performance Goals | Check public patient-facing workflows for tracker, scheduler, portal, TLS, certificate, redirect, and ownership observations that should be routed to the website vendor, MSP, or qualified reviewer. | external-evidence-precheck.md |
| Patient data outside the EHR map | ePHI-like workflow visibility, asset inventory, data protection | HHS 405(d) HICP, CISA Cybersecurity Performance Goals, HHS HIPAA Security Rule NPRM Fact Sheet, FDA Medical Device Cybersecurity Guidance | Ask where patient data leaves the EHR, which vendor or system handles it, whether a BAA may be needed, what connected devices, portals, apps, or integrations touch the workflow, and what evidence reference proves the control. | ephi-flow-map.md, connected-device-inventory.md, portal-api-flow-review.md |
| AI/PHI review | AI data-use boundary, data protection, governance | HHS 405(d) HICP, CISA Cybersecurity Performance Goals | Separate no-PHI administrative drafting from workflows that need vendor, retention, training-use, and human-review scrutiny. | ai-workflow-review.md |
| Vendor/BAA review | Third-party risk, BAA posture, subcontractors, incident notice | HHS 405(d) HICP, CISA Cybersecurity Performance Goals | Ask vendors for BAA scope, SOC 2/HITRUST evidence status, security contact, subcontractor posture, incident notification terms, retention/deletion, AI training-use, and export/delete options. | vendor-baa-review.md, vendor-baa-ai-questionnaire.md |
| Access/offboarding review | Identity, access management, MFA, unique accounts | HHS 405(d) HICP, CISA Cybersecurity Performance Goals | Ask the MSP for proof of MFA enforcement, user list exports, admin role review, shared-account exceptions, and offboarding cadence. | readiness-review.md, owner-msp-handoff.md, msp-remediation-brief.md |
| Downtime/ransomware review | Ransomware resilience, backups, restore testing, downtime operations | HHS Cyber Gateway, HHS 405(d) HICP, CISA Cybersecurity Performance Goals | Ask for backup scope, restore-test notes, tabletop lessons, critical-system owners, and downtime workflow continuity. | downtime-ransomware-tabletop.md, incident-decision-log.md, day-one-workshop-agenda.md |
| Findings/risk register | Prioritized readiness gaps and fix sequencing | HHS 405(d) HICP, CISA Cybersecurity Performance Goals | Sort gaps by likely patient-safety and operational impact, then assign owners and a 30/60/90 evidence path. | risk-register.csv, 30-60-90-roadmap.md |
| Evidence packet/export | Reference-only evidence index and reviewer packet | ONC/OCR Security Risk Assessment Tool, CISA Cybersecurity Performance Goals | Collect evidence references and review status locally; do not upload raw evidence, PHI, secrets, contracts, logs, or private links to this public repo. | review-packet.md, review-packet.html, packet-manifest.json, evidence-index.json, evidence-collection-checklist.md |
| Owner/MSP handoff | Governance, accountable cyber owner, MSP/vendor/legal lanes | HHS Cyber Gateway, HHS 405(d) HICP, CISA Cybersecurity Performance Goals, ONC/OCR Security Risk Assessment Tool | Turn every gap into a lane-specific question so the owner, MSP, vendor, and legal/compliance reviewer each know what to answer next. | owner-msp-handoff.md, handoff-actions.csv, owner-action-plan.md |
