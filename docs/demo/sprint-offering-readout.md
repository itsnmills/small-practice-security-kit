# Velari Cyber Readiness Sprint for Small Healthcare Practices

Practice: **Family Dental Clinic**

Review period: **2026 Q2**

Readiness signal: **high**

## What We Reviewed

- Intake: packet-manifest.json
- Patient data outside the EHR map: ephi-flow-map.md, connected-device-inventory.md, portal-api-flow-review.md
- AI/PHI review: ai-workflow-review.md
- Vendor/BAA review: vendor-baa-review.md
- Access/offboarding review: readiness-review.md, owner-msp-handoff.md
- Downtime/ransomware review: downtime-ransomware-tabletop.md, incident-decision-log.md
- Findings/risk register: risk-register.csv, 30-60-90-roadmap.md
- Evidence packet/export: review-packet.md, review-packet.html, packet-manifest.json, evidence-index.json
- Owner/MSP handoff: owner-msp-handoff.md, handoff-actions.csv

## What This Means For Patient Safety And Client Trust

HHS Cyber Gateway frames the work plainly: cyber safety is patient safety. For a small practice, that means the sprint focuses on whether patient-data workflows, vendors, access, AI use, and downtime plans are understandable enough for the owner and MSP to act this week. The packet turns guidance from HHS 405(d) HICP, CISA Cybersecurity Performance Goals, and the ONC/OCR SRA Tool into practical questions and evidence requests.

## Top 5 Findings Or Gaps

| Finding or gap | Priority | Plain-English summary | Why it matters | Owner lane | Question to ask | Evidence to collect | Unsafe inputs | Timeframe | Reviewer needed | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Enable MFA for EHR access | high | MFA evidence for an EHR or remote-access workflow is missing or not recorded. | Weak access proof makes it harder to show who can reach systems that support patient care and patient-data workflows. | msp | Can you provide an MFA enforcement export or screenshot for EHR, billing, email, remote access, admin, and vendor-support accounts? | MFA policy export; admin screenshot with date observed; covered groups; exception list; MSP attestation | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data | 30_days | msp; office_manager | Request MFA proof, document exceptions, and assign an owner for any missing enforcement. |
| Run and record a quarterly access review | high | The practice does not have current evidence that user access was reviewed. | Weak access proof makes it harder to show who can reach systems that support patient care and patient-data workflows. | msp | Can you provide user list exports, admin role lists, shared-account exceptions, and owner signoff for access review? | user list export; admin role list; owner access-review signoff; removed-account notes; exception sunset dates | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data | 30_days | msp; office_manager | Run the access review, remove or document exceptions, and store evidence references. |
| Run a restore test and record evidence | high | Backup restore evidence is missing or stale for systems needed during patient care. | Unproven recovery can turn a ransomware or outage event into patient-care disruption and billing downtime. | msp | Can you provide backup scope, last restore-test date, recovery owner, and a private binder reference ID? | backup scope summary; restore-test note; date observed; recovery owner; systems excluded from backup | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; raw backup data; private console links | 30_days | msp; office_manager | Run or schedule a restore test and record reference-only evidence. |
| Complete the BAA register and review dates | high | A vendor appears to support a workflow involving patient data, but BAA status or review evidence is missing. | Vendor uncertainty leaves the practice without clear privacy, incident notice, retention, deletion, and subcontractor answers. | vendor | Can you confirm whether this vendor stores, processes, transmits, or accesses PHI, whether a BAA is in place, and when it was last reviewed? | BAA status; BAA review date; vendor security page; SOC 2 or HITRUST status; incident notification terms; retention/deletion terms | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; raw contracts with sensitive details | 30_days | vendor_owner; legal_or_compliance_reviewer | Add the vendor to the register, confirm PHI access level, and request BAA/evidence status. |
| Document downtime procedures for critical systems | high | Downtime workflow evidence is missing for a system the practice may need during patient care. | Unproven recovery can turn a ransomware or outage event into patient-care disruption and billing downtime. | msp | Does this item require owner signoff, MSP evidence, vendor clarification, or professional review before action? | owner signoff; evidence reference ID; date observed; workflow owner; review note | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data | 30_days | msp; office_manager | Assign an owner, collect reference-only evidence, and update the action packet. |

## First 7 Days

