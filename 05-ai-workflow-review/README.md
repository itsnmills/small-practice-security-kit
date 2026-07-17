# AI Workflow Review

This module answers the concrete clinic question: can this workflow use AI safely?

Decisions should be simple:

- **allowed**
- **restricted**
- **prohibited**

The default rule is that patient-level or clinical data should not be pasted into unapproved tools.

## Decision gates (2026 refresh)

Before marking a workflow **allowed**, the practice owner or MSP should be able to answer:

| Gate | Allowed only if… | Restricted / prohibited when… |
| --- | --- | --- |
| Data boundary | Workflow never needs PHI, or BAA + retention + training posture are documented | PHI use with missing/unknown BAA or customer-data training |
| Human review | Clinical outputs have a named clinician owner review | Clinical or patient-facing use without review |
| Agent tools | Tool list is least-privilege; high-impact actions need human approval | Email, EHR write, billing, shell, browser without approval gates |
| MCP / tool broker | Servers are inventory + allowlisted; disable switch exists | Open MCP, unknown servers, or unsupervised tool brokers |
| Autonomous mode | Autonomous mode is off or supervised for PHI / high-impact tools | Unsupervised agents that can message patients or change records |
| Logging | Tool calls, approver, and destination class are logged | No audit trail for agent actions |
| Prompt injection | Direct + indirect tests done for RAG / browser / MCP | Network-capable agents with no injection testing |

## Suggested labels

- **Allowed** — inventory complete, BAA (if needed), no high-impact tools or tools are gated, logging present.
- **Restricted** — usable only with guardrails (no PHI paste, human approval on writes, limited MCP allowlist).
- **Prohibited** — Critical flags from inventory (missing BAA on PHI tool, autonomous MCP agent, unlogged egress, etc.).

## Companion input

Use the public CLI companion for structured inventory scoring:

- [health-ai-governance-auditor](https://github.com/itsnmills/health-ai-governance-auditor) — v0.1.1+ scores BAA, RAG, agent tools, MCP servers, autonomous mode, and egress.

Import **summary risk cards and owner actions** into the packet — not raw logs, patient data, or vendor contracts.

## Outputs this module should contribute

- AI workflow decision table (allowed / restricted / prohibited)
- Vendor follow-up questions
- Owner/MSP actions for the 30/60/90 roadmap
- Evidence references (BAA status, policy excerpt, training opt-out, tool allowlist screenshot references)

See the suite map: [`docs/suite.md`](../docs/suite.md).
