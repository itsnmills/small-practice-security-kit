# AI Workflow Review

| Workflow | Use | Data Used | Vendor | Decision | Lifecycle | Closeout | Trace | Evidence Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Marketing email drafting | Draft generic outreach copy | No patient data | General AI assistant | allowed | Closed | Closed | flows FLOW-005; vendors General AI assistant; workflows Marketing email drafting | staff guidance and prohibited data examples |
| Insurance renewal questionnaire drafting | Draft plain-language answers for cyber insurance renewal questions | Control status summaries and evidence reference IDs only | General AI assistant | allowed | Closed | Closed | flows FLOW-005; vendors General AI assistant; workflows Insurance renewal questionnaire drafting | owner review and no-PHI/no-secret prompt guidance |
| Billing appeal drafter | Draft payer appeal language | billing scenario summary; real patient-level details are not approved | General AI assistant | restricted | Requested | Needs evidence | flows FLOW-005; vendors General AI assistant; workflows Billing appeal drafter | BAA review, redaction workflow, owner approval |
| AI scribe pilot | Draft visit summaries after provider review | potential PHI if enabled after vendor approval | Example AI Scribe Vendor | restricted | Requested | Needs evidence | flows FLOW-006; vendors Example AI Scribe Vendor; workflows AI scribe pilot | BAA, retention/model-training terms, human review workflow, pilot owner signoff |
| Paste patient-level note into public chatbot | Summarize patient-level documentation | patient-level documentation category | Public chatbot | prohibited | Blocked | Blocked | vendors Public chatbot; workflows Paste patient-level note into public chatbot | training reminder and AI use policy |

## Rules of Thumb

- Allowed: generic administrative drafting with no patient or clinical details.
- Restricted: workflows involving claim, treatment, billing, or operationally sensitive data.
- Prohibited: pasting patient-level notes or identifiers into tools without approved safeguards and a reviewed vendor relationship.
