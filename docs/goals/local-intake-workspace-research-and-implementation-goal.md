# Goal: Build the Local Intake Workspace for Small Practice Security Kit

Date: 2026-05-12

Status: implemented v1

## Goal Prompt

Implement a secure-first, local-first intake mode that lets a small healthcare practice move from "downloaded the repo" to a useful practice security review packet in less than one day without requiring command-line editing or YAML knowledge.

The intake mode must behave like a practical owner/MSP workflow, not a generic questionnaire. It should understand the systems, vendors, documents, and evidence that most small healthcare practices already use, offer specialty-aware defaults, guide users through confirming what applies, prevent PHI entry where possible, save locally, and regenerate the dashboard and review packet from the captured profile.

The implementation must be differentiated from existing market tools by combining:

- local-first operation,
- open-source code,
- healthcare-practice-specific defaults,
- evidence binder outputs,
- ePHI flow mapping,
- vendor/BAA review,
- AI workflow safety review,
- secure local file/document inventory,
- explicit no-PHI guardrails,
- browser-based owner intake,
- end-to-end local testing.

## Research Snapshot

This plan is based on research performed on 2026-05-12.

### Official baseline sources

- HHS OCR Security Rule overview: The HIPAA Security Rule protects ePHI created, received, used, or maintained by covered entities and business associates, and requires appropriate administrative, physical, and technical safeguards.
- HHS OCR risk analysis guidance: risk analysis is foundational; practices need to identify ePHI, external sources of ePHI, threats, vulnerabilities, and reasonable safeguards.
- ONC/OCR SRA Tool: current federal reference point for small and medium providers. It is local, wizard-based, includes multiple-choice questions, threat/vulnerability assessment, asset and vendor management, references, and printable reports. It stores entered information locally and HHS says it does not collect, view, store, or transmit tool data.
- NIST SP 800-66r2: practical HIPAA Security Rule implementation guidance for regulated entities of all sizes.
- HHS business associate guidance: business associate functions include claims processing, data processing, billing, practice management, consulting, legal, accounting, administrative, data aggregation, management, accreditation, and financial services when PHI is involved.
- NIST AI RMF and Generative AI Profile: useful baseline for AI workflow governance, especially use-case risk, documentation, monitoring, privacy, and human oversight.
- ONC Health IT Playbook: useful for common practice workflows such as EHR use, patient portals, scheduling, billing, patient engagement, and workflow mapping.

### Market landscape

#### Federal free tool: ONC/OCR SRA Tool

Strengths:

- Trusted official baseline.
- Local storage.
- Wizard-based flow.
- Asset and vendor management.
- References and printable reports.
- Excel workbook fallback.
- Updated SRA v3.6 includes reviewed-by dates, section approvals, updated risk scale, improved reports, and content updates.

Limitations / opportunity:

- Windows desktop app plus workbook, not a modern cross-platform local web workspace.
- Focused on risk assessment, not a full evidence operating workflow.
- Does not appear positioned around prefilled practice system catalogs, AI workflow safety, vendor BAA due diligence, ePHI map generation, downtime packet generation, or evidence-binder exports as one coherent owner workflow.
- Not open for community-driven extension in the same way as an OSS repo.

#### Open-source GRC tools

Examples found:

- CISO Assistant
- SimpleRisk Core
- GovReady-Q / OSCAL-oriented tooling
- OpenGRC and newer OSS/self-hosted GRC projects

Strengths:

- Open-source or self-hosted options exist.
- Useful for risk registers, audits, controls, compliance mapping, vendor risk, evidence, and broader GRC workflows.
- Some projects support multiple frameworks and evidence tracking.

Limitations / opportunity:

- Usually generic GRC, not "small healthcare practice first."
- Setup and terminology often assume security/compliance practitioners.
- They do not start from the actual owner question: "what systems and vendors does my clinic use, what ePHI flows exist, what evidence do I need, and what can/cannot staff send to AI?"
- They are often too broad for a one-day small practice setup.
- They rarely ship with healthcare-specific system presets, BAA prompts, ePHI flow suggestions, AI workflow examples, and packet outputs in a single no-cloud workflow.

