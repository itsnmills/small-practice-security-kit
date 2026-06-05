# Practice Assurance Packet Product Contract

## What Sprint Mode Is

Velari Sprint Mode is the guided, local-first public runner that generates the Velari Practice Assurance Packet demo. It turns a non-PHI practice profile into an owner/MSP-ready report and evidence handoff:

`10-minute intake -> external evidence pre-check -> patient-data-outside-EHR map -> AI/PHI review -> vendor/BAA review -> access/offboarding review -> downtime/ransomware review -> owner decision queue -> evidence packet -> 30/60/90 roadmap -> owner/MSP handoff`

It is designed for synthetic demos, founder/consultant walkthroughs, and first-pass readiness conversations with small healthcare practices.

## What Sprint Mode Is Not

Sprint Mode is not legal advice, does not certify any legal or regulatory requirement, does not decide incident reporting duties, is not cyber insurance advice, and is not penetration testing, MDR, SOC, vendor acceptance, AI production-use authorization, or a formal Security Risk Analysis.

It does not verify real contracts, BAAs, access lists, logs, backup restores, insurance questionnaires, vendor claims, or production evidence.

External Evidence Pre-Check observations are reference-only prompts for review. They do not submit real patient forms, store sensitive intercepted payloads, run unauthorized scanning, declare HIPAA violations, or replace qualified privacy/security review.

With connector evidence enabled, Sprint Mode can ingest metadata-only connector bundles from CSV imports or local collectors. Connector evidence can reduce manual intake, but it still produces readiness evidence and handoff questions rather than legal, compliance, or remediation conclusions.

## Stages

| Stage | Purpose | Primary output |
|---|---|---|
| Intake | Validate practice profile and safety boundary | `practice-assurance-packet.html`, `practice-assurance-packet.md`, `sprint-summary.json`, `sprint-command-center.html` |
| External evidence pre-check | Turn authorized public-site tracker, appointment, intake, portal, TLS, and certificate observations into safe owner/MSP/vendor/reviewer questions | `external-evidence-precheck.md` |
| Patient data outside the EHR map | Show where ePHI could move outside the core system | `ephi-flow-map.md` |
| AI/PHI review | Classify AI workflows as allowed, restricted, or prohibited | `ai-workflow-review.md` |
| Vendor/BAA review | Identify vendor evidence and BAA gaps | `vendor-baa-review.md` |
| Access/offboarding review | Identify MFA, access review, and offboarding gaps | `owner-msp-handoff.md` |
| Downtime/ransomware review | Identify backup, restore, downtime, and tabletop gaps | `downtime-ransomware-tabletop.md` |
| Findings/risk register | Convert findings into owner/MSP action rows | `risk-register.csv` |
| Evidence packet/export | Build packet, manifest, evidence index, and collection checklist | `review-packet.md`, `review-packet.html`, `packet-manifest.json`, `evidence-index.json`, `evidence-collection-checklist.md` |
| Owner/MSP handoff | Make questions and next actions explicit | `owner-msp-handoff.md`, `handoff-actions.csv`, `owner-action-plan.md`, `msp-remediation-brief.md` |

## Data Contracts

Sprint Mode writes contract-oriented outputs for later private app import:

- `sprint-summary.json` validates against `schemas/sprint-summary.schema.json`.
- `evidence-index.json` validates against `schemas/evidence-index.schema.json`.
- Connector bundles validate against `schemas/connector-run.schema.json`, and individual connector evidence items validate against `schemas/normalized-evidence.schema.json`.
- Finding/action packets follow `schemas/velari-answer-standard.schema.json` and the product language rules in `docs/product/velari-answer-standard.md`.
- `packet-manifest.json` includes lifecycle-aware evidence references with source kind, source reference, lifecycle status, closeout state, acceptable evidence, unsafe inputs, next action, closeout rule, and trace metadata back to flows, systems, vendors, workflows, artifacts, and source modules.
- `risk-register.csv` and `handoff-actions.csv` include audience, recipient, owner, stage, priority, timeframe, plain-English summary, why-it-matters text, recommended question, acceptable evidence, unsafe inputs, reviewer needed, next action, output views, evidence reference, artifact reference, and 30/60/90 bucket fields.
- `sprint-summary.json` includes `offering_summary` for private-app import of audience lanes, source anchors, first-week actions, artifact checklist, boundary statements, and stage-to-source mapping.
- `offering_summary.simple_intake_steps` defines the five-question 10-minute intake contract for practice owner, vendor, public URL, AI, and MSP evidence-status collection.
- `connector-evidence-summary.json` records connector run provenance, confidence, safety manifest status, and metadata-only boundaries.

## Accepted Inputs

- Synthetic or client-supplied reference metadata.
- System names, vendor names, role names, workflow summaries, and evidence IDs.
- Evidence location labels, ticket references, status summaries, owner roles, and review dates.
- AI workflow descriptions that do not include patient-level data.
- Connector evidence bundles generated by approved metadata-only imports or local collectors.

## Prohibited Inputs

- Patient names, MRNs, dates of birth, diagnoses, chart notes, patient images, claim contents, clinical narratives, raw incident details, credentials, API keys, tokens, private keys, MFA recovery codes, private URLs, presigned links, raw contracts, raw logs, or screenshots containing sensitive data.

## Output Contract

The command:

```bash
python3 -m small_practice_security_kit sprint samples/family_dental_clinic.yaml --output-root out
```

The connector-enabled command:

```bash
python3 -m small_practice_security_kit sprint samples/family_dental_clinic.yaml --evidence evidence/*.json --output-root out
```

The owner-friendly alias:

```bash
python3 -m small_practice_security_kit build samples/family_dental_clinic.yaml --evidence evidence/*.json --output-root out
```

creates `out/family_dental_clinic/` with the existing packet artifacts plus:

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
- `evidence-binder-export/`

The existing output names are preserved, including `review-packet.md`, `review-packet.html`, `owner-msp-handoff.md`, `30-60-90-roadmap.md`, and `packet-manifest.json`.
