# Sprint Mode Delivery Playbook

## 1. Prepare the Profile

Use a synthetic or sanitized profile. Confirm the profile contains only reference metadata:

- practice size and owner roles,
- system and vendor names,
- workflow summaries,
- evidence reference IDs,
- BAA/review status summaries,
- no PHI, no secrets, no raw evidence.

Run:

```bash
python3 -m small_practice_security_kit validate samples/family_dental_clinic.yaml
```

## 2. Run the Sprint Packet

Run:

```bash
python3 -m small_practice_security_kit sprint samples/family_dental_clinic.yaml --output-root out
```

Open `out/family_dental_clinic/sprint-index.md` first.

## 3. Owner Review

Use `sprint-index.md` and `sprint-summary.json` to walk the owner through:

- top stage statuses,
- high-priority evidence gaps,
- what the packet does not prove,
- which decisions require owner approval,
- what should go to the MSP, vendors, insurer, or legal/compliance reviewer.

Do not collect raw evidence in the public demo repo.

## 4. MSP Review

Use `handoff-actions.csv` and `owner-msp-handoff.md` to request:

- MFA enforcement evidence,
- user list and access review exports,
- backup scope and restore-test evidence references,
- downtime procedure status,
- remote support and administrator account review,
- log review cadence status.

Ask for evidence references or sanitized summaries, not raw screenshots, logs, credentials, or private links.

## 5. Vendor/BAA Review

Use `vendor-baa-review.md`, `risk-register.csv`, and `evidence-binder-export/evidence-binder-index.csv` to track:

- BAA status and review date,
- incident notification terms,
- subcontractor posture,
- AI/model-training/data-use terms,
- security contact and support escalation path.

## 6. AI Workflow Review

Use `ai-workflow-review.md` to separate:

- allowed no-PHI administrative drafting,
- restricted workflows that need vendor, BAA, redaction, or owner approval,
- prohibited workflows such as entering patient-level content into public chatbots.

The default public-demo rule is no PHI in public AI tools.

## 7. Evidence Binder Export

Use `evidence-index.json` and `evidence-binder-export/` to seed a private evidence binder. Keep raw evidence in restricted client-approved locations outside this public repo.

## 8. Roadmap and Handoff

Use:

- `risk-register.csv` for assigned findings,
- `30-60-90-roadmap.md` for sequencing,
- `handoff-actions.csv` for owner/MSP/vendor questions,
- `limitations-appendix.md` for the boundary statement.

Close the sprint only after open questions have owners and next review dates.
