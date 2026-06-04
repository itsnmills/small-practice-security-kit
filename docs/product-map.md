# Product Map

Small Practice Security Kit should read as the Velari public flagship proof repo: a PHI-avoidant, local-first readiness packet builder for small healthcare practices.

The front door is the generated owner/MSP-ready packet and demo, not the old module list.

```text
Small Practice Security Kit
├── flagship packet workflow
│   ├── local intake workspace
│   ├── patient-data-outside-the-EHR map
│   ├── vendor/BAA review
│   ├── AI workflow review
│   ├── downtime and incident readiness
│   ├── evidence index and manifest
│   └── owner/MSP handoff plus 30/60/90 roadmap
├── module building blocks
│   ├── 01-readiness-checklist/
│   ├── 02-ephi-data-flow-map/
│   ├── 03-hipaa-evidence-binder/
│   ├── 04-vendor-baa-review/
│   ├── 05-ai-workflow-review/
│   ├── 06-downtime-ransomware-tabletop/
│   ├── 07-review-packet-builder/
│   └── 08-incident-evidence-timeline/
└── companion/reference integrations
    └── optional imports and supporting proof patterns
```

The practical user journey is:

```text
start -> local intake -> map ePHI flows -> review vendors/BAAs -> review AI workflows -> prepare downtime/incident evidence -> build packet -> hand off owner/MSP actions -> plan 30/60/90
```

## Public Flagship Surface

| Surface | Role |
|---|---|
| [`README.md`](../README.md) | Buyer/hiring-manager front door with immediate demo packet links |
| [`docs/demo/`](demo/) | Sanitized sample packet, HTML packet, screenshot, manifest, and Sprint Mode artifacts |
| [`docs/security-model.md`](security-model.md) | PHI-avoidant and no-secret boundary |
| [`scripts/build.py`](../scripts/build.py) | Packet builder CLI |
| [`docs/sprint-mode/`](sprint-mode/) | Velari-style public runner docs and output contracts |

## Supporting Material

The numbered module directories remain useful implementation blocks and historical structure. They should be described as inputs to the flagship workflow, not as standalone products.

Companion repos should be referenced as optional integration sources or examples:

- vendor, BAA, and AI governance inputs;
- PHI guardrail examples;
- scanner or control-mapping reference checks;
- audit-log and evidence-reference patterns.

Future integrations should import metadata-only summaries and evidence references from companion repos instead of duplicating their full functionality or copying raw sensitive evidence.

## Positioning Boundary

Public language should stay focused on readiness, evidence organization, and owner/MSP handoff. Do not describe the repo as a HIPAA compliance guarantee, legal advice, breach-notification decision tool, formal Security Risk Analysis, MDR/SOC service, or audit-readiness certification.
