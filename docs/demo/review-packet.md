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

## Evidence Closeout Queue

| Item | Lifecycle | Closeout | Owner | Acceptable evidence | Closeout rule |
| --- | --- | --- | --- | --- | --- |
| EHR MFA evidence | Missing | Blocked | MSP Lead | MFA enforcement export; admin screenshot with date observed; covered groups; exceptions; and MSP attestation | Close when mfa enforcement export, admin screenshot with date observed, covered groups, exceptions, and msp attestation are recorded as reference-only evidence. |
| Unique account evidence | Provided | Closed | MSP Lead | User list export; shared-account exception list; owner signoff; and sunset dates | Close when user list export, shared-account exception list, owner signoff, and sunset dates are recorded as reference-only evidence. |
| Quarterly access review evidence | Missing | Needs evidence | MSP Lead | User list export; admin role list; owner signoff; removed-account notes; and exception sunset dates | Close when user list export, admin role list, owner signoff, removed-account notes, and exception sunset dates are recorded as reference-only evidence. |
| Backup restore evidence | Missing | Blocked | MSP Lead | Backup scope summary; restore-test note; date observed; recovery owner; and excluded systems | Close when backup scope summary, restore-test note, date observed, recovery owner, and excluded systems are recorded as reference-only evidence. |
| BAA register evidence | Missing | Blocked | Office Manager | BAA status; review date; vendor security page; SOC 2/HITRUST status; and incident terms | Close when baa status, review date, vendor security page, soc 2/hitrust status, and incident terms are recorded as reference-only evidence. |
| Downtime plan evidence | Missing | Blocked | MSP Lead | Downtime workflow; manual workaround owner; staff acknowledgement; and tabletop attendance | Close when downtime workflow, manual workaround owner, staff acknowledgement, and tabletop attendance are recorded as reference-only evidence. |
| Log review cadence evidence | Missing | Blocked | MSP Lead | Log source list; review cadence record; alert owner; escalation path; and date observed | Close when log source list, review cadence record, alert owner, escalation path, and date observed are recorded as reference-only evidence. |


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

| Flow | Source | Destination | Vendor | ePHI Type | BAA Needed | Risk | Lifecycle | Closeout | Evidence Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FLOW-001 | Patient intake form | Cloud EHR | Example EHR Vendor | demographic and insurance categories | Yes | medium | Requested | Needs evidence | BAA, portal access controls, intake workflow owner |
| FLOW-002 | Cloud EHR | Billing Portal | Example Billing Vendor | billing and payer-submission categories | Yes | high | Requested | Needs evidence | BAA, integration owner, incident notification terms |
| FLOW-003 | Staff email | External specialist | Email provider | referral attachments | Yes | high | Requested | Needs evidence | secure email policy, forwarding review, staff training |
| FLOW-004 | Dental Imaging Workstation | Shared Drive | Workspace Provider | image export categories | Yes | high | Requested | Needs evidence | export procedure, shared-folder access review, backup scope reference |
| FLOW-005 | Front desk notes | General AI Assistant | General AI Assistant Vendor | no patient data approved; generic administrative drafting only | No | medium | Provided | Closed | AI acceptable-use guidance and staff acknowledgement |
| FLOW-006 | Provider conversation | AI Scribe Pilot | Example AI Scribe Vendor | potential visit-summary categories if approved after vendor review | Yes | high | Requested | Needs evidence | BAA, retention terms, model-training terms, human review approval |

## Traceability Summary

| Flow | Trace | Downstream artifacts | Closeout rule |
| --- | --- | --- | --- |
| FLOW-001 | flows FLOW-001; systems Cloud EHR; vendors Example EHR Vendor | ephi-flow-map.md; evidence-binder-index.md | Close when owner, vendor path, BAA need, access/retention control, and private evidence reference are recorded. |
| FLOW-002 | flows FLOW-002; systems Cloud EHR, Billing Portal; vendors Example Billing Vendor | ephi-flow-map.md; evidence-binder-index.md | Close when owner, vendor path, BAA need, access/retention control, and private evidence reference are recorded. |
| FLOW-003 | flows FLOW-003; vendors Email provider | ephi-flow-map.md; evidence-binder-index.md | Close when owner, vendor path, BAA need, access/retention control, and private evidence reference are recorded. |
| FLOW-004 | flows FLOW-004; systems Dental Imaging Workstation, Shared Drive; vendors Workspace Provider | ephi-flow-map.md; evidence-binder-index.md | Close when owner, vendor path, BAA need, access/retention control, and private evidence reference are recorded. |
| FLOW-005 | flows FLOW-005; systems General AI Assistant; vendors General AI Assistant Vendor | ephi-flow-map.md; evidence-binder-index.md | Close when owner, vendor path, BAA need, access/retention control, and private evidence reference are recorded. |
| FLOW-006 | flows FLOW-006; systems AI Scribe Pilot; vendors Example AI Scribe Vendor | ephi-flow-map.md; evidence-binder-index.md | Close when owner, vendor path, BAA need, access/retention control, and private evidence reference are recorded. |


---

# Vendor and BAA Review

