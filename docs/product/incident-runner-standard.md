# Incident Runner Standard

This standard turns the incident runner from a generic note form into an operational workflow for small healthcare practices. The runner must help a practice owner, office manager, MSP, and qualified reviewers keep care moving, preserve evidence by reference, and avoid making legal or regulatory conclusions inside the kit.

## Source Basis

- NIST SP 800-61 Rev. 3, April 2025: incident response is part of cybersecurity risk management across Govern, Identify, Protect, Detect, Respond, and Recover. Detect, Respond, and Recover drive active incident work; lessons learned feed continuous improvement.
- HIPAA Security Rule, 45 CFR 164.308(a)(6): regulated entities must have security incident procedures, identify and respond to suspected or known security incidents, mitigate harmful effects where practicable, and document incidents and outcomes.
- HHS HICP Technical Volume 1, 2023: small healthcare organizations often lack dedicated IT/security staff and rely on MSPs or vendors; incident response needs simple roles, clear ownership, and practical evidence.
- CISA ransomware and incident playbooks: response workflows should identify impacted systems, isolate where needed, preserve evidence, coordinate internal and external teams, and avoid losing forensic value during containment.

## Product Rules

1. The runner is a sanitized coordination tool, not a substitute for qualified incident response, legal advice, insurance guidance, breach notification review, or a formal Security Risk Analysis.
2. The public packet must store categories, owners, timestamps, decisions, status, and private evidence reference IDs only.
3. The runner must never ask for patient identifiers, screenshots, raw logs, credentials, private URLs, contracts, or real incident-sensitive evidence.
4. Every phase must answer one primary question and end with concrete completion criteria.
5. Every phase must separate owner actions from MSP/vendor questions and qualified-review decisions.
6. Every scenario must create an after-action queue tied to evidence refreshes, not vague lessons.
7. Ransomware, active unauthorized access, lost device with patient-data access, vendor security notice, backup impact, or patient-care disruption must surface as escalation triggers.
8. Completion is not just "notes entered." A phase is complete only when the owner, evidence reference, next action, and escalation review are recorded.

## Phase Model

The local UI should guide one phase at a time so the owner is not presented with a long free-form incident report.

| Phase type | Owner lane | Expected output |
| --- | --- | --- |
| Detection | Owner/MSP | Concern category, affected workflow, owner, private evidence reference, escalation review |
| Triage/scope | MSP/technical owner | Confirmed/unknown scope, checked sources, missing facts, next technical step |
| Containment | MSP/technical owner | Access, endpoint, vendor, backup, or network action category plus private ticket/reference |
| Continuity | Practice owner/office manager | Approved downtime workflow and check-in point |
| Evidence preservation | Owner/MSP | Private evidence index entries, owners, artifact categories, reviewer lane |
| Qualified review | Qualified reviewer | Parked decisions, fact packet, reviewer owner, communication boundary |
| After-action | Practice owner/MSP | Owners, due dates, evidence refreshes, and follow-up review |

## Practice Owner Value

The valuable job is not "write an incident report." The valuable job is helping a practice owner do the next safe thing when they are stressed and under-informed:

- Keep patients moving without creating unsafe data copies.
- Avoid wiping, deleting, forwarding, or pasting evidence into the wrong place.
- Know what to ask the MSP or vendor.
- Know which decisions must be parked for counsel, insurer, compliance, vendor, or a qualified incident responder.
- Leave behind an evidence-backed improvement queue that makes the practice safer after the event.

## Implementation Requirements

- Scenario templates must include `source_alignment`, `plain_english_goal`, `owner_prompt`, `staff_script`, `do_now`, `ask_msp_or_vendor`, `allowed_inputs`, `blocked_inputs`, `evidence_required`, `completion_criteria`, and `escalation_triggers`.
- The browser UI must render phase navigation and one active phase panel.
- Packet output must include the original timeline plus a guided phase checklist and owner/MSP call sheet.
- API save must block sensitive incident content before writing the profile or rebuilding artifacts.
- Tests must prove scenario templates include operational guidance and generated packets include the guided sections.

## References

- NIST SP 800-61 Rev. 3: https://csrc.nist.gov/pubs/sp/800/61/r3/final
- 45 CFR 164.308: https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-C/section-164.308
- HHS HICP Technical Volume 1: https://hhscyber.hhs.gov/Documents/HICP/tech-vol1-508.pdf
- CISA Ransomware Response Checklist: https://www.cisa.gov/ransomware-response-checklist
- CISA Incident and Vulnerability Response Playbooks: https://www.cisa.gov/resources-tools/resources/federal-government-cybersecurity-incident-and-vulnerability-response-playbooks
