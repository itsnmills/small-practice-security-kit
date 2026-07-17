# Velari Public Suite Map

Last public refresh: **2026-07-16**

This page is the living map of public Velari companions that feed the flagship
[Small Practice Security Kit](https://github.com/itsnmills/small-practice-security-kit).

All public companions stay **local-first and PHI-avoidant**. They produce
evidence references, owner/MSP actions, and reviewer-safe packets — not SaaS
dashboards, breach determinations, or HIPAA certifications.

## Public surface

| Repo | Role | Notes |
| --- | --- | --- |
| [small-practice-security-kit](https://github.com/itsnmills/small-practice-security-kit) | **Flagship** readiness packet builder | Demo packet + Sprint Command Center |
| [security-operations-triage-pipeline](https://github.com/itsnmills/security-operations-triage-pipeline) | Finding triage → tickets → handoff | Companion for SecOps evidence |
| [health-ai-governance-auditor](https://github.com/itsnmills/health-ai-governance-auditor) | AI vendor / agent governance CLI | **v0.1.1** adds MCP, autonomous mode, egress scoring |
| [cloud-iam-access-review-analyzer](https://github.com/itsnmills/cloud-iam-access-review-analyzer) | Cloud/IAM access-review packets | Workspace / Entra / AWS export workbench |
| [Strands-PHI-Guardrails-Demo](https://github.com/itsnmills/Strands-PHI-Guardrails-Demo) | Deterministic PHI guardrails demo | RBAC, purpose-of-use, BAA gate, audit log |
| [itsnmills.github.io](https://github.com/itsnmills/itsnmills.github.io) | Portfolio front door | Links the suite for hiring managers |

## How companions roll into a packet

```text
AI inventory (health-ai-governance-auditor)
  + IAM export review (cloud-iam-access-review-analyzer)
  + SecOps findings (security-operations-triage-pipeline)
  + Guardrail pattern (Strands-PHI-Guardrails-Demo)
        │
        ▼
Small Practice Security Kit
  → Practice Assurance / review packet
  → owner-MSP handoff
  → 30/60/90 roadmap
```

Companion outputs are **untrusted draft inputs** until a human previews them,
checks for PHI/secrets, and accepts specific rows into a practice workspace.

## July 2026 refresh focus

- Keep the public suite visibly active (not a one-day dump of frozen repos).
- Ship **HealthAI Audit v0.1.1** agent/MCP scoring so AI review matches 2026 tool reality.
- Point the flagship README and AI workflow module at agent/MCP decision gates.
- Leave private product surfaces (`velari-secure-practice`, chainrisk, etc.) out of public buyer paths.

## Safety

Do not open GitHub issues or sample packets that include PHI, credentials,
private URLs, contracts, logs, patient details, or incident details.
See [`security-model.md`](security-model.md).
