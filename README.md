# Small Practice Security Kit

Open-source security kit for small healthcare practices that need practical HIPAA, ePHI, vendor, AI, downtime, and evidence workflows without buying enterprise GRC software.

This is the flagship umbrella project for a privacy-first healthcare security toolkit. It turns a simple practice profile into a review packet:

```text
intake -> readiness review -> ePHI flow map -> vendor/BAA review -> AI workflow review -> evidence index -> 30/60/90 roadmap
```

The goal is not to replace attorneys, security assessors, incident responders, or full GRC platforms. The goal is to give small practices a local, understandable way to organize the first evidence-backed conversation.

## Why This Exists

Small practices often know they need MFA, backups, BAAs, access reviews, AI rules, incident procedures, and risk documentation. The problem is that the proof gets scattered across email, vendor portals, tickets, screenshots, spreadsheets, and memory.

This kit creates one local-first packet that helps answer:

- Where does ePHI enter, move, rest, and leave?
- Which vendors touch ePHI?
- Which workflows use AI, and are they allowed, restricted, or prohibited?
- Which evidence references should be collected?
- Which gaps should be fixed in the next 30, 60, and 90 days?
- What should be handed to a qualified reviewer, MSP, consultant, or practice owner?

## What You Get

| Output | Purpose |
|---|---|
| `readiness-review.md` | Plain-English baseline readiness review |
| `ephi-flow-map.md` | Systems, workflows, vendors, ePHI categories, BAA needs, and risk |
| `vendor-baa-review.md` | Vendor, BAA, incident terms, subcontractor, and AI data-use review |
| `ai-workflow-review.md` | Allowed, restricted, and prohibited AI workflow review |
| `downtime-ransomware-tabletop.md` | Downtime planning and tabletop starter packet |
| `evidence-binder-index.md` | Evidence references to collect in a binder |
| `owner-msp-handoff.md` | Owner/MSP follow-up, vendor asks, access actions, and handoff boundary |
| `30-60-90-roadmap.md` | Prioritized remediation and evidence plan |
| `limitations-appendix.md` | Explicit statement of what the packet does and does not prove |
| `review-packet.md` | Complete Markdown packet |
| `review-packet.html` | Print-friendly HTML packet |
| `packet-manifest.json` | Canonical non-PHI manifest of sections, evidence references, roadmap items, findings, and artifact hashes |
| `dashboard.html` | Owner-friendly local workflow dashboard |

## Quick Start

### Owner-friendly local intake workspace

On macOS, double-click:

```text
open_dashboard.command
```

That opens a local dashboard for the sample practice at:

```text
http://127.0.0.1:8765/
```

The intake workspace is the preferred owner-facing experience. It lets a practice or consultant create a local profile from healthcare presets, select common systems, review suggested ePHI flows, edit vendor/BAA status, answer the readiness checklist, add evidence references, review AI workflows, and generate the local dashboard and review packet.

