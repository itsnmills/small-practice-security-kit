# Readiness Review

Practice: Family Dental Clinic

Overall initial risk: **High**

| Item | Ready? | Area |
| --- | --- | --- |
| Email MFA | Yes | Access |
| EHR MFA | No | Access |
| Unique accounts | Yes | Access |
| Quarterly access review | No | Evidence |
| Tested backups | No | Resilience |
| Vendor inventory | Yes | Vendor |
| BAA register | No | Vendor |
| Incident contact list | Yes | Incident |
| Downtime plan | No | Resilience |
| Training current | Yes | Workforce |
| Log review cadence | No | Monitoring |

## Priority Gaps

- Enable MFA for EHR access.
- Run and record a quarterly access review.
- Run a restore test and record evidence.
- Complete the BAA register and review dates.
- Document downtime procedures for critical systems.
- Set a monthly log review cadence.


---

# ePHI Flow Map

## Systems

| System | Category | ePHI Role | Vendor | Evidence Needed |
| --- | --- | --- | --- | --- |
| Cloud EHR | EHR | creates, receives, maintains, transmits | Example EHR Vendor | admin settings export, BAA, user access review |
| Billing Portal | Billing | receives, maintains, transmits | Example Billing Vendor | BAA, user list, incident contact |
| Shared Drive | File storage | maintains | Workspace Provider | access review, sharing settings, backup reference |
| Dental Imaging Workstation | Imaging | creates and maintains | Example Imaging Vendor | local account list, backup scope reference, vendor support access procedure |
| Patient Messaging Portal | Patient communications | receives and transmits | Example Messaging Vendor | BAA, secure message settings, retention settings |
| General AI Assistant | AI drafting | no PHI approved for public demo workflow | General AI Assistant Vendor | staff no-PHI guidance, acceptable-use acknowledgement |
| AI Scribe Pilot | AI documentation | potentially receives or creates ePHI if approved later | Example AI Scribe Vendor | BAA review, retention terms, human review process, pilot approval |

## Flows

| Flow | Source | Destination | Vendor | ePHI Type | BAA Needed | Risk | Evidence Needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FLOW-001 | Patient intake form | Cloud EHR | Example EHR Vendor | demographic and insurance categories | Yes | medium | BAA, portal access controls, intake workflow owner |
| FLOW-002 | Cloud EHR | Billing Portal | Example Billing Vendor | billing and payer-submission categories | Yes | high | BAA, integration owner, incident notification terms |
| FLOW-003 | Staff email | External specialist | Email provider | referral attachments | Yes | high | secure email policy, forwarding review, staff training |
| FLOW-004 | Dental Imaging Workstation | Shared Drive | Workspace Provider | image export categories | Yes | high | export procedure, shared-folder access review, backup scope reference |
| FLOW-005 | Front desk notes | General AI Assistant | General AI Assistant Vendor | no patient data approved; generic administrative drafting only | No | medium | AI acceptable-use guidance and staff acknowledgement |
| FLOW-006 | Provider conversation | AI Scribe Pilot | Example AI Scribe Vendor | potential visit-summary categories if approved after vendor review | Yes | high | BAA, retention terms, model-training terms, human review approval |


---

# Vendor and BAA Review

| Vendor | Service | Touches ePHI? | BAA Status | AI Training Use | SOC 2 Status | HITRUST Status | Subcontractors | Incident Terms | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Example EHR Vendor | EHR hosting and support | Yes | signed | not reviewed | not provided | not provided | partial | 24 hours in contract | medium |
| Example Billing Vendor | Claims and billing | Yes | missing review date | unknown | not provided | not provided | unknown | unknown | high |
| Workspace Provider | Email, calendar, and shared drive | Yes | signed | not reviewed for add-on AI features | not provided | not provided | published list not reviewed | portal notice terms need review | medium |
| Example Imaging Vendor | Dental imaging software and support | Yes | unknown | not applicable in current deployment | not provided | not provided | unknown | unknown | high |
| General AI Assistant Vendor | Administrative drafting assistant | No | not needed for no-PHI demo workflow | consumer/default settings not approved for sensitive data | not applicable | not applicable | not reviewed | not reviewed | medium |
| Example AI Scribe Vendor | AI scribe pilot | Yes | requested | unknown | not provided | not provided | unknown | unknown | high |

