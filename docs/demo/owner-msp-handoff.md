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

## Closeout Gates

| Evidence | Closeout | Owner | Trace | Next action |
| --- | --- | --- | --- | --- |
| EXT-TRACKER-SCHEDULER-001 | Ready for review | Office Manager | EXT-TRACKER-SCHEDULER-001 | Ask the website vendor and qualified privacy reviewer whether this tracker should be removed or restricted on scheduler pages. |
| EXT-TRACKER-INTAKE-002 | Ready for review | Office Manager | EXT-TRACKER-INTAKE-002 | Ask the website vendor to document tag purpose, data sent, and whether the intake workflow should suppress analytics tags pending reviewer decision. |
| EXT-TLS-PORTAL-003 | Needs evidence | MSP Lead | EXT-TLS-PORTAL-003 | Ask the MSP or portal vendor for TLS scan summary, certificate expiry, redirect behavior, HSTS status, and covered host list. |
| EVID-ACCESS-Q2 | Needs evidence | Office Manager | EVID-ACCESS-Q2 | Collect or refresh the reference-only evidence and record owner/date/scope without uploading raw evidence. |
| EVID-BACKUP-RESTORE | Blocked | MSP Lead | EVID-BACKUP-RESTORE | Collect or refresh the reference-only evidence and record owner/date/scope without uploading raw evidence. |
| EVID-CYBER-INSURANCE | Needs evidence | Practice Owner | EVID-CYBER-INSURANCE | Collect or refresh the reference-only evidence and record owner/date/scope without uploading raw evidence. |
| EVID-AI-GUIDANCE | Needs evidence | Office Manager | EVID-AI-GUIDANCE | Collect or refresh the reference-only evidence and record owner/date/scope without uploading raw evidence. |
| EVID-VENDOR-BAA-GAPS | Needs evidence | Office Manager | EVID-VENDOR-BAA-GAPS | Collect or refresh the reference-only evidence and record owner/date/scope without uploading raw evidence. |
| READINESS-MFA-EHR | Blocked | MSP Lead | mfa_ehr | Request proof, document exceptions, and assign an owner before closeout. |
| READINESS-ACCESS-REVIEW | Needs evidence | MSP Lead | quarterly_access_review | Request proof, document exceptions, and assign an owner before closeout. |
| READINESS-BACKUP-RESTORE | Blocked | MSP Lead | tested_backups | Request proof, document exceptions, and assign an owner before closeout. |
| READINESS-BAA-REGISTER | Blocked | Office Manager | baa_register | Request proof, document exceptions, and assign an owner before closeout. |

## Handoff Boundary

This handoff is a coordination aid for the practice owner, MSP, and qualified reviewers. It does not issue compliance certification, provide legal advice, decide incident reporting duties, or replace a formal Security Risk Analysis.
