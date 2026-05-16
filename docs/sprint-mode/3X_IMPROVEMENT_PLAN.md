# Sprint Mode 3x Improvement Plan

Date: 2026-05-16

Scope: second-pass improvement of the public `small-practice-security-kit` Sprint Mode runner for the Velari Cyber Readiness Sprint.

Research basis: repo docs, sibling private app Sprint Mode docs, Dario planning notes, and a compact live web check. External references used for direction only: HHS Cyber Gateway (`https://hhscyber.hhs.gov/`), HHS/ASPR HPH Cybersecurity Performance Goals resource (`https://asprtracie.hhs.gov/technical-resources/resource/12863/healthcare-and-public-health-sector-specific-cybersecurity-performance-goals`), CISA Cross-Sector Cybersecurity Performance Goals (`https://www.cisa.gov/cybersecurity-performance-goals-cpgs`), and HHS AI Strategic Plan material (`https://www.healthit.gov/sites/default/files/2025-01/2025%20HHS%20AI%20Strategic%20Plan_Full_508.pdf`).

## 1. Current State Audit

What works:

- The public runner already builds the sprint packet with one command.
- The existing outputs cover stage status, risk rows, evidence references, handoff rows, packet artifacts, and binder-compatible exports.
- The synthetic sample has useful small-practice pressure points: EHR MFA, access review, stale backup restore evidence, vendor/BAA gaps, AI workflow boundaries, and cyber insurance evidence pressure.
- The first-pass docs define clear boundaries: reference-only evidence, no PHI, no secrets, no certification, no legal advice, and no incident reporting decision.
- Tests already cover CLI output creation, expected stage ordering, reference-only evidence exports, and sensitive-data blocking.

What still feels thin:

- A buyer/MSP still has to open several files to understand status, risks, evidence gaps, and handoff actions.
- The generated JSON files are useful but not contract-grade for the future private app importer.
- `risk-register.csv` and `handoff-actions.csv` are close to importable task rows but need stronger audience, recipient, owner, artifact, and 30/60/90 fields.
- There is no polished local readout artifact that can be opened first in a demo.
- The safety boundary is present, but the new first-open artifact should make no-PHI/no-certification limits impossible to miss.

What would stop Noah from proudly showing it:

- The first artifact is Markdown, not a command center that shows the sprint in one glance.
- The private app integration story relies on prose rather than schemas and validation tests.
- The action exports do not yet look like clean task seeds for owner, MSP, vendor, and legal/compliance lanes.
- Evidence gaps are present, but not summarized in the executive readout by stage and owner.

## 2. Improvement Candidates Ranked By Leverage

1. Add `sprint-command-center.html` as a self-contained local first-open artifact.
2. Add schemas for `sprint-summary.json` and `evidence-index.json`.
3. Strengthen `handoff-actions.csv` and `risk-register.csv` with audience, recipient, owner, stage, priority, artifact, evidence reference, and 30/60/90 bucket fields.
4. Add `sprint-client-readout.md` for a portable concise client readout.
5. Enrich `sprint-summary.json` with readiness signal, delivery signal, top risks, evidence gap summary, handoff lanes, and schema pointers.
6. Add tests that generated Sprint outputs validate against the new schemas.
7. Add tests that command-center/readout/action outputs remain reference-only and avoid overclaim language.
8. Update output-map, product contract, delivery playbook, and README so users open the command center first.
9. Add generated artifact size/existence verification for new HTML/readout/schema outputs.
10. Add optional future ZIP/PDF export and signed receipt fields.

## 3. Chosen Implementation Set For This Pass

Implemented in this pass:

- `sprint-command-center.html`
- `sprint-client-readout.md`
- `schemas/sprint-summary.schema.json`
- `schemas/evidence-index.schema.json`
- Enriched `sprint-summary.json`
- Expanded `risk-register.csv`
- Expanded `handoff-actions.csv`
- Tests for output existence, schemas, action row fields, reference-only safety, and overclaim guardrails
- README and sprint-mode docs updates
- `docs/sprint-mode/3X_FINAL_STATUS.md`

Rationale: these changes directly improve demo/readout quality, data contract quality, actionability, trust/safety, and presentation without changing the public CLI behavior or adding private app dependencies.

## 4. Deferred Suggestions With Rationale

- PDF/ZIP packaging: useful for delivery, but less important than a single local HTML command center and stable data contracts.
- Private app import UI: belongs in `velari-secure-practice`, not this public runner pass.
- Receipt signing/attestation: valuable later, but the packet and schema contract should stabilize first.
- Hosted storage, auth, EHR, Microsoft 365, Google Workspace, insurer, vendor, or AI integrations: outside the public proof runner boundary.
- Real contract/log/screenshot ingestion: intentionally deferred because this repo must remain PHI-avoidant and reference-only.

## 5. Acceptance Criteria For 3x Better

- Demo/readout quality: a buyer/MSP can open `sprint-command-center.html` and understand sprint status, top risks, evidence gaps, handoff lanes, and generated artifacts without opening CSV/JSON first.
- Data contract quality: `sprint-summary.json` and `evidence-index.json` have schema files and validation tests.
- Actionability: risk and handoff exports include audience/recipient, owner, stage, priority, evidence/artifact references, and 30/60/90 bucket fields.
- Trust/safety: new artifacts repeat the no-PHI/no-secrets/no-certification boundary and tests scan for patient identifier placeholders and overclaim phrases.
- Design/presentation: Sprint Mode produces a polished self-contained local HTML artifact and a concise Markdown readout.
- Compatibility: existing CLI behavior and packet outputs remain intact.

## 6. Verification Commands And Results

Planned required verification:

```bash
python3 -m unittest discover -s tests
python3 scripts/validate_content.py
python3 -m small_practice_security_kit validate samples/family_dental_clinic.yaml
python3 -m small_practice_security_kit sprint samples/family_dental_clinic.yaml --output-root /tmp/velari-public-sprint-3x-smoke
git diff --check
```

Planned artifact verification:

```bash
find /tmp/velari-public-sprint-3x-smoke/family_dental_clinic -maxdepth 2 -type f -name 'sprint-*' -o -name '*schema.json'
wc -c /tmp/velari-public-sprint-3x-smoke/family_dental_clinic/sprint-command-center.html
wc -c /tmp/velari-public-sprint-3x-smoke/family_dental_clinic/sprint-client-readout.md
```

Results:

- `python3 -m unittest discover -s tests`: passed, 49 tests.
- `python3 scripts/validate_content.py`: passed.
- `python3 -m small_practice_security_kit validate samples/family_dental_clinic.yaml`: passed.
- `python3 -m small_practice_security_kit sprint samples/family_dental_clinic.yaml --output-root /tmp/velari-public-sprint-3x-smoke`: passed.
- `git diff --check`: passed.
- Smoke output directory: `/tmp/velari-public-sprint-3x-smoke/family_dental_clinic`.
- New artifact sizes:
  - `sprint-command-center.html`: 22,937 bytes.
  - `sprint-client-readout.md`: 3,714 bytes.
  - `sprint-summary.json`: 14,590 bytes.
  - `evidence-index.json`: 10,738 bytes.
