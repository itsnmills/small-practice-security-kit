# Local Intake Mode

The local intake mode turns the kit from a packet generator into an owner/MSP workflow.

It is designed around this loop:

```text
practice preset -> common systems -> suggested vendors/flows/evidence -> local save -> dashboard and packet
```

## What it does

- Creates a local profile under `profiles/`.
- Starts from practice-type presets instead of a blank form.
- Offers common healthcare system defaults.
- Builds vendor/BAA review rows from selected systems.
- Suggests ePHI flows from deterministic rules.
- Tracks evidence references without storing PHI.
- Includes AI workflow safety review.
- Generates the dashboard, packet, roadmap, and evidence index.

## Who it is for

- small healthcare MSPs,
- HIPAA consultants,
- solo compliance officers,
- practice administrators,
- tech-savvy clinic managers,
- healthcare security students and analysts,
- small healthcare startups and business associates.

The owner-friendly path is still important, but the best first user is often the person helping the practice gather a clean first-pass evidence packet.

## Presets included

- Dental
- Primary care / family medicine
- Behavioral health
- PT / OT / chiropractic
- Urgent care
- Specialty clinic
- Telehealth-first practice
- Small lab
- Billing / RCM company

## One-day setup workflow

1. Open `open_dashboard.command`.
2. Pick a practice preset and size tier.
3. Confirm the systems the practice uses.
4. Review generated vendors and BAA questions.
5. Review suggested ePHI flows.
6. Answer the short readiness checklist.
7. Review AI workflows and prohibited data guidance.
8. Add evidence references.
9. Generate the dashboard and packet.

## Evidence folder inventory

The evidence step can optionally scan a local evidence folder and import metadata-only references.

It does not read document contents. It records relative file names, extensions, sizes, modified timestamps, and reference paths so the packet can point reviewers to evidence without storing PHI.

## Non-goals

- It is not a HIPAA certification tool.
- It is not legal advice.
- It is not a formal Security Risk Analysis replacement.
- It is not a cloud GRC platform.
- It does not parse patient records.
- It does not use cloud AI.
