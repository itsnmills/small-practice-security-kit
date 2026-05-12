# Goal: Fully Implement Small Practice Security Kit Repo Integrations

## Objective

Fully implement the planned repository integrations for `small-practice-security-kit` so it becomes the public front door for the existing `itsnmills` healthcare security ecosystem.

The final implementation should convert the current standalone packet generator into a reusable, tested, CI-backed package that can:

- validate practice profiles,
- build review packets,
- export evidence needs into the HIPAA evidence binder format,
- import ePHI flow rows,
- import vendor/BAA register rows,
- normalize imported/exported records into a shared exchange contract,
- preserve PHI/secrets safety,
- refresh public demo output,
- document the integration model clearly.

## Repository

Target repo:

```text
/Users/noahmills/Projects/small-practice-security-kit
https://github.com/itsnmills/small-practice-security-kit
```

Current public repo purpose:

> Open-source security kit for small healthcare practices that need practical HIPAA, ePHI, vendor, AI, downtime, and evidence workflows without buying enterprise GRC software.

Current workflow:

```bash
python scripts/build.py samples/family_dental_clinic.yaml
python scripts/validate_content.py
python -m unittest discover -s tests
```

Current generated packet:

```text
out/family_dental_clinic/
├── readiness-review.md
├── ephi-flow-map.md
├── vendor-baa-review.md
├── ai-workflow-review.md
├── downtime-ransomware-tabletop.md
├── evidence-binder-index.md
├── 30-60-90-roadmap.md
├── review-packet.md
└── review-packet.html
```

## Product Thesis

This repo should not become a bloated GRC platform. It should stay the small-practice front door:

```text
practice profile -> ePHI flows -> vendor review -> AI workflow review -> evidence binder export -> review packet
```

The key is to make the umbrella kit useful by itself while allowing deeper companion repos to feed it structured inputs or receive exports.

## Companion Repos

Primary first-wave integrations:

1. `hipaa-evidence-binder-template`
2. `ephi-data-flow-mapper`
3. `vendor-risk-manager`

Follow-on integrations:

1. `health-ai-governance-auditor`
2. `ai-governance-auditor`
3. `agent-audit-trail`
4. `Strands-PHI-Guardrails-Demo`
5. `healthcare-ai-security-lab`
6. `iomt-risk-scorer`
7. `hipaa-scanner`
8. `hipaa-compliance-engine`

Do not implement follow-on adapters in this goal unless all first-wave work is done and verified.

## Required Final Capabilities

### Capability 1: Internal Python Package

Create a reusable package so the repo is no longer script-only.

Add:

```text
small_practice_security_kit/
├── __init__.py
├── profile.py
├── validation.py
├── packet.py
├── exchange.py
├── safety.py
└── adapters/
    ├── __init__.py
    ├── evidence_binder.py
    ├── ephi_mapper.py
    └── vendor_risk.py
```

Responsibilities:

- `profile.py`: load, normalize, and write practice profile YAML.
- `validation.py`: validate profile structure and adapter inputs.
- `packet.py`: risk scoring and Markdown/HTML packet rendering.
- `exchange.py`: canonical exchange row model and CSV/Markdown writing.
- `safety.py`: PHI/secrets pattern scanning and public-demo safety checks.
- `adapters/evidence_binder.py`: export evidence binder rows.
- `adapters/ephi_mapper.py`: import ePHI flows from CSV.
- `adapters/vendor_risk.py`: import vendor register from CSV.

Acceptance criteria:

- `scripts/build.py` uses package functions.
- Existing CLI/script behavior remains backward compatible.
- Tests import package modules directly.

### Capability 2: Practice Profile Validation

Add schema-style validation for profile files.

Required top-level sections:

- `practice`
- `readiness`
- `systems`
- `flows`
- `vendors`
- `ai_workflows`
- `downtime`

Required `practice` fields:

- `name`
- `type`
- `staff_count`
- `locations`
- `review_period`
- `security_owner`
- `technical_owner`

Required `readiness` booleans:

- `mfa_email`
- `mfa_ehr`
- `unique_accounts`
- `quarterly_access_review`
- `tested_backups`
- `vendor_inventory`
- `baa_register`
- `incident_contact_list`
- `downtime_plan`
- `security_training_current`
- `log_review_cadence`

Required `systems` fields:

