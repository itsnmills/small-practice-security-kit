# Sprint Mode Product Contract

## What Sprint Mode Is

Velari Sprint Mode is a guided, local-first public runner for the Velari Cyber Readiness Sprint demo. It turns a non-PHI practice profile into an owner/MSP-ready packet:

`practice intake -> patient-data-outside-EHR map -> AI/PHI review -> vendor/BAA review -> access/offboarding review -> downtime/ransomware review -> findings -> evidence packet -> 30/60/90 roadmap -> owner/MSP handoff`

It is designed for synthetic demos, founder/consultant walkthroughs, and first-pass readiness conversations with small healthcare practices.

## What Sprint Mode Is Not

Sprint Mode is not legal advice, HIPAA certification, breach determination, cyber insurance advice, penetration testing, MDR, SOC, vendor approval, AI tool approval for PHI, or a formal Security Risk Analysis opinion.

It does not verify real contracts, BAAs, access lists, logs, backup restores, insurance questionnaires, vendor claims, or production evidence.

## Stages

| Stage | Purpose | Primary output |
|---|---|---|
| Intake | Validate practice profile and safety boundary | `sprint-summary.json` |
| Patient data outside the EHR map | Show where ePHI could move outside the core system | `ephi-flow-map.md` |
| AI/PHI review | Classify AI workflows as allowed, restricted, or prohibited | `ai-workflow-review.md` |
| Vendor/BAA review | Identify vendor evidence and BAA gaps | `vendor-baa-review.md` |
| Access/offboarding review | Identify MFA, access review, and offboarding gaps | `owner-msp-handoff.md` |
| Downtime/ransomware review | Identify backup, restore, downtime, and tabletop gaps | `downtime-ransomware-tabletop.md` |
| Findings/risk register | Convert findings into owner/MSP action rows | `risk-register.csv` |
| Evidence packet/export | Build packet, manifest, and evidence index | `review-packet.md`, `review-packet.html`, `packet-manifest.json`, `evidence-index.json` |
| Owner/MSP handoff | Make questions and next actions explicit | `owner-msp-handoff.md`, `handoff-actions.csv` |

## Accepted Inputs

- Synthetic or client-supplied reference metadata.
- System names, vendor names, role names, workflow summaries, and evidence IDs.
- Evidence location labels, ticket references, status summaries, owner roles, and review dates.
- AI workflow descriptions that do not include patient-level data.

## Prohibited Inputs

- Patient names, MRNs, dates of birth, diagnoses, chart notes, patient images, claim contents, clinical narratives, raw incident details, credentials, API keys, tokens, private keys, MFA recovery codes, private URLs, presigned links, raw contracts, raw logs, or screenshots containing sensitive data.

## Output Contract

The command:

```bash
python3 -m small_practice_security_kit sprint samples/family_dental_clinic.yaml --output-root out
```

creates `out/family_dental_clinic/` with the existing packet artifacts plus:

- `sprint-index.md`
- `sprint-summary.json`
- `risk-register.csv`
- `evidence-index.json`
- `handoff-actions.csv`
- `evidence-binder-export/`

The existing output names are preserved, including `review-packet.md`, `review-packet.html`, `owner-msp-handoff.md`, `30-60-90-roadmap.md`, and `packet-manifest.json`.
