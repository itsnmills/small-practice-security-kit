# Portal And API Flow Review

This worksheet extends `ephi-flow-map.md` for portals, integrations, apps, and API/FHIR-style connections. It does not validate live APIs, prove identity controls, approve apps, or replace vendor/legal review.

## Portal And API Flows

| Flow | Source | Destination | Vendor/app owner | Connection | Data category | BAA needed | Evidence needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FLOW-001 | Patient intake form | Cloud EHR | Example EHR Vendor | HTTPS portal | demographic and insurance categories | Yes | BAA, portal access controls, intake workflow owner |
| FLOW-002 | Cloud EHR | Billing Portal | Example Billing Vendor | vendor integration | billing and payer-submission categories | Yes | BAA, integration owner, incident notification terms |
| FLOW-006 | Provider conversation | AI Scribe Pilot | Example AI Scribe Vendor | vendor app | potential visit-summary categories if approved after vendor review | Yes | BAA, retention terms, model-training terms, human review approval |

## Evidence Checklist

- [ ] Portal users and role list, including inactive or shared-account exceptions.
- [ ] Patient identity workflow: invitation, registration, reset, proxy/delegate access, and support verification.
- [ ] FHIR/app/API connections: app name, vendor owner, scope, authorization path, and review date.
- [ ] Audit logs for portal access, secure messages, exports, failed logins, admin changes, and support access.
- [ ] Secure messaging settings, attachment rules, retention, and deletion/export workflow.
- [ ] Vendor ownership, BAA status, incident notice, subcontractors, and data-use terms.

## Patient Identity Workflow

Document who can invite a patient, reset access, change contact details, approve proxy/delegate access, and handle portal support. Use reference IDs only; do not include patient examples.

## FHIR/app/API connections

For each app or integration, record owner, scope, vendor, authorization method, audit-log availability, export/delete path, and reviewer notes in the private binder.