## Next Evidence

- Confirm BAA review date for each vendor touching ePHI.
- Record SOC 2 and HITRUST evidence status as provided, not provided, absent, or not applicable; do not infer attestations from marketing pages.
- Record incident notification terms.
- Ask AI/data-use questions for any vendor using automation or model training.


---

# AI Workflow Review

| Workflow | Use | Data Used | Vendor | Decision | Evidence Needed |
| --- | --- | --- | --- | --- | --- |
| Marketing email drafting | Draft generic outreach copy | No patient data | General AI assistant | allowed | staff guidance and prohibited data examples |
| Insurance renewal questionnaire drafting | Draft plain-language answers for cyber insurance renewal questions | Control status summaries and evidence reference IDs only | General AI assistant | allowed | owner review and no-PHI/no-secret prompt guidance |
| Billing appeal drafter | Draft payer appeal language | billing scenario summary; real patient-level details are not approved | General AI assistant | restricted | BAA review, redaction workflow, owner approval |
| AI scribe pilot | Draft visit summaries after provider review | potential PHI if enabled after vendor approval | Example AI Scribe Vendor | restricted | BAA, retention/model-training terms, human review workflow, pilot owner signoff |
| Paste patient-level note into public chatbot | Summarize patient-level documentation | patient-level documentation category | Public chatbot | prohibited | training reminder and AI use policy |

## Rules of Thumb

- Allowed: generic administrative drafting with no patient or clinical details.
- Restricted: workflows involving claim, treatment, billing, or operationally sensitive data.
- Prohibited: pasting patient-level notes or identifiers into tools without approved safeguards and a reviewed vendor relationship.


---

# Downtime and Ransomware Tabletop

Downtime plan status: **not documented**

Restore test status: **not recorded**

Tabletop status: **not run**

| Critical System | Downtime Owner | Evidence Needed |
| --- | --- | --- |
| Cloud EHR | Needs downtime owner | Needs restore or manual workaround evidence |
| Billing Portal | Needs downtime owner | Needs restore or manual workaround evidence |
| Phones | Needs downtime owner | Needs restore or manual workaround evidence |
| Shared Drive | Needs downtime owner | Needs restore or manual workaround evidence |

## Tabletop Scenario

Run a 30-minute walkthrough: EHR unavailable at 8:30 AM, phones are working, billing portal is delayed, and staff need to continue patient care safely.


---

# Connected Device Inventory

This worksheet extends the ePHI flow map for small-practice IoMT and medical-device-adjacent systems. It is a readiness worksheet, not a live network scan, penetration test, FDA safety assessment, or compliance determination.

## Connected Device Worksheet

| Device / system | Vendor | Network location or access path | PHI handled | Firmware / patch owner | Default credential status | Downtime fallback | Safety notice review |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Cloud EHR | Example EHR Vendor | browser | creates, receives, maintains, transmits | Practice Owner | unknown - verify default credentials disabled | manual workflow or restore path to confirm | review vendor safety/security notices and patch advisories |
| Billing Portal | Example Billing Vendor | browser | receives, maintains, transmits | Billing Lead | unknown - verify default credentials disabled | manual workflow or restore path to confirm | review vendor safety/security notices and patch advisories |
| Shared Drive | Workspace Provider | managed endpoint and browser | maintains | Office Manager | unknown - verify default credentials disabled | manual workflow or restore path to confirm | review vendor safety/security notices and patch advisories |
| Dental Imaging Workstation | Example Imaging Vendor | local workstation and vendor support session | creates and maintains | Lead Dental Assistant | unknown - verify default credentials disabled | manual workflow or restore path to confirm | review vendor safety/security notices and patch advisories |

## Evidence To Request

- Current device or workstation inventory export, with owner and date observed.
- Vendor support path, remote-access method, and account owner.
- Firmware, patch, or managed endpoint status reference.
- Default credential exception review and compensating-control note.
- Backup/restore or downtime fallback for devices needed during patient care.
- Vendor safety/security notice review cadence and owner.

## Boundary

Record only reference IDs, owners, and short status summaries here. Keep serial numbers, screenshots, network diagrams, private IPs, raw logs, credentials, and patient details in the private/offline evidence binder.


---

