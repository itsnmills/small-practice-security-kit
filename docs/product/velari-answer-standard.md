# Velari Answer Standard

## Purpose

Velari converts healthcare security uncertainty into owner, MSP, vendor, and reviewer actions without requiring PHI, enterprise software, or a security team. Every output should become an action packet: plain enough for a practice owner to use, specific enough for an MSP or vendor to answer, and bounded enough for legal/compliance or technical reviewers to assess safely.

Velari outputs are readiness and evidence support tools. They improve workflow review, risk visibility, owner/MSP handoff, public evidence organization, gated proof collection, and professional review routing. They do not make legal, breach, HIPAA, vendor, or AI-production-use determinations.

## Required Finding Fields

Every major finding or action packet must include:

1. Plain-English summary
2. Why it matters
3. Owner lane
4. Recommended question
5. Acceptable evidence
6. Unsafe inputs
7. Priority
8. Timeframe
9. Reviewer needed
10. Next action

## Output Views

- Owner view: the short operational meaning and next owner/MSP handoff.
- MSP view: the technical check, expected evidence support, and remediation owner.
- Vendor view: the exact vendor question and gated proof requested.
- Legal/compliance view: the professional review recommended boundary and any contract or formal assessment question.
- Technical reviewer view: the workflow review, control evidence, missing evidence, or stale evidence to inspect.

## Language Rules

Use these terms:

- readiness
- evidence support
- workflow review
- risk visibility
- owner/MSP handoff
- professional review recommended
- public evidence
- gated proof
- missing evidence
- stale evidence
- action packet

Avoid these claims:

- certified compliant
- guaranteed HIPAA compliance
- legal determination
- breach determination
- vendor approved
- AI tool approved for PHI

## Examples

| Scenario | Plain-English summary | Owner lane | Recommended question | Acceptable evidence | Unsafe inputs | Priority | Timeframe | Reviewer needed | Next action |
|---|---|---|---|---|---|---|---|---|---|
| Missing MFA evidence | MFA evidence for an EHR or remote-access workflow is missing or not recorded. | MSP | Can you provide an MFA enforcement export or screenshot for EHR, billing, email, remote access, admin, and vendor-support accounts? | MFA policy export, admin screenshot with date observed, covered groups, exception list, MSP attestation | Patient names, patient records, credentials, raw logs, private portal links | high | 30_days | MSP, office manager | Request MFA proof, document exceptions, and assign an owner for any missing enforcement. |
| Unknown BAA status | A vendor appears to support a workflow involving patient data, but BAA status or review date is not recorded. | Vendor | Can you confirm whether this vendor stores, processes, transmits, or accesses PHI, whether a BAA is in place, and when it was last reviewed? | BAA status, BAA review date, vendor security page, SOC 2 or HITRUST status, incident notification terms, retention/deletion terms | Patient names, patient records, raw contracts with sensitive details, private portal links, credentials | high | 30_days | Vendor owner, legal/compliance reviewer | Add the vendor to the register, confirm PHI access level, and request BAA/evidence status. |
| AI tool with unclear data-use terms | An AI workflow may receive patient, billing, clinical, credential, or raw evidence details before data-use and human-review terms are clear. | Office manager | Should this workflow remain no-PHI, restricted, or paused until vendor terms, retention, model-training use, and human-review controls are reviewed? | AI acceptable-use guidance, vendor terms summary, model-training setting, retention/deletion terms, staff acknowledgement | Patient notes, claim narratives, credentials, raw contracts, raw logs, screenshots with sensitive data | high | 30_days | Office manager, legal/compliance reviewer, technical reviewer | Keep the workflow no-PHI or restricted, collect gated proof, and route terms to professional review if needed. |
| Stale backup restore evidence | Backup restore evidence is missing or stale for systems needed during patient care. | MSP | Can you provide backup scope, last restore-test date, recovery owner, and a private binder reference ID? | Backup scope summary, restore-test note, date observed, recovery owner, systems excluded from backup | Raw backup data, patient records, screenshots with patient data, credentials, private console links | high | 30_days | MSP, office manager | Run or schedule a restore test and record reference-only evidence. |
| Missing access review | The practice does not have current evidence that user access was reviewed for EHR, billing, email, remote access, or admin roles. | MSP | Can you provide user list exports, admin role lists, shared-account exceptions, and owner signoff for access review? | User list export, admin role list, owner signoff, removed-account note, exception sunset date | Patient records, credentials, raw logs, private portal links, screenshots with patient data | medium | 60_days | MSP, office manager | Run the access review, remove or document exceptions, and store evidence references. |
| Patient data in email/shared drives | Patient-data workflows may be happening in email or shared drives without a clear owner, retention path, or access review. | Office manager | Which email or shared-drive workflows handle patient data, who owns them, and what evidence shows access, retention, and secure sharing controls? | Workflow map, secure email policy, shared-drive access review, retention summary, staff guidance | Patient names, clinical notes, claim narratives, shared-drive private URLs, screenshots with sensitive data | high | 30_days | Office manager, MSP, legal/compliance reviewer | Map the workflow, confirm the owner/MSP handoff, and collect reference-only evidence. |

## Safety Boundary

Do not request PHI, credentials, private URLs, raw logs, raw contracts, patient screenshots, or patient examples. Ask for evidence reference IDs, owners, dates observed, status labels, and short summaries. Use public evidence only when it is intentionally public; use gated proof and professional review when evidence is private, contractual, incident-sensitive, or legally meaningful.
