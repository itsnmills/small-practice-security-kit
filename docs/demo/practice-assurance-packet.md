# Velari Practice Assurance Packet

A plain-English security and vendor evidence report for small dental practices.

Practice: **Family Dental Clinic**

Practice type: **Dental practice**

Review period: **2026 Q2**

Readiness signal: **high**

Target delivery signal: **needs evidence before closeout**

Review basis: questions are informed by HHS/ONC/OCR SRA guidance, CISA baseline goals, healthcare cybersecurity guidance, and dental ransomware risk guidance. This packet can support preparation for a formal Security Risk Analysis, but it is not itself a formal SRA.

## What This Packet Is For

This packet helps a small dental practice understand what security and vendor evidence it already has, what is missing, and what the owner should ask the MSP, vendors, and qualified reviewers next. It is designed as a report and handoff packet, not another dashboard the practice has to manage.

It focuses on the common places evidence gets scattered: EHR, billing, email, fax, shared drives, telehealth, backup, remote support, patient messaging, imaging, AI tools, vendor contracts, and MSP tickets.

## 10-Minute Intake

Use this as the first call checklist. The owner or office manager should be able to answer these without finding raw files or handling PHI. Unknown is acceptable; the packet turns unknowns into MSP, vendor, or reviewer questions.

| Step | Owner | Question | Evidence format | Do not send | Artifact |
| --- | --- | --- | --- | --- | --- |
| Practice and owners | Practice owner / office manager | Confirm the practice name, review period, Office Manager as security owner, and MSP Lead as technical owner. | Owner names, review period, location count, staff count, and a no-PHI/no-secret signoff note. | PHI, patient identifiers, credentials, private admin links, raw logs, raw contracts. | practice-assurance-packet.html |
| Key vendors | Office manager | List the EHR, billing, email, fax, cloud storage, telehealth, backup, imaging, website, scheduler, portal, AI, and MSP vendors. | Vendor names, owner, workflow touched, BAA status label, security evidence status label, and review date if known. | Full contracts, patient screenshots, claim details, credentials, private vendor portal links. | vendor-baa-ai-questionnaire.md |
| Patient-facing URLs | Website owner / MSP | Identify the public website, scheduler, new patient intake, portal login, payment, registration, and contact workflows to review. | Public URL labels, page/workflow names, owner, date observed, tracker/tag summary, TLS/certificate summary. | Real patient form submissions, session cookies, full intercepted payloads, private portal links. | external-evidence-precheck.md |
| AI use | Practice owner / department lead | Name AI tools being used or considered, what staff want to use them for, and whether any workflow could include patient, billing, clinical, credential, or raw evidence details. | Tool name, proposed use, data category, vendor, decision label, policy or training reference. | Patient notes, transcripts, images, claims, clinical narratives, credentials, raw evidence, prompts with patient details. | ai-workflow-review.md |
| MSP evidence status | MSP / technical owner | Mark each proof area as have it, need MSP, need vendor, needs reviewer, or unknown. | MFA status, access review date, backup scope, restore-test date, remote support method, log review cadence, patch/vulnerability process. | Raw logs, credentials, private URLs, sensitive screenshots, patient data, full network captures. | msp-remediation-brief.md |

## Executive Snapshot

- Stages needing evidence: 6 of 10
- High or critical findings: 12
- Evidence references needing attention: 40
- Control evidence rows needing attention: 30
- Handoff actions: 18
- Connector evidence items reviewed: 0


## External Evidence Pre-Check

These are public-site observations from patient-facing workflows such as the website, scheduler, portal, intake, payment, or registration path. They are evidence questions for the practice, MSP, website vendor, and qualified reviewer. They are not HIPAA violation, breach, legal, or compliance determinations.

