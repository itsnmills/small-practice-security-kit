# Flagship Positioning

The public story:

> Open-source security kits for small healthcare practices that need practical HIPAA, ePHI, vendor, AI, and incident evidence workflows without buying enterprise GRC software.

## Why This Is Different

This project is not trying to be a full GRC platform, a scanner, or a policy library. It gives small practices a simple operating path:

```text
intake -> ePHI map -> vendor review -> AI workflow review -> evidence index -> 30/60/90 plan
```

## Best Demo

```bash
python scripts/build.py samples/family_dental_clinic.yaml
```

Output:

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

The ePHI flow map should remain the star because it makes every other module more concrete.