| Vendor | Service | Touches ePHI? | BAA Status | AI Training Use | SOC 2 Status | HITRUST Status | Subcontractors | Incident Terms | Risk | Lifecycle | Closeout | Trace |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Example EHR Vendor | EHR hosting and support | Yes | signed | not reviewed | not provided | not provided | partial | 24 hours in contract | medium | Provided | Ready for review | flows FLOW-001; systems Cloud EHR; vendors Example EHR Vendor |
| Example Billing Vendor | Claims and billing | Yes | missing review date | unknown | not provided | not provided | unknown | unknown | high | Stale | Blocked | flows FLOW-002; systems Billing Portal; vendors Example Billing Vendor |
| Workspace Provider | Email, calendar, and shared drive | Yes | signed | not reviewed for add-on AI features | not provided | not provided | published list not reviewed | portal notice terms need review | medium | Provided | Ready for review | flows FLOW-004; systems Shared Drive; vendors Workspace Provider |
| Example Imaging Vendor | Dental imaging software and support | Yes | unknown | not applicable in current deployment | not provided | not provided | unknown | unknown | high | Missing | Blocked | systems Dental Imaging Workstation; vendors Example Imaging Vendor |
| General AI Assistant Vendor | Administrative drafting assistant | No | not needed for no-PHI demo workflow | consumer/default settings not approved for sensitive data | not applicable | not applicable | not reviewed | not reviewed | medium | Not applicable | Not applicable | flows FLOW-005; systems General AI Assistant; vendors General AI Assistant Vendor |
| Example AI Scribe Vendor | AI scribe pilot | Yes | requested | unknown | not provided | not provided | unknown | unknown | high | Requested | Needs evidence | flows FLOW-006; systems AI Scribe Pilot; vendors Example AI Scribe Vendor |

## Next Evidence

- Confirm BAA review date for each vendor touching ePHI.
- Record SOC 2 and HITRUST evidence status as provided, not provided, absent, or not applicable; do not infer attestations from marketing pages.
- Record incident notification terms.
- Ask AI/data-use questions for any vendor using automation or model training.


---

# AI Workflow Review

| Workflow | Use | Data Used | Vendor | Decision | Lifecycle | Closeout | Trace | Evidence Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Marketing email drafting | Draft generic outreach copy | No patient data | General AI assistant | allowed | Closed | Closed | flows FLOW-005; vendors General AI assistant; workflows Marketing email drafting | staff guidance and prohibited data examples |
| Insurance renewal questionnaire drafting | Draft plain-language answers for cyber insurance renewal questions | Control status summaries and evidence reference IDs only | General AI assistant | allowed | Closed | Closed | flows FLOW-005; vendors General AI assistant; workflows Insurance renewal questionnaire drafting | owner review and no-PHI/no-secret prompt guidance |
| Billing appeal drafter | Draft payer appeal language | billing scenario summary; real patient-level details are not approved | General AI assistant | restricted | Requested | Needs evidence | flows FLOW-005; vendors General AI assistant; workflows Billing appeal drafter | BAA review, redaction workflow, owner approval |
| AI scribe pilot | Draft visit summaries after provider review | potential PHI if enabled after vendor approval | Example AI Scribe Vendor | restricted | Requested | Needs evidence | flows FLOW-006; vendors Example AI Scribe Vendor; workflows AI scribe pilot | BAA, retention/model-training terms, human review workflow, pilot owner signoff |
| Paste patient-level note into public chatbot | Summarize patient-level documentation | patient-level documentation category | Public chatbot | prohibited | Blocked | Blocked | vendors Public chatbot; workflows Paste patient-level note into public chatbot | training reminder and AI use policy |

## Rules of Thumb

- Allowed: generic administrative drafting with no patient or clinical details.
- Restricted: workflows involving claim, treatment, billing, or operationally sensitive data.
- Prohibited: pasting patient-level notes or identifiers into tools without approved safeguards and a reviewed vendor relationship.


---

# Downtime and Ransomware Tabletop

Downtime plan status: **not documented**

Restore test status: **not recorded**

Tabletop status: **not run**

| Critical System | Downtime Owner | Lifecycle | Closeout | Trace | Closeout rule |
| --- | --- | --- | --- | --- | --- |
| Cloud EHR | MSP Lead | Missing | Blocked | flows FLOW-001, FLOW-002; systems Cloud EHR | Close when downtime owner, manual workaround, backup scope, restore-test evidence, and tabletop notes are recorded. |
| Billing Portal | MSP Lead | Missing | Blocked | flows FLOW-002; systems Billing Portal | Close when downtime owner, manual workaround, backup scope, restore-test evidence, and tabletop notes are recorded. |
| Phones | MSP Lead | Missing | Blocked | systems Phones | Close when downtime owner, manual workaround, backup scope, restore-test evidence, and tabletop notes are recorded. |
| Shared Drive | MSP Lead | Missing | Blocked | flows FLOW-004; systems Shared Drive | Close when downtime owner, manual workaround, backup scope, restore-test evidence, and tabletop notes are recorded. |

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

# Incident Evidence Timeline

Scenario: **Suspicious login and EHR downtime tabletop**

Type: **tabletop**