# Portal And API Flow Review

This worksheet extends `ephi-flow-map.md` for portals, integrations, apps, and API/FHIR-style connections. It does not validate live APIs, prove identity controls, approve apps, or replace vendor/legal review.

## Portal And API Flows

| Flow | Source | Destination | Vendor/app owner | Connection | Data category | BAA needed | Evidence needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FLOW-001 | Patient intake form | Cloud EHR | Example EHR Vendor | HTTPS portal | demographic and insurance categories | Yes | BAA, portal access controls, intake workflow owner |
| FLOW-002 | Cloud EHR | Billing Portal | Example Billing Vendor | vendor integration | billing and payer-submission categories | Yes | BAA, integration owner, incident notification terms |
| FLOW-006 | Provider conversation | AI Scribe Pilot | Example AI Scribe Vendor | vendor app | potential visit-summary categories if approved after vendor review | Yes | BAA, retention terms, model-training terms, human review approval |

## Evidence Checklist

- [ ] Portal users and role list, including inactive or shared-account exceptions.
- [ ] Patient identity workflow: invitation, registration, reset, proxy/delegate access, and support verification.
- [ ] FHIR/app/API connections: app name, vendor owner, scope, authorization path, and review date.
- [ ] Audit logs for portal access, secure messages, exports, failed logins, admin changes, and support access.
- [ ] Secure messaging settings, attachment rules, retention, and deletion/export workflow.
- [ ] Vendor ownership, BAA status, incident notice, subcontractors, and data-use terms.

## Patient Identity Workflow

Document who can invite a patient, reset access, change contact details, approve proxy/delegate access, and handle portal support. Use reference IDs only; do not include patient examples.

## FHIR/app/API connections

For each app or integration, record owner, scope, vendor, authorization method, audit-log availability, export/delete path, and reviewer notes in the private binder.


---

# Incident Decision Log

Use this as a handoff template when an outage, ransomware concern, lost device, vendor notice, misdirected message, or suspicious access question appears during the sprint. It separates technical response work from qualified breach-notification and legal/compliance decisions.

## Decision Log Template

| Lane | Question to answer | Decision owner | Status | Evidence boundary |
| --- | --- | --- | --- | --- |
| Incident or concern | What happened at a sanitized category level? | Owner/MSP | open | Do not record patient names, screenshots, raw logs, or private URLs. |
| Technical containment | What system/account/vendor path was contained or isolated? | MSP Lead | open | Track actions, timestamps, and evidence reference IDs only. |
| Qualified legal/compliance decision | Does this require breach-notification, contract, insurance, or regulatory analysis? | Qualified reviewer | parked for review | The public packet does not decide reportability. |
| Owner communication | What plain-English operational update can the owner approve? | Office Manager | draft | Keep incident-sensitive details out of public artifacts. |

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


---

# Evidence Binder Index

