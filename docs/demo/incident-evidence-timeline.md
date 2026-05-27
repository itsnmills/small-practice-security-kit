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
