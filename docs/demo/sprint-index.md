# Velari Practice Assurance Packet Index

Practice: **Family Dental Clinic**

Review period: **2026 Q2**

Overall readiness signal: **high**

This public packet is a local, reference-only planning aid for a buyer-facing Practice Assurance Packet. It does not provide legal advice, establish legal or regulatory status, decide incident reporting duties, secure insurer acceptance, or replace a formal Security Risk Analysis. Do not add PHI, patient identifiers, credentials, secrets, private URLs, raw contracts, logs, or incident-sensitive details.

## Stage Status

| Stage | Status | Evidence gaps | Output | Next action |
|---|---|---:|---|---|
| Intake | ready_for_review | 0 | packet-manifest.json | Confirm the practice profile, owners, review period, and no-PHI evidence-reference boundary. |
| External evidence pre-check | needs_evidence | 3 | external-evidence-precheck.md | Review public-site tracker, TLS, scheduler, intake, and portal observations before the practice relies on patient-facing workflows. |
| Patient data outside the EHR map | needs_evidence | 4 | ephi-flow-map.md, connected-device-inventory.md, portal-api-flow-review.md | Confirm each high-risk flow owner, channel, BAA need, and reference-only evidence location. |
| AI/PHI review | needs_evidence | 3 | ai-workflow-review.md | Separate no-PHI administrative AI use from restricted or prohibited PHI workflows before staff rollout. |
| Vendor/BAA review | needs_evidence | 4 | vendor-baa-review.md | Collect BAA status, SOC 2/HITRUST evidence status, security contact, incident terms, subcontractor posture, and AI/data-use answers. |
| Access/offboarding review | needs_evidence | 2 | readiness-review.md, owner-msp-handoff.md | Export user lists, verify MFA enforcement, and document owner signoff for access and offboarding review. |
| Downtime/ransomware review | needs_evidence | 4 | downtime-ransomware-tabletop.md, incident-decision-log.md | Run or schedule a restore test and tabletop, then record reference IDs and lessons learned. |
| Findings/risk register | ready_for_review | 6 | risk-register.csv, 30-60-90-roadmap.md | Review top findings with the owner and assign 30-day remediation owners. |
| Evidence packet/export | complete | 0 | review-packet.md, review-packet.html, packet-manifest.json, evidence-index.json | Share generated packet artifacts only after confirming they contain references, not PHI or secrets. |
| Owner/MSP handoff | ready_for_review | 9 | owner-msp-handoff.md, handoff-actions.csv | Use the handoff actions to collect MSP, vendor, owner, and legal/compliance reviewer responses. |

## Top Findings

| Finding | Priority | Plain-English summary | Why it matters | Owner lane | Evidence status | Recommended question | Next action |
|---|---|---|---|---|---|---|---|
| BAA status needs review for Example Imaging Vendor | high | A vendor appears to support a workflow involving patient data, but BAA status or review evidence is missing. | Vendor uncertainty leaves the practice without clear privacy, incident notice, retention, deletion, and subcontractor answers. | vendor | missing | Can you confirm whether this vendor stores, processes, transmits, or accesses PHI, whether a BAA is in place, and when it was last reviewed? | Add the vendor to the register, confirm PHI access level, and request BAA/evidence status. |
| Complete the BAA register and review dates | high | A vendor appears to support a workflow involving patient data, but BAA status or review evidence is missing. | Vendor uncertainty leaves the practice without clear privacy, incident notice, retention, deletion, and subcontractor answers. | vendor | missing | Can you confirm whether this vendor stores, processes, transmits, or accesses PHI, whether a BAA is in place, and when it was last reviewed? | Add the vendor to the register, confirm PHI access level, and request BAA/evidence status. |
| Document downtime procedures for critical systems | high | Downtime workflow evidence is missing for a system the practice may need during patient care. | Unproven recovery can turn a ransomware or outage event into patient-care disruption and billing downtime. | msp | missing | Does this item require owner signoff, MSP evidence, vendor clarification, or professional review before action? | Assign an owner, collect reference-only evidence, and update the action packet. |
| Enable MFA for EHR access | high | MFA evidence for an EHR or remote-access workflow is missing or not recorded. | Weak access proof makes it harder to show who can reach systems that support patient care and patient-data workflows. | msp | missing | Can you provide an MFA enforcement export or screenshot for EHR, billing, email, remote access, admin, and vendor-support accounts? | Request MFA proof, document exceptions, and assign an owner for any missing enforcement. |
| Run a restore test and record evidence | high | Backup restore evidence is missing or stale for systems needed during patient care. | Unproven recovery can turn a ransomware or outage event into patient-care disruption and billing downtime. | msp | missing | Can you provide backup scope, last restore-test date, recovery owner, and a private binder reference ID? | Run or schedule a restore test and record reference-only evidence. |
| Run and record a quarterly access review | high | The practice does not have current evidence that user access was reviewed. | Weak access proof makes it harder to show who can reach systems that support patient care and patient-data workflows. | msp | missing | Can you provide user list exports, admin role lists, shared-account exceptions, and owner signoff for access review? | Run the access review, remove or document exceptions, and store evidence references. |
| Set a monthly log review cadence | high | Log review cadence evidence is missing or not recorded for systems that support patient-data workflows. | Missing log review evidence reduces risk visibility when suspicious access, vendor support, or account misuse questions arise. | msp | missing | Can you provide the log sources, review cadence, alert owner, escalation path, and date last reviewed? | Assign a log review owner, record cadence evidence, and define escalation for suspicious access. |
| AI workflow requires action: Paste patient-level note into public chatbot | high | An AI workflow needs clearer data-use, vendor, and human-review boundaries before staff rely on it. | AI workflows need explicit data boundaries so staff do not enter patient, billing, clinical, credential, or raw evidence details into the wrong tool. | office_manager | requested | Should this workflow remain no-PHI, restricted, or paused until vendor terms, retention, model-training use, and human-review controls are reviewed? | Keep the workflow no-PHI or restricted, collect gated proof, and route terms to professional review if needed. |

