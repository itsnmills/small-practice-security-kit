# 30 Controls, by hand

Worksheet for making `small-practice-security-kit` defensible. One entry per control in
`catalogs/control_evidence_matrix.yaml`. Two controls per session, roughly fifteen sessions.

## How a session works (30-45 minutes)

1. Pick the next unfinished control. Read its name and the prose refs already listed.
2. **Predict before you look.** Say out loud, or write on paper, which CFR section you
   think it lives in and whether you think it is required or addressable. This step is
   the entire difference between learning and transcribing. Do it every time, even when
   you feel sure, especially when you feel sure.
3. Open the eCFR section and find the actual standard or implementation specification.
   Score your prediction honestly. Being wrong is fine; it is the signal that you are
   working at the right depth.
4. Fill in all six fields in your own words. No copying sentences from the source.
5. Check the box only if you could answer a cold question about this control tomorrow.
6. Log the session at the bottom of this file, then commit:
   `git add docs/30-controls-worksheet.md && git commit -m "controls: N and M done by hand"`

The commits matter as much as the content. Fifteen dated commits over two months are
public proof that this was studied, not generated. Do not batch them.

Do this work in an editor with no AI completion (Obsidian, not Cursor). Autocomplete
will offer you the citations and defeat the exercise without you noticing.

## The rule for this document

**Fill this in yourself. Do not have an AI fill it in.**

That is not a principle, it is the entire mechanism. The point of this exercise is not to
have a correctly cited YAML file at the end. It is to have read the Security Rule closely
enough that when someone asks "which citation drives this control, and is it required or
addressable?" you answer from memory. A generated answer produces a better file and exactly
the same interview you are trying to avoid.

If you get stuck on one, leave it blank and come back. A blank is honest. A filled-in line
you cannot explain is the thing that got you here.

## Where to look things up

- **45 CFR Part 164 Subpart C** is the Security Rule itself. eCFR is the authoritative text:
  https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-C
  - `164.308` Administrative safeguards
  - `164.310` Physical safeguards
  - `164.312` Technical safeguards
  - `164.314` Organizational requirements (this is where BAA content lives)
  - `164.316` Policies, procedures, and documentation
- **Required vs addressable** is defined at `164.306(d)`. Read that one first, before any
  control. Addressable does not mean optional, and being able to explain that distinction
  cleanly is worth more in an interview than any single citation.
- **NIST SP 800-66r2** maps each Security Rule standard to practices in plain language:
  https://csrc.nist.gov/pubs/sp/800/66/r2/final
- **HHS 405(d) HICP**, use the Small volume specifically:
  https://405d.hhs.gov/documents (Health Industry Cybersecurity Practices, Technical Volume 1)
- **CISA Cross-Sector Cybersecurity Performance Goals:**
  https://www.cisa.gov/cross-sector-cybersecurity-performance-goals
- **HHS HPH sector CPGs:** https://hphcyber.hhs.gov/performance-goals.html
- For the "how this fails in real breaches" field:
  - OCR resolution agreements: https://www.hhs.gov/hipaa/for-professionals/compliance-enforcement/agreements/index.html
  - The HHS breach portal ("wall of shame"): https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf

## How to use the last two fields

"What a practice must actually produce" should be a concrete artifact a dental office could
hand you, not a restatement of the control. "A screenshot of the M365 admin center showing
MFA enforced for all 9 user accounts, dated" beats "evidence of MFA."

"How this fails in real breaches" is where the interview value is. Read OCR enforcement
actions and breach write-ups and connect each control to a case where its absence mattered.
The HHS breach portal and OCR settlement summaries are free and specific.

## Progress

0 / 30 complete.

---

## Administrative Safeguards (6)

