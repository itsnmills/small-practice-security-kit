# Why Healthcare AI Governance Starts With Vendors, BAAs, and Evidence

AI governance gets framed as a tech stack decision, but in operational healthcare it is a workflow decision. The first layer is not model quality or a policy paragraph. It is knowing which workflows move sensitive material, and who owns each vendor path.

This walkthrough uses the synthetic sample in:

- `../demo/ai-workflow-review.md`
- `../demo/vendor-baa-review.md`

to show a practical path: make evidence first-class and policy practical.

## The order that actually works

The common mistake is to write a broad AI policy and then test current behavior against it. For small teams, that usually causes two problems:

1. the policy sounds great but is ignored in practice,
2. critical gaps become visible only during a pressure event.

A more effective order is:

- map workflow classes (allowed/restricted/prohibited),
- map vendor touchpoints and BAA posture,
- define review/approval steps,
- then finalize policy language.

The synthetic `ai-workflow-review.md` intentionally keeps this concrete. You can see the same workflow categorized three ways: marketing drafting, billing appeals, and clinical-note summarization. This one file gives the team a real decision gate for what is risky right now.

## Vendors are where many AI programs fail

A policy without vendor evidence decouples itself from reality. In many small practices, AI tools are introduced by staff need, then reviewed by operations later. That backward sequence hides risk.

In the demo `vendor-baa-review.md`, workflow ownership appears with risk labels:

- signed BAA but AI training use not reviewed,
- unknown incident terms,
- unknown subcontractor context,
- high-risk billing workflow lacking full visibility.

This is exactly the type of information that needs to be explicit, not implied.

## Evidence-first governance loop

The practical loop should be short enough to run every month:

1. **Capture new/changed AI workflow**
2. **Assign data class and decision status**
3. **Link to vendor + BAA status**
4. **Create a next-evidence step**
5. **Revisit in owner/MSP review cadence**

Every cycle should update the same reference list, not create new docs in ad hoc places.

## Use this as an onramp for operations, not a policy freeze

This packet model is designed for founder/operator execution:

- Staff can continue allowed admin AI use where safe,
- restricted workflows get a guardrail path and owner,
- prohibited workflows are blocked until evidence and process are corrected.

That is a realistic posture for small teams: you preserve productivity where risk is low and slow down only where risk needs scrutiny.

## The 4 checkpoints owners care about

1. **What changed?**
   - New workflow, new staff AI tool, new external vendor.
2. **Who owns it?**
   - Workflow owner and technical owner assigned.
3. **What is the vendor boundary?**
   - BAA status, training/use policy, incident terms.
4. **What is the next validation step?**
   - Evidence reference + deadline + status.

This mirrors how owner/MSP operations naturally runs. You can use those checkpoints as monthly agenda items.

## Common mistakes to avoid

- **Policy without workflow ownership**: creates ambiguous accountability.
- **Vendor review without data-class detail**: gives a false sense of control.
- **Restricting everything**: blocks productivity and encourages shadow AI use.
- **Allowing everything**: normalizes risk without controls.

The strongest outcome is the middle path: explicit classes with explicit exceptions.

## Why local-first helps here

The repo’s model in `docs/security-model.md` is intentionally local-first:

- no telemetry,
- no cloud sync,
- no hidden calls,
- no model calls in default mode.

That architecture matters for AI governance because it keeps discovery and planning in your control. The practice can decide governance policy without forcing a full data pipeline change.

## How to explain this to leadership in one breath

A concise founder framing:

> “We are not banning AI. We are defining exactly where AI can run today, and giving each risky workflow a specific owner, evidence requirement, and timeline.”

That message is usually easier to execute than broad policy claims.



## From synthetic example to live profile (minimal process)

The synthetic demo gives you a baseline structure, but real onboarding should stay intentional:

1. Interview the people currently using AI tools.
2. Capture each workflow in one line: task, input, destination, intended output.
3. Tag each row with data class and risk.
4. For rows touching PHI/billing/clinical context, attach a reviewed vendor row.
5. Add evidence references in owner-friendly language.

This process usually takes less time than a full policy rewrite and gives concrete items in one pass.

### MSP handoff pattern

When MSP support is involved, this is where ownership gets cleaner:

- MSP owns technical control implementation and restore/access verification.
- Owner runs workflow taxonomy and prioritizes business impact.
- Consultant or coach coordinates the manifest and review cadence.

You still keep the same output artifact family: packet + manifest + roadmap.

## What to include in your internal AI governance registry

A compact registry row should include:

- workflow name,
- data class,
- allowed/restricted/prohibited flag,
- vendor,
- owner,
- required evidence,
- next review date.

This is simple enough to maintain and hard enough to reduce ambiguity.

## Why this approach scales for recruiters/clients

This is recruiter- and client-friendly because it is practical:

- clear outcome language,
- clear ownership,
- no overstatement,
- and repeatable evidence behavior.

It communicates readiness in terms people understand: not just “security exists,” but “we have a map and a plan.”

## Command sequence for the repo workflow

```bash
python -m small_practice_security_kit validate samples/family_dental_clinic.yaml
python -m small_practice_security_kit build samples/family_dental_clinic.yaml
python -m small_practice_security_kit export-demo --profile samples/family_dental_clinic.yaml --output docs/demo
python scripts/validate_content.py
```

Run this when new workflow classes are added or vendor terms change.

## What this does not prove

- It does not certify legal compliance.
- It does not replace legal counsel, penetration testing, incident response, or formal Security Risk Analysis.
- It does not prove that every AI model or vendor is “safe by default.”
- It does not replace contract legal review when data-sharing terms change.

It is a practical governance scaffold, not a final assurance artifact.

## Links

- AI workflow matrix: [`../demo/ai-workflow-review.md`](../demo/ai-workflow-review.md)
- Vendor and BAA matrix: [`../demo/vendor-baa-review.md`](../demo/vendor-baa-review.md)
- Security model context: [`../security-model.md`](../security-model.md)
- Packet output context: [`../demo/review-packet.md`](../demo/review-packet.md)
