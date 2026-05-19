# Velari Sprint Client Readout

Practice: **Family Dental Clinic**

Review period: **2026 Q2**

Readiness signal: **high**

Target delivery signal: **needs_evidence_before_closeout**

This readout is a local, reference-only planning artifact. It does not provide legal advice, establish legal or regulatory status, decide incident reporting duties, secure insurer or vendor acceptance, authorize AI production use, or replace a formal Security Risk Analysis. Do not add PHI, patient identifiers, credentials, secrets, private URLs, raw contracts, logs, or incident-sensitive details.

## Executive Snapshot

- Stages needing evidence: 5 of 9
- High or critical findings: 10
- Evidence references: 17
- Evidence references needing attention: 15
- Control evidence rows: 30
- Control evidence needing attention: 30
- Handoff actions: 17

## Top Risks

| Finding | Priority | Plain-English summary | Owner lane | Question | Evidence to collect | Unsafe inputs | Timeframe | Reviewer needed | Next action |
|---|---|---|---|---|---|---|---|---|---|
| Enable MFA for EHR access | high | MFA evidence for an EHR or remote-access workflow is missing or not recorded. | msp | Can you provide an MFA enforcement export or screenshot for EHR, billing, email, remote access, admin, and vendor-support accounts? | MFA policy export; admin screenshot with date observed; covered groups; exception list; MSP attestation | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data | 30_days | msp; office_manager | Request MFA proof, document exceptions, and assign an owner for any missing enforcement. |
| Run and record a quarterly access review | high | The practice does not have current evidence that user access was reviewed. | msp | Can you provide user list exports, admin role lists, shared-account exceptions, and owner signoff for access review? | user list export; admin role list; owner access-review signoff; removed-account notes; exception sunset dates | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data | 30_days | msp; office_manager | Run the access review, remove or document exceptions, and store evidence references. |
| Run a restore test and record evidence | high | Backup restore evidence is missing or stale for systems needed during patient care. | msp | Can you provide backup scope, last restore-test date, recovery owner, and a private binder reference ID? | backup scope summary; restore-test note; date observed; recovery owner; systems excluded from backup | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; raw backup data; private console links | 30_days | msp; office_manager | Run or schedule a restore test and record reference-only evidence. |
| Complete the BAA register and review dates | high | A vendor appears to support a workflow involving patient data, but BAA status or review evidence is missing. | vendor | Can you confirm whether this vendor stores, processes, transmits, or accesses PHI, whether a BAA is in place, and when it was last reviewed? | BAA status; BAA review date; vendor security page; SOC 2 or HITRUST status; incident notification terms; retention/deletion terms | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data; raw contracts with sensitive details | 30_days | vendor_owner; legal_or_compliance_reviewer | Add the vendor to the register, confirm PHI access level, and request BAA/evidence status. |
| Document downtime procedures for critical systems | high | Downtime workflow evidence is missing for a system the practice may need during patient care. | msp | Does this item require owner signoff, MSP evidence, vendor clarification, or professional review before action? | owner signoff; evidence reference ID; date observed; workflow owner; review note | patient names; patient records; credentials; private portal links; raw logs; screenshots with sensitive data | 30_days | msp; office_manager | Assign an owner, collect reference-only evidence, and update the action packet. |

## Evidence Gaps By Stage

| Stage | Owner | Recipient | Gaps | Artifact |
|---|---|---|---:|---|
| Patient data outside the EHR map | MSP Lead | MSP | 4 | ephi-flow-map.md, connected-device-inventory.md, portal-api-flow-review.md |
| AI/PHI review | Office Manager | Owner | 3 | ai-workflow-review.md |
| Vendor/BAA review | Office Manager | Vendor | 4 | vendor-baa-review.md |
| Access/offboarding review | MSP Lead | MSP | 2 | readiness-review.md, owner-msp-handoff.md |
| Downtime/ransomware review | MSP Lead | MSP | 4 | downtime-ransomware-tabletop.md, incident-decision-log.md |
| Findings/risk register | Practice owner/MSP | Owner | 6 | risk-register.csv, 30-60-90-roadmap.md |

## Handoff Lanes

| Recipient | Actions | High priority | Artifacts |
|---|---:|---:|---|
| Owner/MSP | 2 | 0 | packet-manifest.json, owner-msp-handoff.md |
| MSP | 9 | 9 | ephi-flow-map.md, readiness-review.md, downtime-ransomware-tabletop.md, owner-msp-handoff.md |
| Owner | 3 | 1 | ai-workflow-review.md, risk-register.csv, sprint-index.md |
| Vendor | 3 | 3 | vendor-baa-review.md |

## Next Actions

- **MSP**: Confirm each high-risk flow owner, channel, BAA need, and reference-only evidence location. (`ephi-flow-map.md`)
- **Owner**: Separate no-PHI administrative AI use from restricted or prohibited PHI workflows before staff rollout. (`ai-workflow-review.md`)
- **Vendor**: Collect BAA status, SOC 2/HITRUST evidence status, security contact, incident terms, subcontractor posture, and AI/data-use answers. (`vendor-baa-review.md`)
- **MSP**: Export user lists, verify MFA enforcement, and document owner signoff for access and offboarding review. (`readiness-review.md`)
- **MSP**: Run or schedule a restore test and tabletop, then record reference IDs and lessons learned. (`downtime-ransomware-tabletop.md`)
- **MSP**: Which EHR, billing, imaging, email, remote support, and administrator accounts have MFA technically enforced? (`owner-msp-handoff.md`)
- **MSP**: Which systems are in backup scope, when was the last restore test, and what evidence reference proves it? (`downtime-ransomware-tabletop.md`)
- **Vendor**: Can the billing, imaging, and AI scribe vendors confirm BAA scope, incident terms, subcontractors, and model-training posture? (`vendor-baa-review.md`)

## Generated Artifacts

- `sprint-command-center.html`
- `sprint-offering-readout.md`
- `owner-action-plan.md`
- `msp-remediation-brief.md`
- `vendor-baa-ai-questionnaire.md`
- `evidence-collection-checklist.md`
- `day-one-workshop-agenda.md`
- `source-map.md`
- `sprint-summary.json`
- `evidence-index.json`
- `risk-register.csv`
- `handoff-actions.csv`
- `control-evidence-matrix.csv`
- `evidence-freshness-report.md`
- `msp-evidence-request.md`
- `vendor-evidence-request.md`
- `insurance-evidence-packet.md`
- `review-packet.md`
- `review-packet.html`
- `packet-manifest.json`
