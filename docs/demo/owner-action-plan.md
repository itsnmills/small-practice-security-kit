# Owner Action Plan

Practice: **Family Dental Clinic**

Owner lane: **practice owner / office manager**

## Do Not Upload Or Send PHI To This Public Tool

Do not upload, paste, email into, or store PHI, patient identifiers, credentials, secrets, private URLs, presigned links, raw contracts, raw logs, screenshots with sensitive data, or incident-sensitive details in this public repo or public runner. Use evidence reference IDs and keep raw evidence in the private/offline binder.

## First 7 Days

- **Day 1 (Owner)**: Confirm Office Manager owns the sprint, MSP Lead owns technical evidence, and all outputs stay reference-only. Expected reference: Owner signoff note that the public runner contains no PHI, secrets, private URLs, raw contracts, or raw logs.
- **Days 1-2 (MSP)**: Request MFA enforcement status and user-list exports for EHR, billing, imaging, email, remote access, administrator, and vendor-support accounts. Expected reference: MFA status screenshot or admin export, user list export, admin role list, shared-account exception list, and owner access-review signoff.
- **Days 2-3 (MSP)**: Confirm backup scope and last restore-test evidence for Cloud EHR, Billing Portal, Phones, Shared Drive. Expected reference: Backup scope summary, restore-test note, recovery owner, date observed, and private binder reference ID.
- **Days 3-4 (Vendor)**: Send BAA, SOC 2/HITRUST evidence status, subcontractor, incident notice, retention/deletion, AI training-use, access control, audit-log, and export/delete questions to Example EHR Vendor, Example Billing Vendor, Workspace Provider, Example Imaging Vendor. Expected reference: Vendor written answers, BAA status/link label, SOC 2/HITRUST status label, security contact, incident notice terms, and reviewer notes kept outside the public repo.
- **Days 4-5 (Owner)**: Decide interim AI rules for Billing appeal drafter, AI scribe pilot, Paste patient-level note into public chatbot and issue no-PHI staff guidance before any rollout. Expected reference: AI acceptable-use page, staff acknowledgement reference, vendor terms review status, and human-review owner.
- **Days 5-7 (Owner/MSP)**: Run a 30-minute downtime/ransomware tabletop for an EHR outage during patient care and record lessons learned. Expected reference: Tabletop agenda, participant roles, manual workflow decisions, communications owner, and private binder reference ID.
- **Day 7 (Legal/compliance reviewer)**: Escalate BAA, AI, incident, insurance, and formal risk-assessment questions that require qualified review. Expected reference: Question list with artifact references only; no PHI, secrets, raw contracts, raw logs, or incident-sensitive details.

## Top Priorities

- Complete the BAA register and review dates (high, vendor): A vendor appears to support a workflow involving patient data, but BAA status or review evidence is missing. Question: Can you confirm whether this vendor stores, processes, transmits, or accesses PHI, whether a BAA is in place, and when it was last reviewed? Evidence: BAA status; BAA review date; vendor security page; SOC 2 or HITRUST status; incident notification terms; retention/deletion terms. Next action: Add the vendor to the register, confirm PHI access level, and request BAA/evidence status.
- Document downtime procedures for critical systems (high, msp): Downtime workflow evidence is missing for a system the practice may need during patient care. Question: Does this item require owner signoff, MSP evidence, vendor clarification, or professional review before action? Evidence: owner signoff; evidence reference ID; date observed; workflow owner; review note. Next action: Assign an owner, collect reference-only evidence, and update the action packet.
- Enable MFA for EHR access (high, msp): MFA evidence for an EHR or remote-access workflow is missing or not recorded. Question: Can you provide an MFA enforcement export or screenshot for EHR, billing, email, remote access, admin, and vendor-support accounts? Evidence: MFA policy export; admin screenshot with date observed; covered groups; exception list; MSP attestation. Next action: Request MFA proof, document exceptions, and assign an owner for any missing enforcement.
- Run a restore test and record evidence (high, msp): Backup restore evidence is missing or stale for systems needed during patient care. Question: Can you provide backup scope, last restore-test date, recovery owner, and a private binder reference ID? Evidence: backup scope summary; restore-test note; date observed; recovery owner; systems excluded from backup. Next action: Run or schedule a restore test and record reference-only evidence.
- Run and record a quarterly access review (high, msp): The practice does not have current evidence that user access was reviewed. Question: Can you provide user list exports, admin role lists, shared-account exceptions, and owner signoff for access review? Evidence: user list export; admin role list; owner access-review signoff; removed-account notes; exception sunset dates. Next action: Run the access review, remove or document exceptions, and store evidence references.

## Questions To Send To The MSP

- Can you confirm MFA enforcement for EHR, billing, imaging, email, remote access, administrator, and vendor-support accounts?
- Can you send a user list export and admin role list for each system using reference IDs only?
- Can you document backup scope, last restore test, recovery owner, and any system not covered?
- Can you identify remote support methods, vendor accounts, log review cadence, and known exploited vulnerability handling?

## Questions To Send To Vendors

- Do we have a BAA for this service, and what workflow or data does it cover?
- What SOC 2 or HITRUST evidence status should we record: provided, not provided, absent, or not applicable?
- Who is the security contact, and what are the incident-notification terms?
- Which subcontractors may access or process our data?
- What are the retention, deletion, export, audit-log, and AI training-use terms?

## Questions For Legal Or Compliance Reviewer

- Which vendor or AI answers need contract interpretation before use?
- Which incident, lost-device, insurance, or formal risk-assessment questions require qualified review?
- Which evidence should stay in the private/offline binder instead of public artifacts?

## Owner Script For This Week

Please review the attached reference-only packet. We are not sending PHI, passwords, private URLs, raw logs, raw contracts, or incident details. We need evidence references, dates observed, owners, and any gaps you need us to decide on. Start with MFA/user access, backup restore evidence, vendor/BAA answers, AI data-use boundaries, and downtime workflow questions.