#### Commercial small-practice HIPAA/compliance tools

Examples found:

- GuardWell Compliance
- PHIGuard
- HIPAAGuard-style small practice compliance apps
- HIPAAYAK
- Accountable data flow mapping
- BAA-focused vendor tools

Strengths:

- Small-practice positioning is real.
- Dashboards, policies, training, recurring tasks, vendor BAAs, incidents, evidence, and compliance calendars are common paid features.
- Some claim quick onboarding and AI-assisted PHI/data-flow mapping.

Limitations / opportunity:

- Generally SaaS and subscription-based.
- Not open source.
- Usually not local-first.
- Practice data, evidence metadata, vendor lists, and assessment answers typically live in a vendor-controlled system.
- AI/data-flow functionality is often a feature in a larger paid platform rather than an auditable local workflow.
- They may include HIPAA operations but do not necessarily include open import/export contracts for adjacent scanner/evidence tooling.

### Product gap

The open niche is not "HIPAA checklist" or "generic GRC."

The gap is:

> A local-first, open-source, owner-friendly intake workspace that knows common small healthcare practice systems, helps identify ePHI flows and vendors without making users start from a blank page, blocks PHI entry, organizes evidence references, reviews AI workflows, and produces a useful security review packet in less than a day.

## Product Positioning

Working tagline:

> A local-first intake and evidence workspace for small healthcare practices that need to understand their ePHI flows, vendors, AI usage, security gaps, and proof packet without buying enterprise GRC software.

Sharper wedge:

> Not a HIPAA SaaS. Not a generic GRC. A local-first healthcare evidence intake and review packet builder for small practices and the people helping them.

Anti-positioning:

- Do not call this "HIPAA compliance software" as the primary story.
- Do not compete head-on with broad HIPAA SaaS dashboards.
- Do not compete head-on with generic open-source GRC suites.
- Do not lead with a score.
- Do not lead with a 200-question assessment.
- Do not imply certification, legal advice, or formal SRA replacement.

The product magic is:

> Make the messy first day of healthcare security evidence collection actually doable.

Primary users:

- practice owner,
- office manager,
- privacy/security officer by role but not by profession,
- small MSP,
- healthcare security consultant,
- compliance analyst helping smaller practices.

Best first users:

- small healthcare MSPs,
- HIPAA consultants,
- solo compliance officers,
- practice administrators,
- tech-savvy clinic managers,
- healthcare security students and analysts building proof-of-work,
- small healthcare startups and business associates needing a local evidence packet.

Go-to-market framing:

> Open-source tool for consultants, MSPs, admins, and analysts who need to produce a clean first-pass evidence packet for a small healthcare practice.

Longer-term owner framing:

> A practice owner can open it, confirm what applies, and understand what evidence is missing without becoming a GRC analyst.

The user should not need to know:

- YAML,
- control frameworks,
- GRC vocabulary,
- NIST terminology,
- OCR citations,
- data-flow diagramming.

The app should translate their answers into:

- profile YAML,
- ePHI map,
- vendor/BAA review,
- AI workflow review,
- evidence queue,
- review packet,
- 30/60/90 roadmap,
- future evidence binder exports.

## Design Principle

The intake must feel like:

> "Confirm what applies to your practice, fill the few things only you know, and we will build the packet."

It must not feel like:

> "Answer 200 compliance questions before you get value."

Bad version to avoid:

> "Answer 200 HIPAA questions and get a score."

Good version to build:

> "Pick your practice type, confirm common systems, answer guided prompts, attach/reference evidence, review risky flows, generate an owner packet."

## Target Outcome

A practice should be able to finish a useful first pass in one day:

1. Download repo.
2. Double-click launcher.
3. Create a new practice workspace.
4. Pick practice type and size.
5. Select from common system/vendor categories.
6. Confirm automatically suggested ePHI flows.
7. Confirm vendor/BAA status.
8. Answer short readiness questions.
9. Add document/evidence references without uploading PHI.
10. Review AI workflows and prohibited data examples.
11. Generate dashboard, packet, roadmap, and evidence queue.

