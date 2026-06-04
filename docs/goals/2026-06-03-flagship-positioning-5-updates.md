# Small Practice Security Kit Flagship Positioning — Research-First Implementation Goal

## Mission
Update the public repo positioning so `small-practice-security-kit` clearly reads as the Velari public flagship proof repo, not a loose collection of healthcare-security modules.

Implement Noah's five requested updates:
1. GitHub description recommendation / local documented command.
2. README top-fold rewrite.
3. Buyer-facing "What you get" section.
4. Sanitized sample packet visible immediately.
5. Repo map explaining flagship / modules / legacy/supporting material.

## Project Context
- Repo: `/Users/noahmills/Projects/small-practice-security-kit`
- Stack: Python stdlib + PyYAML/jsonschema docs/demo generator.
- Primary public file: `README.md`
- Supporting product docs:
  - `docs/demo/README.md` — sanitized demo overview.
  - `docs/security-model.md` — PHI/secrets safety boundary.
  - `docs/flagship-positioning.md` — positioning source.
  - `docs/product-map.md` — existing product map.
  - `docs/import-plans/existing-repos.md` — companion repo integration notes.
- Validation commands:
  - `python3 -m venv .venv`
  - `.venv/bin/python -m pip install -r requirements.txt`
  - `.venv/bin/python scripts/validate_content.py`
  - `.venv/bin/python -m unittest discover -s tests`

## Research Inputs Used
- Repo inspection: README, docs/demo, docs/product, docs/import-plans, tests, CI workflow.
- Research stream A: public GitHub proof repo/product README positioning recommendations.
- Research stream B: repo-specific file inspection recommendations.
- GitHub description gap: cannot be committed directly as file metadata; `gh` is not installed locally. Document the exact suggested description and command/manual action in repo docs.
- Security/privacy research: avoid overclaiming HIPAA compliance; keep PHI-avoidant, no credentials, no raw logs/contracts, no legal/breach determination language.

## Candidate Features Considered

| Candidate | User impact | Strategic leverage | Feasibility | Security risk inverse | Testability | Maintenance inverse | Total | Evidence |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| README top-fold + demo-first positioning | 5 | 5 | 5 | 5 | 5 | 5 | 30 | Directly fixes repo first impression and buyer path. |
| Grouped "What you get" section | 5 | 4 | 5 | 5 | 5 | 5 | 29 | Existing table is complete but too flat; flagship packet gets buried. |
| Repo map flagship/module/legacy | 4 | 5 | 5 | 5 | 5 | 5 | 29 | Reduces fragmentation narrative and clarifies canonical surface. |
| GitHub description metadata update | 4 | 5 | 2 | 5 | 2 | 5 | 23 | Important but local `gh` unavailable; document exact text and command. |
| New demo/sample artifacts | 3 | 3 | 4 | 4 | 4 | 4 | 22 | Demo already exists; better to surface it than create redundant artifacts. |

## Selected Feature
Implement the complete positioning/doc update set in README and supporting docs.

### Why This Feature Wins
- Impact: fixes the public front door before deeper product consolidation.
- Feasibility: mostly documentation, minimal risk, existing demo artifacts already present.
- Security posture: strengthens no-PHI/no-compliance-guarantee boundary.
- Testability: content validator and full test suite can verify links/content generation safety.

## Non-Goals
- Do not add new runtime features.
- Do not create fake demo data or new placeholder artifacts.
- Do not claim HIPAA certification, compliance guarantee, legal advice, breach determination, SRA completion, MDR/SOC service, or audit readiness.
- Do not modify generated demo artifacts unless validation requires it.
- Do not push, publish, or change remote GitHub metadata if `gh` is unavailable.

## Requirements

### Functional
1. Update `README.md` top fold to lead with:
   - PHI-avoidant/local-first readiness packet builder.
   - target users: small practice owner/manager/MSP/consultant.
   - immediate links to demo packet, HTML packet, screenshot, manifest, safety boundary.
   - short workflow line.
   - short disclaimer.
2. Ensure the sanitized demo packet is visible in the first screen of README.
3. Rewrite `What you get` into grouped buyer-facing categories:
   - Flagship packet.
   - Core readiness artifacts.
   - Downtime/incident readiness.
   - Owner/MSP follow-up.
   - Extended worksheets.
4. Replace/expand repo map so it explains:
   - flagship workflow areas,
   - modules/legacy building blocks,
   - companion repos as supporting/reference integrations not main products.
5. Add a local documentation note with the exact GitHub description recommendation and the command/UI instruction for updating GitHub metadata later.
6. Keep `docs/product-map.md` consistent with the new flagship/module/legacy language.

### UX / Developer Experience
1. README should be skimmable by a buyer or hiring manager in under 60 seconds.
2. Demo packet must be one click from the top.
3. Technical commands should remain intact after the buyer-facing proof sections.

### Security and Privacy
1. Use `PHI-avoidant`, `local-first`, `readiness`, `evidence organization`, and `owner/MSP handoff` language.
2. Explicitly say this does not certify HIPAA compliance, provide legal advice, make breach-notification decisions, or replace qualified professionals.
3. Do not add secrets, real org names, real patient data, raw logs, contracts, private URLs, or credentials.

## Implementation Plan

### Task 1 — README top fold
- Modify: `README.md`
- Replace the opening section before `## What this helps answer` with a concise buyer-facing intro and immediate demo links.

### Task 2 — What you get grouping
- Modify: `README.md`
- Replace the flat output table with grouped artifact categories while preserving all artifact names and links/meaning.

### Task 3 — Repo map
- Modify: `README.md`
- Replace/expand `## Modules` and `## Companion repo map` with a `## Repo map` section that separates flagship workflow, current modules, companion/supporting repos, and legacy/reference notes.

### Task 4 — Product map consistency
- Modify: `docs/product-map.md`
- Add or update a short front-door map aligning with the README.

### Task 5 — GitHub description local note
- Create or modify: `docs/github-repo-description.md`
- Include recommended description and future commands:
  - `gh repo edit itsnmills/small-practice-security-kit --description "PHI-avoidant security readiness packet builder for small healthcare practices."`
- Note local blocker: if `gh` is unavailable, update via GitHub UI.

## Test Plan

### Content validation
- Command: `.venv/bin/python scripts/validate_content.py`
- Expected: exits 0.

### Unit tests
- Command: `.venv/bin/python -m unittest discover -s tests`
- Expected: all tests pass.

### Diff/security review
- Command: `git diff --check`
- Expected: no whitespace errors.
- Command: `git diff | grep -Ei 'api[_-]?key|secret|token|password|private key|patient name|medical record|mrn' || true`
- Expected: no introduced secrets or PHI; disclaimer references may match terms but no actual sensitive values.

## Acceptance Criteria
- [ ] README top fold has immediate demo links and clear no-PHI/no-compliance-guarantee boundary.
- [ ] `What you get` emphasizes the flagship packet first.
- [ ] Repo map clarifies flagship vs module vs companion/reference.
- [ ] GitHub description text and update command are documented.
- [ ] Product map is consistent with the new positioning.
- [ ] Content validation passes.
- [ ] Full unit suite passes.
- [ ] Diff reviewed for unsafe claims/secrets/PHI.

## Codex Execution Prompt
Read this entire goal file. Implement the docs updates to production quality. Do not add placeholders, fake artifacts, or overclaiming HIPAA/compliance language. Preserve existing technical command sections and demo links. Run the verification plan and fix failures. Summarize changed files and exact command outputs.
