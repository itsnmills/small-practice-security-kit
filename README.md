# Small Practice Security Kit

**Local-first healthcare security readiness packets for small practices.**

This repo is the public front door for a Velari-style readiness workflow: take a non-PHI practice profile, map where patient data can move outside the EHR, review vendors/BAAs and AI usage, then generate an owner/MSP-ready evidence packet and 30/60/90 roadmap.

```text
local intake -> readiness review -> ePHI flow map -> vendor/BAA review -> AI workflow review -> evidence index -> 30/60/90 roadmap
```

The goal is not to replace attorneys, security assessors, incident responders, or enterprise GRC software. The goal is to give small healthcare practices a practical way to organize the first evidence-backed conversation before an audit, incident, renewal, AI rollout, or MSP handoff.

## What this helps answer

Small practices often know they need MFA, backups, BAAs, access reviews, AI rules, incident procedures, downtime plans, and risk documentation. The hard part is proving what exists when evidence is scattered across email, vendor portals, tickets, screenshots, spreadsheets, and memory.

This kit helps answer:

- Where does ePHI enter, move, rest, and leave?
- Which systems and vendors touch ePHI?
- Which AI workflows are allowed, restricted, or prohibited?
- Which evidence references should be collected, refreshed, or handed to an MSP?
- Which gaps should be handled in the next 30, 60, and 90 days?
- What can the practice owner safely show a reviewer without uploading PHI?

## Velari Cyber Readiness Sprint narrative

This repo demonstrates the public version of a focused small-practice readiness sprint:

> In one focused sprint, a small healthcare practice maps AI, vendor, access, ePHI-flow, downtime, and ransomware-readiness gaps, then receives an owner/MSP-ready evidence packet and prioritized 30/60/90 roadmap.

The strongest wedge is the **Patient Data Outside the EHR Map**: inboxes, shared drives, AI tools, vendors, portals, exports, contractors, backups, billing systems, and MSP-managed systems. Once those flows are visible, the evidence binder, vendor/BAA register, AI workflow review, and downtime plan become concrete.

## Public demo

A complete synthetic demo is checked into [`docs/demo/`](docs/demo/). It uses a fictional `Family Dental Clinic` profile and contains no real PHI, credentials, private URLs, contracts, or incident details.

Start here:

- Demo overview: [`docs/demo/README.md`](docs/demo/README.md)
- Complete Markdown packet: [`docs/demo/review-packet.md`](docs/demo/review-packet.md)
- Print-friendly HTML packet: [`docs/demo/review-packet.html`](docs/demo/review-packet.html)
- Canonical manifest: [`docs/demo/packet-manifest.json`](docs/demo/packet-manifest.json)
- Screenshot: [`docs/demo/screenshots/review-packet.png`](docs/demo/screenshots/review-packet.png)

![Review packet screenshot](docs/demo/screenshots/review-packet.png)

## What you get

| Output | Purpose |
|---|---|
| `readiness-review.md` | Plain-English baseline readiness review |
| `ephi-flow-map.md` | Systems, workflows, vendors, ePHI categories, BAA needs, and risk |
| `vendor-baa-review.md` | Vendor, BAA, SOC 2/HITRUST evidence status, incident terms, subcontractor, and AI data-use review |
| `ai-workflow-review.md` | Allowed, restricted, and prohibited AI workflow review |
| `downtime-ransomware-tabletop.md` | Downtime planning and tabletop starter packet |
| `connected-device-inventory.md` | IoMT/connected-device worksheet for patch owner, default credentials, downtime fallback, and safety notices |
| `portal-api-flow-review.md` | Portal, app, API/FHIR-style flow worksheet for identity, audit logs, secure messaging, and export/delete evidence |
| `incident-decision-log.md` | Decision-log template separating technical containment from legal/compliance breach-notification decisions |
| `evidence-binder-index.md` | Evidence references to collect in a binder |
| `owner-msp-handoff.md` | Owner/MSP follow-up, vendor asks, access actions, and handoff boundary |
| `30-60-90-roadmap.md` | Prioritized remediation and evidence plan |
| `limitations-appendix.md` | Explicit statement of what the packet does and does not prove |
| `review-packet.md` | Complete Markdown packet |
| `review-packet.html` | Print-friendly HTML packet |
| `packet-manifest.json` | Canonical non-PHI manifest of sections, evidence references, roadmap items, findings, and artifact hashes |
| `dashboard.html` | Owner-friendly local workflow dashboard |

## Quick start

### Owner-friendly local intake workspace

On macOS, double-click:

```text
open_dashboard.command
```

That opens a local dashboard for the sample practice at:

```text
http://127.0.0.1:8765/
```

Terminal version:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/serve_dashboard.py --profile samples/family_dental_clinic.yaml
```

The intake workspace lets a practice or consultant create a local profile from healthcare presets, select common systems, review suggested ePHI flows, edit vendor/BAA status, answer the readiness checklist, add evidence references, review AI workflows, and generate the local dashboard and review packet.

More details:

- [`docs/dashboard.md`](docs/dashboard.md)
- [`docs/intake-mode.md`](docs/intake-mode.md)
- [`docs/security-model.md`](docs/security-model.md)

### Packet builder CLI

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/build.py samples/family_dental_clinic.yaml
.venv/bin/python scripts/export_binder_index.py samples/family_dental_clinic.yaml
.venv/bin/python scripts/validate_content.py
.venv/bin/python -m unittest discover -s tests
```