### 1. `VEL-GOV-OWNER-001` — Security official and accountable owner designated
*Risk area: Governance. Current refs in repo: HIPAA Security Rule - assigned security responsibility; HHS HPH CPG - governance; CISA CPG - governance and cybersecurity leadership*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 2. `VEL-GOV-SRA-001` — Security risk analysis record
*Risk area: Risk Analysis. Current refs in repo: HIPAA Security Rule - risk analysis; ONC/OCR Security Risk Assessment Tool; HHS HPH CPG - risk management*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 3. `VEL-GOV-RISK-001` — Risk treatment and corrective action register
*Risk area: Corrective Action. Current refs in repo: HIPAA Security Rule - risk management; HHS HPH CPG - risk management; CISA CPG - vulnerability remediation planning*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 4. `VEL-GOV-POLICY-001` — Security policy set with last review date
*Risk area: Policy Review. Current refs in repo: HIPAA Security Rule - policies and procedures; HHS HPH CPG - policies and training*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 5. `VEL-WORKFORCE-TRAIN-001` — Workforce security training record
*Risk area: Workforce Training. Current refs in repo: HIPAA Security Rule - security awareness and training; HHS HPH CPG - security awareness training; CISA CPG - foundational cybersecurity training*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 6. `VEL-OFFBOARDING-001` — Termination and offboarding evidence
*Risk area: Offboarding. Current refs in repo: HIPAA Security Rule - workforce security; HIPAA Security Rule - access termination procedures; CISA CPG - account deprovisioning*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

## Physical Safeguards (2)

### 7. `VEL-PHYSICAL-ACCESS-001` — Physical access basics
*Risk area: Physical Access. Current refs in repo: HIPAA Security Rule - facility access controls; HIPAA Security Rule - workstation security; HHS HPH CPG - physical security basics*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 8. `VEL-MEDIA-DISPOSAL-001` — Device and media disposal or transfer evidence
*Risk area: Device / Media Handling. Current refs in repo: HIPAA Security Rule - device and media controls; HHS HPH CPG - asset management; CISA CPG - asset disposal*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

## Technical Safeguards (12)

### 9. `VEL-MFA-REMOTE-001` — MFA coverage for email, cloud, admin, and remote access
*Risk area: Access / MFA. Current refs in repo: HIPAA Security Rule - access control; HIPAA Security Rule - person or entity authentication; HHS HPH CPG - multifactor authentication; CISA CPG - implement MFA*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 10. `VEL-ACCESS-REVIEW-001` — User access review for EHR, email, file shares, billing, VPN, and RMM
*Risk area: Access Review. Current refs in repo: HIPAA Security Rule - access control; HHS HPH CPG - identity and access management; CISA CPG - account inventory*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 11. `VEL-PRIV-ACCOUNTS-001` — Privileged and administrator account inventory
*Risk area: Privileged Access. Current refs in repo: HIPAA Security Rule - access control; HHS HPH CPG - privileged access management; CISA CPG - admin account separation*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 12. `VEL-VENDOR-REMOTE-001` — Vendor and MSP remote access inventory
*Risk area: Vendor Remote Access. Current refs in repo: HIPAA Security Rule - access control; HIPAA Security Rule - business associate contracts; CISA CPG - third-party remote access*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 13. `VEL-BREAKGLASS-001` — Break-glass account register and last test date
*Risk area: Emergency Access. Current refs in repo: HIPAA Security Rule - emergency access procedure; HHS HPH CPG - account recovery; CISA CPG - resilience planning*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 14. `VEL-BACKUP-SCOPE-001` — Backup configuration and asset coverage
*Risk area: Backup / downtime. Current refs in repo: HIPAA Security Rule - data backup plan; HHS HPH CPG - backup and recovery; CISA CPG - data backup*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 15. `VEL-PATCH-MGMT-001` — Patch management report
*Risk area: Patch Management. Current refs in repo: HHS HPH CPG - vulnerability management; CISA CPG - patch vulnerabilities; NIST Cybersecurity Framework - protect and detect*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 16. `VEL-VULN-MGMT-001` — Vulnerability scan report and remediation status
*Risk area: Vulnerability Management. Current refs in repo: HHS HPH CPG - vulnerability management; CISA CPG - vulnerability remediation; NIST Cybersecurity Framework - identify and protect*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 17. `VEL-EDR-STATUS-001` — Endpoint protection or EDR status
*Risk area: Endpoint Protection. Current refs in repo: HHS HPH CPG - endpoint security; CISA CPG - security monitoring; NIST Cybersecurity Framework - detect*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 18. `VEL-LOG-REVIEW-001` — Log source inventory and log review record
*Risk area: Monitoring. Current refs in repo: HIPAA Security Rule - audit controls; HIPAA Security Rule - information system activity review; CISA CPG - logging*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 19. `VEL-ENCRYPT-DEVICE-001` — Encryption and device protection status
*Risk area: Device Protection. Current refs in repo: HIPAA Security Rule - encryption addressable implementation specification; HHS HPH CPG - endpoint security; CISA CPG - data protection*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 20. `VEL-ASSET-EXPOSURE-001` — Asset inventory and internet-facing exposure review
*Risk area: Asset Inventory. Current refs in repo: HHS HPH CPG - asset inventory; CISA CPG - asset inventory; CISA CPG - reduce exposure to common attacks*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