## Generated Outputs

- `sprint-index.md`
- `practice-assurance-packet.html`
- `practice-assurance-packet.md`
- `external-evidence-precheck.md`
- `sprint-client-readout.md`
- `sprint-command-center.html`
- `sprint-offering-readout.md`
- `owner-action-plan.md`
- `msp-remediation-brief.md`
- `vendor-baa-ai-questionnaire.md`
- `evidence-collection-checklist.md`
- `day-one-workshop-agenda.md`
- `source-map.md`
- `sprint-summary.json`
- `risk-register.csv`
- `evidence-index.json`
- `handoff-actions.csv`
- `connector-evidence-summary.json`
- `control-evidence-matrix.csv`
- `control-evidence-matrix.json`
- `evidence-freshness-report.md`
- `msp-evidence-request.md`
- `vendor-evidence-request.md`
- `insurance-evidence-packet.md`
- `readiness-review.md`
- `ephi-flow-map.md`
- `vendor-baa-review.md`
- `ai-workflow-review.md`
- `downtime-ransomware-tabletop.md`
- `connected-device-inventory.md`
- `portal-api-flow-review.md`
- `external-evidence-precheck.md`
- `incident-decision-log.md`
- `incident-evidence-timeline.md`
- `incident-after-action-report.md`
- `evidence-binder-index.md`
- `owner-msp-handoff.md`
- `30-60-90-roadmap.md`
- `limitations-appendix.md`
- `review-packet.md`
- `review-packet.html`
- `evidence-binder-export/`

## Owner/MSP Use

    - Open `practice-assurance-packet.html` first for the polished report a practice owner can read.
    - Use `practice-assurance-packet.md` when a plain Markdown copy is easier to review.
- Use `external-evidence-precheck.md` for public-site tracker, TLS, scheduler, intake, and portal observations that need owner/MSP/vendor/reviewer follow-up.
- Use `sprint-command-center.html` for the self-contained local command center when a dashboard-style view helps.
- Use `sprint-offering-readout.md` and `owner-action-plan.md` for the real-offering walkthrough.
- Use `sprint-client-readout.md` for a portable Markdown summary.
- Use `connector-evidence-summary.json` to review local connector/import runs, confidence, and safety manifests before relying on automated evidence.
- Start with `sprint-summary.json` for stage status and counts.
- Use `risk-register.csv` to assign owners and remediation priority.
- Use `evidence-index.json` and `evidence-binder-export/` to collect reference-only evidence.
- Use `control-evidence-matrix.csv`, `evidence-freshness-report.md`, `msp-evidence-request.md`, `vendor-evidence-request.md`, and `insurance-evidence-packet.md` to map actions to controls, owners, evidence cadence, and scoped handoffs.
- Use `msp-remediation-brief.md`, `vendor-baa-ai-questionnaire.md`, `evidence-collection-checklist.md`, `source-map.md`, `owner-msp-handoff.md`, and `handoff-actions.csv` to coordinate owner, MSP, vendor, and legal/compliance reviewer follow-up.
