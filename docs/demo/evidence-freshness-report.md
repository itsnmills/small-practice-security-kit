# Evidence Freshness Report

Practice: **Family Dental Clinic**

Review period: **2026 Q2**

This report maps Velari action packets to dated evidence expectations. It supports readiness review and professional assessment; it does not provide legal advice, establish legal or regulatory status, guarantee insurer acceptance, or replace a formal Security Risk Analysis.

## Safety Boundary

Do not send PHI, patient identifiers, credentials, private admin URLs, raw logs, patient screenshots, full private contracts, or incident-sensitive details.

## Summary

- Total control/evidence rows: 30
- Mapped controls: 20
- Evidence needing attention: 30
- Freshness statuses: {"missing": 30}
- Evidence statuses: {"gated": 3, "missing": 26, "needs_professional_review": 1}

## Top Missing Or Stale Evidence

| Control | Owner | Evidence status | Freshness | Cadence | Next action |
|---|---|---|---|---|---|
| Security official and accountable owner designated | owner | missing | missing | annual | Confirm the named owner for security readiness decisions and where owner/MSP handoffs are recorded. |
| Security risk analysis record | legal_compliance | needs_professional_review | missing | annual | Identify whether a current formal risk analysis exists and route gaps to qualified professional review. |
| Risk treatment and corrective action register | owner | missing | missing | monthly | Assign each open finding to an owner, due date, and evidence reference. |
| Security policy set with last review date | office_manager | missing | missing | annual | Record the current policy set, last review date, owner, and staff acknowledgement reference. |
| Workforce security training record | office_manager | missing | missing | annual | Confirm current staff training completion and record the date and evidence reference. |
| Incident response plan and contact tree | owner | missing | missing | annual | Confirm the incident contact tree and separate technical response from qualified notice decisions. |
| Contingency, downtime, and disaster recovery plan | msp | missing | missing | annual | Run or schedule a downtime tabletop and record owner, MSP, and evidence references. |
| Evidence freshness report | velari_reviewer | missing | missing | monthly | Review missing and stale evidence weekly until owner, MSP, and vendor asks are assigned. |
| MFA coverage for email, cloud, admin, and remote access | msp | missing | missing | quarterly | Ask the MSP to confirm MFA is enforced for EHR, email, administrator accounts, remote support, and remote access tools. |
| User access review for EHR, email, file shares, billing, VPN, and RMM | msp | missing | missing | quarterly | Export user and admin-role lists, reconcile owners, and record quarterly owner signoff. |
| Termination and offboarding evidence | office_manager | missing | missing | event_driven | Confirm offboarding checklist ownership and evidence references for accounts, devices, and physical access. |
| Privileged and administrator account inventory | msp | missing | missing | quarterly | Inventory privileged accounts and document owner, MFA status, and shared-account exceptions. |

## This Week

- Review the missing MSP-owned and vendor-owned evidence rows.
- Send `msp-evidence-request.md` and `vendor-evidence-request.md` instead of forwarding raw exports.
- Record evidence pointers, dates, owners, and reviewer notes before uploading any files.

## 30 / 60 / 90 Day Use

- 30 days: close MFA, access review, BAA, backup restore, and incident contact evidence gaps.
- 60 days: verify patch/vulnerability, log review, endpoint, device, and policy evidence.
- 90 days: refresh the matrix, review exceptions, and export a PHI-safe owner/MSP packet.