## Vendor / BAA / AI (6)

### 21. `VEL-VENDOR-INV-001` — Vendor inventory with ePHI access flag
*Risk area: Vendor / BAA. Current refs in repo: HIPAA Security Rule - business associate contracts; HHS HPH CPG - third-party risk management; CISA CPG - supply chain risk management*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 22. `VEL-BAA-STATUS-001` — BAA status and review date
*Risk area: Vendor / BAA. Current refs in repo: HIPAA Security Rule - business associate contracts; HHS HPH CPG - vendor management*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 23. `VEL-VENDOR-EVIDENCE-001` — Vendor security evidence status
*Risk area: Vendor Security Evidence. Current refs in repo: HHS HPH CPG - third-party risk management; CISA CPG - supply chain risk management; NIST Cybersecurity Framework - supply chain risk management*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 24. `VEL-VENDOR-TERMS-001` — Vendor incident-notification and retention/deletion terms
*Risk area: Vendor Terms. Current refs in repo: HIPAA Security Rule - business associate contracts; HHS HPH CPG - incident response and vendor management; CISA CPG - supply chain risk management*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 25. `VEL-AI-INVENTORY-001` — AI tool inventory and allowed/restricted/prohibited workflow decision
*Risk area: AI Workflow Review. Current refs in repo: HHS HPH CPG - data protection; NIST AI Risk Management Framework - governance; OCR HIPAA guidance on online tracking and regulated data handling*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 26. `VEL-AI-DATA-USE-001` — AI data-use and model-training evidence
*Risk area: AI Data Use. Current refs in repo: HHS HPH CPG - data protection; NIST AI Risk Management Framework - data governance; CISA CPG - data protection*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

## Operational Readiness (4)

### 27. `VEL-IR-CONTACT-001` — Incident response plan and contact tree
*Risk area: Incident Response. Current refs in repo: HIPAA Security Rule - security incident procedures; HHS HPH CPG - incident response; CISA CPG - incident response planning*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 28. `VEL-DR-DOWNTIME-001` — Contingency, downtime, and disaster recovery plan
*Risk area: Downtime / Ransomware. Current refs in repo: HIPAA Security Rule - contingency plan; HHS HPH CPG - backup and recovery; CISA CPG - data recovery*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 29. `VEL-EVID-FRESHNESS-001` — Evidence freshness report
*Risk area: Evidence Freshness. Current refs in repo: HHS HPH CPG - asset and evidence management; CISA CPG - measurable security outcomes*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

### 30. `VEL-BACKUP-RESTORE-001` — Backup restore test report
*Risk area: Backup / downtime. Current refs in repo: HIPAA Security Rule - disaster recovery plan; HIPAA Security Rule - emergency mode operation plan; CISA CPG - test backups*

- **45 CFR citation:** 
- **Required or addressable:** 
- **405(d)/HICP practice:** 
- **CISA CPG:** 
- **What a practice must actually produce:** 
- **How this fails in real breaches:** 
- [ ] Done, and I can answer cold

---

## Session log

One row per sitting. The last column is the one that pays off in interviews: a specific
thing that surprised you is a story, and stories are what you answer questions with.

| Date | Controls worked | Prediction right? | One thing that surprised me |
|---|---|---|---|
|  |  |  |  |
