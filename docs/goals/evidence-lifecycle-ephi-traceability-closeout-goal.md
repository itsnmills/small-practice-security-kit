# Goal: Evidence Lifecycle, ePHI Traceability, and Dashboard Closeout

Date: 2026-05-27

Repo: `small-practice-security-kit`

Status: Active implementation goal

## Objective

Make the existing Small Practice Security Kit features feel 10x more useful by turning the current packet generator into a stronger evidence-backed readiness workflow.

This goal intentionally does not add another major product module on top of the current kit. It deepens the features that already exist:

- readiness review
- ePHI flow map
- vendor and BAA review
- AI workflow review
- downtime and ransomware tabletop
- incident evidence timeline
- evidence binder index
- owner/MSP handoff
- packet manifest
- local dashboard

The core product shift is:

```text
static readiness packet -> traceable evidence lifecycle and closeout workflow
```

Every important row should answer:

1. What evidence is needed?
2. Which ePHI flow, system, vendor, workflow, or incident event does it support?
3. Who owns it?
4. Is it missing, requested, partial, provided, stale, blocked, or closed?
5. What would make it ready for review or closed?
6. What should the owner, MSP, vendor, or reviewer do next?
7. What must not be uploaded or pasted because it may contain PHI, secrets, private URLs, raw logs, screenshots, contracts, or incident-sensitive facts?

## Product Rationale

Small practices usually do not fail because nobody knows MFA, backups, BAAs, AI boundaries, access reviews, downtime plans, and vendor evidence matter. They fail because proof is scattered across email, vendor portals, MSP tickets, screenshots, shared drives, local machines, memory, and half-complete spreadsheets.

The existing kit already covers the right workflow. The biggest improvement is to make every current feature evidence-aware and traceable:

- the readiness checklist should not only say "EHR MFA: No"; it should say what evidence closes it, who owns it, which systems and flows it affects, and whether it is missing or stale;
- the ePHI map should not only list flows; it should become the source of truth that downstream vendor, AI, downtime, access, and evidence artifacts trace back to;
- the vendor review should not only say "BAA status unknown"; it should create a closeout rule and link the vendor to affected ePHI flows and packet artifacts;
- the AI review should not only classify workflows; it should show what evidence or policy acknowledgement is needed before a workflow moves from restricted to ready for review;
- the dashboard should not just summarize outputs; it should tell the owner/MSP what remains blocked, what is ready for review, and what can be closed.

## Non-Goals

This pass must not become a generic feature expansion. Specifically, this goal does not add:

- hosted storage;
- auth;
- real PHI ingestion;
- raw log ingestion;
- raw contract ingestion;
- EHR integrations;
- new vendor portal integrations;
- new security scanning features;
- formal compliance scoring;
- legal, breach-notification, vendor-approval, AI-production-use, or insurer-acceptance decisions.

The repo remains local-first, synthetic/reference-only, and PHI-avoidant.

## Existing Surfaces To Improve

### Readiness Review

Current behavior:

- lists baseline readiness items;
- calculates a broad initial risk;
- lists priority gaps.

Target behavior:

- preserve the existing plain-English review;
- add evidence lifecycle and closeout rows for the readiness controls;
- show owner, status, closeout state, acceptable evidence, and closeout rule;
- keep the language bounded as readiness and evidence support, not certification.

### ePHI Flow Map

Current behavior:

- lists systems;
- lists flows with source, destination, vendor, ePHI type, BAA need, risk, and evidence needed.

Target behavior:

- make each flow traceable to system names, vendor names, affected artifacts, and evidence lifecycle rows;
- add closeout visibility directly to flow rows;
- preserve the "Patient Data Outside the EHR" wedge as the strongest product signal;
- avoid pretending to verify live network paths, portals, APIs, contracts, or production evidence.

### Vendor and BAA Review

Current behavior:

- lists vendor service, ePHI status, BAA status, SOC 2/HITRUST status, subcontractor visibility, incident terms, and risk.

