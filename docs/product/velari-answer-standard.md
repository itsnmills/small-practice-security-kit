# Velari Answer Standard

The Velari Answer Standard turns uncertainty into a next safe action. Every major finding, risk, task, report item, and roadmap action should tell a small practice what to ask, who owns the follow-up, what evidence is acceptable, and what data must stay out of the workflow.

This standard uses readiness, evidence, and workflow language only. It does not claim legal compliance, HIPAA certification, breach determination, vendor approval, insurer acceptance, or formal Security Risk Analysis completion.

## Required Fields

| Field | Purpose |
|---|---|
| `plain_english_summary` | One readable sentence explaining the uncertainty or gap. |
| `why_it_matters` | Operational reason the practice, MSP, vendor, or reviewer should care. |
| `owner_lane` | Accountable lane: practice owner, MSP, vendor, qualified reviewer, or shared lane. |
| `recommended_question` | The exact question to ask next. |
| `acceptable_evidence` | Safe evidence references that can support the answer. |
| `unsafe_inputs` | Data that must not be requested or pasted into the tool. |
| `priority` | Existing severity or priority value used by the artifact. |
| `timeframe` | `0-30 days`, `31-60 days`, or `61-90 days`. |
| `reviewer_needed` | Whether the item should be routed to a qualified reviewer. |
| `next_action` | The concrete next step. |
| `owner_view` | What the practice owner should do or decide. |
| `msp_view` | What the MSP should verify, configure, or summarize. |
| `vendor_view` | Vendor-facing question or evidence request where applicable. |
| `legal_compliance_view` | Qualified-review handoff language without claiming compliance. |

## Safety Boundary

Velari outputs must not request or depend on:

- PHI,
- credentials,
- private URLs,
- raw logs,
- patient screenshots,
- raw contracts,
- patient examples,
- claim details,
- clinical notes,
- secrets or keys,
- full incident contents.

Acceptable evidence should be safe to store in a local evidence workflow: dated summaries, contract section references, redacted admin exports, owner signoff notes, metadata-only review summaries, ticket references, vendor attestations, and policy acknowledgements.

## Reviewer Language

Allowed:

- "Route this item to a qualified reviewer."
- "A qualified reviewer can decide whether the evidence and contract language are adequate."
- "This kit supports readiness, evidence collection, and workflow handoff."

Not allowed:

- Wording that says the practice is legally compliant.
- Wording that says a vendor is certified or approved.
- Wording that says an output proves compliance.
- Wording that says the tool completes a formal Security Risk Analysis.

## Sprint Mode Contract

In `small-practice-security-kit`, the standard is validated through:

- `sprint-summary.json`,
- `risk-register.csv`,
- `handoff-actions.csv`,
- `sprint-client-readout.md`,
- `owner-action-plan.md`,
- `msp-remediation-brief.md`,
- `vendor-baa-ai-questionnaire.md`,
- `evidence-collection-checklist.md`,
- `30-60-90-roadmap.md`.

`risk-register.csv`, `handoff-actions.csv`, and `sprint-summary.json` carry the full field set so private Velari workspaces can import the same owner/MSP/vendor/reviewer action language without reinterpreting the finding.