Synthetic scenario: staff notice an unusual admin login alert shortly before the Cloud EHR becomes unavailable. The practice needs to keep care moving, preserve evidence references, and separate technical containment from qualified breach, insurance, contract, and regulatory decisions.

## Evidence Boundary

Use categories, owners, timestamps, and evidence reference IDs only. Do not include PHI, patient identifiers, screenshots, raw logs, private URLs, credentials, vendor contracts, or real incident details.

## Timeline

| Time | Phase | Sanitized event | System/workflow | Owner | Evidence ref | Decision gate | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T+00 | Detection | Front desk reports the Cloud EHR is unavailable and the owner sees a suspicious admin-login alert category. | Cloud EHR; Email | Office Manager | restricted-evidence/incidents/tabletop-detection-note | Is there active compromise, patient-care disruption, or vendor notice? | requested |
| T+15 | Continuity | Practice switches to downtime workflow while the MSP checks whether the issue affects EHR, email, billing, or shared drive access. | Cloud EHR; Billing Portal; Shared Drive | Office Manager | restricted-evidence/incidents/downtime-workflow-reference | Which manual workflow keeps care moving without creating new unsafe data copies? | requested |
| T+30 | Containment | MSP confirms account, device, vendor-support, and remote-access categories that need review or containment. | Cloud EHR; Workspace Provider | MSP Lead | restricted-evidence/incidents/containment-action-reference | Which accounts, tokens, sessions, or vendor paths should be disabled or reviewed first? | requested |
| T+60 | Qualified review | Owner parks breach-notification, insurance, contract notice, and regulatory questions for qualified reviewers. | Cloud EHR; Example EHR Vendor | Qualified reviewer | restricted-evidence/incidents/qualified-review-queue | Which facts and private evidence references must be prepared for counsel, insurer, vendor, or incident responder? | requested |
| T+1 business day | After-action | Practice assigns remediation owners for access review, MFA evidence, restore-test proof, vendor incident terms, and staff communication. | Cloud EHR; Billing Portal; Shared Drive | Practice Owner | restricted-evidence/incidents/after-action-items | Which improvements must be completed in the next 30 days before the tabletop can be closed? | requested |

## Guided Phase Checklist

| Phase | Owner lane | Source alignment | Goal | Do now | Evidence required | Completion criteria | Escalation triggers | Complete? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Detection | Owner/MSP | NIST CSF 2.0 Detect: find and analyze possible attacks or compromises; HIPAA Security Rule 45 CFR 164.308(a)(6): identify and respond to suspected or known incidents; CISA playbook pattern: collect and preserve enough data to verify, categorize, prioritize, and report internally | Confirm whether the concern is a normal operational issue, a security event, or something that needs immediate containment without copying sensitive evidence into the kit. | Record the concern category, reporter role, time observed, and affected system category.; Assign a practice owner and technical owner before anyone starts changing systems.; Create a private evidence reference outside the public packet for screenshots, alerts, or logs.; Check whether patient-care operations, admin access, backups, or vendor access are affected. | private detection note reference; owner or MSP observation reference; affected system category | concern category recorded; initial owner assigned; private evidence reference created; escalation trigger reviewed | active unauthorized access; ransomware indicator; patient-care disruption; lost device with patient-data access; vendor breach/security notice | No |
| Continuity | Practice owner/Office manager | NIST CSF 2.0 Recover: restore assets and operations affected by an incident; HIPAA Security Rule contingency planning: continue critical business processes while protecting ePHI; HICP small-organization reality: small practices often rely on simple downtime workflows and outsourced IT | Keep care and core operations moving with the least risky manual workflow while the technical owner investigates. | Name the critical workflow affected: scheduling, chart access, billing, phones, imaging, prescribing, or patient messaging.; Choose the approved manual workaround and owner.; Record where the downtime workflow lives by reference ID, not by copying patient-level data.; Set a check-in time for the owner and MSP to reassess continuity risk. | downtime workflow reference; critical-system owner; patient-care continuity decision reference | manual workflow selected; critical systems listed; owner approval reference recorded; unsafe data-copy risk reviewed | care cannot continue safely; communications unavailable; backup or restore path unknown; multiple critical systems unavailable | No |
| Containment | MSP/technical owner | NIST CSF 2.0 Respond: take action regarding a detected incident; CISA ransomware response guidance: determine impacted systems and isolate them when needed; CISA playbook containment: reduce immediate impact while considering evidence preservation | Limit further harm while preserving the facts a qualified responder, insurer, vendor, or reviewer may need later. | Assign the technical owner and record the containment action category.; Confirm whether the suspected path is account, endpoint, email, EHR, vendor-support, network, backup, or shared-drive related.; Record any isolation or access action by ticket/reference ID.; Preserve private evidence before destructive remediation whenever qualified guidance is needed. | containment action reference; affected account/system category; MSP or vendor ticket reference | technical owner assigned; containment action category recorded; private evidence reference recorded; qualified-review need assessed | active compromise continues; ransomware spreads; admin account suspected; backup system affected; vendor support path uncertain | No |
| Qualified review | Qualified reviewer | HIPAA Security Rule: respond, mitigate where practicable, and document outcomes; NIST SP 800-61 Rev. 3: legal, privacy, technology, leadership, and third parties may all have response roles; HHS Security Rule summary: safeguards are scalable and should fit size, capabilities, cost, and risk | Park legal, regulatory, insurance, contract, and formal reporting questions for qualified reviewers while the practice keeps the fact packet clean. | Name the reviewer lane: counsel, compliance, insurer, incident responder, vendor, or regulator support.; List decision questions without answering them inside the kit.; Prepare private evidence references and the sanitized timeline.; Record who is allowed to communicate externally and what boundary they must follow. | qualified-review queue reference; decision category; reviewer owner; private evidence reference list | qualified reviewer identified; parked decisions listed; private evidence references ready; owner communication boundary confirmed | possible reportability question; insurance notice question; contract notice question; vendor or regulator communication needed | No |
| After-action | Practice owner/MSP | NIST CSF 2.0 Identify Improvement: feed lessons into future governance, protection, detection, response, and recovery; NIST CSF 2.0 Recover: complete documentation and confirm return to normal operations based on criteria; HICP Technical Volume 1: practical, low-cost cyber hygiene and MSP-supported improvements matter for small practices | Convert the incident or tabletop into closed owners, due dates, and evidence refreshes instead of vague lessons. | Assign no more than five high-value improvements with owners and dates.; Tie each improvement to an evidence reference needed for closeout.; Schedule a follow-up review and tabletop refresh.; Update staff guidance, vendor questions, access review, backup proof, or downtime workflow as needed. | after-action owner; priority; due date; closure evidence reference | top fixes assigned; evidence needed for closure listed; owner review scheduled; next tabletop improvement identified | high-priority fix has no owner; restore evidence missing; access review missing; vendor terms unresolved | No |

