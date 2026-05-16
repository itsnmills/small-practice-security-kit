# Sprint Mode Output Map

| Buyer/MSP/legal question | Artifact | Why it helps |
|---|---|---|
| What is the quickest human-readable starting point? | `sprint-index.md` | Shows stage status, top findings, generated files, and handoff path. |
| What did the runner generate and what is the data boundary? | `sprint-summary.json` | Machine-readable stage status, counts, source profile hash, output list, and limitations. |
| Which risks need owners and next actions? | `risk-register.csv` | CSV for sorting by severity, stage, owner, evidence status, and action. |
| What evidence should exist without storing raw evidence? | `evidence-index.json` | Reference-only evidence overlay tied to `packet-manifest.json` and binder export files. |
| What should the owner, MSP, vendor, or reviewer answer next? | `handoff-actions.csv` | Action rows grouped by audience, priority, stage, evidence reference, and artifact. |
| Where can I read the full packet? | `review-packet.md` and `review-packet.html` | Preserved complete Markdown and print-friendly packet. |
| Where is the canonical generated manifest? | `packet-manifest.json` | Artifact hashes, evidence references, findings, roadmap items, and data boundary. |
| Where is the patient-data-outside-EHR map? | `ephi-flow-map.md` | Systems and flows with evidence needs, BAA needs, and risk. |
| Which AI workflows are allowed, restricted, or prohibited? | `ai-workflow-review.md` | Staff-facing workflow decisions and evidence needed. |
| Which vendor or BAA questions remain? | `vendor-baa-review.md` | Vendor rows for BAA status, AI training use, subcontractors, incident terms, and risk. |
| What should the MSP handle first? | `owner-msp-handoff.md` | Owner decisions, MSP follow-up, vendor asks, and handoff boundary. |
| What is the first 30/60/90 sequence? | `30-60-90-roadmap.md` | Plain-language remediation and evidence cadence plan. |
| What can be imported into a private evidence binder? | `evidence-binder-export/` | Binder-compatible CSV/Markdown exchange files with reference-only evidence rows. |
| What does this packet not prove? | `limitations-appendix.md` | Explicit non-certification, no-legal-advice, no-breach-determination boundary. |
