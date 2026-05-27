# ePHI Flow Map

## Systems

| System | Category | ePHI Role | Vendor | Evidence Needed |
| --- | --- | --- | --- | --- |
| Cloud EHR | EHR | creates, receives, maintains, transmits | Example EHR Vendor | admin settings export, BAA, user access review |
| Billing Portal | Billing | receives, maintains, transmits | Example Billing Vendor | BAA, user list, incident contact |
| Shared Drive | File storage | maintains | Workspace Provider | access review, sharing settings, backup reference |
| Dental Imaging Workstation | Imaging | creates and maintains | Example Imaging Vendor | local account list, backup scope reference, vendor support access procedure |
| Patient Messaging Portal | Patient communications | receives and transmits | Example Messaging Vendor | BAA, secure message settings, retention settings |
| General AI Assistant | AI drafting | no PHI approved for public demo workflow | General AI Assistant Vendor | staff no-PHI guidance, acceptable-use acknowledgement |
| AI Scribe Pilot | AI documentation | potentially receives or creates ePHI if approved later | Example AI Scribe Vendor | BAA review, retention terms, human review process, pilot approval |

## Flows

| Flow | Source | Destination | Vendor | ePHI Type | BAA Needed | Risk | Lifecycle | Closeout | Evidence Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FLOW-001 | Patient intake form | Cloud EHR | Example EHR Vendor | demographic and insurance categories | Yes | medium | Requested | Needs evidence | BAA, portal access controls, intake workflow owner |
| FLOW-002 | Cloud EHR | Billing Portal | Example Billing Vendor | billing and payer-submission categories | Yes | high | Requested | Needs evidence | BAA, integration owner, incident notification terms |
| FLOW-003 | Staff email | External specialist | Email provider | referral attachments | Yes | high | Requested | Needs evidence | secure email policy, forwarding review, staff training |
| FLOW-004 | Dental Imaging Workstation | Shared Drive | Workspace Provider | image export categories | Yes | high | Requested | Needs evidence | export procedure, shared-folder access review, backup scope reference |
| FLOW-005 | Front desk notes | General AI Assistant | General AI Assistant Vendor | no patient data approved; generic administrative drafting only | No | medium | Provided | Closed | AI acceptable-use guidance and staff acknowledgement |
| FLOW-006 | Provider conversation | AI Scribe Pilot | Example AI Scribe Vendor | potential visit-summary categories if approved after vendor review | Yes | high | Requested | Needs evidence | BAA, retention terms, model-training terms, human review approval |

## Traceability Summary

| Flow | Trace | Downstream artifacts | Closeout rule |
| --- | --- | --- | --- |
| FLOW-001 | flows FLOW-001; systems Cloud EHR; vendors Example EHR Vendor | ephi-flow-map.md; evidence-binder-index.md | Close when owner, vendor path, BAA need, access/retention control, and private evidence reference are recorded. |
| FLOW-002 | flows FLOW-002; systems Cloud EHR, Billing Portal; vendors Example Billing Vendor | ephi-flow-map.md; evidence-binder-index.md | Close when owner, vendor path, BAA need, access/retention control, and private evidence reference are recorded. |
| FLOW-003 | flows FLOW-003; vendors Email provider | ephi-flow-map.md; evidence-binder-index.md | Close when owner, vendor path, BAA need, access/retention control, and private evidence reference are recorded. |
| FLOW-004 | flows FLOW-004; systems Dental Imaging Workstation, Shared Drive; vendors Workspace Provider | ephi-flow-map.md; evidence-binder-index.md | Close when owner, vendor path, BAA need, access/retention control, and private evidence reference are recorded. |
| FLOW-005 | flows FLOW-005; systems General AI Assistant; vendors General AI Assistant Vendor | ephi-flow-map.md; evidence-binder-index.md | Close when owner, vendor path, BAA need, access/retention control, and private evidence reference are recorded. |
| FLOW-006 | flows FLOW-006; systems AI Scribe Pilot; vendors Example AI Scribe Vendor | ephi-flow-map.md; evidence-binder-index.md | Close when owner, vendor path, BAA need, access/retention control, and private evidence reference are recorded. |
