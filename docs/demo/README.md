# Synthetic Demo Packet

This directory contains a complete public demo generated from [`samples/family_dental_clinic.yaml`](../../samples/family_dental_clinic.yaml).

The demo is fictional. It is designed to show how a small healthcare practice could organize a first-pass security readiness conversation without uploading PHI, credentials, private contracts, private incident details, or raw evidence files.

## Scenario

**Family Dental Clinic** is a fictional 14-person dental practice with one location, a cloud EHR, billing portal, shared drive, email workflows, an MSP, and staff interest in AI-assisted administrative work.

The sample intentionally includes realistic gaps:

- EHR MFA needs verification/enforcement.
- Quarterly access review is not documented.
- Backup restore evidence is missing.
- BAA register review dates are incomplete.
- Public-site tracker and TLS observations need website vendor, MSP, and qualified-review follow-up.
- Downtime plan and tabletop evidence are missing.
- AI workflow rules need clearer allowed/restricted/prohibited examples.

## Start here

- Practice Assurance Packet: [`practice-assurance-packet.html`](practice-assurance-packet.html)
- Markdown copy with 10-minute intake and owner decision queue: [`practice-assurance-packet.md`](practice-assurance-packet.md)
- External Evidence Pre-Check: [`external-evidence-precheck.md`](external-evidence-precheck.md)
- Complete packet, Markdown: [`review-packet.md`](review-packet.md)
- Complete packet, print-friendly HTML: [`review-packet.html`](review-packet.html)
- Canonical manifest and hashes: [`packet-manifest.json`](packet-manifest.json)
- Sprint client readout: [`sprint-client-readout.md`](sprint-client-readout.md)
- Sprint summary JSON: [`sprint-summary.json`](sprint-summary.json)
- Action CSVs: [`risk-register.csv`](risk-register.csv), [`handoff-actions.csv`](handoff-actions.csv)
- Review packet screenshot: [`screenshots/review-packet.png`](screenshots/review-packet.png)

## Packet sections

- [`readiness-review.md`](readiness-review.md) — baseline readiness review.
- [`ephi-flow-map.md`](ephi-flow-map.md) — patient-data-outside-the-EHR map for systems, vendors, and flows.
- [`vendor-baa-review.md`](vendor-baa-review.md) — vendor, BAA, SOC 2/HITRUST evidence status, incident terms, subcontractor, and AI data-use review.
- [`ai-workflow-review.md`](ai-workflow-review.md) — allowed, restricted, and prohibited AI workflow review.
- [`downtime-ransomware-tabletop.md`](downtime-ransomware-tabletop.md) — downtime/tabletop starter packet.
- [`connected-device-inventory.md`](connected-device-inventory.md) — IoMT/connected-device worksheet for vendor, patch owner, default credentials, fallback, and safety notices.
- [`portal-api-flow-review.md`](portal-api-flow-review.md) — portal, app, API/FHIR-style flow worksheet for identity, logs, messaging, ownership, and export/delete evidence.
- [`external-evidence-precheck.md`](external-evidence-precheck.md) — reference-only tracker, scheduler, portal, TLS, and certificate observations translated into safe follow-up questions.
- [`incident-decision-log.md`](incident-decision-log.md) — decision-log template separating technical containment from qualified legal/compliance decisions.
- [`evidence-binder-index.md`](evidence-binder-index.md) — evidence references to collect.
- [`owner-msp-handoff.md`](owner-msp-handoff.md) — owner/MSP action handoff.
- [`30-60-90-roadmap.md`](30-60-90-roadmap.md) — prioritized remediation plan.
- [`limitations-appendix.md`](limitations-appendix.md) — what the packet does and does not prove.

## Sprint action artifacts

- [`practice-assurance-packet.html`](practice-assurance-packet.html) — polished buyer-facing report for the practice owner/MSP conversation, including 10-minute intake and owner decision queue.
- [`practice-assurance-packet.md`](practice-assurance-packet.md) — plain Markdown copy of the same report.
- [`external-evidence-precheck.md`](external-evidence-precheck.md) — public-site observation handoff for website vendor, MSP, and qualified-review questions.
- [`sprint-index.md`](sprint-index.md) — entry point for generated Sprint Mode outputs.
- [`sprint-client-readout.md`](sprint-client-readout.md) — owner-facing action packet summary.
- [`sprint-command-center.html`](sprint-command-center.html) — self-contained HTML command center.
- [`sprint-offering-readout.md`](sprint-offering-readout.md) — offering readout with owner/MSP/vendor/reviewer questions.
- [`owner-action-plan.md`](owner-action-plan.md) — first-week owner plan.
- [`msp-remediation-brief.md`](msp-remediation-brief.md) — MSP evidence support and remediation brief.
- [`vendor-baa-ai-questionnaire.md`](vendor-baa-ai-questionnaire.md) — vendor, BAA, and AI data-use questionnaire.
- [`evidence-collection-checklist.md`](evidence-collection-checklist.md) — reference-only evidence collection checklist.
- [`sprint-summary.json`](sprint-summary.json) — structured Sprint summary with top action-packet risks.
- [`evidence-index.json`](evidence-index.json) — structured evidence reference index.
- [`risk-register.csv`](risk-register.csv) and [`handoff-actions.csv`](handoff-actions.csv) — sortable action rows with owner, MSP, vendor, legal/compliance, and technical reviewer views.

## Evidence boundary

The demo stores **references and summaries only**. Public demo artifacts should never include:

- patient names,
- MRNs,
- DOBs,
- diagnoses,
- clinical notes,
- claim narratives,
- real incident details,
- passwords,
- API keys,
- private keys,
- private URLs or presigned links,
- full private contracts or BAAs.

The full data-boundary model lives in [`../security-model.md`](../security-model.md).

## Regenerate locally

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/build.py samples/family_dental_clinic.yaml
.venv/bin/python -m small_practice_security_kit sprint samples/family_dental_clinic.yaml --output-root out
.venv/bin/python scripts/export_binder_index.py samples/family_dental_clinic.yaml
.venv/bin/python -m small_practice_security_kit export-demo --profile samples/family_dental_clinic.yaml --output docs/demo
.venv/bin/python scripts/validate_content.py
.venv/bin/python -m unittest discover -s tests
```

Generated runtime files appear under `out/family_dental_clinic/`. This checked-in demo directory is the public, safe snapshot.