- `name`
- `category`
- `ephi_role`
- `owner`
- `vendor`
- `access_method`
- `evidence_needed`

Required `flows` fields:

- `id`
- `source`
- `destination`
- `ephi_type`
- `vendor`
- `transmission`
- `baa_needed`
- `risk`
- `evidence_needed`

Required `vendors` fields:

- `name`
- `service`
- `touches_ephi`
- `baa_status`
- `ai_training_use`
- `subcontractors_known`
- `incident_notification_terms`
- `risk`

Required `ai_workflows` fields:

- `name`
- `proposed_use`
- `data_used`
- `vendor`
- `decision`
- `evidence_needed`

Required `downtime` fields:

- `critical_systems`
- `last_restore_test`
- `downtime_plan_status`
- `tabletop_status`

Add:

```text
schemas/practice-profile.schema.json
```

The schema file can be documentation-grade JSON Schema even if runtime validation is implemented with standard library checks.

Acceptance criteria:

- Valid sample passes.
- Missing top-level section fails clearly.
- Missing nested required field fails clearly.
- Invalid boolean in readiness fails clearly.
- Invalid `risk` value fails clearly.
- Invalid AI decision value fails clearly.

Allowed risk values:

- `low`
- `medium`
- `high`
- `critical`

Allowed AI decisions:

- `allowed`
- `restricted`
- `prohibited`

### Capability 3: Canonical Exchange Contract

All adapters should normalize into one shared record shape.

Fields:

- `source_repo`
- `source_artifact`
- `item_id`
- `module`
- `title`
- `status`
- `risk`
- `owner`
- `evidence_needed`
- `evidence_reference`
- `source_mapping`
- `next_review_due`
- `notes`

Add an `ExchangeRecord` representation in `exchange.py`.

Functions:

- `records_to_csv(records, path)`
- `records_to_markdown(records, path, title)`
- `records_from_csv(path)`
- `validate_exchange_records(records)`

Acceptance criteria:

- Evidence binder export uses this contract internally.
- ePHI import can emit exchange rows.
- Vendor import can emit exchange rows.
- Tests verify headers and required fields.

### Capability 4: Evidence Binder Export

Implement export to the companion evidence binder.

Add:

```text
small_practice_security_kit/adapters/evidence_binder.py
scripts/export_binder_index.py
docs/import-plans/hipaa-evidence-binder-template.md
examples/exports/evidence-binder/
```

Script usage:

```bash
python scripts/export_binder_index.py samples/family_dental_clinic.yaml
python scripts/export_binder_index.py samples/family_dental_clinic.yaml --output out/family_dental_clinic/evidence-binder-export
```

Outputs:

```text
out/family_dental_clinic/evidence-binder-export/
├── evidence-binder-index.csv
├── evidence-binder-index.md
└── binder-import-notes.md
```

CSV headers:

- `evidence_id`
- `section`
- `evidence_type`
- `owner_role`
- `priority`
- `review_frequency`
- `evidence_needed`
- `evidence_reference`
- `source_mapping`
- `share_safety`
- `notes`

Export must include rows for:

- ePHI flows,
- vendors/BAAs,
- access review,
- backup restore test,
- downtime plan/tabletop,
- AI workflow policy/guidance,
- log review cadence,
- management review.

Mapping guidance:

- ePHI flow rows -> `03_ephi_systems_data_flows/ephi_flow_register.md`
- vendor rows -> `07_vendors_baas/vendor_baa_register.md`
- access rows -> `04_access/access_review.md`
- backup rows -> `06_backups_downtime_incidents/backup_restore_test.md`
- downtime rows -> `06_backups_downtime_incidents/downtime_drill.md`
- AI rows -> `05-ai-workflow-review` plus binder notes until a dedicated binder section exists
- log review rows -> `10_monitoring/log_review_record.md`
- management rows -> `11_reviews_signoffs/management_review_signoff.md`

Acceptance criteria:

- Export command creates all three output files.
- Export output has no PHI/secrets patterns.
- Export references `hipaa-evidence-binder-template`.
- Tests assert expected headers and key rows.
- README documents the command.

### Capability 5: ePHI Flow Import

Implement import from an ePHI flow CSV into the practice profile.

Add:

