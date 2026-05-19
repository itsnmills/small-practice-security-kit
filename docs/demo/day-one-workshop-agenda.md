# Day-One Workshop Agenda

Practice: **Family Dental Clinic**

## Agenda

| Time | Segment | What to decide |
| --- | --- | --- |
| 0-10 min | Owner framing | Confirm patient-safety priority, sprint scope, owner/MSP/legal lanes, and no-PHI evidence boundary. |
| 10-25 min | Practice workflow discovery | Walk through intake, EHR, billing, referrals, messaging, shared drive, imaging, remote support, and AI-adjacent workflows. |
| 25-40 min | Evidence safety check | Decide where private evidence lives, how references will be named, and who can access raw evidence outside the public repo. |
| 40-60 min | MSP technical lane | Review MFA, user lists, admin roles, backup scope, restore testing, logs, remote support, and vulnerability handling. |
| 60-75 min | Vendor/BAA/AI lane | Review vendors touching ePHI-like workflows, AI tools, BAA status, SOC 2/HITRUST evidence status, retention/deletion, subcontractors, and incident notice questions. |
| 75-85 min | Legal/compliance reviewer lane | Park contract, incident, insurance, and formal risk-assessment questions for qualified review. |
| 85-90 min | Closeout | Assign first-week actions, evidence owners, and the next review checkpoint. |

## Discovery Questions

- Where does patient information leave the EHR during normal work?
- Which workflow would hurt patient care fastest if the EHR, billing portal, phones, or shared drive were unavailable?
- Which vendors can support staff access, remote sessions, exports, backups, messaging, billing, imaging, or AI workflows?
- Which evidence already exists but lives in email, vendor portals, screenshots, spreadsheets, tickets, or memory?
- Which AI use is clearly no-PHI administrative drafting, and which use needs vendor and policy review first?

## Evidence Safety Boundaries

- Use synthetic or client-supplied reference metadata only.
- Do not upload, paste, or send PHI, patient identifiers, credentials, secrets, private URLs, presigned links, raw contracts, raw logs, screenshots with sensitive data, or incident-sensitive details to this public tool.
- The packet is a readiness and evidence-gap organizer; it does not establish legal, regulatory, cyber-insurance, vendor, or AI production-use acceptance.
- Formal Security Risk Analysis, legal/compliance review, incident reporting decisions, and contract interpretation stay with qualified reviewers.

## Lanes

- Owner / office manager: priorities, vendor asks, staff guidance, evidence owner decisions.
- MSP / IT partner: technical checks, proof, remediation sequence, recovery readiness.
- Vendor / BAA / AI reviewer: contract, SOC 2/HITRUST evidence status, data-use, retention, incident notice, subcontractor, access, log, and export/delete answers.
- Legal / compliance reviewer: formal risk-assessment, contract, insurance, incident, and reporting questions.

## Expected Outputs

- `sprint-offering-readout.md`
- `owner-action-plan.md`
- `msp-remediation-brief.md`
- `vendor-baa-ai-questionnaire.md`
- `evidence-collection-checklist.md`
- `day-one-workshop-agenda.md`
- `source-map.md`
- `connected-device-inventory.md`
- `portal-api-flow-review.md`
- `incident-decision-log.md`