| Observation | Priority | Send to | Owner takeaway | Question to ask | Evidence to request |
| --- | --- | --- | --- | --- | --- |
| Analytics tag observed on new patient intake page | high | Vendor/legal/compliance reviewer | Ask the website vendor and privacy reviewer what data the tracker receives on patient-facing pages. | Can the website/vendor confirm which trackers fire on patient-facing scheduler, intake, portal, payment, or registration workflows, what data is sent, and whether BAA, authorization, or qualified privacy review is needed? | tracker inventory; tag manager export; sanitized network request summary; page/workflow label; vendor BAA or authorization review note; privacy reviewer disposition |
| Third-party tracker observed on appointment scheduler | high | Vendor/legal/compliance reviewer | Ask the website vendor and privacy reviewer what data the tracker receives on patient-facing pages. | Can the website/vendor confirm which trackers fire on patient-facing scheduler, intake, portal, payment, or registration workflows, what data is sent, and whether BAA, authorization, or qualified privacy review is needed? | tracker inventory; tag manager export; sanitized network request summary; page/workflow label; vendor BAA or authorization review note; privacy reviewer disposition |
| Patient portal TLS and certificate evidence needs confirmation | medium | MSP | Ask the MSP or website vendor to confirm TLS, certificate, redirect, and HSTS evidence. | Can the MSP confirm certificate validity, HTTPS redirect behavior, TLS posture, HSTS status, and ownership for the public patient-facing workflow? | TLS scan summary; certificate expiry and issuer; HTTPS redirect evidence; HSTS status; covered host list; MSP attestation |


## What Needs Action First

| Risk or question | Priority | Send to | Owner takeaway | Plain-English reason | Question to ask | Evidence to request | Do not send |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BAA status needs review for Example Imaging Vendor | high | Vendor | Ask the vendor for BAA status, security evidence status, and incident terms. | A vendor appears to support a workflow involving patient data, but BAA status or review evidence is missing. | Can you confirm whether this vendor stores, processes, transmits, or accesses PHI, whether a BAA is in place, and when it was last reviewed? | BAA status; BAA review date; vendor security page; SOC 2 or HITRUST status; incident notification terms; retention/deletion terms | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; raw contracts with sensitive details |
| Complete the BAA register and review dates | high | Vendor | Ask the vendor for BAA status, security evidence status, and incident terms. | A vendor appears to support a workflow involving patient data, but BAA status or review evidence is missing. | Can you confirm whether this vendor stores, processes, transmits, or accesses PHI, whether a BAA is in place, and when it was last reviewed? | BAA status; BAA review date; vendor security page; SOC 2 or HITRUST status; incident notification terms; retention/deletion terms | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; raw contracts with sensitive details |
| Document downtime procedures for critical systems | high | MSP | Assign a downtime owner and record tabletop or manual-workflow evidence. | Downtime workflow evidence is missing for a system the practice may need during patient care. | Does this item require owner signoff, MSP evidence, vendor clarification, or professional review before action? | Reference-only screenshot/export/note in the private binder with owner, date observed, and no PHI or secrets. | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data |
| Enable MFA for EHR access | high | MSP | Ask the MSP for MFA proof and any exception list. | MFA evidence for an EHR or remote-access workflow is missing or not recorded. | Can you provide an MFA enforcement export or screenshot for EHR, billing, email, remote access, admin, and vendor-support accounts? | MFA policy export; admin screenshot with date observed; covered groups; exception list; MSP attestation | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data |
| Run a restore test and record evidence | high | MSP | Ask the MSP for backup scope and restore-test evidence. | Backup restore evidence is missing or stale for systems needed during patient care. | Can you provide backup scope, last restore-test date, recovery owner, and a private binder reference ID? | backup scope summary; restore-test note; date observed; recovery owner; systems excluded from backup | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; raw backup data; private console links |

## Owner Decision Queue

These are the decisions or approvals the practice owner should not leave buried in an MSP ticket. Each row separates the owner takeaway from the proof request.