## Owner/MSP Call Sheet

| Phase | Owner question | Staff script | Ask MSP/vendor | Do not record |
| --- | --- | --- | --- | --- |
| Detection | What did we notice, who owns the next decision, and where is the private evidence reference? | Thanks for reporting this. Do not forward screenshots or patient details. Tell the owner which system or workflow category is affected and when you noticed it. | Can you confirm whether this is active unauthorized access, service outage, malware, or a false alarm?; Which systems, accounts, devices, integrations, or vendor-support paths should be reviewed first?; What private ticket or evidence reference should the practice record? | patient names or identifiers; screenshots; raw logs; credentials or MFA codes; private URLs |
| Continuity | Can the practice continue safely, and which workflow is approved until systems return? | Use the approved downtime workflow only. Do not create new spreadsheets, photos, exports, or message threads unless the owner has approved the method. | Which services are degraded, unavailable, or still safe to use?; What restoration estimate or vendor-status reference can be shared with the owner?; What should staff avoid doing until restoration is confirmed? | patient schedule details; patient message contents; clinical note text; billing claim details |
| Containment | What can be isolated, disabled, reset, or monitored now without destroying evidence or disrupting care unnecessarily? | Stop using the affected system or account if the owner or MSP says to. Do not wipe devices, reinstall software, delete messages, or clear alerts. | Which systems or accounts are believed impacted, and which are confirmed clean enough to keep operating?; Should any system be isolated from the network, have sessions revoked, or have privileged access rotated?; Should forensic images, memory capture, log export, or vendor evidence be preserved by a qualified party before rebuilding? | user passwords; session tokens; raw firewall logs; endpoint screenshots; private IPs or admin URLs |
| Qualified review | Which decisions are outside the practice owner's lane, and what facts must be handed to the reviewer? | Do not tell patients, vendors, or public channels anything beyond an owner-approved operational update. Route formal notice questions to the assigned reviewer. | Which facts are confirmed versus suspected?; Which private evidence references support system access, availability, containment, and recovery?; What vendor, contract, or insurance notice terms may affect the review path? | legal conclusions; reportability conclusions; patient details; raw incident evidence |
| After-action | What has to change before we can say this practice is safer than before the scenario? | The goal is to fix workflows, training, vendor terms, and evidence gaps. Do not blame individuals in the packet. | Which control would have reduced the incident fastest: MFA, access review, backup test, log alert, endpoint control, vendor terms, or downtime process?; Which evidence can be refreshed in the next 30 days?; Which issue needs budget, vendor change, or owner approval? | patient examples; raw logs; credential details; legal conclusions |

## Decision Gates

| Gate | Owner | Trigger | Action |
| --- | --- | --- | --- |
| Active compromise escalation | MSP Lead | Ransomware indicator, active unauthorized access, lost device, vendor breach notice, or patient-care disruption. | Escalate to qualified incident response and preserve private evidence references. |
| Breach or notice review | Qualified reviewer | Possible impermissible access, disclosure, contract notice, insurance notice, or regulatory reporting question. | Park for qualified legal, compliance, insurer, vendor, or incident-response review. |
| Operational continuity | Office Manager | EHR, billing, phones, shared drive, or messaging portal unavailable during patient-care operations. | Use documented downtime workflow and record reference-only evidence of decisions and owner approvals. |

## Handoff Rules

- Separate technical containment from breach-notification, insurance, contract, regulatory, and legal/compliance decisions.
- Preserve private evidence references without copying raw evidence into the public packet.
- Escalate active compromise, ransomware, unauthorized access, lost device, vendor breach notice, or patient-care disruption to qualified incident response.
- Use this timeline to prepare the qualified-review conversation; do not use it to decide reportability.