Target behavior:

- add lifecycle status and closeout state;
- show affected ePHI flows;
- keep exact vendor asks and acceptable evidence;
- distinguish signed/provided evidence from stale, requested, missing, blocked, or not applicable states;
- keep private contracts and private portal links out of generated public artifacts.

### AI Workflow Review

Current behavior:

- classifies workflows as allowed, restricted, or prohibited;
- lists evidence needed.

Target behavior:

- add lifecycle and closeout state for each workflow;
- connect AI workflows back to ePHI flows and vendor evidence where possible;
- make the closeout rule explicit: staff guidance, vendor terms, retention/model-training posture, human review, owner signoff, or prohibited-use training;
- preserve no-PHI and no-secrets boundaries.

### Downtime and Ransomware Tabletop

Current behavior:

- lists plan status, restore-test status, tabletop status, critical systems, and a starter scenario.

Target behavior:

- add lifecycle and closeout rows per critical system;
- connect downtime systems back to the ePHI map and backup evidence;
- make stale or missing restore evidence visible;
- keep this as readiness/tabletop support, not incident response or recovery assurance.

### Incident Timeline

Current behavior:

- the local dirty checkout already adds a sanitized timeline and after-action report.

Target behavior:

- include incident timeline evidence in the same lifecycle model;
- make after-action ownership and evidence references visible in the dashboard;
- keep qualified legal/compliance, insurance, regulatory, contract, and incident-response decisions parked for qualified reviewers.

### Evidence Binder Index

Current behavior:

- lists profile evidence, flow evidence, vendor evidence, and generated references.

Target behavior:

- become the unified evidence lifecycle index;
- include lifecycle status, closeout state, owner, source, trace, acceptable evidence, next action, and module/artifact;
- still avoid raw evidence, PHI, screenshots, private URLs, credentials, and contracts.

### Packet Manifest

Current behavior:

- records sections, artifacts, evidence references, findings, roadmap items, hashes, and boundaries.

Target behavior:

- make evidence lifecycle fields contract-grade in `packet-manifest.json`;
- include closeout state and trace metadata;
- keep schema validation green;
- preserve compatibility with existing action-packet finding contracts.

### Dashboard

Current behavior:

- shows overview metrics, task list, readiness, flows, vendors, AI, evidence, incident, downtime, and packet links.

Target behavior:

- become the closeout cockpit;
- show lifecycle counts and blocked/ready/closed counts;
- rank evidence work by closeout state and risk;
- show ePHI traceability in the evidence queue;
- make each dashboard row point the owner/MSP toward a concrete closeout action.

## Evidence Lifecycle Vocabulary

The generated lifecycle vocabulary should support these states:

- `missing`: evidence is expected but not known to exist;
- `requested`: evidence has been requested or identified but not yet supplied;
- `partial`: some evidence exists but scope, owner, date, or exception handling is incomplete;
- `provided`: reference-only evidence appears available but may still need review;
- `reviewed`: evidence has been reviewed in the profile context;
- `stale`: evidence exists but is outdated or beyond a reasonable review window;
- `blocked`: the workflow should not proceed until a specific owner, MSP, vendor, or reviewer action is taken;
- `closed`: the row has enough reference-only support for this public readiness workflow;
- `not_applicable`: evidence is not expected for that workflow.

Closeout states should be simpler for owners:

- `blocked`: action cannot reasonably proceed because evidence is missing, stale, prohibited, or reviewer-gated;
- `needs_evidence`: the owner, MSP, vendor, or reviewer must collect or refresh evidence;
- `ready_for_review`: evidence appears available enough for a human review conversation;
- `closed`: no further action is generated for this public readiness packet;
- `not_applicable`: not relevant for this workflow.

## Traceability Requirements

Every generated lifecycle row should include as much trace context as is safely available:

