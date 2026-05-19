# Vendor, BAA, And AI Questionnaire

Use this as a source-backed question list, not as legal advice or vendor approval. Keep answers, contracts, screenshots, and links in the private/offline binder; enter only reference IDs and short status summaries in public artifacts.

## Vendors In Scope

| Vendor | Service | Touches ePHI-like workflow? | BAA status | SOC 2 status | HITRUST status | AI training/use | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Example EHR Vendor | EHR hosting and support | yes | signed | not provided | not provided | not reviewed | medium |
| Example Billing Vendor | Claims and billing | yes | missing review date | not provided | not provided | unknown | high |
| Workspace Provider | Email, calendar, and shared drive | yes | signed | not provided | not provided | not reviewed for add-on AI features | medium |
| Example Imaging Vendor | Dental imaging software and support | yes | unknown | not provided | not provided | not applicable in current deployment | high |
| General AI Assistant Vendor | Administrative drafting assistant | no | not needed for no-PHI demo workflow | not applicable | not applicable | consumer/default settings not approved for sensitive data | medium |
| Example AI Scribe Vendor | AI scribe pilot | yes | requested | not provided | not provided | unknown | high |

## AI Workflows In Scope

| Workflow | Decision | Data used | Vendor | Evidence needed |
| --- | --- | --- | --- | --- |
| Marketing email drafting | allowed | No patient data | General AI assistant | staff guidance and prohibited data examples |
| Insurance renewal questionnaire drafting | allowed | Control status summaries and evidence reference IDs only | General AI assistant | owner review and no-PHI/no-secret prompt guidance |
| Billing appeal drafter | restricted | billing scenario summary; real patient-level details are not approved | General AI assistant | BAA review, redaction workflow, owner approval |
| AI scribe pilot | restricted | potential PHI if enabled after vendor approval | Example AI Scribe Vendor | BAA, retention/model-training terms, human review workflow, pilot owner signoff |
| Paste patient-level note into public chatbot | prohibited | patient-level documentation category | Public chatbot | training reminder and AI use policy |

## Questions To Ask

- Is a BAA available for the service and the workflow we use?
- Can you provide SOC 2 or HITRUST evidence for private review, or should the status be recorded as not provided, absent, or not applicable?
- Which legal entity provides the service, and who is the security or privacy contact?
- Which subcontractors or subprocessors may access, store, support, or process the data?
- What incident-notification terms apply, including timing, contact path, and required customer action?
- What are the retention, deletion, backup, export, and account-closure terms?
- Is customer data used for AI model training, product improvement, human review, analytics, or benchmarking?
- Can customer data be excluded from AI training or human review, and is the setting on by default or configurable?
- Which access controls are available: MFA, SSO, role-based access, admin roles, support access approval, and offboarding?
- Are audit logs available for user activity, admin changes, support access, exports, deletions, and failed logins?
- Can the practice export all needed data and delete data on request or at termination?
- What security documentation can be reviewed by the practice or qualified reviewer without exposing PHI?

## Reviewer Notes

- If a vendor touches ePHI-like workflows or could receive patient, billing, clinical, credential, or raw evidence details later, escalate unanswered BAA, SOC 2/HITRUST evidence status, subcontractor, incident notice, retention/deletion, and AI training-use questions.
- Do not treat a vendor marketing page as enough by itself. Ask for the contract lane, security contact, and evidence reference a qualified reviewer can inspect privately.
- Do not paste patient examples, chart content, claim details, credentials, logs, raw contracts, or private links into vendor questionnaires generated from this public repo.
