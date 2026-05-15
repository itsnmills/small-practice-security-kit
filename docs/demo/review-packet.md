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

## Flows

| Flow | Source | Destination | Vendor | ePHI Type | BAA Needed | Risk | Evidence Needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FLOW-001 | Patient intake form | Cloud EHR | Example EHR Vendor | demographics, insurance, treatment notes | Yes | medium | BAA, portal access controls, intake workflow owner |
| FLOW-002 | Cloud EHR | Billing Portal | Example Billing Vendor | claim and billing data | Yes | high | BAA, integration owner, incident notification terms |
| FLOW-003 | Staff email | External specialist | Email provider | referral attachments | Yes | high | secure email policy, forwarding review, staff training |


---

# Vendor and BAA Review

| Vendor | Service | Touches ePHI? | BAA Status | AI Training Use | Subcontractors | Incident Terms | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Example EHR Vendor | EHR hosting and support | Yes | signed | not reviewed | partial | 24 hours in contract | medium |
| Example Billing Vendor | Claims and billing | Yes | missing review date | unknown | unknown | unknown | high |

## Next Evidence

- Confirm BAA review date for each vendor touching ePHI.
- Record incident notification terms.
- Ask AI/data-use questions for any vendor using automation or model training.


---

# AI Workflow Review

| Workflow | Use | Data Used | Vendor | Decision | Evidence Needed |
| --- | --- | --- | --- | --- | --- |
| Marketing email drafting | Draft generic outreach copy | No patient data | General AI assistant | allowed | staff guidance and prohibited data examples |
| Billing appeal drafter | Draft payer appeal language | claim and treatment details | General AI assistant | restricted | BAA review, redaction workflow, owner approval |
| Paste visit note into public chatbot | Summarize a clinical note | clinical note | Public chatbot | prohibited | training reminder and AI use policy |

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

# Evidence Binder Index

| Evidence ID | Area | Evidence Needed | Module |
| --- | --- | --- | --- |
| FLOW-001 | ePHI flow | BAA, portal access controls, intake workflow owner | 03-hipaa-evidence-binder |
| FLOW-002 | ePHI flow | BAA, integration owner, incident notification terms | 03-hipaa-evidence-binder |
| FLOW-003 | ePHI flow | secure email policy, forwarding review, staff training | 03-hipaa-evidence-binder |
| Example EHR Vendor | Vendor/BAA | BAA, security contact, AI data-use review for Example EHR Vendor | 04-vendor-baa-review |
| Example Billing Vendor | Vendor/BAA | BAA, security contact, AI data-use review for Example Billing Vendor | 04-vendor-baa-review |
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

## MSP / Technical Follow-Up

- Enable or verify MFA for EHR access.
- Export user lists and record a quarterly access review.
- Confirm backup restore evidence for critical systems: Cloud EHR, Billing Portal, Phones, Shared Drive.
- Confirm downtime owner, manual workaround, and escalation contact for each critical system.
- Return evidence references only; do not send PHI, passwords, private URLs, presigned links, or raw incident details.

## Vendor Follow-Up

| Vendor | Service | BAA Status | Risk | Owner | Ask |
| --- | --- | --- | --- | --- | --- |
| Example EHR Vendor | EHR hosting and support | signed | medium | Practice manager | Confirm BAA scope, incident terms, subcontractors, and AI/data-use posture. |
| Example Billing Vendor | Claims and billing | missing review date | high | Practice manager | Confirm BAA scope, incident terms, subcontractors, and AI/data-use posture. |

## Handoff Boundary

This handoff is a coordination aid for the practice owner, MSP, and qualified reviewers. It does not certify compliance, provide legal advice, determine breach status, or replace a formal Security Risk Analysis.


---

# 30-60-90 Roadmap

Initial risk level: **High**

## First 30 Days

- Enable MFA for EHR access.
- Run and record a quarterly access review.
- Run a restore test and record evidence.

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
- It is not HIPAA compliance certification.
- It is not a formal HIPAA Security Risk Analysis opinion.
- It is not breach determination.
- It is not penetration testing, vulnerability scanning, MDR, SOC, or incident response.
- It does not prove that a vendor, workflow, system, or AI tool is safe for PHI/ePHI.
- It does not verify real contracts, BAAs, subprocessors, access lists, backup restores, logs, or insurance requirements.

## Evidence Boundary

Use evidence references, owners, review dates, and sanitized descriptions. Do not include PHI/ePHI, patient identifiers, staff credentials, secrets, private URLs, presigned links, raw incident details, or full contract text in public packet artifacts.

## Recommended Review

Bring this packet to the practice owner, MSP/IT provider, counsel/compliance advisor, insurer, or qualified security reviewer before relying on it for operational decisions.