- **Day 1 - Owner**: Confirm Office Manager owns the sprint, MSP Lead owns technical evidence, and all outputs stay reference-only. Evidence to request: Owner signoff note that the public runner contains no PHI, secrets, private URLs, raw contracts, or raw logs. (`owner-action-plan.md`)
- **Days 1-2 - MSP**: Request MFA enforcement status and user-list exports for EHR, billing, imaging, email, remote access, administrator, and vendor-support accounts. Evidence to request: MFA status screenshot or admin export, user list export, admin role list, shared-account exception list, and owner access-review signoff. (`msp-remediation-brief.md`)
- **Days 2-3 - MSP**: Confirm backup scope and last restore-test evidence for Cloud EHR, Billing Portal, Phones, Shared Drive. Evidence to request: Backup scope summary, restore-test note, recovery owner, date observed, and private binder reference ID. (`evidence-collection-checklist.md`)
- **Days 3-4 - Vendor**: Send BAA, SOC 2/HITRUST evidence status, subcontractor, incident notice, retention/deletion, AI training-use, access control, audit-log, and export/delete questions to Example EHR Vendor, Example Billing Vendor, Workspace Provider, Example Imaging Vendor. Evidence to request: Vendor written answers, BAA status/link label, SOC 2/HITRUST status label, security contact, incident notice terms, and reviewer notes kept outside the public repo. (`vendor-baa-ai-questionnaire.md`)
- **Days 4-5 - Owner**: Decide interim AI rules for Billing appeal drafter, AI scribe pilot, Paste patient-level note into public chatbot and issue no-PHI staff guidance before any rollout. Evidence to request: AI acceptable-use page, staff acknowledgement reference, vendor terms review status, and human-review owner. (`owner-action-plan.md`)
- **Days 5-7 - Owner/MSP**: Run a 30-minute downtime/ransomware tabletop for an EHR outage during patient care and record lessons learned. Evidence to request: Tabletop agenda, participant roles, manual workflow decisions, communications owner, and private binder reference ID. (`day-one-workshop-agenda.md`)
- **Day 7 - Legal/compliance reviewer**: Escalate BAA, AI, incident, insurance, and formal risk-assessment questions that require qualified review. Evidence to request: Question list with artifact references only; no PHI, secrets, raw contracts, raw logs, or incident-sensitive details. (`sprint-offering-readout.md`)

## Questions To Send

### Practice owner / office manager
- Which patient-data workflows create the most urgent evidence gaps?
- Which vendor or MSP answers do we need this week?
- Which decisions require a qualified legal/compliance reviewer?
### MSP / IT partner
- Which accounts have MFA enforced, and which systems still need review?
- Which systems are in backup scope, and when was restore last tested?
- Which logs, admin roles, remote support methods, and known-exploited-vulnerability processes can be evidenced?
### Vendor / BAA / AI reviewer
- Does the vendor touch ePHI or support a workflow that could later receive ePHI?
- What are the BAA, SOC 2/HITRUST evidence status, subcontractor, incident notice, retention, deletion, and AI training-use answers?
- Can the practice export or delete its data, and can audit logs be reviewed?
### Legal / compliance reviewer
- Which questions require contract interpretation or formal risk assessment work?
- Which vendor, AI, incident, or insurance answers should be reviewed before the owner acts?
- Which evidence references are enough for planning, and which require private review?

## Immediate Handoff Preview

- Owner/MSP: Confirm the practice profile, owners, review period, and no-PHI evidence-reference boundary. (`packet-manifest.json`)
- MSP: Confirm each high-risk flow owner, channel, BAA need, and reference-only evidence location. (`ephi-flow-map.md`)
- Owner: Separate no-PHI administrative AI use from restricted or prohibited PHI workflows before staff rollout. (`ai-workflow-review.md`)
- Vendor: Collect BAA status, SOC 2/HITRUST evidence status, security contact, incident terms, subcontractor posture, and AI/data-use answers. (`vendor-baa-review.md`)
- MSP: Export user lists, verify MFA enforcement, and document owner signoff for access and offboarding review. (`readiness-review.md`)
- MSP: Run or schedule a restore test and tabletop, then record reference IDs and lessons learned. (`downtime-ransomware-tabletop.md`)

## Source Anchors

- HHS Cyber Gateway: https://hhscyber.hhs.gov/. Every finding is translated into patient-care continuity, trust, and owner/MSP action language.
- HHS 405(d) HICP: https://405d.hhs.gov/cornerstone/hicp. The packet asks about social engineering, ransomware, lost equipment or data, insider data loss, connected devices, identity, endpoint, data protection, asset, network, vulnerability, response, and governance evidence.
- CISA Cybersecurity Performance Goals: https://www.cisa.gov/cybersecurity-performance-goals-2-0-cpg-2-0, https://www.cisa.gov/cybersecurity-performance-goals-cpgs. The packet turns asset inventory, accountable ownership, third-party notification, known exploited vulnerability handling, backups, MFA, incident response, and secure defaults into concrete evidence requests.
- ONC/OCR Security Risk Assessment Tool: https://healthit.gov/privacy-security/security-risk-assessment-tool/. The public runner stays local-first and reference-only, and it points practices toward qualified review for formal risk assessment decisions.
- HHS HIPAA Security Rule NPRM Fact Sheet: https://www.hhs.gov/hipaa/for-professionals/security/hipaa-security-rule-nprm/factsheet/index.html. Modernization items such as asset inventory, network maps, MFA, encryption, vulnerability scanning, segmentation, backups, incident response, and BA verification are tracked as watchlist deltas, not guaranteed current obligations.
- FDA Medical Device Cybersecurity Guidance: https://www.fda.gov/medical-devices/digital-health-center-excellence/cybersecurity. The packet adds a connected-device worksheet for device/vendor ownership, patch evidence, default credential status, downtime fallback, and safety/security notice review.

## What This Does Not Prove

- It does not establish legal, regulatory, cyber-insurance, vendor, or AI production-use acceptance.
- It does not replace a formal Security Risk Analysis, legal/compliance review, incident reporting decision, penetration test, vulnerability scan, MDR, SOC, or contract review.
- It does not verify live systems, contracts, backups, logs, user lists, vendor claims, AI terms, or insurance answers.
- It does not permit PHI, patient identifiers, credentials, secrets, private URLs, raw contracts, raw logs, or incident-sensitive details in this public repo.
