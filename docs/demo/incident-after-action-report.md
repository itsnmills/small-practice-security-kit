# Incident After-Action Report

Scenario: **Suspicious login and EHR downtime tabletop**

This report turns the timeline into owner/MSP follow-up work. It is an operational improvement packet, not a reportability conclusion, legal opinion, formal Security Risk Analysis, or incident-response substitute.

## What Worked

- A single owner/MSP timeline can preserve the order of events without exposing PHI or secrets.
- Evidence is tracked by reference ID, not by copying screenshots, logs, private URLs, contracts, or patient-level details into public artifacts.
- Legal/compliance, insurance, regulatory, and contract-notice questions stay parked for qualified reviewers.

## Phase Closeout Review

| Phase | Owner lane | Goal | Completion criteria | Evidence reference | Closeout |
| --- | --- | --- | --- | --- | --- |
| Detection | Owner/MSP | Confirm whether the concern is a normal operational issue, a security event, or something that needs immediate containment without copying sensitive evidence into the kit. | concern category recorded; initial owner assigned; private evidence reference created; escalation trigger reviewed | restricted-evidence/incidents/tabletop-detection-note | Needs owner review |
| Continuity | Practice owner/Office manager | Keep care and core operations moving with the least risky manual workflow while the technical owner investigates. | manual workflow selected; critical systems listed; owner approval reference recorded; unsafe data-copy risk reviewed | restricted-evidence/incidents/downtime-workflow-reference | Needs owner review |
| Containment | MSP/technical owner | Limit further harm while preserving the facts a qualified responder, insurer, vendor, or reviewer may need later. | technical owner assigned; containment action category recorded; private evidence reference recorded; qualified-review need assessed | restricted-evidence/incidents/containment-action-reference | Needs owner review |
| Qualified review | Qualified reviewer | Park legal, regulatory, insurance, contract, and formal reporting questions for qualified reviewers while the practice keeps the fact packet clean. | qualified reviewer identified; parked decisions listed; private evidence references ready; owner communication boundary confirmed | restricted-evidence/incidents/qualified-review-queue | Needs owner review |
| After-action | Practice owner/MSP | Convert the incident or tabletop into closed owners, due dates, and evidence refreshes instead of vague lessons. | top fixes assigned; evidence needed for closure listed; owner review scheduled; next tabletop improvement identified | restricted-evidence/incidents/after-action-items | Needs owner review |

## Owner Review Agenda

- Which phase is still open, and who owns it?
- Which private evidence reference would a reviewer ask for first?
- Which MSP/vendor question is still unanswered?
- Which continuity workflow prevented unsafe data copies?
- Which improvement should be funded or completed in the next 30 days?

## Improvement Actions

| ID | Priority | Owner | Action | Evidence needed | Due |
| --- | --- | --- | --- | --- | --- |
| INC-AA-001 | high | MSP Lead | Confirm MFA enforcement, session reset, administrator list, and access-review evidence for EHR and workspace accounts. | Admin settings export reference, access review reference, session reset reference, and owner signoff. | 30 days |
| INC-AA-002 | high | Office Manager | Update downtime workflow for Cloud EHR, Billing Portal, Phones, and Shared Drive. | Downtime workflow reference, staff acknowledgement reference, and tabletop attendance reference. | 30 days |
| INC-AA-003 | medium | Practice Owner | Review vendor incident terms and support contacts for EHR, billing, imaging, workspace, and AI scribe vendors. | Vendor terms reference, security contact reference, BAA review date, and qualified-review notes. | 60 days |
| INC-AA-004 | medium | MSP Lead | Run a restore-test evidence refresh for systems needed during patient-care continuity. | Restore-test record reference, backup-scope reference, and exception list. | 60 days |

## Reviewer Packet

- Incident evidence timeline.
- Private evidence reference list.
- Owner/MSP containment summary.
- Vendor notification or support-ticket reference, if applicable.
- Backup/restore and access-review evidence references for affected systems.
- List of decisions parked for counsel, compliance, insurer, vendor, or qualified incident responder.