```text
small_practice_security_kit/adapters/ephi_mapper.py
scripts/import_ephi_flows.py
schemas/ephi-flows.schema.json
docs/import-plans/ephi-data-flow-mapper.md
examples/imports/ephi-data-flow-mapper/flows.csv
```

Script usage:

```bash
python scripts/import_ephi_flows.py examples/imports/ephi-data-flow-mapper/flows.csv \
  --base samples/family_dental_clinic.yaml \
  --output out/family_dental_clinic/imported-ephi-profile.yaml
```

CSV headers:

- `id`
- `source`
- `destination`
- `ephi_type`
- `vendor`
- `transmission`
- `baa_needed`
- `risk`
- `evidence_needed`

Outputs:

- updated profile YAML,
- `imported-ephi-flows.md`,
- normalized exchange CSV.

Acceptance criteria:

- Importer replaces or appends flows based on a flag:
  - default: replace flows,
  - `--append`: append flows.
- Imported profile builds successfully.
- Imported flows appear in `ephi-flow-map.md`.
- Missing required CSV columns fail clearly.
- Invalid boolean/risk values fail clearly.
- Tests cover valid import, append mode, and missing column failure.

### Capability 6: Vendor Register Import

Implement import from lightweight vendor register CSV into the practice profile.

Add:

```text
small_practice_security_kit/adapters/vendor_risk.py
scripts/import_vendor_register.py
schemas/vendor-register.schema.json
docs/import-plans/vendor-risk-manager.md
examples/imports/vendor-risk-manager/vendor_register.csv
```

Script usage:

```bash
python scripts/import_vendor_register.py examples/imports/vendor-risk-manager/vendor_register.csv \
  --base samples/family_dental_clinic.yaml \
  --output out/family_dental_clinic/imported-vendor-profile.yaml
```

CSV headers:

- `name`
- `service`
- `touches_ephi`
- `baa_status`
- `ai_training_use`
- `subcontractors_known`
- `incident_notification_terms`
- `risk`

Outputs:

- updated profile YAML,
- `imported-vendor-register.md`,
- normalized exchange CSV.

Acceptance criteria:

- Importer replaces or appends vendors based on a flag:
  - default: replace vendors,
  - `--append`: append vendors.
- Imported profile builds successfully.
- Imported vendors appear in `vendor-baa-review.md`.
- High-risk or missing-BAA vendors create evidence needs.
- Missing required CSV columns fail clearly.
- Invalid boolean/risk values fail clearly.
- Tests cover valid import, append mode, and missing column failure.

### Capability 7: Public Safety Scanning

Centralize sensitive pattern detection in `safety.py`.

Detect at minimum:

- MRN-like labels,
- `Patient Name:` labels,
- DOB labels,
- diagnosis labels,
- SSN-like values,
- API key labels,
- password labels,
- token labels,
- private key blocks.

Functions:

- `find_sensitive_patterns(text)`
- `scan_file(path)`
- `scan_tree(path)`
- `assert_safe_tree(path)`

Update:

- `scripts/validate_content.py`

Acceptance criteria:

- Existing public sample passes.
- Tests confirm PHI-like pattern fails.
- Tests confirm secret-like pattern fails.
- `out/` generated files pass.

### Capability 8: Better CI

Update:

```text
.github/workflows/ci.yml
```

CI should run:

```bash
python -m pip install -r requirements.txt
python scripts/build.py samples/family_dental_clinic.yaml
python scripts/export_binder_index.py samples/family_dental_clinic.yaml
python scripts/import_ephi_flows.py examples/imports/ephi-data-flow-mapper/flows.csv --base samples/family_dental_clinic.yaml --output out/family_dental_clinic/imported-ephi-profile.yaml
python scripts/build.py out/family_dental_clinic/imported-ephi-profile.yaml
python scripts/import_vendor_register.py examples/imports/vendor-risk-manager/vendor_register.csv --base samples/family_dental_clinic.yaml --output out/family_dental_clinic/imported-vendor-profile.yaml
python scripts/build.py out/family_dental_clinic/imported-vendor-profile.yaml
python scripts/validate_content.py
python -m unittest discover -s tests
```

Acceptance criteria:

- CI passes locally using the same command sequence.
- GitHub Actions passes after push.

### Capability 9: Docs and README Refresh

Update:

