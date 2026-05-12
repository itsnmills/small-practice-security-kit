# Existing Repo Import Plan

This kit should become the front door for the existing healthcare security repos, not a replacement for them. The umbrella packet should stay simple, while deeper repos provide richer inputs and evidence references.

## Integration Principles

- Prefer imports and generated references over copy-pasting raw evidence.
- Keep PHI and secrets out of generated public artifacts.
- Preserve each source repo's specialty.
- Use stable CSV/YAML/JSON exchange formats.
- Make every imported item traceable to a module and evidence reference.

## Repo Map

| Repo | Current Value | Import/Export Direction | First Useful Adapter |
|---|---|---|---|
| `hipaa-evidence-binder-template` | Evidence binder generator, validator, review calendar, summaries | Export this kit's evidence index into binder-ready Markdown/CSV | `scripts/export_binder_index.py` |
| `healthcare-cyber-readiness-checklist` | Practice readiness checklist and PDF/Markdown outputs | Import checklist rows and status into readiness review | `scripts/import_readiness_checklist.py` |
| `ephi-data-flow-mapper` | Guided ePHI flow mapping worksheet and CSV templates | Adopt its flow schema as canonical for `flows` | `schemas/flows.schema.json` |
| `vendor-risk-manager` | Healthcare vendor lifecycle, BAA tracking, annual verification | Import/export vendor register fields | `scripts/import_vendor_register.py` |
| `health-ai-governance-auditor` | Local AI tool inventory, governance gaps, vendor review | Import AI workflow/vendor findings | `scripts/import_ai_governance.py` |
| `ai-governance-auditor` | AI vendor risk cards and policy templates | Import AI vendor risk card summaries | `scripts/import_ai_vendor_cards.py` |
| `agent-audit-trail` | Tamper-evident AI agent logs and violation rules | Link audit trail report paths as restricted evidence references | `scripts/import_agent_audit_refs.py` |
| `Strands-PHI-Guardrails-Demo` | Deterministic PHI guardrails and BAA/purpose checks | Reuse allowed/prohibited data examples | `05-ai-workflow-review/examples.md` |
| `healthcare-ai-security-lab` | Healthcare KEV triage CLI | Import KEV priority rows as technical evidence references | `scripts/import_kev_triage.py` |
| `iomt-risk-scorer` | IoMT risk scoring and reports | Import device risk summary into ePHI/technical review | `scripts/import_iomt_risk.py` |
| `hipaa-scanner` | Rapid HIPAA scanner | Import scanner findings into readiness and evidence index | `scripts/import_hipaa_scanner.py` |
| `hipaa-compliance-engine` | Control verification and freshness scoring | Import control status and freshness into evidence index | `scripts/import_compliance_engine.py` |

## Canonical Exchange Fields

Adapters should normalize into these fields:

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

## First Three Adapters

Build these first:

1. `hipaa-evidence-binder-template` export because the evidence binder is the strongest companion.
2. `ephi-data-flow-mapper` import because ePHI flow is the star module.
3. `vendor-risk-manager` import because vendor/BAA review is a direct practice need.

## Public Safety Rules

- Public samples must stay fictional.
- Adapters should write references, not raw sensitive evidence.
- Incident, breach, and AI-agent logs should default to restricted-reference mode.
- Generated public demo packets should pass `scripts/validate_content.py`.
