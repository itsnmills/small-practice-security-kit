# ePHI Flow Map

## Systems

| System | Category | ePHI Role | Vendor | Evidence Needed |
| --- | --- | --- | --- | --- |
| Cloud EHR | EHR | creates, receives, maintains, transmits | Example EHR Vendor | admin settings export, BAA, user access review |
| Billing Portal | Billing | receives, maintains, transmits | Example Billing Vendor | BAA, user list, incident contact |
| Shared Drive | File storage | maintains | Workspace Provider | access review, sharing settings, backup reference |

## Flows

| Flow | Source | Destination | Vendor | ePHI Type | BAA Needed | Risk | Evidence Needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FLOW-001 | Patient intake form | Cloud EHR | Example EHR Vendor | demographics, insurance, treatment notes | Yes | medium | BAA, portal access controls, intake workflow owner |
| FLOW-002 | Cloud EHR | Billing Portal | Example Billing Vendor | claim and billing data | Yes | high | BAA, integration owner, incident notification terms |
| FLOW-003 | Staff email | External specialist | Email provider | referral attachments | Yes | high | secure email policy, forwarding review, staff training |
