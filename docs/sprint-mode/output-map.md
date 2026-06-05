# Sprint Mode Output Map

| Buyer/MSP/legal question | Artifact | Why it helps |
|---|---|---|
| What is the buyer-facing starting point? | `practice-assurance-packet.html` | Polished, client-ready security and vendor evidence report for small dental practices, with 10-minute intake, top risks, owner decisions, evidence asks, audience handoffs, MSP value, and boundaries. |
| What if Markdown is easier to review? | `practice-assurance-packet.md` | Plain Markdown copy of the same assurance packet, including the 10-minute intake and owner decision queue. |
| What can we safely observe before internal access is needed? | `external-evidence-precheck.md` | Reference-only tracker, scheduler, intake, portal, TLS, and certificate observations translated into owner/MSP/vendor/reviewer questions. |
| What is the quickest local command-center view? | `sprint-command-center.html` | Self-contained local readout for sprint status, stage stepper, top risks, evidence gaps, handoff lanes, generated artifacts, and boundary language. |
| What supports the offer walkthrough? | `sprint-offering-readout.md` | Client-ready readout covering what was reviewed, patient-safety/trust meaning, top gaps, first-week actions, reviewer questions, source anchors, and limitations. |
| What should the office manager do first? | `owner-action-plan.md` | First 7 days plan with scripts/questions to send to the MSP, vendors, and legal/compliance reviewer. |
| What should the MSP prove or fix? | `msp-remediation-brief.md` | Technical checks, expected proof, owners, stage references, and source mapping for an IT partner. |
| What should vendors answer about BAA and AI use? | `vendor-baa-ai-questionnaire.md` | BAA availability, subcontractor, incident notice, retention/deletion, AI training-use, access control, audit-log, and export/delete questions. |
| What exact evidence should be gathered privately? | `evidence-collection-checklist.md` | Reference-only checklist of screenshots, exports, policy pages, restore notes, BAA status, AI policy pages, and insurance questionnaire evidence. |
| How should a first client workshop run? | `day-one-workshop-agenda.md` | Consultative agenda with discovery questions, evidence safety boundaries, owner/MSP/vendor/legal lanes, and expected outputs. |
| Which sources shaped each Sprint Mode question? | `source-map.md` | Stage-to-HHS/HICP/CISA/ONC-OCR map with a concise "how this source changes what we ask" line. |
| What concise client readout can be shared as Markdown? | `sprint-client-readout.md` | Portable summary of readiness signal, top risks, evidence gaps, handoff lanes, and next actions. |
| What did the runner generate and what is the data boundary? | `sprint-summary.json` | Machine-readable stage status, readiness signal, evidence gap summary, connector evidence summary, handoff lanes, `offering_summary`, counts, source profile hash, output list, and limitations. |
| Which imported evidence did local connectors observe? | `connector-evidence-summary.json` | Run provenance, connector modes, safety manifests, confidence counts, status counts, and metadata-only boundary for local imports/collectors. |
| Which risks need owners and next actions? | `risk-register.csv` | CSV for sorting by severity, stage, owner, recipient, evidence status, connector-derived findings, 30/60/90 bucket, and action. |
| What evidence should exist without storing raw evidence? | `evidence-index.json` | Reference-only evidence overlay tied to `packet-manifest.json`, connector evidence, and binder export files. |
| What should the owner, MSP, vendor, or reviewer answer next? | `handoff-actions.csv` | Action rows grouped by audience, recipient, owner, priority, stage, evidence reference, artifact, and 30/60/90 bucket. |
| What schemas define the private app import contract? | `schemas/sprint-summary.schema.json`, `schemas/evidence-index.schema.json`, `schemas/normalized-evidence.schema.json`, and `schemas/connector-run.schema.json` | Validates generated JSON structure before a future reviewed import. |
| Where can I read the full packet? | `review-packet.md` and `review-packet.html` | Preserved complete Markdown and print-friendly packet. |
| Where is the canonical generated manifest? | `packet-manifest.json` | Artifact hashes, evidence references, findings, roadmap items, and data boundary. |
| Where is the patient-data-outside-EHR map? | `ephi-flow-map.md` | Systems and flows with evidence needs, BAA needs, and risk. |
| Which AI workflows are allowed, restricted, or prohibited? | `ai-workflow-review.md` | Staff-facing workflow decisions and evidence needed. |
| Which vendor or BAA questions remain? | `vendor-baa-review.md` | Vendor rows for BAA status, SOC 2/HITRUST evidence status, AI training use, subcontractors, incident terms, and risk. |
| What should the MSP handle first? | `owner-msp-handoff.md` | Owner decisions, MSP follow-up, vendor asks, and handoff boundary. |
| What is the first 30/60/90 sequence? | `30-60-90-roadmap.md` | Plain-language remediation and evidence cadence plan. |
| What can be imported into a private evidence binder? | `evidence-binder-export/` | Binder-compatible CSV/Markdown exchange files with reference-only evidence rows. |
| What does this packet not prove? | `limitations-appendix.md` | Explicit boundary: no legal advice, no certification, no incident reporting decision, and no substitute for qualified review. |
