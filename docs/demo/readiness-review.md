# Readiness Review

Practice: Family Dental Clinic

Overall initial risk: **High**

| Item | Ready? | Area |
| --- | --- | --- |
| Email MFA | Yes | Access |
| EHR MFA | No | Access |
| Unique accounts | Yes | Access |
| Quarterly access review | No | Evidence |
| Tested backups | No | Resilience |
| Vendor inventory | Yes | Vendor |
| BAA register | No | Vendor |
| Incident contact list | Yes | Incident |
| Downtime plan | No | Resilience |
| Training current | Yes | Workforce |
| Log review cadence | No | Monitoring |

## Priority Gaps

- Enable MFA for EHR access.
- Run and record a quarterly access review.
- Run a restore test and record evidence.
- Complete the BAA register and review dates.
- Document downtime procedures for critical systems.
- Set a monthly log review cadence.

## Evidence Closeout Queue

| Item | Lifecycle | Closeout | Owner | Acceptable evidence | Closeout rule |
| --- | --- | --- | --- | --- | --- |
| EHR MFA evidence | Missing | Blocked | MSP Lead | MFA enforcement export; admin screenshot with date observed; covered groups; exceptions; and MSP attestation | Close when mfa enforcement export, admin screenshot with date observed, covered groups, exceptions, and msp attestation are recorded as reference-only evidence. |
| Unique account evidence | Provided | Closed | MSP Lead | User list export; shared-account exception list; owner signoff; and sunset dates | Close when user list export, shared-account exception list, owner signoff, and sunset dates are recorded as reference-only evidence. |
| Quarterly access review evidence | Missing | Needs evidence | MSP Lead | User list export; admin role list; owner signoff; removed-account notes; and exception sunset dates | Close when user list export, admin role list, owner signoff, removed-account notes, and exception sunset dates are recorded as reference-only evidence. |
| Backup restore evidence | Missing | Blocked | MSP Lead | Backup scope summary; restore-test note; date observed; recovery owner; and excluded systems | Close when backup scope summary, restore-test note, date observed, recovery owner, and excluded systems are recorded as reference-only evidence. |
| BAA register evidence | Missing | Blocked | Office Manager | BAA status; review date; vendor security page; SOC 2/HITRUST status; and incident terms | Close when baa status, review date, vendor security page, soc 2/hitrust status, and incident terms are recorded as reference-only evidence. |
| Downtime plan evidence | Missing | Blocked | MSP Lead | Downtime workflow; manual workaround owner; staff acknowledgement; and tabletop attendance | Close when downtime workflow, manual workaround owner, staff acknowledgement, and tabletop attendance are recorded as reference-only evidence. |
| Log review cadence evidence | Missing | Blocked | MSP Lead | Log source list; review cadence record; alert owner; escalation path; and date observed | Close when log source list, review cadence record, alert owner, escalation path, and date observed are recorded as reference-only evidence. |