## Security-First Requirements

### Local-only defaults

- Bind server to `127.0.0.1` by default.
- No external network calls during dashboard/intake use.
- No analytics, telemetry, cloud sync, model calls, or hidden update checks.
- Every future online connector must be explicitly opt-in and disabled by default.
- Add a visible local-only indicator in the UI.
- Add a "Network status: offline/local only" diagnostic in settings.

### PHI avoidance

The intake must repeatedly and practically explain:

- do not enter patient names,
- do not enter MRNs,
- do not enter dates of birth,
- do not paste clinical notes,
- do not paste claim narratives,
- do not upload patient records,
- do not store real incident details that identify patients,
- use evidence references and folder paths instead of sensitive content.

### Sensitive data detection

Add local validation before save:

- SSN-like patterns,
- MRN-like labels,
- DOB-like labels,
- patient-name hints,
- diagnosis-heavy pasted text,
- long clinical-note style text,
- API keys/tokens,
- private keys,
- passwords,
- credit card-like patterns,
- email addresses in fields that should be generic,
- phone numbers in fields that should be generic.

Behavior:

- warn and block save for high-confidence sensitive data,
- warn and allow with confirmation for ambiguous generic business contact fields,
- show exact field names with the concern,
- never transmit the content,
- log only the rule ID and field path, not the sensitive value.

### Local write safety

- Save only inside an approved workspace directory.
- Prevent path traversal.
- Use atomic writes.
- Keep timestamped local backups of profile changes.
- Keep an append-only local change log for profile edits.
- Never overwrite sample profiles by default.
- Create real profiles under `profiles/`.

### Browser/server safety

- Restrict write endpoints to localhost.
- Require same-origin requests.
- Use a per-session CSRF token for write actions.
- Accept JSON only.
- Enforce request size limits.
- Validate schema on every save.
- Validate profile before generating packets.
- Serve only the selected output directory, not the whole repo.

### Evidence safety

- Prefer evidence references over evidence file ingestion.
- If file inventory is added, scan only metadata by default:
  - filename,
  - extension,
  - size,
  - modified date,
  - user-selected evidence category.
- Do not parse document contents by default.
- If content parsing is later added, make it opt-in, local-only, and PHI-guarded.
- Never index patient chart folders.

### Future local AI safety

Local AI may be useful later, but it must be phase-gated:

- no AI in Intake v1,
- deterministic discovery first,
- optional local model only after guardrails and tests exist,
- support local models only through explicit user opt-in,
- no cloud LLM default,
- require a "no PHI" preflight,
- force review-before-import for every AI suggestion,
- store model output as suggestions, not facts,
- clearly mark provenance and confidence.

## Out-of-Box Defaults

The intake must not begin with a blank form. It should ship with presets.

### Practice type presets

Include at least:

- family medicine / primary care,
- dental,
- behavioral health,
- physical therapy / occupational therapy,
- chiropractic,
- urgent care,
- dermatology,
- pediatrics,
- ophthalmology / optometry,
- small lab,
- telehealth-first practice,
- small specialty clinic,
- billing-only / RCM service,
- business associate supporting practices.

Each preset should include:

- likely systems,
- likely ePHI flows,
- likely vendors,
- likely AI workflow risks,
- likely evidence items,
- common downtime concerns,
- suggested first-day tasks.

### Practice size presets

Include:

- solo practice,
- 2-5 providers,
- 6-15 providers,
- 16-50 staff,
- multi-location small group,
- business associate / support vendor.

Size affects:

- role suggestions,
- access review cadence prompts,
- vendor review complexity,
- downtime planning depth,
- evidence owner suggestions.

### Common system catalog

The intake should let users select from a checklist of systems that most practices may have:

- EHR / EMR,
- practice management system,
- scheduling,
- patient portal,
- digital intake forms,
- medical billing / RCM,
- clearinghouse,
- claims portal,
- eligibility verification,
- e-prescribing / EPCS,
- lab ordering/results portal,
- imaging portal,
- referral portal,
- HIE / interoperability service,
- telehealth platform,
- AI scribe / ambient documentation,
- public AI / chatbot usage,
- dictation/transcription,
- patient texting,
- secure messaging,
- reminder system,
- VoIP / phone system,
- call recording/transcription,
- fax / eFax,
- email/calendar,
- shared drive/file storage,
- document scanner/MFP,
- backup service,
- endpoint security/EDR/AV,
- firewall/router/Wi-Fi,
- remote access/VPN/RMM,
- MSP tools,
- accounting/payroll,
- HR/training system,
- website/contact forms,
- online reviews/marketing,
- CRM,
- payment processor,
- shredding service,
- legal/accounting/consulting,
- offsite storage,
- paper charts/records room.

Each catalog item should include:

- plain-English description,
- likely ePHI role,
- common evidence needed,
- common BAA question,
- common risk flags,
- common flows it suggests,
- whether it is usually a vendor, internal system, or both.

### Common vendor catalog

The system should offer categories and example placeholder names:

- EHR vendor,
- billing vendor,
- clearinghouse,
- eRx vendor,
- lab/imaging vendor,
- telehealth vendor,
- patient messaging/texting vendor,
- phone/VoIP vendor,
- fax/eFax vendor,
- email provider,
- cloud storage provider,
- MSP/IT support,
- backup provider,
- endpoint security provider,
- website/form provider,
- payment processor,
- payroll/accounting vendor,
- legal/accounting/consultant,
- shredding/offsite records vendor,
- AI assistant,
- AI scribe,
- transcription vendor.

No real vendor names are required in v1, but the data model should allow them.

### Auto-suggested ePHI flows

The app should generate candidate flows based on selected systems. Users confirm, edit, or mark not applicable.

Examples:

- Patient intake form -> EHR.
- EHR -> billing/RCM system.
- EHR -> clearinghouse.
- EHR -> patient portal.
- EHR -> lab/imaging portal.
- EHR -> eRx service.
- Patient portal -> staff inbox/EHR.
- EHR -> referral specialist.
- Staff email -> external specialist.
- Fax/eFax -> EHR or shared drive.
- Telehealth platform -> EHR.
- AI scribe -> EHR note draft.
- Phone/VoIP recording -> storage/transcription system.
- Website contact form -> staff email.
- Shared drive -> backup provider.
- Endpoint/workstation -> backup/EDR/RMM.

For each suggested flow:

- source,
- destination,
- ePHI type,
- vendor,
- transmission method,
- whether BAA is likely needed,
- default risk,
- evidence needed,
- why it was suggested.

### Default evidence catalog

Offer an evidence picker instead of making users invent evidence names:

- signed BAA,
- BAA review date,
- vendor security contact,
- vendor incident notification terms,
- subcontractor list,
- AI/customer-data use statement,
- EHR admin settings export,
- user access list,
- MFA settings screenshot/reference,
- quarterly access review signoff,
- backup configuration,
- restore test result,
- incident contact list,
- downtime procedure,
- tabletop notes,
- security awareness training roster,
- sanctions/OIG check reference if relevant,
- policy acknowledgement,
- risk analysis report,
- vulnerability scan reference,
- patch review reference,
- firewall/Wi-Fi configuration reference,
- endpoint protection dashboard reference,
- email security settings reference,
- file sharing settings reference,
- data flow map,
- network diagram,
- asset inventory,
- vendor inventory.

Evidence fields should collect:

- evidence title,
- evidence type,
- owner,
- location/reference,
- date collected,
- review date,
- sensitivity level,
- related system/vendor/flow/control,
- status,
- notes without PHI.

## Intake UX Specification

### Navigation model

Top-level sections:

- Dashboard
- Intake
- Evidence
- Packet
- Imports
- Settings

Intake sections:

- Start
- Practice basics
- Specialty and size
- Systems used
- Vendors and BAAs
- ePHI flows
- Readiness checklist
- AI workflows
- Downtime and incident prep
- Evidence references
- Review and generate

### Owner-friendly first screen

The first screen should ask:

