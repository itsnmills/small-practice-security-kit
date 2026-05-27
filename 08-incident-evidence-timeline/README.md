# Incident Evidence Timeline

This module turns a suspicious-access, downtime, vendor-notice, lost-device, ransomware, or tabletop scenario into a sanitized owner/MSP handoff.

It tracks:

- event order,
- affected system or workflow category,
- owner,
- source-aligned phase goal,
- owner question,
- MSP/vendor ask,
- safe inputs and blocked inputs,
- completion criteria,
- escalation triggers,
- private evidence reference,
- decision gate,
- current status,
- after-action remediation owner.

## Data Boundary

Use reference-only evidence. Do not enter PHI, patient identifiers, screenshots, raw logs, private URLs, credentials, vendor contract text, or real incident-sensitive details into generated public artifacts.

## What It Produces

The packet builder generates:

- `incident-evidence-timeline.md`
- `incident-after-action-report.md`
- incident timeline entries in `evidence-binder-index.md`
- incident timeline entries in `packet-manifest.json`
- incident timeline and after-action links in `dashboard.html`

The local intake workspace also includes an Incident Runner. It lets the owner or MSP pick a scenario, walk one phase at a time, record private evidence references, assign after-action owners, and rebuild the local packet.

Each phase shows:

- what to do now,
- what staff can safely say,
- what to ask the MSP or vendor,
- what evidence reference is needed,
- when to escalate,
- what must be true before the phase is complete.

## What It Is Not

This is not a reportability conclusion, legal opinion, cyber insurance notice, regulatory notice, formal Security Risk Analysis, managed detection and response workflow, SOC tool, or substitute for qualified incident response.

Use it to prepare the facts and evidence references that qualified reviewers need.