- source kind: readiness, evidence, flow, vendor, AI workflow, downtime, incident timeline, or after-action;
- source reference: profile key, evidence ID, flow ID, vendor name, workflow name, system name, or incident item ID;
- system references;
- vendor references;
- flow IDs;
- workflow references;
- artifact references;
- source module names;
- private evidence boundary.

The trace does not need to be perfect, but it should be useful enough for an owner/MSP conversation.

## Implementation Plan

1. Add a shared evidence lifecycle module.
2. Generate lifecycle records from the current profile without requiring users to add new profile fields.
3. Use the lifecycle records in:
   - `packet-manifest.json`;
   - `evidence-binder-index.md`;
   - `readiness-review.md`;
   - `ephi-flow-map.md`;
   - `vendor-baa-review.md`;
   - `ai-workflow-review.md`;
   - `downtime-ransomware-tabletop.md`;
   - `owner-msp-handoff.md`;
   - `dashboard.html`.
4. Update the packet manifest schema to validate the new lifecycle and trace fields.
5. Update tests to assert lifecycle, closeout, and traceability appear in generated artifacts.
6. Regenerate demo outputs.
7. Run proof gates.

## Acceptance Criteria

The implementation is complete when:

- `packet-manifest.json` includes lifecycle and closeout fields for evidence references;
- evidence references include trace metadata to flows, systems, vendors, workflows, and artifacts where available;
- `evidence-binder-index.md` is a lifecycle index rather than a flat evidence list;
- `readiness-review.md`, `ephi-flow-map.md`, `vendor-baa-review.md`, `ai-workflow-review.md`, and `downtime-ransomware-tabletop.md` expose closeout context without adding new modules;
- `dashboard.html` shows closeout metrics and an evidence lifecycle queue;
- schema validation passes;
- content validation passes;
- profile validation passes;
- unit tests pass through the repo venv;
- generated artifacts preserve the no-PHI/no-secrets/no-raw-evidence boundary;
- no legal, compliance, breach, insurer, vendor-approval, or AI-production authorization claims are introduced.

## Proof Commands

Use the repo virtual environment:

```bash
.venv/bin/python -m unittest tests.test_build tests.test_catalogs tests.test_connectors tests.test_dashboard tests.test_demo_export tests.test_ephi_import tests.test_evidence_binder_export tests.test_exchange tests.test_file_inventory tests.test_packet_manifest tests.test_profile_validation tests.test_safety tests.test_security_config tests.test_sensitive_data tests.test_sprint tests.test_suggestions tests.test_vendor_evidence_status tests.test_vendor_import tests.test_workspace_writes
.venv/bin/python scripts/validate_content.py
.venv/bin/python -m small_practice_security_kit validate samples/family_dental_clinic.yaml
.venv/bin/python -m small_practice_security_kit sprint samples/family_dental_clinic.yaml --output-root /tmp/spsk-lifecycle-smoke
git diff --check
```

The local intake API server test may require a non-sandboxed loopback socket. If the sandbox blocks `127.0.0.1` bind, record that explicitly and verify the rest of the suite through the venv.

## Risk Controls

- Do not store PHI, patient identifiers, secrets, private URLs, raw logs, raw screenshots, raw contracts, or real incident details.
- Do not infer legal/compliance conclusions from lifecycle state.
- Do not infer a vendor is approved because evidence is provided.
- Do not infer an AI workflow is approved for PHI because evidence is provided.
- Do not call readiness evidence a formal Security Risk Analysis.
- Keep generated fields deterministic enough for tests and private-app import.
- Preserve existing CLI commands and artifact names.

## Expected Product Impact

After this pass, the public repo should feel less like a collection of helpful packet files and more like a working readiness cockpit:

- owners can see exactly what remains blocked;
- MSPs can see what evidence to return;
- vendors can see precise questions;
- reviewers can see what needs professional review;
- the ePHI map becomes the connective tissue across the whole packet;
- the dashboard becomes a closeout surface instead of only a summary surface.