| Evidence ID | Area | Evidence Needed | Module |
| --- | --- | --- | --- |
| EVID-ACCESS-Q2 | Access | Quarterly access review export placeholder - restricted-evidence/access/q2-access-review | 03-hipaa-evidence-binder |
| EVID-BACKUP-RESTORE | Backup | Backup restore test record placeholder - restricted-evidence/backups/restore-test-record | 03-hipaa-evidence-binder |
| EVID-CYBER-INSURANCE | Insurance | Cyber insurance renewal evidence list - restricted-evidence/insurance/renewal-evidence-list | 03-hipaa-evidence-binder |
| EVID-AI-GUIDANCE | AI | Staff AI acceptable-use acknowledgement - restricted-evidence/ai/staff-ai-guidance | 03-hipaa-evidence-binder |
| EVID-VENDOR-BAA-GAPS | Vendor | Vendor BAA and incident terms follow-up list - restricted-evidence/vendors/baa-follow-up-list | 03-hipaa-evidence-binder |
| FLOW-001 | ePHI flow | BAA, portal access controls, intake workflow owner | 03-hipaa-evidence-binder |
| FLOW-002 | ePHI flow | BAA, integration owner, incident notification terms | 03-hipaa-evidence-binder |
| FLOW-003 | ePHI flow | secure email policy, forwarding review, staff training | 03-hipaa-evidence-binder |
| FLOW-004 | ePHI flow | export procedure, shared-folder access review, backup scope reference | 03-hipaa-evidence-binder |
| FLOW-005 | ePHI flow | AI acceptable-use guidance and staff acknowledgement | 03-hipaa-evidence-binder |
| FLOW-006 | ePHI flow | BAA, retention terms, model-training terms, human review approval | 03-hipaa-evidence-binder |
| Example EHR Vendor | Vendor/BAA | BAA, SOC 2/HITRUST status, security contact, AI data-use review for Example EHR Vendor | 04-vendor-baa-review |
| Example Billing Vendor | Vendor/BAA | BAA, SOC 2/HITRUST status, security contact, AI data-use review for Example Billing Vendor | 04-vendor-baa-review |
| Workspace Provider | Vendor/BAA | BAA, SOC 2/HITRUST status, security contact, AI data-use review for Workspace Provider | 04-vendor-baa-review |
| Example Imaging Vendor | Vendor/BAA | BAA, SOC 2/HITRUST status, security contact, AI data-use review for Example Imaging Vendor | 04-vendor-baa-review |
| General AI Assistant Vendor | Vendor/BAA | BAA, SOC 2/HITRUST status, security contact, AI data-use review for General AI Assistant Vendor | 04-vendor-baa-review |
| Example AI Scribe Vendor | Vendor/BAA | BAA, SOC 2/HITRUST status, security contact, AI data-use review for Example AI Scribe Vendor | 04-vendor-baa-review |
| ACCESS-QTR | Access | Quarterly access review for EHR, billing, email, remote access | 03-hipaa-evidence-binder |
| BACKUP-RESTORE | Backup | Restore test record for EHR, billing, shared drive, key workstation | 06-downtime-ransomware-tabletop |
| AI-POLICY | AI workflow | Allowed/prohibited AI use guidance and staff acknowledgement | 05-ai-workflow-review |


---

# Owner/MSP Handoff

Practice: Family Dental Clinic

Initial risk level: **High**

## Owner Decisions Needed

- Enable MFA for EHR access.
- Run and record a quarterly access review.
- Run a restore test and record evidence.
- Complete the BAA register and review dates.
- Document downtime procedures for critical systems.
- Set a monthly log review cadence.

## Action Packet Summary

