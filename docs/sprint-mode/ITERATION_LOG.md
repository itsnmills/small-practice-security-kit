# Sprint Mode Iteration Log

Date: 2026-05-16

## Loop 1: Research/Domain

Status: complete

Inputs reviewed:

- `CODEX_GOAL.md`
- Current README, CLI, packet, manifest, profile, demo export, sensitive-data, sample, tests, and safety docs.
- Dario Sprint Mode, consolidation, and overlap audit notes.
- HHS/OCR, HHS HPH CPG, FTC, NAIC, NIST, and CMS public guidance.

Decisions:

- Treat Sprint Mode as an orchestration layer over the existing public packet generator.
- Keep the wedge around patient data outside the EHR, then tie each gap to owner/MSP evidence.
- Avoid compliance, legal, breach, or insurer acceptance claims.

## Loop 2: Architecture/Data Model

Status: complete

Decisions:

- Use the existing practice profile as the source of truth.
- Keep generated packet outputs in the existing practice slug directory.
- Add stage statuses with the vocabulary `not_started`, `needs_evidence`, `ready_for_review`, and `complete`.
- Use `packet-manifest.json` as the canonical packet manifest and add `evidence-index.json` as the Sprint Mode evidence overlay.

Artifacts planned:

- `sprint-summary.json` for machine-readable stage status.
- `risk-register.csv` for owner/MSP action tracking.
- `handoff-actions.csv` for owner, MSP, vendor, and reviewer questions.
- `sprint-index.md` for the human starting point.

## Loop 3: Implementation

Status: complete

Implemented:

- New `small_practice_security_kit.sprint` module.
- New CLI command: `python3 -m small_practice_security_kit sprint samples/family_dental_clinic.yaml --output-root out`.
- Existing packet builder and binder exporter are called before Sprint Mode overlay files are written.
- Sensitive-data blocking runs before output generation.

## Loop 4: Domain Usefulness and Copy

Status: complete

Updated:

- Demo profile now includes a richer synthetic dental scenario with imaging, messaging, shared drive, staff AI drafting, AI scribe pilot, stale backup evidence, unclear access review, missing/unknown BAA evidence, and cyber insurance evidence references.
- Sprint Mode docs describe what the offer is and is not.
- Output copy uses evidence posture and next actions rather than compliance scores.

## Loop 5: QA/Security/Hardening

Status: complete

Checks planned and run before final status:

- `python3 -m unittest discover -s tests`
- `python3 scripts/validate_content.py`
- `python3 -m small_practice_security_kit validate samples/family_dental_clinic.yaml`
- `python3 -m small_practice_security_kit build samples/family_dental_clinic.yaml --output-root /tmp/velari-public-build-smoke`
- `python3 -m small_practice_security_kit sprint samples/family_dental_clinic.yaml --output-root /tmp/velari-public-sprint-smoke`
- `git diff --check`

Hardening decisions:

- Do not store raw evidence in Sprint Mode outputs.
- Keep source profile paths non-absolute through the existing manifest model.
- Keep generated outputs in Markdown, JSON, and CSV with explicit no-PHI/no-secret boundaries.
