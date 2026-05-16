# Sprint Mode Real Offering 3x Status

Date: 2026-05-16

## Implemented Changes

- Added a maintainable offering knowledge layer in `small_practice_security_kit/offering.py` with source anchors, audience lanes, first-week actions, stage-to-source mapping, boundary statements, escalation triggers, and renderer functions.
- Turned Sprint Mode into a stronger public proof of the **Velari Cyber Readiness Sprint for Small Healthcare Practices**.
- Added seven generated, client/use-case-specific offering artifacts:
  - `sprint-offering-readout.md`
  - `owner-action-plan.md`
  - `msp-remediation-brief.md`
  - `vendor-baa-ai-questionnaire.md`
  - `evidence-collection-checklist.md`
  - `day-one-workshop-agenda.md`
  - `source-map.md`
- Enriched `sprint-command-center.html` with an Offering Mode section for value delivered, first 7 days, audience lanes, source-backed themes, and artifact checklist.
- Added `offering_summary` to `sprint-summary.json` so the private app can import the offering name, audience lanes, source anchors, first-week actions, top value outcomes, artifact list, boundary statements, escalation triggers, and stage-to-source mapping.
- Updated `schemas/sprint-summary.schema.json` and tests for the new offering contract.
- Added `docs/sprint-mode/OFFERING_BLUEPRINT.md` with positioning, scope, audience value, delivery flow, artifacts, safety boundaries, escalation lanes, and private-app mapping.
- Tightened wording across public artifacts to avoid implying legal/regulatory status, incident decisions, vendor acceptance, AI production authorization, or formal risk assessment conclusions.

## Generated Outputs

The Sprint Mode command now creates a more complete offering packet:

```bash
python3 -m small_practice_security_kit sprint samples/family_dental_clinic.yaml --output-root out
```

Primary output directory:

```text
out/family_dental_clinic/
```

Offering-specific outputs:

- `sprint-command-center.html`
- `sprint-offering-readout.md`
- `owner-action-plan.md`
- `msp-remediation-brief.md`
- `vendor-baa-ai-questionnaire.md`
- `evidence-collection-checklist.md`
- `day-one-workshop-agenda.md`
- `source-map.md`

Existing Sprint Mode contract outputs remain:

- `sprint-client-readout.md`
- `sprint-index.md`
- `sprint-summary.json`
- `risk-register.csv`
- `evidence-index.json`
- `handoff-actions.csv`
- `evidence-binder-export/`

Existing review packet outputs are preserved, including `review-packet.md`, `review-packet.html`, `packet-manifest.json`, `owner-msp-handoff.md`, and `30-60-90-roadmap.md`.

## What A Small Practice Actually Benefits From

A practice owner or office manager now receives more than a generic cyber checklist:

- A plain-English readout of what was reviewed and why it matters for patient safety and trust.
- A first 7 days plan with concrete actions and questions to send to the MSP, vendors, and reviewers.
- A technical MSP brief that asks for specific evidence such as MFA enforcement exports, user lists, backup scope, restore-test notes, admin role lists, and remote-support review.
- A vendor/BAA/AI questionnaire covering BAA status, subcontractors, incident notice, retention/deletion, AI training-use, access controls, audit logs, and export/delete capability.
- A reference-only evidence checklist so the real proof can be gathered in a private/offline binder without putting PHI, secrets, raw logs, screenshots, contracts, or incident-sensitive details in this public repo.
- A source map that explains how HHS Cyber Gateway, HHS 405(d) HICP, CISA Cybersecurity Performance Goals, and the ONC/OCR Security Risk Assessment Tool shaped the questions.
- Clear escalation triggers for MSP, vendor, legal/compliance, incident response, and formal risk-assessment review.

## Verification Results

Passed before merge/push:

```bash
python3 -m unittest discover -s tests
python3 scripts/validate_content.py
python3 -m small_practice_security_kit validate samples/family_dental_clinic.yaml
python3 -m small_practice_security_kit sprint samples/family_dental_clinic.yaml --output-root /tmp/velari-public-sprint-real-offering-smoke
python3 -m pytest -q
git diff --check
```

Results:

- Unit tests: passed, 50 tests.
- Content validation: passed.
- Sample profile validation: passed.
- Sprint smoke build: passed.
- Pytest suite: passed, 50 tests and 20 subtests.
- Whitespace check: passed.

Smoke output from `/tmp/velari-public-sprint-real-offering-smoke-jarvis/family_dental_clinic` included non-empty offering artifacts:

- `sprint-offering-readout.md`: 9,064 bytes
- `owner-action-plan.md`: 4,763 bytes
- `msp-remediation-brief.md`: 4,458 bytes
- `vendor-baa-ai-questionnaire.md`: 3,786 bytes
- `evidence-collection-checklist.md`: 4,368 bytes
- `day-one-workshop-agenda.md`: 3,003 bytes
- `source-map.md`: 5,315 bytes
- `sprint-command-center.html`: 30,542 bytes
- `sprint-summary.json`: 34,473 bytes

## Remaining Deferred Improvements

- Private `velari-secure-practice` reviewed import UI for `offering_summary`, `sprint-summary.json`, `evidence-index.json`, `risk-register.csv`, `handoff-actions.csv`, and `packet-manifest.json`.
- PDF/ZIP delivery packaging for a client handoff bundle.
- Optional receipt signing or attestation hash fields for packet integrity.
- Hosted auth/storage/integration work for Microsoft 365, Google Workspace, EHR context, cyber insurance questionnaires, vendor portals, or AI governance systems.
- Real raw-evidence handling remains out of scope for the public runner and belongs only in a private, access-controlled workflow.

## Private App Integration Improvement

This pass gives `velari-secure-practice` a stronger import contract:

- `offering_summary.audience_lanes` can seed owner, MSP, vendor, and legal/compliance task lanes.
- `offering_summary.first_7_days_actions` can seed a first-week implementation checklist.
- `offering_summary.source_anchors` and `stage_source_map` can power explainability and reviewer context in the private app.
- `offering_summary.artifact_list` can drive a client packet/download surface.
- `boundary_statements` and `escalation_triggers` can become hard UI warnings before any private evidence import.

The public repo remains local-first, synthetic/reference-only, and bounded as an offering proof rather than a production evidence store.