- `README.md`
- `docs/import-plans/existing-repos.md`
- `docs/flagship-positioning.md`
- `docs/product-map.md`

Add:

- `docs/import-plans/hipaa-evidence-binder-template.md`
- `docs/import-plans/ephi-data-flow-mapper.md`
- `docs/import-plans/vendor-risk-manager.md`
- `docs/adapter-contract.md`
- `docs/public-demo-safety.md`

README must include:

- quick start,
- build sample packet,
- export binder index,
- import ePHI flows,
- import vendor register,
- validation/test commands,
- safety model,
- companion repo map,
- first three integrations.

Acceptance criteria:

- README commands work.
- Docs do not overclaim compliance.
- Docs state outputs are evidence references, not legal/compliance certification.

### Capability 10: Tests

Expand tests beyond current build tests.

Add or update:

```text
tests/test_profile_validation.py
tests/test_exchange.py
tests/test_evidence_binder_export.py
tests/test_ephi_import.py
tests/test_vendor_import.py
tests/test_safety.py
tests/test_build.py
```

Test cases:

- valid sample builds,
- missing profile section fails,
- missing required field fails,
- invalid risk fails,
- invalid AI decision fails,
- exchange record CSV headers are stable,
- evidence binder export writes CSV/Markdown/notes,
- evidence binder export includes required rows,
- ePHI import valid CSV,
- ePHI import missing column failure,
- ePHI import append mode,
- vendor import valid CSV,
- vendor import missing column failure,
- vendor import append mode,
- safety scan catches PHI-like pattern,
- safety scan catches secret-like pattern,
- generated out tree passes safety scan,
- HTML packet contains table markup and print CSS.

Acceptance criteria:

- Test suite passes locally.
- CI passes.

## Implementation Sequence

### Step 1: Package Refactor

Move current logic from `scripts/build.py` into:

- `profile.py`
- `packet.py`
- `validation.py`
- `safety.py`

Keep `scripts/build.py` as thin wrapper.

### Step 2: Evidence Binder Export

Build the first adapter completely.

This proves the architecture.

### Step 3: ePHI Flow Import

Build import flow and schema.

### Step 4: Vendor Register Import

Build vendor import and schema.

### Step 5: Docs/CI/Test Hardening

Update README, docs, CI, and tests.

### Step 6: Public Demo Refresh

Regenerate sample outputs and ensure generated public packet is safe.

## Local Validation Commands

Run all before committing:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/build.py samples/family_dental_clinic.yaml
.venv/bin/python scripts/export_binder_index.py samples/family_dental_clinic.yaml
.venv/bin/python scripts/import_ephi_flows.py examples/imports/ephi-data-flow-mapper/flows.csv --base samples/family_dental_clinic.yaml --output out/family_dental_clinic/imported-ephi-profile.yaml
.venv/bin/python scripts/build.py out/family_dental_clinic/imported-ephi-profile.yaml
.venv/bin/python scripts/import_vendor_register.py examples/imports/vendor-risk-manager/vendor_register.csv --base samples/family_dental_clinic.yaml --output out/family_dental_clinic/imported-vendor-profile.yaml
.venv/bin/python scripts/build.py out/family_dental_clinic/imported-vendor-profile.yaml
.venv/bin/python scripts/validate_content.py
.venv/bin/python -m unittest discover -s tests
```

## Definition of Done

This goal is complete when:

- Internal package exists and scripts use it.
- Profile validation is reusable and tested.
- Evidence binder export works and is tested.
- ePHI flow import works and is tested.
- Vendor register import works and is tested.
- Canonical exchange contract is implemented and documented.
- Safety scanning is centralized and tested.
- CI runs build, export, imports, validation, and tests.
- README documents all new commands.
- Import plan docs exist for the first three companion repos.
- Public generated artifacts remain fictional and pass safety checks.
- All validation commands pass locally.
- Changes are committed and pushed to `main`.

## Suggested Branch Name

```text
feature/repo-integration-adapters
```

## Suggested Commit Message

```text
Implement repo integration adapters
```

## Portfolio Bullet Target

Built the first integration layer for an open-source small healthcare practice security kit, adding reusable Python package architecture, validated practice profiles, HIPAA evidence binder exports, ePHI flow imports, vendor/BAA register imports, canonical exchange records, PHI/secrets safety checks, CI, and source-grounded public documentation.