| Finding | Priority | Plain-English summary | Why it matters | Owner lane | Recommended question | Acceptable evidence | Unsafe inputs | Timeframe | Reviewer needed | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Enable MFA for EHR access | high | MFA evidence for an EHR or remote-access workflow is missing or not recorded. | Weak access proof makes it harder to show who can reach systems that support patient care and patient-data workflows. | msp | Can you provide an MFA enforcement export or screenshot for EHR, billing, email, remote access, admin, and vendor-support accounts? | MFA policy export; admin screenshot with date observed; covered groups; exception list; MSP attestation | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data | 30_days | msp; office_manager | Request MFA proof, document exceptions, and assign an owner for any missing enforcement. |
| Run and record a quarterly access review | high | The practice does not have current evidence that user access was reviewed. | Weak access proof makes it harder to show who can reach systems that support patient care and patient-data workflows. | msp | Can you provide user list exports, admin role lists, shared-account exceptions, and owner signoff for access review? | user list export; admin role list; owner access-review signoff; removed-account notes; exception sunset dates | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data | 30_days | msp; office_manager | Run the access review, remove or document exceptions, and store evidence references. |
| Run a restore test and record evidence | high | Backup restore evidence is missing or stale for systems needed during patient care. | Unproven recovery can turn a ransomware or outage event into patient-care disruption and billing downtime. | msp | Can you provide backup scope, last restore-test date, recovery owner, and a private binder reference ID? | backup scope summary; restore-test note; date observed; recovery owner; systems excluded from backup | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; raw backup data; private console links | 30_days | msp; office_manager | Run or schedule a restore test and record reference-only evidence. |
| Complete the BAA register and review dates | high | A vendor appears to support a workflow involving patient data, but BAA status or review evidence is missing. | Vendor uncertainty leaves the practice without clear privacy, incident notice, retention, deletion, and subcontractor answers. | vendor | Can you confirm whether this vendor stores, processes, transmits, or accesses PHI, whether a BAA is in place, and when it was last reviewed? | BAA status; BAA review date; vendor security page; SOC 2 or HITRUST status; incident notification terms; retention/deletion terms | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; raw contracts with sensitive details | 30_days | vendor_owner; legal_or_compliance_reviewer | Add the vendor to the register, confirm PHI access level, and request BAA/evidence status. |
| Document downtime procedures for critical systems | high | Downtime workflow evidence is missing for a system the practice may need during patient care. | Unproven recovery can turn a ransomware or outage event into patient-care disruption and billing downtime. | msp | Does this item require owner signoff, MSP evidence, vendor clarification, or professional review before action? | owner signoff; evidence reference ID; date observed; workflow owner; review note | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data | 30_days | msp; office_manager | Assign an owner, collect reference-only evidence, and update the action packet. |
| Set a monthly log review cadence | high | Log review cadence evidence is missing or not recorded for systems that support patient-data workflows. | Missing log review evidence reduces risk visibility when suspicious access, vendor support, or account misuse questions arise. | msp | Can you provide the log sources, review cadence, alert owner, escalation path, and date last reviewed? | log source list; review cadence record; alert owner; escalation path; date observed | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data | 30_days | msp; office_manager | Assign a log review owner, record cadence evidence, and define escalation for suspicious access. |
| AI workflow requires action: Billing appeal drafter | medium | An AI workflow needs clearer data-use, vendor, and human-review boundaries before staff rely on it. | AI workflows need explicit data boundaries so staff do not enter patient, billing, clinical, credential, or raw evidence details into the wrong tool. | office_manager | Should this workflow remain no-PHI, restricted, or paused until vendor terms, retention, model-training use, and human-review controls are reviewed? | AI acceptable-use guidance; vendor terms summary; model-training setting; retention/deletion terms; staff acknowledgement | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; patient notes; claim narratives; raw contracts | 90_days | office_manager; legal_or_compliance_reviewer; technical_reviewer | Keep the workflow no-PHI or restricted, collect gated proof, and route terms to professional review if needed. |
| AI workflow requires action: AI scribe pilot | medium | An AI workflow needs clearer data-use, vendor, and human-review boundaries before staff rely on it. | AI workflows need explicit data boundaries so staff do not enter patient, billing, clinical, credential, or raw evidence details into the wrong tool. | office_manager | Should this workflow remain no-PHI, restricted, or paused until vendor terms, retention, model-training use, and human-review controls are reviewed? | AI acceptable-use guidance; vendor terms summary; model-training setting; retention/deletion terms; staff acknowledgement | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; patient notes; claim narratives; raw contracts | 90_days | office_manager; legal_or_compliance_reviewer; technical_reviewer | Keep the workflow no-PHI or restricted, collect gated proof, and route terms to professional review if needed. |
| AI workflow requires action: Paste patient-level note into public chatbot | high | An AI workflow needs clearer data-use, vendor, and human-review boundaries before staff rely on it. | AI workflows need explicit data boundaries so staff do not enter patient, billing, clinical, credential, or raw evidence details into the wrong tool. | office_manager | Should this workflow remain no-PHI, restricted, or paused until vendor terms, retention, model-training use, and human-review controls are reviewed? | AI acceptable-use guidance; vendor terms summary; model-training setting; retention/deletion terms; staff acknowledgement | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; patient notes; claim narratives; raw contracts | 30_days | office_manager; legal_or_compliance_reviewer; technical_reviewer | Keep the workflow no-PHI or restricted, collect gated proof, and route terms to professional review if needed. |
| BAA status needs review for Example Billing Vendor | high | A vendor appears to support a workflow involving patient data, but BAA status or review evidence is missing. | Vendor uncertainty leaves the practice without clear privacy, incident notice, retention, deletion, and subcontractor answers. | vendor | Can you confirm whether this vendor stores, processes, transmits, or accesses PHI, whether a BAA is in place, and when it was last reviewed? | BAA status; BAA review date; vendor security page; SOC 2 or HITRUST status; incident notification terms; retention/deletion terms | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; raw contracts with sensitive details | 30_days | vendor_owner; legal_or_compliance_reviewer | Add the vendor to the register, confirm PHI access level, and request BAA/evidence status. |

## MSP / Technical Follow-Up