> What kind of practice are we setting up?

Then present cards:

- Primary care
- Dental
- Behavioral health
- PT/OT
- Urgent care
- Specialty clinic
- Telehealth-first
- Business associate

Each card should say:

- estimated setup time,
- likely systems,
- likely evidence,
- common pitfalls.

### Guided setup flow

Each step should include:

- one plain-language heading,
- short explanation,
- "why this matters",
- "what not to enter",
- selectable defaults,
- edit/add controls,
- save progress,
- next-step button,
- status summary.

### Editing patterns

Use simple row-based editors:

- add system,
- edit system,
- mark system not used,
- duplicate system,
- add vendor from system,
- add flow from selected systems,
- confirm suggested flows,
- attach evidence reference.

Avoid:

- giant forms,
- framework jargon,
- nested modals,
- mandatory free-text long answers,
- raw YAML display as the primary interface.

### Smart assistance without AI in v1

Use deterministic rule suggestions first:

- selected system suggests vendor category,
- selected vendor touching ePHI suggests BAA evidence,
- missing BAA creates next action,
- selected AI workflow creates AI policy evidence item,
- selected EHR + billing creates billing flow,
- selected telehealth creates scheduling/check-in/documentation flow,
- selected email + referrals creates external specialist flow,
- selected backup creates restore-test evidence,
- selected MSP/RMM creates remote access/vendor evidence.

Every suggestion should show:

- why suggested,
- source answers,
- accept/edit/dismiss.

## Data Model Changes

Add or extend profile fields for:

- workspace metadata,
- intake status,
- preset selected,
- practice specialty,
- practice size tier,
- roles/owners,
- locations,
- system catalog selections,
- vendor relationships,
- evidence references,
- suggested flows with provenance,
- dismissed suggestions,
- sensitive-data warnings,
- change history,
- packet generation history.

Draft profile layout:

```yaml
workspace:
  id: ""
  created_at: ""
  updated_at: ""
  source: "local-intake"
  profile_version: "3.0"
  local_only: true

intake:
  preset: "dental"
  size_tier: "2-5 providers"
  status:
    basics: "complete"
    systems: "in_progress"
    vendors: "needs_review"
    flows: "needs_review"
    evidence: "not_started"
  dismissed_suggestions: []

systems:
  - id: "system-ehr"
    name: "Cloud EHR"
    catalog_key: "ehr"
    selected: true
    vendor_id: "vendor-ehr"
    ephi_role: "creates, receives, maintains, transmits"
    evidence_refs: []

vendors:
  - id: "vendor-ehr"
    name: "Example EHR Vendor"
    category: "ehr_vendor"
    touches_ephi: true
    baa_status: "signed"
    evidence_refs: []

flows:
  - id: "FLOW-001"
    source_system_id: "system-intake"
    destination_system_id: "system-ehr"
    suggested_by: ["preset:dental", "system:ehr", "system:digital_intake"]
    confirmed: true

evidence:
  - id: "EVID-001"
    title: "EHR BAA"
    type: "signed_baa"
    reference: "Evidence/Vendors/EHR/BAA.pdf"
    stores_sensitive_content: false
```

## API Requirements

Add local HTTP endpoints:

- `GET /api/profile`
- `POST /api/profile`
- `POST /api/build`
- `GET /api/catalogs`
- `POST /api/suggestions/rebuild`
- `GET /api/evidence`
- `POST /api/evidence`
- `GET /api/status`
- `GET /api/packet-links`

Security:

- localhost only,
- JSON only,
- schema validation,
- request size limit,
- CSRF/session token,
- atomic writes,
- backups,
- path allowlist,
- no arbitrary file reads,
- no arbitrary file writes.

## File/Folder Plan

Likely additions:

- `profiles/.gitkeep`
- `small_practice_security_kit/intake.py`
- `small_practice_security_kit/catalogs.py`
- `small_practice_security_kit/suggestions.py`
- `small_practice_security_kit/local_api.py`
- `small_practice_security_kit/sensitive_data.py`
- `small_practice_security_kit/workspaces.py`
- `small_practice_security_kit/static/intake.html`
- `small_practice_security_kit/static/intake.css`
- `small_practice_security_kit/static/intake.js`
- `catalogs/practice_presets.yaml`
- `catalogs/system_catalog.yaml`
- `catalogs/vendor_catalog.yaml`
- `catalogs/evidence_catalog.yaml`
- `schemas/intake-workspace.schema.json`
- `docs/intake-mode.md`
- `docs/security-model.md`
- `tests/test_intake_api.py`
- `tests/test_catalogs.py`
- `tests/test_suggestions.py`
- `tests/test_sensitive_data.py`
- `tests/test_workspace_writes.py`
- `tests/test_intake_e2e.py`

Likely updates:

- `scripts/serve_dashboard.py`
- `small_practice_security_kit/dashboard.py`
- `small_practice_security_kit/profile.py`
- `small_practice_security_kit/validation.py`
- `small_practice_security_kit/packet.py`
- `README.md`
- `.github/workflows/ci.yml`

## Implementation Phases

### Phase 1: Secure local workspace foundation

Deliver:

- `profiles/` workspace support.
- Profile create/copy flow from presets.
- Atomic profile writes.
- Timestamped backups.
- Append-only local profile change log.
- Local API server with safe endpoints.
- Dashboard launcher opens the app home, not just output HTML.

Definition of done:

- Can create `profiles/my_practice.yaml` from a preset.
- Can save profile changes through API.
- Cannot write outside approved profile/output dirs.
- Tests cover path traversal attempts.
- Existing packet generation still works.

### Phase 2: Catalogs and presets

Deliver:

- Practice type presets.
- Practice size presets.
- System catalog.
- Vendor catalog.
- Evidence catalog.
- Default flow templates.

Definition of done:

- New practice can be created from a preset.
- Selecting a practice type preloads likely systems/vendors/flows.
- Catalog tests verify required keys, evidence mappings, and suggestion mappings.

### Phase 3: Intake UI v1

Deliver:

- Intake landing screen.
- Practice basics form.
- Specialty/size picker.
- Systems checklist with common systems.
- Vendor/BAA editor.
- Suggested ePHI flow review.
- Readiness checklist.
- AI workflow review.
- Downtime setup.
- Evidence reference editor.
- Review and generate page.

Definition of done:

- A user can create a practice without touching YAML.
- A user can choose default systems instead of typing everything.
- A user can confirm/edit suggested flows.
- A user can add vendor BAA status.
- A user can generate dashboard and packet from the UI.

### Phase 4: PHI guardrails and secure validation

Deliver:

- Sensitive data detection library.
- Field-level warnings.
- Block high-confidence sensitive entries.
- No-PHI hints in every intake section.
- Local-only network status.
- Audit log for warning rule IDs only.

Definition of done:

- Tests cover SSN, DOB, MRN-like text, private keys, passwords, long clinical note patterns, and API keys.
- UI shows a useful warning and prevents unsafe save.
- No sensitive values are written into the warning log.

### Phase 5: Evidence reference workspace

Deliver:

- Evidence reference table.
- Evidence-to-system/vendor/flow links.
- Evidence completeness status.
- Evidence needed suggestions.
- Evidence export into packet and binder-compatible export.

Definition of done:

- Evidence references appear in dashboard, packet, roadmap, and binder export.
- Users can track evidence without uploading sensitive files.
- Missing evidence produces next actions.

### Phase 6: Import and "less than one day" setup helpers

Deliver:

- CSV import for systems.
- CSV import for vendors.
- CSV import for evidence references.
- Optional local folder inventory that stores metadata only.
- Setup checklist with time estimates.
- Import review screen before profile changes.

Definition of done:

- A practice can bulk add vendors/systems/evidence references.
- Imports show preview, warnings, and accept/reject.
- No content parsing happens by default.

### Phase 7: Future local discovery assistant

Do not implement until the deterministic intake is stable.

Potential future features:

