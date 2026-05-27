# Local Intake Workspace Standard

The intake workspace must act like a small-practice security workbench, not a generic questionnaire.

Every section should help a practice owner answer four practical questions:

1. What decision has to be made?
2. Who owns the decision or evidence?
3. What proof can be referenced without exposing sensitive material?
4. What must stay out of the packet?

## Section Pattern

Every non-incident section uses a section playbook with:

- owner question,
- plain-English goal,
- do-now checklist,
- owner/MSP/vendor asks,
- evidence required,
- do-not-enter boundary,
- source alignment.

The incident runner has its own phase-level version of the same pattern because incident work needs step-by-step decision gates.

## Command Summaries

High-value sections must also render a live command summary. This is the owner-facing queue that turns saved profile data into action:

- Practice basics: owner, technical owner, staff count, locations, review period.
- Systems: selected systems, ePHI touchpoints, categories, generated vendors.
- Vendors: ePHI vendors, BAA follow-up, high-risk vendors, unknown AI/data terms.
- ePHI flows: mapped flows, BAA review count, high-risk flows, unconfirmed flows.
- Readiness: evidence-backed checklist completion and priority gaps.
- AI workflows: allowed, restricted, and prohibited workflow counts.
- Downtime: critical systems, plan status, restore test, tabletop status.
- Evidence: collected/reviewed references, open references, sensitive-content flags.
- Generate: open owner actions before handoff.

## Research Basis

The workspace aligns its language with official, conservative source families:

- HHS HIPAA Security Rule framing: protect electronic protected health information with administrative, physical, and technical safeguards.
- HHS/OCR small-provider and risk-analysis guidance: gather context, risk evidence, and appropriate safeguards without treating the kit as a certification tool.
- HHS 405(d) HICP: prioritize practical, high-impact healthcare cyber practices.
- NIST CSF 2.0: Govern, Identify, Protect, Detect, Respond, and Recover should be visible to the practice owner.
- CISA incident and ransomware guidance: identify impacted systems, coordinate internal and external teams, preserve evidence by reference, and test response/recovery plans.

## Product Rules

- Never ask for patient details, raw logs, screenshots, private URLs, credentials, or raw contracts.
- Prefer reference IDs, owners, dates observed, folder paths, ticket IDs, connector summaries, and vendor trust-page references.
- Do not imply certification, breach determination, legal conclusion, or universal safety.
- Make unknowns visible. An unchecked or unknown field is an action item, not a failure.
- Use owner/MSP/vendor/reviewer lanes so the practice knows who should answer each question.
- Keep the first-pass packet useful in one work session for a small practice with limited staff and limited budget.
