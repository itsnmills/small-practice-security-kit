# Velari Cyber Readiness Sprint Offering Blueprint

## Positioning

Velari Cyber Readiness Sprint for Small Healthcare Practices is a short, local-first readiness sprint for owners, office managers, MSPs, vendor reviewers, and legal/compliance reviewers.

The promise is practical: map where ePHI-like workflows create risk, show which evidence is missing, turn guidance into questions the practice can ask this week, and separate owner/MSP/vendor/legal lanes without moving PHI or raw evidence into the public repo.

## Source Anchors

- HHS Cyber Gateway: https://hhscyber.hhs.gov/
  - Sprint implication: frame the packet around patient safety and care continuity, not abstract IT maturity.
- HHS 405(d) HICP: https://405d.hhs.gov/cornerstone/hicp
  - Sprint implication: ask about social engineering, ransomware, lost equipment or data, insider data loss, connected devices, email, endpoint, identity, data protection, assets, network, vulnerability, response, and governance evidence.
- CISA Cybersecurity Performance Goals: https://www.cisa.gov/cybersecurity-performance-goals-2-0-cpg-2-0 and https://www.cisa.gov/cybersecurity-performance-goals-cpgs
  - Sprint implication: treat CPGs as voluntary high-impact baseline practices and translate them into asset, ownership, MFA, backup, incident response, third-party, and known-exploited-vulnerability questions.
- ONC/OCR Security Risk Assessment Tool: https://healthit.gov/privacy-security/security-risk-assessment-tool/
  - Sprint implication: keep the public runner local-first/reference-only and route formal risk assessment decisions to qualified reviewers.

## Included Scope

- Intake safety boundary and owner/MSP lane assignment.
- Patient-data-outside-EHR workflow map.
- AI workflow review with no-PHI, restricted, and prohibited-use prompts.
- Vendor, BAA, subcontractor, incident notice, retention/deletion, and AI training-use questions.
- Access, MFA, offboarding, shared-account, and admin-role evidence requests.
- Backup, restore-test, ransomware, downtime, and tabletop readiness prompts.
- Reference-only evidence checklist for a private/offline binder.
- First 7 days owner action plan and MSP remediation brief.
- Source map that explains why each stage asks what it asks.
- Machine-readable `offering_summary` in `sprint-summary.json` for future private-app import.

## Excluded Scope

- PHI, patient identifiers, credentials, secrets, private URLs, presigned links, raw contracts, raw logs, screenshots with sensitive data, and incident-sensitive details.
- Formal Security Risk Analysis, legal/compliance conclusions, incident reporting decisions, cyber-insurance advice, penetration testing, vulnerability scanning, MDR, SOC, forensic work, live system verification, vendor acceptance, or AI production-use authorization.
- Any claim that a practice, vendor, system, workflow, AI tool, or evidence binder satisfies a legal or regulatory requirement.

## Audience Value

| Audience | Value delivered |
|---|---|
| Practice owner / office manager | Plain-English top gaps, first-week actions, and scripts to send to the MSP, vendors, and reviewers. |
| MSP / IT partner | Technical checks, expected proof, stage reference, owner, priority, and source mapping without requiring direct access through the public runner. |
| Vendor / BAA / AI reviewer | Answerable questions about BAA scope, subcontractors, incident notice, retention/deletion, AI training-use, access controls, audit logs, and export/delete capability. |
| Legal / compliance reviewer | Bounded review prompts, escalation triggers, and a clear distinction between readiness evidence and professional determinations. |

## Delivery Flow

1. Confirm safety boundary: no PHI, no secrets, no raw evidence, reference metadata only.
2. Review practice profile: owner, technical owner, systems, vendors, workflows, AI use, downtime systems, and evidence references.
3. Build Sprint Mode packet:

   ```bash
   python3 -m small_practice_security_kit sprint samples/family_dental_clinic.yaml --output-root out
   ```

4. Start with `sprint-command-center.html` and `sprint-offering-readout.md`.
5. Use `owner-action-plan.md` for the first 7 days.
6. Send `msp-remediation-brief.md` to the MSP for evidence references and remediation sequence.
7. Send `vendor-baa-ai-questionnaire.md` to vendor owners or qualified reviewers.
8. Use `evidence-collection-checklist.md` to gather proof in the private/offline binder.
9. Use `source-map.md` to explain how HHS/HICP/CISA/ONC-OCR anchors shaped the questions.
10. Import `sprint-summary.json`, `evidence-index.json`, `risk-register.csv`, and `handoff-actions.csv` into the private app only after review.

## Artifacts

| Artifact | Purpose |
|---|---|
| `sprint-offering-readout.md` | Client-ready readout: what was reviewed, patient-safety/trust meaning, top gaps, first-week actions, questions to send, source anchors, and limitations. |
| `owner-action-plan.md` | Office-manager plan with first 7 days and scripts/questions for MSP, vendors, and reviewers. |
| `msp-remediation-brief.md` | IT handoff converting gaps into technical checks, expected proof, owners, stage references, and source mapping. |
| `vendor-baa-ai-questionnaire.md` | Vendor/BAA/AI questions for BAA availability, subcontractors, incident notice, retention/deletion, AI training-use, access controls, logs, and export/delete. |
| `evidence-collection-checklist.md` | Exact reference-only evidence checklist for private/offline collection. |
| `day-one-workshop-agenda.md` | First client session agenda with discovery questions, evidence boundaries, lanes, and expected outputs. |
| `source-map.md` | Source-to-stage map showing how each federal anchor changes Sprint Mode questions. |
| `sprint-summary.json` | Machine-readable stage, risk, handoff, output, and `offering_summary` contract. |
| `evidence-index.json` | Reference-only evidence overlay for private binder import. |
| `risk-register.csv` and `handoff-actions.csv` | Sortable action rows for owner/MSP/vendor/reviewer lanes. |

## Safety Boundaries

- Use synthetic or client-supplied reference metadata only.
- Keep raw evidence in the private/offline binder.
- Public artifacts may contain evidence IDs, dates observed, owner roles, statuses, and short notes.
- Public artifacts must not contain PHI, patient identifiers, credentials, secrets, private URLs, presigned links, raw contracts, raw logs, screenshots with sensitive data, or incident-sensitive details.

## When To Involve MSP, Legal, Or Compliance

- Involve the MSP when MFA, access lists, admin roles, remote support, backup scope, restore testing, logs, patching, or known-exploited-vulnerability handling is unclear.
- Involve vendors or vendor owners when BAA status, subcontractors, incident-notification terms, retention/deletion, AI training-use, support access, audit logs, or export/delete capability is unclear.
- Involve legal/compliance reviewers when contract interpretation, formal risk assessment, incident reporting, insurance, AI rollout, vendor data use, or policy acceptance decisions are needed.
- Pause public-runner use and move to qualified incident response if there is a suspected active incident, ransomware event, lost device, unauthorized disclosure, or urgent legal/insurance question.

## Private App Integration Later

The public runner now exposes `offering_summary` inside `sprint-summary.json` so `velari-secure-practice` can import:

- offering name and positioning,
- audience lanes,
- source anchors,
- first 7 days actions,
- top value outcomes,
- artifact checklist,
- boundary statements,
- escalation triggers,
- stage-to-source mapping.

The private app should treat this as a reviewed draft. It can seed client workspaces, tasks, evidence requests, reviewer lanes, and source-backed checklists, but raw evidence import should stay behind private auth, storage controls, and reviewer approval.