## Source Basis

- NIST SP 800-61 Rev. 3: incident response should support preparation, detection, response, recovery, and continuous improvement across cybersecurity risk management.
- HIPAA Security Rule 45 CFR 164.308(a)(6): security incident procedures should support response, mitigation where practicable, and incident documentation.
- HHS HICP Technical Volume 1: small healthcare organizations often need practical, MSP-supported incident response workflows.
- CISA ransomware and incident playbooks: isolate impacted systems when needed, preserve evidence, coordinate response roles, and document actions.


---

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


---

# Evidence Binder Index

This is a lifecycle index for reference-only evidence. Store raw proof in the private/offline binder and keep this packet limited to owners, dates, status labels, trace context, and safe evidence references.

## Lifecycle Summary

- Total evidence rows: 46
- Blocked: 13
- Needs evidence: 22
- Ready for review: 2
- Closed: 8
- Traceable to ePHI flows: 23

## Evidence Lifecycle

| Evidence ID | Area | Lifecycle | Closeout | Owner | Trace | Acceptable evidence | Next action | Artifacts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVID-ACCESS-Q2 | access | Partial | Needs evidence | Office Manager | EVID-ACCESS-Q2 | Quarterly access review export placeholder; date observed; owner signoff; scope covered; exception note | Collect or refresh the reference-only evidence and record owner/date/scope without uploading raw evidence. | evidence-binder-index.md |
| EVID-BACKUP-RESTORE | backup | Stale | Blocked | MSP Lead | EVID-BACKUP-RESTORE | Backup restore test record placeholder; date observed; owner signoff; scope covered; exception note | Collect or refresh the reference-only evidence and record owner/date/scope without uploading raw evidence. | evidence-binder-index.md |
| EVID-CYBER-INSURANCE | insurance | Requested | Needs evidence | Practice Owner | EVID-CYBER-INSURANCE | Cyber insurance renewal evidence list; date observed; owner signoff; scope covered; exception note | Collect or refresh the reference-only evidence and record owner/date/scope without uploading raw evidence. | evidence-binder-index.md |
| EVID-AI-GUIDANCE | ai | Requested | Needs evidence | Office Manager | EVID-AI-GUIDANCE | Staff AI acceptable-use acknowledgement; date observed; owner signoff; scope covered; exception note | Collect or refresh the reference-only evidence and record owner/date/scope without uploading raw evidence. | evidence-binder-index.md |
| EVID-VENDOR-BAA-GAPS | vendor | Requested | Needs evidence | Office Manager | EVID-VENDOR-BAA-GAPS | Vendor BAA and incident terms follow-up list; date observed; owner signoff; scope covered; exception note | Collect or refresh the reference-only evidence and record owner/date/scope without uploading raw evidence. | evidence-binder-index.md |
| READINESS-MFA-EMAIL | access___mfa | Provided | Closed | Office Manager | mfa_email | MFA policy export; covered groups; exceptions; and date observed | Keep this evidence on a quarterly refresh cadence. | readiness-review.md |
| READINESS-MFA-EHR | access___mfa | Missing | Blocked | MSP Lead | mfa_ehr | MFA enforcement export; admin screenshot with date observed; covered groups; exceptions; and MSP attestation | Request proof, document exceptions, and assign an owner before closeout. | owner-msp-handoff.md; readiness-review.md |
| READINESS-UNIQUE-ACCOUNTS | access_review | Provided | Closed | MSP Lead | unique_accounts | User list export; shared-account exception list; owner signoff; and sunset dates | Keep this evidence on a quarterly refresh cadence. | owner-msp-handoff.md; readiness-review.md |
| READINESS-ACCESS-REVIEW | access_review | Missing | Needs evidence | MSP Lead | quarterly_access_review | User list export; admin role list; owner signoff; removed-account notes; and exception sunset dates | Request proof, document exceptions, and assign an owner before closeout. | owner-msp-handoff.md; readiness-review.md |
| READINESS-BACKUP-RESTORE | backup___downtime | Missing | Blocked | MSP Lead | tested_backups | Backup scope summary; restore-test note; date observed; recovery owner; and excluded systems | Request proof, document exceptions, and assign an owner before closeout. | downtime-ransomware-tabletop.md; readiness-review.md |
| READINESS-VENDOR-INVENTORY | vendor___baa | Provided | Closed | Office Manager | vendor_inventory | Vendor register; owner; service; ePHI touch status; BAA status; and review date | Keep this evidence on a quarterly refresh cadence. | vendor-baa-review.md; readiness-review.md |
| READINESS-BAA-REGISTER | vendor___baa | Missing | Blocked | Office Manager | baa_register | BAA status; review date; vendor security page; SOC 2/HITRUST status; and incident terms | Request proof, document exceptions, and assign an owner before closeout. | vendor-baa-review.md; readiness-review.md |
| READINESS-INCIDENT-CONTACTS | incident_readiness | Provided | Closed | Office Manager | incident_contact_list | Incident contact list; MSP contact; vendor contact; qualified-review contact; and review date | Keep this evidence on a quarterly refresh cadence. | incident-decision-log.md; readiness-review.md |
| READINESS-DOWNTIME-PLAN | downtime | Missing | Blocked | MSP Lead | downtime_plan | Downtime workflow; manual workaround owner; staff acknowledgement; and tabletop attendance | Request proof, document exceptions, and assign an owner before closeout. | downtime-ransomware-tabletop.md; readiness-review.md |
| READINESS-TRAINING | workforce | Provided | Closed | Office Manager | security_training_current | Training roster; acknowledgement date; no-PHI AI guidance; and exception list | Keep this evidence on a quarterly refresh cadence. | readiness-review.md |
| READINESS-LOG-REVIEW | monitoring | Missing | Blocked | MSP Lead | log_review_cadence | Log source list; review cadence record; alert owner; escalation path; and date observed | Request proof, document exceptions, and assign an owner before closeout. | owner-msp-handoff.md; readiness-review.md |
| FLOW-001 | ephi_flow | Requested | Needs evidence | MSP or workflow owner | flows FLOW-001; systems Cloud EHR; vendors Example EHR Vendor | BAA; portal access controls; intake workflow owner | Confirm the flow owner, channel, BAA need, and private evidence reference. | ephi-flow-map.md; evidence-binder-index.md |
| FLOW-002 | ephi_flow | Requested | Needs evidence | MSP or workflow owner | flows FLOW-002; systems Cloud EHR, Billing Portal; vendors Example Billing Vendor | BAA; integration owner; incident notification terms | Confirm the flow owner, channel, BAA need, and private evidence reference. | ephi-flow-map.md; evidence-binder-index.md |
| FLOW-003 | ephi_flow | Requested | Needs evidence | MSP or workflow owner | flows FLOW-003; vendors Email provider | secure email policy; forwarding review; staff training | Confirm the flow owner, channel, BAA need, and private evidence reference. | ephi-flow-map.md; evidence-binder-index.md |
| FLOW-004 | ephi_flow | Requested | Needs evidence | MSP or workflow owner | flows FLOW-004; systems Dental Imaging Workstation, Shared Drive; vendors Workspace Provider | export procedure; shared-folder access review; backup scope reference | Confirm the flow owner, channel, BAA need, and private evidence reference. | ephi-flow-map.md; evidence-binder-index.md |
| FLOW-005 | ephi_flow | Provided | Closed | MSP or workflow owner | flows FLOW-005; systems General AI Assistant; vendors General AI Assistant Vendor | AI acceptable-use guidance and staff acknowledgement | Confirm the flow owner, channel, BAA need, and private evidence reference. | ephi-flow-map.md; evidence-binder-index.md |
| FLOW-006 | ephi_flow | Requested | Needs evidence | MSP or workflow owner | flows FLOW-006; systems AI Scribe Pilot; vendors Example AI Scribe Vendor | BAA; retention terms; model-training terms; human review approval | Confirm the flow owner, channel, BAA need, and private evidence reference. | ephi-flow-map.md; evidence-binder-index.md |
| VENDOR-EXAMPLE_EHR_VENDOR | vendor_baa | Provided | Ready for review | Practice manager | flows FLOW-001; systems Cloud EHR; vendors Example EHR Vendor | BAA status; BAA review date; SOC 2 or HITRUST status; incident notification terms; retention/deletion terms; AI/data-use response | Request vendor BAA, incident, subcontractor, retention/deletion, and AI/data-use answers without uploading raw contracts. | vendor-baa-review.md; evidence-binder-index.md |
| VENDOR-EXAMPLE_BILLING_VENDOR | vendor_baa | Stale | Blocked | Practice manager | flows FLOW-002; systems Billing Portal; vendors Example Billing Vendor | BAA status; BAA review date; SOC 2 or HITRUST status; incident notification terms; retention/deletion terms; AI/data-use response | Request vendor BAA, incident, subcontractor, retention/deletion, and AI/data-use answers without uploading raw contracts. | vendor-baa-review.md; evidence-binder-index.md |
| VENDOR-WORKSPACE_PROVIDER | vendor_baa | Provided | Ready for review | Practice manager | flows FLOW-004; systems Shared Drive; vendors Workspace Provider | BAA status; BAA review date; SOC 2 or HITRUST status; incident notification terms; retention/deletion terms; AI/data-use response | Request vendor BAA, incident, subcontractor, retention/deletion, and AI/data-use answers without uploading raw contracts. | vendor-baa-review.md; evidence-binder-index.md |
| VENDOR-EXAMPLE_IMAGING_VENDOR | vendor_baa | Missing | Blocked | Practice manager | systems Dental Imaging Workstation; vendors Example Imaging Vendor | BAA status; BAA review date; SOC 2 or HITRUST status; incident notification terms; retention/deletion terms; AI/data-use response | Request vendor BAA, incident, subcontractor, retention/deletion, and AI/data-use answers without uploading raw contracts. | vendor-baa-review.md; evidence-binder-index.md |
| VENDOR-GENERAL_AI_ASSISTANT_VENDOR | vendor_baa | Not applicable | Not applicable | Practice manager | flows FLOW-005; systems General AI Assistant; vendors General AI Assistant Vendor | BAA status; BAA review date; SOC 2 or HITRUST status; incident notification terms; retention/deletion terms; AI/data-use response | Request vendor BAA, incident, subcontractor, retention/deletion, and AI/data-use answers without uploading raw contracts. | vendor-baa-review.md; evidence-binder-index.md |
| VENDOR-EXAMPLE_AI_SCRIBE_VENDOR | vendor_baa | Requested | Needs evidence | Practice manager | flows FLOW-006; systems AI Scribe Pilot; vendors Example AI Scribe Vendor | BAA status; BAA review date; SOC 2 or HITRUST status; incident notification terms; retention/deletion terms; AI/data-use response | Request vendor BAA, incident, subcontractor, retention/deletion, and AI/data-use answers without uploading raw contracts. | vendor-baa-review.md; evidence-binder-index.md |
| AI-MARKETING_EMAIL_DRAFTING | ai_workflow | Closed | Closed | Office Manager | flows FLOW-005; vendors General AI assistant; workflows Marketing email drafting | staff guidance and prohibited data examples | Keep the workflow no-PHI or restricted until terms, retention, model-training use, and human review are documented. | ai-workflow-review.md; evidence-binder-index.md |
| AI-INSURANCE_RENEWAL_QUESTIONNAIRE_DRAFTING | ai_workflow | Closed | Closed | Office Manager | flows FLOW-005; vendors General AI assistant; workflows Insurance renewal questionnaire drafting | owner review and no-PHI/no-secret prompt guidance | Keep the workflow no-PHI or restricted until terms, retention, model-training use, and human review are documented. | ai-workflow-review.md; evidence-binder-index.md |
| AI-BILLING_APPEAL_DRAFTER | ai_workflow | Requested | Needs evidence | Office Manager | flows FLOW-005; vendors General AI assistant; workflows Billing appeal drafter | BAA review; redaction workflow; owner approval | Keep the workflow no-PHI or restricted until terms, retention, model-training use, and human review are documented. | ai-workflow-review.md; evidence-binder-index.md |
| AI-AI_SCRIBE_PILOT | ai_workflow | Requested | Needs evidence | Office Manager | flows FLOW-006; vendors Example AI Scribe Vendor; workflows AI scribe pilot | BAA; retention/model-training terms; human review workflow; pilot owner signoff | Keep the workflow no-PHI or restricted until terms, retention, model-training use, and human review are documented. | ai-workflow-review.md; evidence-binder-index.md |
| AI-PASTE_PATIENT_LEVEL_NOTE_INTO_PUBLIC_CHATBOT | ai_workflow | Blocked | Blocked | Office Manager | vendors Public chatbot; workflows Paste patient-level note into public chatbot | training reminder and AI use policy | Keep the workflow no-PHI or restricted until terms, retention, model-training use, and human review are documented. | ai-workflow-review.md; evidence-binder-index.md |
| DOWNTIME-CLOUD_EHR | downtime | Missing | Blocked | MSP Lead | flows FLOW-001, FLOW-002; systems Cloud EHR | downtime workflow; manual workaround owner; backup scope; restore-test note; tabletop attendance | Assign downtime owner, document manual workaround, and record restore-test/tabletop evidence references. | downtime-ransomware-tabletop.md; incident-evidence-timeline.md; evidence-binder-index.md |
| DOWNTIME-BILLING_PORTAL | downtime | Missing | Blocked | MSP Lead | flows FLOW-002; systems Billing Portal | downtime workflow; manual workaround owner; backup scope; restore-test note; tabletop attendance | Assign downtime owner, document manual workaround, and record restore-test/tabletop evidence references. | downtime-ransomware-tabletop.md; incident-evidence-timeline.md; evidence-binder-index.md |
| DOWNTIME-PHONES | downtime | Missing | Blocked | MSP Lead | systems Phones | downtime workflow; manual workaround owner; backup scope; restore-test note; tabletop attendance | Assign downtime owner, document manual workaround, and record restore-test/tabletop evidence references. | downtime-ransomware-tabletop.md; incident-evidence-timeline.md; evidence-binder-index.md |
| DOWNTIME-SHARED_DRIVE | downtime | Missing | Blocked | MSP Lead | flows FLOW-004; systems Shared Drive | downtime workflow; manual workaround owner; backup scope; restore-test note; tabletop attendance | Assign downtime owner, document manual workaround, and record restore-test/tabletop evidence references. | downtime-ransomware-tabletop.md; incident-evidence-timeline.md; evidence-binder-index.md |
| INC-TIMELINE-001 | incident_timeline | Requested | Needs evidence | Office Manager | flows FLOW-001, FLOW-002; systems Cloud EHR, Email | timeline event category; owner; timestamp or sequence marker; private evidence reference; decision gate | Preserve reference-only event order and route qualified decisions to the right reviewer. | incident-evidence-timeline.md; incident-after-action-report.md; evidence-binder-index.md |
| INC-TIMELINE-002 | incident_timeline | Requested | Needs evidence | Office Manager | flows FLOW-001, FLOW-002, FLOW-004; systems Cloud EHR, Billing Portal, Shared Drive | timeline event category; owner; timestamp or sequence marker; private evidence reference; decision gate | Preserve reference-only event order and route qualified decisions to the right reviewer. | incident-evidence-timeline.md; incident-after-action-report.md; evidence-binder-index.md |
| INC-TIMELINE-003 | incident_timeline | Requested | Needs evidence | MSP Lead | flows FLOW-001, FLOW-002; systems Cloud EHR, Workspace Provider | timeline event category; owner; timestamp or sequence marker; private evidence reference; decision gate | Preserve reference-only event order and route qualified decisions to the right reviewer. | incident-evidence-timeline.md; incident-after-action-report.md; evidence-binder-index.md |
| INC-TIMELINE-004 | incident_timeline | Requested | Needs evidence | Qualified reviewer | flows FLOW-001, FLOW-002; systems Cloud EHR, Example EHR Vendor | timeline event category; owner; timestamp or sequence marker; private evidence reference; decision gate | Preserve reference-only event order and route qualified decisions to the right reviewer. | incident-evidence-timeline.md; incident-after-action-report.md; evidence-binder-index.md |
| INC-TIMELINE-005 | incident_timeline | Requested | Needs evidence | Practice Owner | flows FLOW-001, FLOW-002, FLOW-004; systems Cloud EHR, Billing Portal, Shared Drive | timeline event category; owner; timestamp or sequence marker; private evidence reference; decision gate | Preserve reference-only event order and route qualified decisions to the right reviewer. | incident-evidence-timeline.md; incident-after-action-report.md; evidence-binder-index.md |
| INC-AA-001 | incident_after_action | Requested | Needs evidence | MSP Lead | INC-AA-001 | Admin settings export reference; access review reference; session reset reference; and owner signoff. | Assign owner, due date, evidence reference, and reviewer lane before closing the after-action item. | incident-after-action-report.md; incident-evidence-timeline.md; evidence-binder-index.md |
| INC-AA-002 | incident_after_action | Requested | Needs evidence | Office Manager | INC-AA-002 | Downtime workflow reference; staff acknowledgement reference; and tabletop attendance reference. | Assign owner, due date, evidence reference, and reviewer lane before closing the after-action item. | incident-after-action-report.md; incident-evidence-timeline.md; evidence-binder-index.md |
| INC-AA-003 | incident_after_action | Requested | Needs evidence | Practice Owner | INC-AA-003 | Vendor terms reference; security contact reference; BAA review date; and qualified-review notes. | Assign owner, due date, evidence reference, and reviewer lane before closing the after-action item. | incident-after-action-report.md; incident-evidence-timeline.md; evidence-binder-index.md |
| INC-AA-004 | incident_after_action | Requested | Needs evidence | MSP Lead | INC-AA-004 | Restore-test record reference; backup-scope reference; and exception list. | Assign owner, due date, evidence reference, and reviewer lane before closing the after-action item. | incident-after-action-report.md; incident-evidence-timeline.md; evidence-binder-index.md |


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

