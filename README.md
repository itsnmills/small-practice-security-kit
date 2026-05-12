# Small Practice Security Kit

Open-source security review kit for small healthcare practices that need practical HIPAA, ePHI, vendor, AI, downtime, and evidence workflows without buying enterprise GRC software.

This repository is the umbrella kit. It turns a simple practice profile into a review packet:

```text
intake -> readiness review -> ePHI flow map -> vendor/BAA review -> AI workflow review -> evidence index -> 30/60/90 roadmap
```

## What This Is

Small practices often know they need MFA, backups, BAAs, access reviews, AI rules, incident procedures, and risk documentation, but the work lives across email, vendor portals, tickets, screenshots, spreadsheets, and memory.

This kit creates one local-first packet that helps a practice understand:

- what needs attention first,
- where ePHI enters, moves, rests, and leaves,
- which vendors touch ePHI,
- which AI workflows are allowed, restricted, or prohibited,
- what evidence should be collected,
- what should be done in the next 30, 60, and 90 days.

## What It Is Not

This is not legal advice, HIPAA certification, a formal Security Risk Analysis opinion, penetration testing, breach determination, or a substitute for qualified legal, security, compliance, or incident response professionals.

Do not put PHI, patient identifiers, medical record numbers, diagnoses, claim contents, passwords, API keys, MFA recovery codes, private keys, or real incident details in sample files.

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

## Quick Start

```bash
python3 scripts/build.py samples/family_dental_clinic.yaml
python3 scripts/validate_content.py
python3 -m unittest discover -s tests
```

Generated files appear in `out/family_dental_clinic/`.

## Generated Packet

The sample build creates:

- `readiness-review.md`
- `ephi-flow-map.md`
- `vendor-baa-review.md`
- `ai-workflow-review.md`
- `downtime-ransomware-tabletop.md`
- `evidence-binder-index.md`
- `30-60-90-roadmap.md`
- `review-packet.md`
- `review-packet.html`

## Companion Projects

This umbrella kit is designed to connect with the broader `itsnmills` healthcare security ecosystem:

- `hipaa-evidence-binder-template`
- `healthcare-cyber-readiness-checklist`
- `ephi-data-flow-mapper`
- `vendor-risk-manager`
- `health-ai-governance-auditor`
- `agent-audit-trail`
- `Strands-PHI-Guardrails-Demo`
- `healthcare-ai-security-lab`
- `iomt-risk-scorer`

The first version here is intentionally lightweight and self-contained. Deeper imports from those repos should be added module-by-module.