| Decision | Send to | Owner takeaway | Question to ask | Evidence format | Do not send | Artifact |
| --- | --- | --- | --- | --- | --- | --- |
| BAA status needs review for Example Imaging Vendor | Vendor | Ask the vendor for BAA status, security evidence status, and incident terms. | Can you confirm whether this vendor stores, processes, transmits, or accesses PHI, whether a BAA is in place, and when it was last reviewed? | BAA status; BAA review date; vendor security page; SOC 2 or HITRUST status; incident notification terms; retention/deletion terms | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; raw contracts with sensitive details | vendor-baa-review.md |
| Complete the BAA register and review dates | Vendor | Ask the vendor for BAA status, security evidence status, and incident terms. | Can you confirm whether this vendor stores, processes, transmits, or accesses PHI, whether a BAA is in place, and when it was last reviewed? | BAA status; BAA review date; vendor security page; SOC 2 or HITRUST status; incident notification terms; retention/deletion terms | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; raw contracts with sensitive details | vendor-baa-review.md |
| Document downtime procedures for critical systems | MSP | Assign a downtime owner and record tabletop or manual-workflow evidence. | Does this item require owner signoff, MSP evidence, vendor clarification, or professional review before action? | Reference-only screenshot/export/note in the private binder with owner, date observed, and no PHI or secrets. | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data | downtime-ransomware-tabletop.md |
| Enable MFA for EHR access | MSP | Ask the MSP for MFA proof and any exception list. | Can you provide an MFA enforcement export or screenshot for EHR, billing, email, remote access, admin, and vendor-support accounts? | MFA policy export; admin screenshot with date observed; covered groups; exception list; MSP attestation | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data | owner-msp-handoff.md |
| Run a restore test and record evidence | MSP | Ask the MSP for backup scope and restore-test evidence. | Can you provide backup scope, last restore-test date, recovery owner, and a private binder reference ID? | backup scope summary; restore-test note; date observed; recovery owner; systems excluded from backup | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; raw backup data; private console links | downtime-ransomware-tabletop.md |

## What To Hand To Whom

| Audience | Give them | Why it helps |
| --- | --- | --- |
| Practice owner / office manager | `practice-assurance-packet.html`, `owner-action-plan.md`, `sprint-client-readout.md` | What matters first, who to ask, and what can be handled this week. |
| MSP / IT partner | `msp-evidence-request.md`, `msp-remediation-brief.md`, `control-evidence-matrix.csv` | Which technical proof is needed for access, MFA, backups, restore testing, logs, and remediation sequencing. |
| Vendors / BAA / AI reviewers | `vendor-evidence-request.md`, `vendor-baa-ai-questionnaire.md`, `vendor-baa-review.md` | Which contract, incident-notice, subcontractor, retention, deletion, audit-log, and AI data-use answers are still unclear. |
| Insurance / legal / compliance reviewer | `insurance-evidence-packet.md`, `limitations-appendix.md`, `source-map.md` | Which evidence references support planning and which questions need qualified review. |

## Evidence Requests To Start This Week

| Recipient | Priority | Ask | Evidence format | Artifact |
| --- | --- | --- | --- | --- |
| Owner/MSP | medium | Confirm the practice profile, owners, review period, and no-PHI evidence-reference boundary. | Reference-only screenshot/export/note in the private binder with owner, date observed, and no PHI or secrets. | packet-manifest.json |
| Owner/MSP | high | Review public-site tracker, TLS, scheduler, intake, and portal observations before the practice relies on patient-facing workflows. | public observation summary; page/workflow label; date observed; owner; vendor/MSP/reviewer note | external-evidence-precheck.md |
| MSP | high | Confirm each high-risk flow owner, channel, BAA need, and reference-only evidence location. | workflow map; secure email policy; shared-drive access review; retention summary; staff guidance | ephi-flow-map.md |
| Owner | high | Separate no-PHI administrative AI use from restricted or prohibited PHI workflows before staff rollout. | AI acceptable-use guidance; vendor terms summary; model-training setting; retention/deletion terms; staff acknowledgement | ai-workflow-review.md |
| Vendor | high | Collect BAA status, SOC 2/HITRUST evidence status, security contact, incident terms, subcontractor posture, and AI/data-use answers. | BAA status; BAA review date; vendor security page; SOC 2 or HITRUST status; incident notification terms; retention/deletion terms | vendor-baa-review.md |
| MSP | high | Export user lists, verify MFA enforcement, and document owner signoff for access and offboarding review. | User list export, admin role list, owner signoff, removed-account notes, and exception sunset dates. | readiness-review.md |
| MSP | high | Run or schedule a restore test and tabletop, then record reference IDs and lessons learned. | Reference-only screenshot/export/note in the private binder with owner, date observed, and no PHI or secrets. | downtime-ransomware-tabletop.md |
| Owner | medium | Review top findings with the owner and assign 30-day remediation owners. | Reference-only screenshot/export/note in the private binder with owner, date observed, and no PHI or secrets. | risk-register.csv |

