# Implementation Start Plan

## Goal

Start turning `small-practice-security-kit` from a standalone packet generator into the public front door for the existing `itsnmills` healthcare security repo ecosystem.

The first implementation wave should be small enough to ship cleanly, but foundational enough that future adapters follow the same pattern.

## Recommended Starting Slice

Build the first wave around three repo connections:

1. `hipaa-evidence-binder-template`
2. `ephi-data-flow-mapper`
3. `vendor-risk-manager`

Why these first:

- The evidence binder is already the strongest local-first evidence operating system.
- The ePHI mapper is the most clinic-useful star module.
- Vendor/BAA review turns ePHI flows into concrete follow-up work.

This gives the public kit a full loop:

```text
practice profile -> ePHI flows -> vendor review -> evidence binder export -> review packet
```

## Architecture Direction

Add a small internal package rather than letting `scripts/` become a pile of one-off files.

Proposed structure:

```text
small_practice_security_kit/
├── __init__.py
├── profile.py
├── validation.py
├── packet.py
├── exchange.py
├── adapters/
│   ├── __init__.py
│   ├── evidence_binder.py
│   ├── ephi_mapper.py
│   └── vendor_risk.py
└── safety.py
```

Keep backwards-compatible scripts:

```text
scripts/build.py
scripts/validate_content.py
scripts/export_binder_index.py
scripts/import_ephi_flows.py
scripts/import_vendor_register.py
```

## Canonical Exchange Contract

Every adapter should normalize records into one exchange row shape:

```yaml
source_repo: hipaa-evidence-binder-template
source_artifact: out/family_dental_clinic/evidence-binder-index.md
item_id: ACCESS-QTR
module: 03-hipaa-evidence-binder
title: Quarterly access review
status: not_started
risk: high
owner: Office Manager
evidence_needed: Quarterly access review for EHR, billing, email, remote access
evidence_reference: restricted-evidence/access/q2-access-review.xlsx
source_mapping: HIPAA Security Rule; NIST SP 800-66r2
next_review_due: ""
notes: Generated from Small Practice Security Kit profile
```

Required normalized fields:

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

## Phase 1: Internal Package and Profile Validation

### Files

Add:

- `small_practice_security_kit/__init__.py`
- `small_practice_security_kit/profile.py`
- `small_practice_security_kit/validation.py`
- `small_practice_security_kit/safety.py`
- `schemas/practice-profile.schema.json`

Update:

- `scripts/build.py`
- `scripts/validate_content.py`
- `tests/test_build.py`

### Work

- Move YAML loading, slugging, risk scoring, packet rendering, and safety checks into reusable package functions.
- Add schema-style validation for required profile sections:
  - `practice`
  - `readiness`
  - `systems`
  - `flows`
  - `vendors`
  - `ai_workflows`
  - `downtime`
- Keep dependencies light. Use standard library validation first unless a dependency clearly earns its place.
- Keep existing commands working.

### Acceptance Criteria

- Existing sample still builds.
- Missing required profile sections fail with clear errors.
- Safety validation still catches PHI/secret-like patterns.
- Tests pass.

## Phase 2: Evidence Binder Export

### Files

Add:

- `small_practice_security_kit/adapters/evidence_binder.py`
- `scripts/export_binder_index.py`
- `docs/import-plans/hipaa-evidence-binder-template.md`
- `examples/exports/evidence-binder/`

### Work

Generate binder-compatible exports:

- `evidence-binder-index.csv`
- `evidence-binder-index.md`
- `binder-import-notes.md`

The export should map this kit's evidence needs into fields usable by `hipaa-evidence-binder-template`.

Proposed CSV headers:

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

### Acceptance Criteria

- Running `scripts/export_binder_index.py samples/family_dental_clinic.yaml` creates CSV and Markdown exports.
- Export contains access review, backup restore, vendor BAA, AI policy, and ePHI flow evidence rows.
- Export has no PHI/secrets patterns.
- Test asserts expected headers and key rows.