- Enable or verify MFA for EHR access.
- Export user lists and record a quarterly access review.
- Confirm backup restore evidence for critical systems: Cloud EHR, Billing Portal, Phones, Shared Drive.
- Confirm downtime owner, manual workaround, and escalation contact for each critical system.
- Return evidence references only; do not send PHI, passwords, private URLs, presigned links, or raw incident details.

## Vendor Follow-Up

| Vendor | Service | BAA Status | SOC 2 Status | HITRUST Status | Risk | Owner | Ask |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Example EHR Vendor | EHR hosting and support | signed | not provided | not provided | medium | Practice manager | Confirm BAA scope, SOC 2/HITRUST evidence status, incident terms, subcontractors, and AI/data-use posture. |
| Example Billing Vendor | Claims and billing | missing review date | not provided | not provided | high | Practice manager | Confirm BAA scope, SOC 2/HITRUST evidence status, incident terms, subcontractors, and AI/data-use posture. |
| Workspace Provider | Email, calendar, and shared drive | signed | not provided | not provided | medium | Practice manager | Confirm BAA scope, SOC 2/HITRUST evidence status, incident terms, subcontractors, and AI/data-use posture. |
| Example Imaging Vendor | Dental imaging software and support | unknown | not provided | not provided | high | Practice manager | Confirm BAA scope, SOC 2/HITRUST evidence status, incident terms, subcontractors, and AI/data-use posture. |
| Example AI Scribe Vendor | AI scribe pilot | requested | not provided | not provided | high | Practice manager | Confirm BAA scope, SOC 2/HITRUST evidence status, incident terms, subcontractors, and AI/data-use posture. |

## Handoff Boundary

This handoff is a coordination aid for the practice owner, MSP, and qualified reviewers. It does not issue compliance certification, provide legal advice, decide incident reporting duties, or replace a formal Security Risk Analysis.


---

# 30-60-90 Roadmap

Initial risk level: **High**

## First 30 Days

- Enable MFA for EHR access.
- Run and record a quarterly access review.
- Run a restore test and record evidence.

## Action Packets To Start