## Ready-To-Send Messages

Copy, paste, and adapt. All requests are reference-only. No PHI, credentials, or raw files needed.

### Email to MSP

```text
Subject: Quick evidence request for Family Dental Clinic - Velari packet

Hi [MSP Contact],

We are using a Velari Practice Assurance Packet for our 2026 Q2 review. It highlights a few high-priority items where we need reference-only evidence this week:

- MFA enforcement status and user/admin list exports for EHR, billing, email, remote access, and administrator accounts
- Backup scope and last restore-test evidence for critical practice systems
- Downtime workflow or tabletop notes for systems needed during patient care

Please reply with evidence reference IDs, dates observed, owners, scope covered, and any gaps we need to decide on. Keep raw files, screenshots, logs, private URLs, credentials, and sensitive details in our private binder.

Can you send what you have by [date], or suggest a short call if that is easier?

Thanks,
[Your Name]
```

### Email to Vendor

```text
Subject: BAA and security evidence request - Family Dental Clinic

Hi [Vendor Contact],

As part of our 2026 Q2 practice security and vendor review, we need to confirm a few reference-only items for [Vendor Name].

Can you please provide:

- Current BAA status and last review date
- SOC 2, HITRUST, or equivalent security evidence status
- Security contact and incident-notification terms
- Retention/deletion terms and subprocessors or subcontractors
- AI data-use or model-training terms, if applicable

We only need status labels, public/gated proof references, or a short written response. Please do not send PHI, credentials, raw contracts, raw logs, patient screenshots, or private admin links in this thread.

Thank you,
[Your Name] / Family Dental Clinic
```

### Internal Note to Practice Owner

```text
Subject: First actions from the Velari packet

The Velari packet is ready for Family Dental Clinic. The fastest next step is to send the MSP and vendor requests, then track responses by reference ID instead of moving sensitive files around.

This week I recommend we:

- Ask the MSP for MFA, access, backup, restore-test, and downtime evidence
- Ask key vendors for BAA, security evidence status, incident, retention/deletion, and AI data-use answers
- Keep PHI, passwords, raw logs, raw contracts, patient screenshots, and private links out of email and public tools
- Escalate legal/compliance, insurance, incident, or formal risk-assessment questions to the right reviewer

I can send the first requests and collect responses into the evidence tracker.
```

### Optional Note to Reviewer

```text
Subject: Reference-only packet for qualified review - Family Dental Clinic

Hi [Reviewer],

We have a Velari Practice Assurance Packet for Family Dental Clinic's 2026 Q2 review. It is a readiness and evidence-handoff packet, not a formal Security Risk Analysis, audit opinion, legal advice, or insurance advice.

Can you review the packet and flag which vendor, AI, incident, insurance, contract, or formal risk-assessment questions need qualified review before the practice relies on them?

We are keeping raw evidence in a private/offline binder and using reference IDs in the packet. Please do not request PHI, credentials, raw logs, raw contracts, private admin links, or incident-sensitive details in public tools.
```

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