## Phase 3: ePHI Mapper Import

### Files

Add:

- `small_practice_security_kit/adapters/ephi_mapper.py`
- `scripts/import_ephi_flows.py`
- `schemas/ephi-flows.schema.json`
- `docs/import-plans/ephi-data-flow-mapper.md`
- `examples/imports/ephi-data-flow-mapper/flows.csv`

### Work

Support importing ePHI flow rows into the sample profile format.

Minimum fields:

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

### Acceptance Criteria

- Importer reads CSV and emits normalized flow records.
- Imported flows appear in `ephi-flow-map.md`.
- Missing required columns fail clearly.
- Test covers valid import and missing-column failure.

## Phase 4: Vendor Risk Import

### Files

Add:

- `small_practice_security_kit/adapters/vendor_risk.py`
- `scripts/import_vendor_register.py`
- `schemas/vendor-register.schema.json`
- `docs/import-plans/vendor-risk-manager.md`
- `examples/imports/vendor-risk-manager/vendor_register.csv`

### Work

Support importing a lightweight vendor register from `vendor-risk-manager` or compatible CSV.

Minimum fields:

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
- `vendor-baa-review.md`,
- normalized exchange CSV.

### Acceptance Criteria

- Importer reads CSV and emits normalized vendor records.
- Vendor rows appear in review packet.
- High-risk/missing-BAA vendors create evidence needs.
- Test covers valid import and missing-column failure.

## Phase 5: CI and Demo Refresh

### Files

Update:

- `.github/workflows/ci.yml`
- `README.md`
- `docs/flagship-positioning.md`
- `tests/test_build.py`

### Work

CI should run:

```bash
python scripts/build.py samples/family_dental_clinic.yaml
python scripts/export_binder_index.py samples/family_dental_clinic.yaml
python scripts/import_ephi_flows.py examples/imports/ephi-data-flow-mapper/flows.csv --base samples/family_dental_clinic.yaml --output out/imported-profile.yaml
python scripts/import_vendor_register.py examples/imports/vendor-risk-manager/vendor_register.csv --base samples/family_dental_clinic.yaml --output out/vendor-profile.yaml
python scripts/validate_content.py
python -m unittest discover -s tests
```

### Acceptance Criteria

- CI passes.
- README has a "First Integrations" section.
- Generated demo output includes binder export, imported ePHI profile, and imported vendor profile.

## First PR Scope

Do not build every planned adapter in the first PR.

First PR should include:

- internal package scaffold,
- profile validation,
- evidence binder export,
- tests,
- README update,
- CI update.

Why:

- It immediately connects the flagship repo to the strongest companion repo.
- It creates the adapter pattern.
- It avoids trying to solve every import shape at once.

## Second PR Scope

Second PR:

- ePHI flow import,
- schema,
- examples,
- tests,
- demo packet refresh.

## Third PR Scope

Third PR:

- vendor register import,
- vendor evidence mapping,
- tests,
- docs.

## Follow-On Adapter Order

After the first three adapters:

1. `health-ai-governance-auditor`
2. `Strands-PHI-Guardrails-Demo`
3. `agent-audit-trail`
4. `healthcare-ai-security-lab`
5. `iomt-risk-scorer`
6. `hipaa-scanner`
7. `hipaa-compliance-engine`

Reasoning:

- AI workflow review is the strongest differentiated wedge after ePHI/vendor evidence.
- Technical triage imports become more useful once the evidence binder and ePHI/vendor context exist.

## Done Criteria for Starting Implementation

The starter implementation is done when:

- `small_practice_security_kit/` package exists.
- Profile validation is reusable.
- Evidence binder export works.
- Tests cover the export.
- CI runs the export.
- README explains the first adapter and next two planned adapters.
- Public demo remains fictional and passes safety checks.