| Finding | Priority | Plain-English summary | Why it matters | Owner lane | Recommended question | Acceptable evidence | Unsafe inputs | Timeframe | Reviewer needed | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Enable MFA for EHR access | high | MFA evidence for an EHR or remote-access workflow is missing or not recorded. | Weak access proof makes it harder to show who can reach systems that support patient care and patient-data workflows. | msp | Can you provide an MFA enforcement export or screenshot for EHR, billing, email, remote access, admin, and vendor-support accounts? | MFA policy export; admin screenshot with date observed; covered groups; exception list; MSP attestation | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data | 30_days | msp; office_manager | Request MFA proof, document exceptions, and assign an owner for any missing enforcement. |
| Run and record a quarterly access review | high | The practice does not have current evidence that user access was reviewed. | Weak access proof makes it harder to show who can reach systems that support patient care and patient-data workflows. | msp | Can you provide user list exports, admin role lists, shared-account exceptions, and owner signoff for access review? | user list export; admin role list; owner access-review signoff; removed-account notes; exception sunset dates | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data | 30_days | msp; office_manager | Run the access review, remove or document exceptions, and store evidence references. |
| Run a restore test and record evidence | high | Backup restore evidence is missing or stale for systems needed during patient care. | Unproven recovery can turn a ransomware or outage event into patient-care disruption and billing downtime. | msp | Can you provide backup scope, last restore-test date, recovery owner, and a private binder reference ID? | backup scope summary; restore-test note; date observed; recovery owner; systems excluded from backup | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; raw backup data; private console links | 30_days | msp; office_manager | Run or schedule a restore test and record reference-only evidence. |
| Complete the BAA register and review dates | high | A vendor appears to support a workflow involving patient data, but BAA status or review evidence is missing. | Vendor uncertainty leaves the practice without clear privacy, incident notice, retention, deletion, and subcontractor answers. | vendor | Can you confirm whether this vendor stores, processes, transmits, or accesses PHI, whether a BAA is in place, and when it was last reviewed? | BAA status; BAA review date; vendor security page; SOC 2 or HITRUST status; incident notification terms; retention/deletion terms | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; raw contracts with sensitive details | 30_days | vendor_owner; legal_or_compliance_reviewer | Add the vendor to the register, confirm PHI access level, and request BAA/evidence status. |
| Document downtime procedures for critical systems | high | Downtime workflow evidence is missing for a system the practice may need during patient care. | Unproven recovery can turn a ransomware or outage event into patient-care disruption and billing downtime. | msp | Does this item require owner signoff, MSP evidence, vendor clarification, or professional review before action? | owner signoff; evidence reference ID; date observed; workflow owner; review note | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data | 30_days | msp; office_manager | Assign an owner, collect reference-only evidence, and update the action packet. |
| Set a monthly log review cadence | high | Log review cadence evidence is missing or not recorded for systems that support patient-data workflows. | Missing log review evidence reduces risk visibility when suspicious access, vendor support, or account misuse questions arise. | msp | Can you provide the log sources, review cadence, alert owner, escalation path, and date last reviewed? | log source list; review cadence record; alert owner; escalation path; date observed | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data | 30_days | msp; office_manager | Assign a log review owner, record cadence evidence, and define escalation for suspicious access. |
| AI workflow requires action: Billing appeal drafter | medium | An AI workflow needs clearer data-use, vendor, and human-review boundaries before staff rely on it. | AI workflows need explicit data boundaries so staff do not enter patient, billing, clinical, credential, or raw evidence details into the wrong tool. | office_manager | Should this workflow remain no-PHI, restricted, or paused until vendor terms, retention, model-training use, and human-review controls are reviewed? | AI acceptable-use guidance; vendor terms summary; model-training setting; retention/deletion terms; staff acknowledgement | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; patient notes; claim narratives; raw contracts | 90_days | office_manager; legal_or_compliance_reviewer; technical_reviewer | Keep the workflow no-PHI or restricted, collect gated proof, and route terms to professional review if needed. |
| AI workflow requires action: AI scribe pilot | medium | An AI workflow needs clearer data-use, vendor, and human-review boundaries before staff rely on it. | AI workflows need explicit data boundaries so staff do not enter patient, billing, clinical, credential, or raw evidence details into the wrong tool. | office_manager | Should this workflow remain no-PHI, restricted, or paused until vendor terms, retention, model-training use, and human-review controls are reviewed? | AI acceptable-use guidance; vendor terms summary; model-training setting; retention/deletion terms; staff acknowledgement | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; patient notes; claim narratives; raw contracts | 90_days | office_manager; legal_or_compliance_reviewer; technical_reviewer | Keep the workflow no-PHI or restricted, collect gated proof, and route terms to professional review if needed. |
| AI workflow requires action: Paste patient-level note into public chatbot | high | An AI workflow needs clearer data-use, vendor, and human-review boundaries before staff rely on it. | AI workflows need explicit data boundaries so staff do not enter patient, billing, clinical, credential, or raw evidence details into the wrong tool. | office_manager | Should this workflow remain no-PHI, restricted, or paused until vendor terms, retention, model-training use, and human-review controls are reviewed? | AI acceptable-use guidance; vendor terms summary; model-training setting; retention/deletion terms; staff acknowledgement | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; patient notes; claim narratives; raw contracts | 30_days | office_manager; legal_or_compliance_reviewer; technical_reviewer | Keep the workflow no-PHI or restricted, collect gated proof, and route terms to professional review if needed. |
| BAA status needs review for Example Billing Vendor | high | A vendor appears to support a workflow involving patient data, but BAA status or review evidence is missing. | Vendor uncertainty leaves the practice without clear privacy, incident notice, retention, deletion, and subcontractor answers. | vendor | Can you confirm whether this vendor stores, processes, transmits, or accesses PHI, whether a BAA is in place, and when it was last reviewed? | BAA status; BAA review date; vendor security page; SOC 2 or HITRUST status; incident notification terms; retention/deletion terms | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; raw contracts with sensitive details | 30_days | vendor_owner; legal_or_compliance_reviewer | Add the vendor to the register, confirm PHI access level, and request BAA/evidence status. |

## Days 31-60

- Complete the BAA register and review dates.
- Document downtime procedures for critical systems.
- Set a monthly log review cadence.

## Days 61-90

- Run a tabletop exercise and record lessons learned.
- Repeat access/vendor/backup evidence review.
- Prepare management signoff packet.


---

# What This Packet Does and Does Not Prove

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
