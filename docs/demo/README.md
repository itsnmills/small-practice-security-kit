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
- Downtime plan and tabletop evidence are missing.
- AI workflow rules need clearer allowed/restricted/prohibited examples.

## Start here

- Complete packet, Markdown: [`review-packet.md`](review-packet.md)
- Complete packet, print-friendly HTML: [`review-packet.html`](review-packet.html)
- Canonical manifest and hashes: [`packet-manifest.json`](packet-manifest.json)
- Review packet screenshot: [`screenshots/review-packet.png`](screenshots/review-packet.png)

## Packet sections

- [`readiness-review.md`](readiness-review.md) — baseline readiness review.
- [`ephi-flow-map.md`](ephi-flow-map.md) — patient-data-outside-the-EHR map for systems, vendors, and flows.
- [`vendor-baa-review.md`](vendor-baa-review.md) — vendor, BAA, SOC 2/HITRUST evidence status, incident terms, subcontractor, and AI data-use review.
- [`ai-workflow-review.md`](ai-workflow-review.md) — allowed, restricted, and prohibited AI workflow review.
- [`downtime-ransomware-tabletop.md`](downtime-ransomware-tabletop.md) — downtime/tabletop starter packet.
- [`connected-device-inventory.md`](connected-device-inventory.md) — IoMT/connected-device worksheet for vendor, patch owner, default credentials, fallback, and safety notices.
- [`portal-api-flow-review.md`](portal-api-flow-review.md) — portal, app, API/FHIR-style flow worksheet for identity, logs, messaging, ownership, and export/delete evidence.
- [`incident-decision-log.md`](incident-decision-log.md) — decision-log template separating technical containment from qualified legal/compliance decisions.
- [`evidence-binder-index.md`](evidence-binder-index.md) — evidence references to collect.
- [`owner-msp-handoff.md`](owner-msp-handoff.md) — owner/MSP action handoff.
- [`30-60-90-roadmap.md`](30-60-90-roadmap.md) — prioritized remediation plan.
- [`limitations-appendix.md`](limitations-appendix.md) — what the packet does and does not prove.

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
.venv/bin/python scripts/export_binder_index.py samples/family_dental_clinic.yaml
.venv/bin/python scripts/validate_content.py
.venv/bin/python -m unittest discover -s tests
```

Generated runtime files appear under `out/family_dental_clinic/`. This checked-in demo directory is the public, safe snapshot.