Terminal version:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/serve_dashboard.py --profile samples/family_dental_clinic.yaml
```

Generated dashboard file:

```text
out/family_dental_clinic/dashboard.html
```

More details live in [docs/dashboard.md](docs/dashboard.md), [docs/intake-mode.md](docs/intake-mode.md), and [docs/security-model.md](docs/security-model.md).

### Packet builder CLI

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/build.py samples/family_dental_clinic.yaml
.venv/bin/python scripts/export_binder_index.py samples/family_dental_clinic.yaml
.venv/bin/python scripts/import_ephi_flows.py examples/imports/ephi-data-flow-mapper/flows.csv --base samples/family_dental_clinic.yaml --output out/family_dental_clinic/imported-ephi-profile.yaml
.venv/bin/python scripts/import_vendor_register.py examples/imports/vendor-risk-manager/vendor_register.csv --base samples/family_dental_clinic.yaml --output out/family_dental_clinic/imported-vendor-profile.yaml
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

## Modules

| Module | Purpose |
|---|---|
| `01-readiness-checklist/` | Plain-English security readiness review |
| `02-ephi-data-flow-map/` | Systems, vendors, workflows, and ePHI movement |
| `03-hipaa-evidence-binder/` | Evidence references and review packet links |
| `04-vendor-baa-review/` | Vendor, BAA, AI training/data-use, and subcontractor review |
| `05-ai-workflow-review/` | Allowed/prohibited AI workflow review |
| `06-downtime-ransomware-tabletop/` | Downtime, restore test, tabletop, and incident evidence |
| `07-review-packet-builder/` | Packet builder scripts and output conventions |

## Companion Repos and Import Plan

This kit is designed to become the front door for the broader `itsnmills` healthcare security ecosystem:

| Repo | Role in the Kit | Planned Integration |
|---|---|---|
| [`hipaa-evidence-binder-template`](https://github.com/itsnmills/hipaa-evidence-binder-template) | Evidence operating system | Export `evidence-binder-index.md` into binder-compatible CSV/Markdown |
| [`healthcare-cyber-readiness-checklist`](https://github.com/itsnmills/healthcare-cyber-readiness-checklist) | Readiness checklist | Import checklist item register and map results into readiness review |
| `ephi-data-flow-mapper` | ePHI flow documentation | Promote flow schema into this kit's `flows` model |
| [`vendor-risk-manager`](https://github.com/itsnmills/vendor-risk-manager) | Vendor/BAA due diligence | Import/export vendor register and annual review fields |
| [`health-ai-governance-auditor`](https://github.com/itsnmills/health-ai-governance-auditor) | AI tool and workflow governance | Import AI vendor/workflow findings into AI workflow review |
| [`agent-audit-trail`](https://github.com/itsnmills/agent-audit-trail) | AI audit evidence | Link agent/tool logs as restricted evidence references |
| [`Strands-PHI-Guardrails-Demo`](https://github.com/itsnmills/Strands-PHI-Guardrails-Demo) | PHI guardrail examples | Reuse allowed/prohibited data handling examples |
| [`healthcare-ai-security-lab`](https://github.com/itsnmills/healthcare-ai-security-lab) | Healthcare KEV triage | Import priority vulnerabilities as technical evidence references |
| [`iomt-risk-scorer`](https://github.com/itsnmills/iomt-risk-scorer) | IoMT risk triage | Import device risk summaries into ePHI and technical evidence |

Detailed import notes live in [docs/import-plans/existing-repos.md](docs/import-plans/existing-repos.md).

## First Integrations

The first implemented integrations are:

| Command | Purpose |
|---|---|
| `python scripts/export_binder_index.py samples/family_dental_clinic.yaml` | Create `hipaa-evidence-binder-template` compatible CSV/Markdown evidence exports |
| `python scripts/import_ephi_flows.py examples/imports/ephi-data-flow-mapper/flows.csv --base samples/family_dental_clinic.yaml --output out/family_dental_clinic/imported-ephi-profile.yaml` | Import ePHI flow rows into a profile |
| `python scripts/import_vendor_register.py examples/imports/vendor-risk-manager/vendor_register.csv --base samples/family_dental_clinic.yaml --output out/family_dental_clinic/imported-vendor-profile.yaml` | Import vendor/BAA rows into a profile |

The adapter contract is documented in [docs/adapter-contract.md](docs/adapter-contract.md).

## Safety Model

This repository is local-first and PHI-avoidant.

Recommended:

- fictional sample practices,
- system names,
- vendor names,
- role names,
- ticket references,
- evidence folder references,
- non-sensitive summary notes.

Do not enter:

- patient names,
- medical record numbers,
- DOBs,
- diagnoses,
- claim contents,
- clinical notes,
- passwords,
- API keys,
- MFA recovery codes,
- private keys,
- real incident details.

## What This Is Not

This is not legal advice, HIPAA certification, a formal Security Risk Analysis opinion, penetration testing, breach determination, or a substitute for qualified legal, security, compliance, or incident response professionals.

Use this as a practical organizer and first-pass evidence workflow.

## Roadmap

1. Add schema validation for practice profiles.
2. Export binder-compatible CSV for `hipaa-evidence-binder-template`.
3. Add imports from readiness checklist, vendor manager, AI governance auditor, and ePHI mapper.
4. Add a public demo packet under `docs/demo/`.
5. Add optional PDF rendering.
6. Add richer scoring and priority explanations.

## License

MIT. See [LICENSE](LICENSE).
