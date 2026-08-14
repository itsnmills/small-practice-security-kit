# ePHI Flow Map

4 flows never touch the EHR; 2 leave or enter the chart. The high-risk paths that stay off the chart are email, imaging / export, and ai tool.

## Patient Data Outside the EHR

- **Cloud EHR → Billing Portal** — Leaves or enters the EHR. Billing / claims. high risk. BAA needed. billing and payer-submission categories. Evidence: BAA, integration owner, incident notification terms.
- **Staff email → External specialist** — Never touches the EHR. Email. high risk. BAA needed. referral attachments. Evidence: secure email policy, forwarding review, staff training.
- **Dental Imaging Workstation → Shared Drive** — Never touches the EHR. Imaging / export. high risk. BAA needed. image export categories. Evidence: export procedure, shared-folder access review, backup scope reference.
- **Provider conversation → AI Scribe Pilot** — Never touches the EHR. AI tool. high risk. BAA needed. potential visit-summary categories if approved after vendor review. Evidence: BAA, retention terms, model-training terms, human review approval.
- **Patient intake form → Cloud EHR** — Leaves or enters the EHR. Vendor portal / intake. medium risk. BAA needed. demographic and insurance categories. Evidence: BAA, portal access controls, intake workflow owner.
- **Front desk notes → General AI Assistant** — Never touches the EHR. AI tool. medium risk. no BAA flag. no patient data approved; generic administrative drafting only. Evidence: AI acceptable-use guidance and staff acknowledgement.
