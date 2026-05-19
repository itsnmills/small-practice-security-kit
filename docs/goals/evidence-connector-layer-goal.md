# GOAL - Velari Evidence Connector Layer Sprint

## Objective

Build the first functional Evidence Connector Layer for `small-practice-security-kit` so a small healthcare practice owner or MSP can import safe system evidence, generate normalized evidence bundles, and run Sprint Mode without manually entering every security detail.

The product shift is:

`manual profile -> generated packet`

to:

`connector/import evidence -> normalized evidence ledger -> Answer Standard action packets -> owner/MSP/vendor/reviewer handoff`

## Scope

This sprint delivers the first seven implementation items:

1. `small_practice_security_kit/connectors/base.py`
2. `small_practice_security_kit/connectors/csv_import.py`
3. `small_practice_security_kit/connectors/dns_email_auth.py`
4. `small_practice_security_kit/connectors/vendor_public.py`
5. `schemas/normalized-evidence.schema.json` and `schemas/connector-run.schema.json`
6. Direct owner-friendly CLI commands: `import csv users`, `collect vendor-public`, `generate msp-request`, and `build --evidence`
7. Sprint Mode support for `--evidence evidence/*.json`

## Product Modes

Owner Mode:

- Shows what evidence was observed, what is missing, who owns the answer, and what unsafe data must stay out.

MSP Partner Mode:

- Converts connector/import findings into exact evidence requests and remediation questions the MSP can answer.

Local Collector Mode:

- Runs metadata-only collectors or imports safe client/MSP exports on the practice-owned or MSP-owned machine.

## New Rule

Manual input is only required when:

- the system cannot observe the answer,
- an owner must approve it,
- a vendor must answer it,
- an MSP must confirm it,
- a qualified reviewer must assess it.

Every build choice is filtered through security, simplicity, and time saving: collect safe metadata, keep commands obvious, and convert evidence gaps into owner/MSP/vendor/reviewer action.

## Safety Requirements

The implementation must not collect or request:

- PHI or patient identifiers,
- credentials,
- private admin URLs,
- raw logs,
- mailbox contents,
- Drive/SharePoint file contents,
- patient screenshots,
- raw contracts,
- patient examples,
- incident-sensitive details.

Connector outputs must summarize counts, source, confidence, owner lane, acceptable evidence, unsafe inputs, and next actions without storing row-level user identities.

## First Supported Imports

- Google Workspace users/MFA CSV
- Microsoft 365 users/MFA/admin/guest CSV
- device/RMM inventory CSV
- backup/restore report CSV
- vendor register CSV
- public DNS/email-auth metadata collector
- public vendor evidence triage collector

## Acceptance Criteria

- A practice owner can run documented commands against sample connector inputs.
- Each connector output validates against `schemas/connector-run.schema.json`.
- Each evidence item validates against `schemas/normalized-evidence.schema.json`.
- Sprint Mode accepts connector evidence with `--evidence`, and `build --evidence` routes to the same evidence-aware packet.
- `generate msp-request` creates a focused MSP request from the profile and optional connector evidence.
- `sprint-summary.json` includes `connector_evidence_summary`.
- `evidence-index.json` includes connector evidence while preserving the reference-only boundary.
- `risk-register.csv` includes connector-derived Answer Standard action packets.
- `connector-evidence-summary.json` records run provenance, connector modes, status counts, confidence counts, owner lanes, and safety boundary.
- Full tests pass.
- Generated outputs do not include PHI, credentials, private URLs, raw logs, patient screenshots, raw contracts, or row-level user identities.

## End-To-End Test Path

```bash
python -m small_practice_security_kit import csv users samples/connectors/google_workspace_users.csv --out /tmp/velari-evidence/users.json
python -m small_practice_security_kit import csv vendor-register samples/connectors/vendor_register.csv --out /tmp/velari-evidence/vendor-register.json
python -m small_practice_security_kit collect dns --domain exampleclinic.test --out /tmp/velari-evidence/dns.json
python -m small_practice_security_kit collect vendor-public --vendor "Example AI Scribe Vendor" --domain example.com --out /tmp/velari-evidence/vendor-public.json
python -m small_practice_security_kit generate msp-request --profile samples/family_dental_clinic.yaml --evidence /tmp/velari-evidence/*.json --out /tmp/velari-evidence/msp-request.md
python -m small_practice_security_kit build samples/family_dental_clinic.yaml --evidence /tmp/velari-evidence/*.json --output-root /tmp/velari-evidence/out
```

Then inspect:

- `/tmp/velari-evidence/out/family_dental_clinic/sprint-command-center.html`
- `/tmp/velari-evidence/out/family_dental_clinic/connector-evidence-summary.json`
- `/tmp/velari-evidence/out/family_dental_clinic/risk-register.csv`
- `/tmp/velari-evidence/out/family_dental_clinic/evidence-index.json`

## Non-Goals

- No live Google Workspace or Microsoft 365 OAuth in this sprint.
- No EHR/FHIR patient-data collection.
- No automatic remediation.
- No legal, breach, HIPAA, vendor approval, AI production-use, insurance, or formal Security Risk Analysis determinations.
