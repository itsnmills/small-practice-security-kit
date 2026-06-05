# External Evidence Pre-Check

Purpose: collect safe public-site observations that can be turned into owner, MSP, website vendor, and qualified-review questions before a practice shares internal access or patient data.

Status: **synthetic demo observations only**

Authorization boundary: **Demo data only. For a real practice, run public-site checks only with written authorization, no real patient submissions, and reference-only evidence.**

## Scope Reviewed

| Type | Target | Context |
| --- | --- | --- |
| Domain | familydental.example | Public DNS/website context only |
| scheduler | Appointment scheduler | appointment request categories; no real form submission in demo |
| intake | New patient intake | demographic and insurance categories; no real form submission in demo |
| portal | Patient portal login | authenticated portal context to review with vendor |

## Observations

| ID | Priority | Page/workflow | Observed item | Destination or host | Send to | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| EXT-TRACKER-SCHEDULER-001 | high | Appointment scheduler | Meta Pixel | connect.facebook.net and graph.facebook.com | Vendor/legal/compliance reviewer | Ask the website vendor and qualified privacy reviewer whether this tracker should be removed or restricted on scheduler pages. |
| EXT-TRACKER-INTAKE-002 | high | New patient intake | Google Tag Manager and Google Analytics | googletagmanager.com and google-analytics.com | Vendor/legal/compliance reviewer | Ask the website vendor to document tag purpose, data sent, and whether the intake workflow should suppress analytics tags pending reviewer decision. |
| EXT-TLS-PORTAL-003 | medium | Patient portal login | HTTPS certificate and redirect posture | portal.familydental.example | MSP | Ask the MSP or portal vendor for TLS scan summary, certificate expiry, redirect behavior, HSTS status, and covered host list. |

## Questions This Creates

| Recipient | Question | Evidence to request |
| --- | --- | --- |
| Website vendor / tag manager owner | Which trackers, analytics tags, pixels, or scripts fire on appointment, intake, portal, payment, registration, or contact workflows? | Tracker inventory, tag manager export, page/workflow label, date observed, and sanitized network destination summary. |
| Privacy/legal/compliance reviewer | Does any tracker observation require BAA, authorization, privacy notice, contract, or formal risk-analysis review before the practice relies on the workflow? | Reviewer disposition, vendor relationship status, data category summary, and decision note. |
| MSP / website host | Can you confirm HTTPS redirect behavior, certificate validity, TLS posture, HSTS status, and ownership for patient-facing hosts? | TLS scan summary, certificate expiry/issuer, HSTS status, covered host list, and MSP/vendor attestation. |

## Review Basis

- HHS/OCR tracking technology guidance says regulated entities must evaluate tracking technologies in authenticated pages and other contexts where PHI may be collected or disclosed.
- A June 20, 2024 federal court order vacated the portion of OCR guidance that treated an IP address plus a visit to certain unauthenticated public webpages as automatically triggering HIPAA obligations.
- This packet therefore flags potential privacy/security evidence questions for review. It does not declare a HIPAA violation, breach, legal conclusion, or regulatory finding.

## Evidence Safety Boundary

- Do not submit real patient forms during public-site testing.
- Do not store patient-entered details, session cookies, private admin links, credentials, raw logs, raw contracts, or full intercepted payloads with sensitive data.
- Use page labels, timestamps, tag/script names, destination domains, certificate status, owner, and reference IDs.
- Keep screenshots or browser captures sanitized and in the private/offline evidence binder if needed.
