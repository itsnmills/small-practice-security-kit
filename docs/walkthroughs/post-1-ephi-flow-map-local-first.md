# How a Small Clinic Can Inventory ePHI Flows Without Uploading PHI

Small practices often discover the same pain after every external audit or security review: data appears to be “managed,” but no one can answer questions quickly because the practice evidence is fragmented across tools. The same pattern appears in incident response checklists, vendor calls, and insurer prep calls.

A reliable way to reduce this noise is to build a shared ePHI map before you start hardening. Not a huge enterprise toolchain. Not cloud exports. Just a local-first map of who touches what.

This walkthrough uses the synthetic Family Dental Clinic sample in this repo to show the baseline process: `docs/demo/ephi-flow-map.md`.

## Where teams get stuck (fast)

In early readiness conversations, I usually see one of three patterns:

1. **Checklist-only approach**: “We set up 15 items, check a few boxes, and call it done.”
2. **Tool-first approach**: “Our stack has logs; that should be enough.”
3. **Policy-only approach**: “We wrote a policy and then forgot to map workflows.”

The first two create false confidence. The map-first approach fixes both by creating a repeatable, evidence-linked model:

- what data leaves the EHR,
- where it lands next,
- which vendor touchpoint owns it,
- and which evidence reference closes each risk.

## Build the map from the synthetic sample

The demo map includes three representative flows:

- Patient intake to EHR,
- EHR to billing,
- staff email to external specialist.

That is intentionally short but complete enough to show the full pattern. Each row includes a **risk level** and **evidence need**.

What matters here is less the number of rows and more the fact that each row can be turned into an owner task.

## Treat flow mapping as an owner workflow, not documentation debt

Instead of “documenting” for its own sake, treat each flow row as a contract between operations and evidence collection:

- Who owns this flow?
- What exact evidence proves control in practice?
- What date does this need review?
- What is the escalation path when evidence is missing?

This is exactly why the map pairs with packet output and manifest metadata. The goal is to make a practical ownership loop that can be checked weekly.

## Keep it local-first from day one

One of the most important details in this repo is that nothing requires cloud syncing to run the map. This aligns with `docs/security-model.md` (local-only default, no telemetry, no hidden cloud calls).

That design choice does three things for owners:

- avoids accidental PHI exposure during mapping,
- reduces dependency on expensive infrastructure,
- keeps a team safe if they only need internal readiness prep today.

In practical terms: you can run the entire workflow from profile data and still produce a useful evidence map. That is exactly the kind of artifact a founder can use while planning upgrades.

## How to run this in practice

1. Define systems + flow names in a clean list.
2. For each flow, identify source, destination, and vendor.
3. Mark whether BAA is required (if ePHI touches that flow).
4. Assign a practical risk label and owner.
5. Convert each gap into evidence references.

In the demo files this translates to rows like:

- `FLOW-002`: EHR -> billing portal, high risk, BAA + incident terms missing.
- `FLOW-003`: email referral workflows, high risk, requires forwarding review and training.

No patient data, no account secrets, no incident logs exported—only references.

## Why evidence references beat raw file dumping

Most security work fails because people upload too much raw evidence and still cannot prove decision quality. This packet model avoids that by linking:

- *where evidence lives*,
- *what evidence should exist*,
- *who should provide it*.

This is especially useful for small teams because it maps cleanly to MSP and compliance reviews. It also keeps your public repo safe: all references are synthetic and scrubbed.

## Converting the map into action (without legal overclaiming)

The flow map alone is only half the loop. The next step is turning the map into prioritized follow-up:

- enable EHR MFA,
- define restore plan owners,
- schedule vendor review cadence,
- complete quarterly access review evidence.

That is where the packet becomes operational. It becomes less of a report and more of a control matrix that your owner and MSP can execute against.

## Suggested local command path

You can regenerate the sample map package from local profile and review the generated artifact structure:

```bash
python -m small_practice_security_kit validate samples/family_dental_clinic.yaml
python -m small_practice_security_kit build samples/family_dental_clinic.yaml
python -m small_practice_security_kit export-demo --profile samples/family_dental_clinic.yaml --output docs/demo
```

This gives you deterministic baseline files and a manifest-backed output for later review.

## What to say in leadership updates

For weekly check-ins with owners, this framing usually lands well:

- “We now have a complete map of ePHI flow paths and owner assignments.”
- “We can show evidence references next, not raw patient material.”
- “Next action is reducing high-risk and medium-risk flow gaps in a prioritized order.”

That keeps the review grounded and avoids the common drift into abstract compliance language.

## What this does not prove

- This does **not** prove full HIPAA compliance or legal sufficiency.
- It does **not** prove all real-world controls are already in place.
- It does **not** determine breach status.
- It does **not** certify vendors.
- It does **not** replace a formal risk analysis, legal review, penetration testing, or incident response function.

This is your practical evidence organizer. Treat it as a control roadmap and not as a certification.

## Links for reference

- Flow map: [`../demo/ephi-flow-map.md`](../demo/ephi-flow-map.md)
- Security boundary model: [`../security-model.md`](../security-model.md)
- Full review packet example: [`../demo/review-packet.md`](../demo/review-packet.md)
- Packet manifest: [`../demo/packet-manifest.json`](../demo/packet-manifest.json)
