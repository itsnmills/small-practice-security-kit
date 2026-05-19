# MSP Evidence Request

Practice: **Family Dental Clinic**

Purpose: give the MSP a narrow evidence request list without asking for PHI, credentials, private admin URLs, or raw logs.

## Do Not Send

Do not send PHI, patient identifiers, credentials, private admin URLs, raw logs, patient screenshots, full private contracts, or incident-sensitive details.

## Requested MSP Evidence

| Evidence | Cadence | Acceptable proof | Do not send | Next action |
|---|---|---|---|---|
| Downtime plan evidence | annual | downtime workflow map; tabletop exercise note; critical system owner list; manual workaround checklist | PHI or patient identifiers; credentials; private admin URLs; raw logs; patient screenshots; full private contracts | Run or schedule a downtime tabletop and record owner, MSP, and evidence references. |
| Remote access MFA enforcement evidence | quarterly | sanitized MFA policy export; conditional access policy reference; admin account MFA coverage report; signed MSP attestation with date and scope | PHI or patient identifiers; credentials; private admin URLs; raw logs; patient screenshots; full private contracts | Ask the MSP to confirm MFA is enforced for EHR, email, administrator accounts, remote support, and remote access tools. |
| Quarterly access review evidence | quarterly | user list export; admin role list; removed-account note; owner access-review signoff | PHI or patient identifiers; credentials; private admin URLs; raw logs; patient screenshots; full private contracts | Export user and admin-role lists, reconcile owners, and record quarterly owner signoff. |
| Offboarding completion record | event_driven | dated offboarding checklist; account disablement reference; equipment return reference; exception owner and sunset date | PHI or patient identifiers; credentials; private admin URLs; raw logs; patient screenshots; full private contracts | Confirm offboarding checklist ownership and evidence references for accounts, devices, and physical access. |
| Administrator account inventory | quarterly | admin account list; named account owner; MFA status for admin accounts; shared-account exception register | PHI or patient identifiers; credentials; private admin URLs; raw logs; patient screenshots; full private contracts | Inventory privileged accounts and document owner, MFA status, and shared-account exceptions. |
| Remote support access inventory | quarterly | vendor remote access list; support account owner; MFA and approval workflow reference; remote access exception log | PHI or patient identifiers; credentials; private admin URLs; raw logs; patient screenshots; full private contracts | Ask the MSP to list vendor support paths, named owners, MFA coverage, and disablement process. |
| Break-glass account record | quarterly | account purpose and owner; last test date; storage or escrow process reference; access alerting reference | PHI or patient identifiers; credentials; private admin URLs; raw logs; patient screenshots; full private contracts | Confirm break-glass accounts exist only where needed and have owners, test dates, and monitored use. |
| Backup scope evidence | quarterly | backup job summary; covered and excluded asset list; retention setting summary; backup owner attestation | PHI or patient identifiers; credentials; private admin URLs; raw logs; patient screenshots; full private contracts | Confirm backup coverage for critical systems and document exclusions with an owner. |
| Restore test evidence | quarterly | restore-test date; system tested; recovery owner; limitations and exclusions; private binder reference ID | PHI or patient identifiers; credentials; private admin URLs; raw logs; patient screenshots; full private contracts | Run or schedule a restore test for critical systems and keep reference-only evidence. |
| Patch status report | monthly | patch compliance summary; exception list; unsupported asset note; remediation owner and date | PHI or patient identifiers; credentials; private admin URLs; raw logs; patient screenshots; full private contracts | Ask the MSP for patch status, unsupported assets, exceptions, and remediation owners. |
| Vulnerability management evidence | monthly | sanitized scan date and scope; high-risk finding count; remediation status; owner and due date | PHI or patient identifiers; credentials; private admin URLs; raw logs; patient screenshots; full private contracts | Confirm scan scope and track remediation status without exporting raw findings into public artifacts. |
| Endpoint protection coverage evidence | monthly | protected endpoint count; missing agent list by asset category; alert owner; remediation notes | PHI or patient identifiers; credentials; private admin URLs; raw logs; patient screenshots; full private contracts | Request endpoint protection coverage for workstations, servers, and critical practice devices. |
| Log source and review cadence evidence | monthly | log source list; review cadence record; alert owner; escalation path; date last reviewed | PHI or patient identifiers; credentials; private admin URLs; raw logs; patient screenshots; full private contracts | Define log sources, review cadence, alert owner, and escalation route. |
| Device encryption and protection evidence | quarterly | encryption status summary; device lock policy; missing device exception list; owner remediation note | PHI or patient identifiers; credentials; private admin URLs; raw logs; patient screenshots; full private contracts | Confirm encryption and device protection status for laptops, workstations, and portable media. |
| Asset inventory and exposure evidence | quarterly | device and system inventory; internet-facing service list; owner and support path; exposure remediation note | PHI or patient identifiers; credentials; private admin URLs; raw logs; patient screenshots; full private contracts | Confirm asset inventory and internet-facing exposure without publishing IP addresses or private diagrams. |
| Media disposal or transfer record | event_driven | disposal or transfer date; device category; wiping or destruction method reference; owner signoff | PHI or patient identifiers; credentials; private admin URLs; raw logs; patient screenshots; full private contracts | Record disposal, transfer, wipe, or destruction evidence when devices or media leave service. |

## Preferred Response Format

- Evidence pointer or ticket/reference ID
- Source system
- Date observed
- Scope covered
- Reviewer/contact
- Exceptions and due dates

## Professional Review Boundary

This request supports readiness evidence collection. It does not ask the MSP to make legal conclusions, breach determinations, or compliance guarantees.
