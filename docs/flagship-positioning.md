# Flagship Positioning

The public story:

> A local-first healthcare security readiness kit for small practices that need practical ePHI, vendor/BAA, AI, downtime, ransomware-readiness, and evidence-reference workflows without buying enterprise GRC software.

## Why this exists

Small practices usually do not need another abstract compliance checklist. They need a safe, concrete way to answer:

> Where does patient data go after the visit, what vendors or AI tools touch it, and what can we prove if an owner, MSP, insurer, attorney, or reviewer asks?

## Why this is different

This project is not trying to be a full GRC platform, a scanner, a policy library, or a certification badge. It gives small practices a simple operating path:

```text
local intake -> patient-data-outside-the-EHR map -> vendor/BAA review -> AI workflow review -> evidence index -> owner/MSP handoff -> 30/60/90 plan
```

The evidence packet is the product center. The ePHI flow map is the wedge because it makes every other module more concrete.

## Best demo

Public demo snapshot:

```text
docs/demo/
├── README.md
├── review-packet.md
├── review-packet.html
├── packet-manifest.json
└── screenshots/review-packet.png
```

Regenerate locally:

```bash
python scripts/build.py samples/family_dental_clinic.yaml
python scripts/export_binder_index.py samples/family_dental_clinic.yaml
python scripts/validate_content.py
```

Runtime output:

```text
out/family_dental_clinic/
├── readiness-review.md
├── ephi-flow-map.md
├── vendor-baa-review.md
├── ai-workflow-review.md
├── downtime-ransomware-tabletop.md
├── evidence-binder-index.md
├── owner-msp-handoff.md
├── 30-60-90-roadmap.md
├── limitations-appendix.md
├── review-packet.md
├── review-packet.html
└── packet-manifest.json
```

## Boundaries to keep in every public narrative

- No PHI in demos.
- Evidence references, not raw evidence archives.
- No legal advice.
- No HIPAA certification or compliance guarantee.
- No breach determination.
- No invasive testing or managed SOC/MDR claim.
- Qualified reviewers still need to validate real contracts, BAAs, access lists, logs, backups, policies, and incident obligations.