## Closeout Gates

| Evidence | Closeout | Owner | Trace | Next action |
| --- | --- | --- | --- | --- |
| EVID-ACCESS-Q2 | Needs evidence | Office Manager | EVID-ACCESS-Q2 | Collect or refresh the reference-only evidence and record owner/date/scope without uploading raw evidence. |
| EVID-BACKUP-RESTORE | Blocked | MSP Lead | EVID-BACKUP-RESTORE | Collect or refresh the reference-only evidence and record owner/date/scope without uploading raw evidence. |
| EVID-CYBER-INSURANCE | Needs evidence | Practice Owner | EVID-CYBER-INSURANCE | Collect or refresh the reference-only evidence and record owner/date/scope without uploading raw evidence. |
| EVID-AI-GUIDANCE | Needs evidence | Office Manager | EVID-AI-GUIDANCE | Collect or refresh the reference-only evidence and record owner/date/scope without uploading raw evidence. |
| EVID-VENDOR-BAA-GAPS | Needs evidence | Office Manager | EVID-VENDOR-BAA-GAPS | Collect or refresh the reference-only evidence and record owner/date/scope without uploading raw evidence. |
| READINESS-MFA-EHR | Blocked | MSP Lead | mfa_ehr | Request proof, document exceptions, and assign an owner before closeout. |
| READINESS-ACCESS-REVIEW | Needs evidence | MSP Lead | quarterly_access_review | Request proof, document exceptions, and assign an owner before closeout. |
| READINESS-BACKUP-RESTORE | Blocked | MSP Lead | tested_backups | Request proof, document exceptions, and assign an owner before closeout. |
| READINESS-BAA-REGISTER | Blocked | Office Manager | baa_register | Request proof, document exceptions, and assign an owner before closeout. |
| READINESS-DOWNTIME-PLAN | Blocked | MSP Lead | downtime_plan | Request proof, document exceptions, and assign an owner before closeout. |
| READINESS-LOG-REVIEW | Blocked | MSP Lead | log_review_cadence | Request proof, document exceptions, and assign an owner before closeout. |
| FLOW-001 | Needs evidence | MSP or workflow owner | flows FLOW-001; systems Cloud EHR; vendors Example EHR Vendor | Confirm the flow owner, channel, BAA need, and private evidence reference. |

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