Generated files appear in:

```text
out/family_dental_clinic/
```

Open the HTML packet locally:

```text
out/family_dental_clinic/review-packet.html
```

### Velari Sprint Mode public runner

The Sprint Mode runner wraps the packet builder into the full Cyber Readiness Sprint demo and adds stage status, risk, evidence, and handoff exports:

```bash
python3 -m small_practice_security_kit sprint samples/family_dental_clinic.yaml --output-root out
```

Start with:

```text
out/family_dental_clinic/sprint-command-center.html
```

Sprint Mode also writes `sprint-offering-readout.md`, `owner-action-plan.md`, `msp-remediation-brief.md`, `vendor-baa-ai-questionnaire.md`, `evidence-collection-checklist.md`, `day-one-workshop-agenda.md`, `source-map.md`, `sprint-client-readout.md`, `sprint-index.md`, `sprint-summary.json`, `risk-register.csv`, `evidence-index.json`, `handoff-actions.csv`, and `evidence-binder-export/` while preserving the existing packet files, including `connected-device-inventory.md`, `portal-api-flow-review.md`, and `incident-decision-log.md`.

The JSON contracts for private-app import are documented in `schemas/sprint-summary.schema.json` and `schemas/evidence-index.schema.json`. `sprint-summary.json` includes an `offering_summary` section for audience lanes, source anchors, first-week actions, artifact checklist, boundaries, and stage-to-source mapping. The action-translation standard lives in [`docs/product/velari-answer-standard.md`](docs/product/velari-answer-standard.md), and Sprint Mode applies it to `risk-register.csv`, `handoff-actions.csv`, and `sprint-summary.json`.

More details:

- [`docs/sprint-mode/product-contract.md`](docs/sprint-mode/product-contract.md)
- [`docs/sprint-mode/OFFERING_BLUEPRINT.md`](docs/sprint-mode/OFFERING_BLUEPRINT.md)
- [`docs/sprint-mode/delivery-playbook.md`](docs/sprint-mode/delivery-playbook.md)
- [`docs/sprint-mode/output-map.md`](docs/sprint-mode/output-map.md)

## Modules

| Module | Purpose |
|---|---|
| `01-readiness-checklist/` | Plain-English security readiness review |
| `02-ephi-data-flow-map/` | Systems, vendors, workflows, and ePHI movement |
| `03-hipaa-evidence-binder/` | Evidence references and review packet links |
| `04-vendor-baa-review/` | Vendor, BAA, SOC 2/HITRUST evidence status, AI training/data-use, and subcontractor review |
| `05-ai-workflow-review/` | Allowed/prohibited AI workflow review |
| `06-downtime-ransomware-tabletop/` | Downtime, restore test, tabletop, and incident evidence |
| `07-review-packet-builder/` | Packet builder scripts and output conventions |

## Companion repo map

This kit is designed to be the front door for a broader healthcare security proof-of-work portfolio:

| Repo | Role in the Kit |
|---|---|
| [`Strands-PHI-Guardrails-Demo`](https://github.com/itsnmills/Strands-PHI-Guardrails-Demo) | PHI guardrail examples for allowed/prohibited data handling |
| [`agent-audit-trail`](https://github.com/itsnmills/agent-audit-trail) | AI audit-log evidence references |
| [`vendor-risk-manager`](https://github.com/itsnmills/vendor-risk-manager) | Vendor/BAA due-diligence register |
| [`hipaa-scanner`](https://github.com/itsnmills/hipaa-scanner) | Public-facing readiness triage and security-header checks |
| [`hipaa-compliance-engine`](https://github.com/itsnmills/hipaa-compliance-engine) | Evidence/control mapping ideas |
| [`ai-governance-auditor`](https://github.com/itsnmills/ai-governance-auditor) | AI governance checklist patterns |

Detailed integration notes live in [`docs/import-plans/existing-repos.md`](docs/import-plans/existing-repos.md).

## Safety and data boundary

This repository is **local-first and PHI-avoidant**.

Recommended inputs:

- fictional sample practices,
- system names,
- vendor names,
- role names,
- ticket references,
- evidence folder references,
- non-sensitive summary notes.

Do **not** enter:

- patient names,
- medical record numbers,
- dates of birth,
- diagnoses,
- claim contents,
- clinical notes,
- passwords,
- API keys,
- MFA recovery codes,
- private keys,
- real incident details.

Read the full boundary before adapting this for real work: [`docs/security-model.md`](docs/security-model.md).

## What this is not

This is not legal advice, does not certify any legal or regulatory requirement, does not decide incident reporting duties, and is not a formal Security Risk Analysis, penetration testing, managed detection and response, a SOC, or a substitute for qualified legal, security, compliance, or incident response professionals.

Use it as a practical organizer and first-pass evidence workflow.

## Roadmap

1. Expand imports from readiness checklist, AI governance auditor, and other companion repos.
2. Add optional PDF rendering and richer scoring/priority explanations.
3. Add more sample profiles and demo packets for different practice types.
4. Add release workflow for demo artifacts across repos and improve compatibility for companion integrations.

## License

MIT. See [LICENSE](LICENSE).
