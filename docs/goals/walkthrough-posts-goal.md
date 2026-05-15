# Walkthrough Posts Goal

**Goal:** Create 2–3 polished public walkthrough posts that turn the demo packet into recruiter/client-readable proof-of-work.

**Output path:** `~/Dario/Velari/Content/Small Practice Security Kit Walkthroughs/`

## Draft topics

1. **How a Small Clinic Can Inventory ePHI Flows Without Uploading PHI**
   - Lead with the Patient Data Outside the EHR map.
   - Use the demo `ephi-flow-map.md` as the example.
   - Emphasize evidence references, not raw patient data.

2. **Why Healthcare AI Governance Starts With Vendors, BAAs, and Evidence**
   - Use the demo `ai-workflow-review.md` and `vendor-baa-review.md`.
   - Show allowed/restricted/prohibited AI examples.
   - Avoid legal conclusions or AI fearmongering.

3. **A Local-First Security Review Packet for Small Healthcare Practices**
   - Walk through `review-packet.md`, `packet-manifest.json`, and `30-60-90-roadmap.md`.
   - Position the packet as an owner/MSP handoff, not certification.

## Acceptance criteria

- Each post is 900–1,400 words.
- Each post links to the relevant checked-in demo artifacts.
- Each post includes a short “what this does not prove” section.
- No PHI, client anecdotes, unverifiable statistics, legal claims, or compliance guarantees.
- Tone: practical, evidence-backed, founder/operator voice.

## Suggested implementation tasks

1. Create `~/Dario/Velari/Content/Small Practice Security Kit Walkthroughs/2026-05-15 Small Practice Security Kit Walkthroughs Index.md` with the index and publishing notes.
2. Draft post 1 from `docs/demo/ephi-flow-map.md` and `docs/security-model.md`.
3. Draft post 2 from `docs/demo/ai-workflow-review.md`, `docs/demo/vendor-baa-review.md`, and `docs/security-model.md`.
4. Draft post 3 from `docs/demo/review-packet.md`, `docs/demo/packet-manifest.json`, and `docs/demo/30-60-90-roadmap.md`.
5. Run `python scripts/validate_content.py` and manually scan for overclaims.

- Repository public mirror `docs/walkthroughs/*` was produced during implementation and then removed from repo, with final notes now maintained in Dario hub.
