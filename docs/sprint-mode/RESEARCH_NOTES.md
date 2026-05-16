# Sprint Mode Research Notes

Date: 2026-05-16

Research scope: repo inspection, Dario planning notes, and compact external scan. External sources were used only to shape workflow and wording; this public runner remains a local demo and does not provide legal, compliance, insurance, or breach advice.

## Sources Reviewed

- HHS/OCR risk analysis guidance: https://www.hhs.gov/hipaa/for-professionals/security/guidance/guidance-risk-analysis/index.html
- HHS/OCR business associate guidance: https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/business-associates/index.html
- HHS HPH Cybersecurity Performance Goals summary: https://asprtracie.hhs.gov/technical-resources/resource/12863/healthcare-and-public-health-sector-specific-cybersecurity-performance-goals
- FTC Cybersecurity for Small Business: https://www.ftc.gov/business-guidance/small-businesses/cybersecurity
- NAIC/FTC cyber insurance small-business explainer: https://content.naic.org/sites/default/files/inline-files/cyber-insurance-naic.pdf
- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
- NIST AI RMF Playbook: https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook
- CMS responsible AI guidance: https://security.cms.gov/policy-guidance/guidance-responsible-use-artificial-intelligence-ai-cms
- Dario planning notes under `/home/noahops/Dario/Velari/planning/`.

## 1. Domain/Workflow Findings

Small healthcare practices need a workflow that starts with where ePHI can move, not with a broad questionnaire. HHS/OCR frames risk analysis as foundational and says there is no one-size-fits-all method; the output should help identify safeguards for confidentiality, integrity, and availability of ePHI. That supports a guided sprint that maps systems, vendors, AI uses, access, backups, downtime, and evidence before making a roadmap.

The buyer/user set is mixed: owner, office manager, MSP, consultant, and downstream legal/compliance reviewer. The packet must make handoff questions explicit because the owner often controls priorities, while the MSP controls exports, MFA, backup evidence, and access lists.

Evidence gaps that matter in a sellable sprint:

- MFA enforcement evidence for EHR, email, billing, remote support, and administrator accounts.
- User access and offboarding review evidence.
- Backup scope and restore-test evidence.
- Downtime procedure and tabletop evidence.
- Vendor/BAA status, incident terms, subcontractors, and AI/data-use posture.
- Cyber insurance renewal evidence for controls, incident response, third-party dependencies, and business interruption readiness.
- AI workflow decisions that separate no-PHI administrative drafting from restricted or prohibited workflows.

## 2. Product/Design Findings

Owner/MSP-readable output should avoid generic checklist language. Every stage should answer:

- What did we review?
- What evidence would prove it?
- Who acts next?
- What output artifact should they open?
- What must not be shared in this public/demo packet?

The product value is orchestration, not another evidence repo. Dario planning notes explicitly position `small-practice-security-kit` as the public proof/demo packet generator and `velari-secure-practice` as the private app shell. Sprint Mode should therefore wrap existing packet, manifest, and binder export logic instead of inventing a parallel packet system.

The output should use "readiness signal," "evidence posture," and "reference-only evidence" rather than "HIPAA score," "certified," or "compliant." This matches the current repo boundary and avoids overclaims.

## 3. Data/Safety Findings

Accepted inputs:

- Synthetic practice names and scenarios.
- Practice type, staff count, locations, owner roles, and review period.
- System, vendor, workflow, and role names.
- Evidence IDs, folder labels, ticket references, and status summaries.
- BAA status summaries and incident-term review status.
- AI workflow descriptions that do not include patient-level data.

Prohibited inputs:

- Patient names, MRNs, dates of birth, diagnoses, chart notes, patient images, claim contents, clinical narratives, raw incident details, credentials, API keys, tokens, private keys, MFA recovery codes, private URLs, presigned links, raw contracts, raw logs, and screenshots containing sensitive data.

The evidence model should remain reference-only. The runner can say which evidence should exist and where the reference belongs, but it should not store or request raw evidence.

AI governance should be conservative. NIST AI RMF and CMS AI guidance both support documented risk review, ongoing monitoring, human review, and prohibitions on entering PHI or sensitive data into public AI tools. Sprint Mode should produce staff-facing boundaries and owner/MSP questions, not approve AI tools as safe for PHI.

## 4. Implementation Findings

Existing modules to reuse:

- `small_practice_security_kit.profile.load_profile` for schema validation.
- `small_practice_security_kit.sensitive_data.blocking_findings` for high-confidence sensitive data blocking.
- `small_practice_security_kit.packet.build_packet` for existing Markdown/HTML packet artifacts.
- `small_practice_security_kit.manifest.build_packet_manifest` indirectly through `build_packet`.
- `small_practice_security_kit.adapters.evidence_binder.export_binder_index` for binder-compatible CSV/Markdown exchange artifacts.
- Existing safety/content validation and unit tests.

Do not duplicate:

- Packet section rendering.
- Manifest hashing and evidence reference model.
- Binder export rows.
- Sensitive-data scanning.
- Dashboard or private app UX.

Implementation shape chosen:

- Add `small_practice_security_kit/sprint.py`.
- Add `python3 -m small_practice_security_kit sprint <profile> --output-root <dir>`.
- Generate Sprint Mode overlays in the same practice output directory:
  - `sprint-index.md`
  - `sprint-summary.json`
  - `risk-register.csv`
  - `evidence-index.json`
  - `handoff-actions.csv`
  - `evidence-binder-export/`