- Local folder scan for filenames and metadata.
- Local email export ingestion from user-supplied `.mbox` or `.eml` files with PHI-safe metadata mode.
- Local browser/manual checklist for collecting vendor docs.
- Optional Ollama/local model summarization of non-PHI policy/vendor documents.
- Local AI-assisted system/vendor suggestions.

Required constraints:

- explicit opt-in,
- no network,
- no PHI,
- review-before-import,
- source provenance,
- model output marked as suggestion,
- deterministic tests for guardrails.

## Differentiation Requirements

The project must clearly differentiate from:

- ONC/OCR SRA Tool by being cross-platform, open-source, browser-based, extensible, evidence-packet oriented, AI-workflow aware, and practice-preset driven.
- Generic open-source GRC by being small-healthcare-practice first, owner-friendly, and ready in less than a day.
- Commercial HIPAA SaaS by being local-first, auditable, no telemetry, no subscription, open source, and exportable.
- Data-flow mapping vendors by producing local ePHI maps from confirmed system/vendor selections instead of requiring cloud AI.
- AI governance platforms by focusing on practical "can staff use this workflow?" healthcare scenarios.

Killer differentiators:

- Local-first / no PHI by design.
- Open-source and inspectable.
- Practice-type presets.
- Common healthcare system/vendor defaults.
- ePHI flow mapping as a first-class workflow.
- AI workflow safety built in.
- Evidence packet output, not just a score.
- One-day setup goal.
- Consultant/MSP-friendly exports.
- Future local AI-assisted discovery without sending sensitive data out.

Crowded lanes to avoid:

- generic HIPAA compliance SaaS,
- generic open-source GRC,
- policy-template library,
- training/reminder dashboard,
- questionnaire-only SRA clone.

Less crowded lane to own:

> Local-first healthcare intake plus evidence packet generation for small practices, MSPs, consultants, and admins.

## UX Acceptance Criteria

The final intake workspace should pass these practical questions:

- Can a dental practice owner open it without the CLI?
- Can they create a profile from a dental preset?
- Can they select likely systems from a checklist?
- Can they avoid typing vendors from scratch where categories are enough?
- Can they see suggested flows immediately?
- Can they understand why a BAA is likely needed?
- Can they add evidence references without storing PHI?
- Can they generate a dashboard and packet from the UI?
- Can they finish a useful first pass in less than one day?
- Can an MSP export/review the profile and packet?
- Can a future agent understand exactly where to add local AI safely?

## Validation Requirements

Run all of the following before calling implementation complete:

- Unit tests for catalogs.
- Unit tests for suggestion rules.
- Unit tests for sensitive-data detection.
- Unit tests for local write safety.
- Existing packet build tests.
- Existing dashboard tests.
- API tests for profile create/save/build.
- Browser E2E:
  - open local app,
  - create profile from preset,
  - select systems,
  - accept suggested flows,
  - add vendor BAA status,
  - add evidence reference,
  - generate packet,
  - open dashboard,
  - open review packet,
  - open roadmap,
  - open evidence index.
- Security E2E:
  - path traversal write rejected,
  - non-local host write rejected or unavailable,
  - high-confidence PHI-like input blocked,
  - profile backups created,
  - change log contains no sensitive field values.

## Non-Goals

- Do not claim HIPAA certification.
- Do not provide legal advice.
- Do not replace a qualified Security Risk Analysis.
- Do not store real patient information.
- Do not integrate with live EHRs in v1.
- Do not scrape email or online services in v1.
- Do not use cloud AI in v1.
- Do not parse patient documents.
- Do not become a generic enterprise GRC platform.

## First Build Recommendation

Start with Phase 1 through Phase 4 as one implementation branch:

1. Workspace creation and safe profile writes.
2. Presets/catalogs.
3. Intake UI with systems/vendors/flows/readiness/AI/downtime/evidence.
4. Sensitive data guardrails.
5. Generate dashboard and packet from the intake UI.
6. Full unit/browser/security validation.

Reason:

This creates the real product loop:

```text
owner intake -> local profile -> suggestions -> evidence references -> dashboard -> packet
```

Everything else, including local AI discovery, should build on that loop later.
