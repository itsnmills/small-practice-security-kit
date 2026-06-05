# Evidence Collection Checklist

Reference-only rule: do not gather or store raw evidence in this public repo. Collect screenshots, exports, notes, policy pages, contract excerpts, and logs only in the private/offline evidence binder. In public outputs, use evidence IDs, dates observed, owners, short status summaries, and artifact references.

## Existing Evidence References

| Evidence ID | Evidence needed | Owner | Status | Artifact refs |
| --- | --- | --- | --- | --- |
| EXT-TRACKER-SCHEDULER-001 | Third-party tracker observed on appointment scheduler | Office Manager | provided | external-evidence-precheck.md |
| EXT-TRACKER-INTAKE-002 | Analytics tag observed on new patient intake page | Office Manager | provided | external-evidence-precheck.md |
| EXT-TLS-PORTAL-003 | Patient portal TLS and certificate evidence needs confirmation | MSP Lead | requested | external-evidence-precheck.md |
| EVID-ACCESS-Q2 | Quarterly access review export placeholder | Office Manager | partial | evidence-binder-index.md |
| EVID-BACKUP-RESTORE | Backup restore test record placeholder | MSP Lead | stale | evidence-binder-index.md |
| EVID-CYBER-INSURANCE | Cyber insurance renewal evidence list | Practice Owner | requested | evidence-binder-index.md |
| EVID-AI-GUIDANCE | Staff AI acceptable-use acknowledgement | Office Manager | requested | evidence-binder-index.md |
| EVID-VENDOR-BAA-GAPS | Vendor BAA and incident terms follow-up list | Office Manager | requested | evidence-binder-index.md |
| READINESS-MFA-EMAIL | Email MFA evidence | Office Manager | provided | readiness-review.md |
| READINESS-MFA-EHR | EHR MFA evidence | MSP Lead | missing | owner-msp-handoff.md, readiness-review.md |
| READINESS-UNIQUE-ACCOUNTS | Unique account evidence | MSP Lead | provided | owner-msp-handoff.md, readiness-review.md |
| READINESS-ACCESS-REVIEW | Quarterly access review evidence | MSP Lead | missing | owner-msp-handoff.md, readiness-review.md |
| READINESS-BACKUP-RESTORE | Backup restore evidence | MSP Lead | missing | downtime-ransomware-tabletop.md, readiness-review.md |
| READINESS-VENDOR-INVENTORY | Vendor inventory evidence | Office Manager | provided | vendor-baa-review.md, readiness-review.md |

## Exact Checklist For The Private Binder

- [ ] MFA status screenshot or admin export for EHR, billing, email, imaging, remote access, administrator, and vendor-support accounts.
- [ ] User list export and admin role list for EHR, billing, imaging, email, shared drive, and remote support.
- [ ] Quarterly access review signoff with removed accounts, exception owners, and dates observed.
- [ ] Backup scope summary and backup restore test note for EHR exports, billing data, shared drive, imaging workstation, and key endpoints.
- [ ] Downtime tabletop agenda, participant list by role, manual workflow decisions, and lessons learned.
- [ ] BAA link/status label, SOC 2/HITRUST status label, vendor security contact, incident notice terms, subcontractor answer, and review date.
- [ ] AI tool policy page, admin settings, retention/model-training terms, staff no-PHI guidance, and acknowledgement reference.
- [ ] Cyber insurance questionnaire evidence references for MFA, backups, incident response, vendor access, training, and endpoint controls.
- [ ] Security awareness training completion summary and phishing/social-engineering reminder reference.
- [ ] Asset list for critical systems, owner, vendor, access method, and patch/vulnerability owner.
- [ ] Log review cadence note showing source systems, reviewer, escalation path, and last review date.
- [ ] Secure email or messaging settings for referral attachments and patient communications.

## What To Record In Public Artifacts

- Evidence ID or ticket/reference label.
- Owner role and date observed.
- Status: missing, requested, partial, reviewed, outdated, or not applicable.
- Short note about what is needed next.
- No PHI, patient identifiers, credentials, secrets, private URLs, presigned links, raw contracts, raw logs, screenshots with sensitive data, or incident-sensitive details.
