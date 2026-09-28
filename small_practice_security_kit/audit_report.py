from __future__ import annotations

import csv
import io
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .control_evidence import load_control_evidence_catalog


@dataclass
class ControlEvaluation:
    control_id: str
    control_name: str
    control_family: str
    risk_area: str
    cfr_citation: str
    cfr_designation: str  # "Required" or "Addressable"
    nist_ref: str
    hicp_practice: str
    status: str  # "addressed", "partial", "gap", "not_applicable"
    severity: str  # "critical", "high", "medium", "low", "info"
    accountable_owner: str
    findings: list[str]
    acceptable_evidence: list[str]
    next_action: str
    linked_connectors: list[str] = field(default_factory=list)


@dataclass
class AuditReportSummary:
    practice_name: str
    practice_type: str
    staff_count: int
    review_period: str
    generated_at: str
    total_controls: int
    addressed_count: int
    partial_count: int
    gap_count: int
    not_applicable_count: int
    readiness_percentage: float
    required_addressed_ratio: str
    addressable_addressed_ratio: str
    critical_gaps_count: int
    high_gaps_count: int
    by_family: dict[str, dict[str, int]]
    by_hicp_practice: dict[str, dict[str, int]]


HICP_CORE_PRACTICE_NAMES: dict[int, str] = {
    1: "Practice 1 - Email Protection Systems",
    2: "Practice 2 - Endpoint Protection Systems",
    3: "Practice 3 - Access Management",
    4: "Practice 4 - Data Protection and Loss Prevention",
    5: "Practice 5 - Asset Management & Device Security",
    6: "Practice 6 - Network Management",
    7: "Practice 7 - Vulnerability Management",
    8: "Practice 8 - Incident Response",
    9: "Practice 9 - Medical Device Security",
    10: "Practice 10 - Cybersecurity Oversight & Governance",
}


def _extract_cfr_info(refs: list[str]) -> tuple[str, str]:
    for ref in refs:
        if "45 CFR § 164." in ref or "45 CFR § 164" in ref:
            has_req = "(Required)" in ref
            has_addr = "(Addressable)" in ref
            if has_req and has_addr:
                designation = "Required"
            elif has_addr:
                designation = "Addressable"
            elif has_req:
                designation = "Required"
            else:
                designation = "Required"
            return ref, designation
    return "45 CFR § 164 (General)", "Required"


def _extract_nist_ref(refs: list[str]) -> str:
    for ref in refs:
        if "NIST SP 800-66r2" in ref:
            return ref
    for ref in refs:
        if "NIST" in ref:
            return ref
    return "NIST SP 800-66r2 § 5 Safeguard Documentation"


def _extract_hicp_ref(refs: list[str]) -> str:
    for ref in refs:
        if "HHS 405(d) HICP" in ref:
            return ref
    return "HHS 405(d) HICP (2023)"


def _sanitize_csv_cell(val: Any) -> str:
    s = str(val) if val is not None else ""
    if s and s[0] in {"=", "+", "-", "@", "\t", "\r"}:
        return "'" + s
    return s


def _sanitize_md_cell(val: Any) -> str:
    s = str(val) if val is not None else ""
    return s.replace("|", "\\|").replace("\n", "<br>")


def evaluate_practice_control(
    control: dict[str, Any],
    profile: dict[str, Any],
    connector_evidence: list[dict[str, Any]] | None = None,
) -> ControlEvaluation:
    cid = str(control.get("control_id", ""))
    cname = str(control.get("control_name", ""))
    family = str(control.get("control_family", ""))
    risk_area = str(control.get("risk_area", ""))
    refs = control.get("control_refs", [])
    cfr_citation, cfr_designation = _extract_cfr_info(refs)
    nist_ref = _extract_nist_ref(refs)
    hicp_practice = _extract_hicp_ref(refs)
    acceptable_evidence = control.get("acceptable_evidence", [])
    next_action = control.get("next_action", "")
    owner = str(control.get("accountable_owner") or control.get("evidence_owner") or "owner")

    readiness = profile.get("readiness", {}) if isinstance(profile.get("readiness"), dict) else {}
    practice = profile.get("practice", {}) if isinstance(profile.get("practice"), dict) else {}
    systems = profile.get("systems", []) if isinstance(profile.get("systems"), list) else []
    flows = profile.get("flows", []) if isinstance(profile.get("flows"), list) else []
    vendors = profile.get("vendors", []) if isinstance(profile.get("vendors"), list) else []
    ai_workflows = profile.get("ai_workflows", []) if isinstance(profile.get("ai_workflows"), list) else []
    evidence_items = profile.get("evidence", []) if isinstance(profile.get("evidence"), list) else []

    status = "gap"
    severity = "high"
    findings: list[str] = []
    linked_connectors: list[str] = []

    # Correlate with connector evidence if available
    connector_items = connector_evidence or []
    for item in connector_items:
        src = str(item.get("source_system") or item.get("source") or "").lower()
        cat = str(item.get("category") or "").lower()
        istatus = str(item.get("status") or "").lower()

        if cid == "VEL-MFA-REMOTE-001" and any(k in src for k in ["google", "microsoft", "m365", "identity"]):
            if src not in linked_connectors:
                linked_connectors.append(src)
            if istatus == "pass":
                findings.append(f"[CONNECTOR VERIFIED - {src.upper()}] Identity provider MFA enforcement verified.")
        elif cid == "VEL-ACCESS-REVIEW-001" and any(k in src or k in cat for k in ["csv", "users", "google", "microsoft", "m365"]):
            if src not in linked_connectors:
                linked_connectors.append(src)
            if istatus in {"pass", "info"}:
                findings.append(f"[CONNECTOR VERIFIED - {src.upper()}] Directory account and user access list exported.")
        elif cid in {"VEL-VULN-MGMT-001", "VEL-VENDOR-REMOTE-001"} and "dns" in src:
            if src not in linked_connectors:
                linked_connectors.append(src)
            if istatus == "pass":
                findings.append(f"[CONNECTOR VERIFIED - {src.upper()}] DNS email authentication perimeter verified.")
        elif "vendor" in src and "VENDOR" in cid:
            if src not in linked_connectors:
                linked_connectors.append(src)
            if istatus in {"pass", "info"}:
                findings.append(f"[CONNECTOR VERIFIED - {src.upper()}] Vendor public security trust disclosure collected.")

    # 1. Security Official & Accountable Owner
    if cid == "VEL-GOV-OWNER-001":
        sec_owner = str(practice.get("security_owner", "")).strip()
        if sec_owner and sec_owner.lower() not in {"tbd", "unassigned", "none", ""}:
            status = "addressed"
            severity = "info"
            findings.append(f"Security official designated: {sec_owner}")
        else:
            status = "gap"
            severity = "high"
            findings.append("No accountable security official designated in practice profile.")

    # 2. Security Risk Analysis (SRA)
    elif cid == "VEL-GOV-SRA-001":
        if readiness.get("risk_analysis"):
            status = "addressed"
            severity = "info"
            findings.append("Profile attests formal Security Risk Analysis completed.")
        else:
            status = "gap"
            severity = "critical"
            findings.append("No formal Security Risk Analysis (SRA) on file.")

    # 3. Risk Treatment & Corrective Action Register
    elif cid == "VEL-GOV-RISK-001":
        if readiness.get("risk_analysis") and readiness.get("tested_backups") and readiness.get("mfa_ehr"):
            status = "addressed"
            severity = "info"
            findings.append("Profile attests core risk treatment items mitigated.")
        elif any(not readiness.get(k) for k in ["mfa_ehr", "tested_backups", "baa_register"]):
            status = "gap"
            severity = "high"
            findings.append("Unaddressed high-risk operational items identified requiring corrective action.")
        else:
            status = "partial"
            severity = "medium"
            findings.append("Corrective action tracking active.")

    # 4. Security Policy Set
    elif cid == "VEL-GOV-POLICY-001":
        if readiness.get("security_policies_current"):
            status = "addressed"
            severity = "info"
            findings.append("Profile attests security policy set reviewed within the last 12 months.")
        else:
            status = "gap"
            severity = "high"
            findings.append("Security policies not confirmed as reviewed within the last 12 months.")

    # 5. Workforce Security Training
    elif cid == "VEL-WORKFORCE-TRAIN-001":
        raw_staff = practice.get("staff_count", 0)
        try:
            staff_val = int(raw_staff)
        except (ValueError, TypeError):
            staff_val = 0
        if readiness.get("security_training_current"):
            status = "addressed"
            severity = "info"
            findings.append(f"Profile attests workforce security training current for {staff_val or 'all'} staff.")
        else:
            status = "gap"
            severity = "high"
            findings.append("Workforce security awareness and training not verified as current.")

    # 6. Incident Response Plan & Contacts
    elif cid == "VEL-IR-CONTACT-001":
        if readiness.get("incident_contact_list"):
            status = "addressed"
            severity = "info"
            findings.append("Profile attests incident response contact list and escalation tree confirmed.")
        else:
            status = "gap"
            severity = "high"
            findings.append("Incident response plan contact tree is unverified or missing.")

    # 7. Contingency / Downtime / DR Plan
    elif cid == "VEL-DR-DOWNTIME-001":
        if readiness.get("downtime_plan"):
            status = "addressed"
            severity = "info"
            findings.append("Profile attests downtime procedures documented for clinical operations.")
        else:
            status = "gap"
            severity = "high"
            findings.append("Downtime operational procedures for EHR and critical systems missing.")

    # 8. Evidence Freshness Report
    elif cid == "VEL-EVID-FRESHNESS-001":
        if not evidence_items and not connector_items:
            status = "gap"
            severity = "high"
            findings.append("No evidence items or connector sources tracked.")
        else:
            stale_items = [e for e in evidence_items if str(e.get("status", "")).lower() in {"outdated", "requested", "partial", "missing"}]
            if stale_items:
                status = "partial"
                severity = "medium"
                findings.append(f"Evidence inventory tracked ({len(evidence_items)} items); {len(stale_items)} item(s) are outdated or requested and require renewal.")
            else:
                status = "addressed"
                severity = "info"
                findings.append(f"Profile attests all {len(evidence_items)} evidence inventory items are current.")

    # 9. MFA Coverage
    elif cid == "VEL-MFA-REMOTE-001":
        mfa_email = readiness.get("mfa_email", False)
        mfa_ehr = readiness.get("mfa_ehr", False)
        if any("[CONNECTOR VERIFIED" in f for f in findings) and mfa_ehr:
            status = "addressed"
            severity = "info"
            findings.append("MFA verified active via identity provider connector and profile attestation.")
        elif mfa_email and mfa_ehr:
            status = "addressed"
            severity = "info"
            findings.append("Profile attests MFA active across both email and EHR access.")
        elif mfa_email and not mfa_ehr:
            status = "partial"
            severity = "critical"
            findings.append("MFA enabled for email, but EHR access lacks verified MFA enforcement.")
        elif not mfa_email and mfa_ehr:
            status = "partial"
            severity = "critical"
            findings.append("MFA enabled for EHR, but cloud email lacks verified MFA.")
        else:
            status = "gap"
            severity = "critical"
            findings.append("MFA not enforced on email or EHR systems.")

    # 10. Access Review
    elif cid == "VEL-ACCESS-REVIEW-001":
        if readiness.get("quarterly_access_review"):
            status = "addressed"
            severity = "info"
            findings.append("Profile attests quarterly access reviews established for ePHI systems.")
        else:
            status = "gap"
            severity = "high"
            findings.append("No quarterly access review cadence established.")

    # 11. Termination Procedures
    elif cid == "VEL-OFFBOARDING-001":
        if readiness.get("termination_procedures") or readiness.get("offboarding_procedure"):
            status = "addressed"
            severity = "info"
            findings.append("Profile attests formal workforce termination and credential revocation procedures in place.")
        elif readiness.get("unique_accounts"):
            status = "partial"
            severity = "high"
            findings.append("Unique user accounts enforced; formal workforce termination and credential revocation checklist required under 45 CFR § 164.308(a)(3)(ii)(C).")
        else:
            status = "gap"
            severity = "high"
            findings.append("No formal offboarding or termination access revocation procedures documented.")

    # 12. Privileged Account Inventory
    elif cid == "VEL-PRIV-ACCOUNTS-001":
        tech_owner = str(practice.get("technical_owner", "")).strip()
        if readiness.get("privileged_account_inventory"):
            status = "addressed"
            severity = "info"
            findings.append("Profile attests dedicated privileged and administrative account inventory maintained.")
        elif tech_owner:
            status = "partial"
            severity = "high"
            findings.append(f"Technical lead assigned ({tech_owner}); formal privileged administrator account inventory and quarterly review required.")
        else:
            status = "gap"
            severity = "high"
            findings.append("No technical lead or privileged account inventory designated.")

    # 13. Vendor Remote Access
    elif cid == "VEL-VENDOR-REMOTE-001":
        remote_kws = ["vendor support", "remote support", "rmm", "vpn", "remote access", "teamviewer", "anydesk", "screenconnect"]
        remote_systems = [
            s for s in systems
            if any(k in (str(s.get("access_method", "")) + " " + str(s.get("name", ""))).lower() for k in remote_kws)
        ]
        if remote_systems:
            status = "partial"
            severity = "high"
            findings.append(f"Remote vendor/administrative access pathways identified in {len(remote_systems)} system(s); authorization bounds, MFA enforcement, and access logging require verification.")
        else:
            status = "addressed"
            severity = "info"
            findings.append("No third-party remote vendor access pathways identified in systems inventory.")

    # 14. Emergency Access / Break-Glass
    elif cid == "VEL-BREAKGLASS-001":
        if readiness.get("breakglass_procedure") or readiness.get("emergency_access_procedure"):
            status = "addressed"
            severity = "info"
            findings.append("Emergency break-glass procedure and credential escrow documented.")
        else:
            status = "gap"
            severity = "high"
            findings.append("Emergency break-glass access procedures and credential escrow not formally documented.")

    # 15. Backup Scope
    elif cid == "VEL-BACKUP-SCOPE-001":
        ephi_systems = [s for s in systems if any(k in str(s.get("ephi_role", "")).lower() for k in ["maintains", "creates", "stores"])]
        covered = [s for s in ephi_systems if "backup" in (str(s.get("evidence_needed", "")) + " " + str(s.get("notes", ""))).lower()]
        if not covered and ephi_systems:
            status = "gap"
            severity = "high"
            findings.append(f"Backup scope not documented for any of the {len(ephi_systems)} ePHI storage systems.")
        elif len(covered) < len(ephi_systems):
            status = "partial"
            severity = "high"
            findings.append(f"Backup scope identified for {len(covered)} of {len(ephi_systems)} ePHI-maintaining systems; {len(ephi_systems) - len(covered)} system(s) unverified.")
        elif ephi_systems:
            status = "addressed" if readiness.get("tested_backups") else "partial"
            severity = "info" if status == "addressed" else "high"
            findings.append(f"Backup scope covers all {len(ephi_systems)} ePHI-maintaining systems.")
        else:
            status = "partial"
            severity = "medium"
            findings.append("No ePHI storage systems identified to define backup scope.")

    # 16. Backup Restore Testing
    elif cid == "VEL-BACKUP-RESTORE-001":
        if readiness.get("tested_backups"):
            status = "addressed"
            severity = "info"
            findings.append("Profile attests regular backup restore testing completed.")
        else:
            status = "gap"
            severity = "critical"
            findings.append("No recorded backup restoration tests.")

    # 17. Patch Management
    elif cid == "VEL-PATCH-MGMT-001":
        tech_owner = str(practice.get("technical_owner", ""))
        is_it_lead = bool(re.search(r"\b(msp|it)\b", tech_owner, re.IGNORECASE))
        has_rmm = any(
            re.search(r"\b(rmm|patch|ninja|datto|kaseya|connectwise)\b", str(s.get("name", "")) + " " + str(s.get("category", "")), re.IGNORECASE)
            for s in systems
        )
        if readiness.get("patch_management_cadence") or (has_rmm and is_it_lead):
            status = "addressed"
            severity = "info"
            findings.append(f"Patch management managed via {tech_owner} with automated cadence.")
        elif is_it_lead:
            status = "partial"
            severity = "medium"
            findings.append(f"IT/MSP lead designated ({tech_owner}); formal patch cadence documentation and vulnerability patch reports required.")
        else:
            status = "gap"
            severity = "high"
            findings.append("No patch management schedule or responsible IT owner documented.")

    # 18. Vulnerability Management
    elif cid == "VEL-VULN-MGMT-001":
        unencrypted_flows = [
            f for f in flows
            if any(k in str(f.get("transmission", "")).lower() for k in ["unencrypted", "plain", "cleartext", "http:", "manual export", "unencrypted email"])
        ]
        if unencrypted_flows:
            status = "partial"
            severity = "high"
            findings.append(f"Data flows mapped ({len(flows)} flows); unencrypted transmission identified in {len(unencrypted_flows)} flow(s) requiring remediation.")
        elif flows:
            status = "addressed"
            severity = "info"
            findings.append(f"Data flows mapped ({len(flows)} flows) with encrypted transmission protocols (HTTPS/TLS).")
        else:
            status = "gap"
            severity = "high"
            findings.append("Data flow perimeter and transmission paths unmapped.")

    # 19. Endpoint Protection / EDR
    elif cid == "VEL-EDR-STATUS-001":
        tech_owner = str(practice.get("technical_owner", ""))
        is_it_lead = bool(re.search(r"\b(msp|it)\b", tech_owner, re.IGNORECASE))
        has_edr = any(
            re.search(r"\b(edr|endpoint|antivirus|av|defender|sentinel|crowdstrike|sophos|bitdefender)\b", str(s.get("name", "")) + " " + str(s.get("category", "")), re.IGNORECASE)
            for s in systems
        )
        if readiness.get("endpoint_protection") or (has_edr and is_it_lead):
            status = "addressed"
            severity = "info"
            findings.append("Managed endpoint protection / EDR confirmed in systems inventory.")
        elif has_edr:
            status = "partial"
            severity = "high"
            findings.append("Endpoint protection tool identified; centralized administration and policy attestation required.")
        else:
            status = "gap"
            severity = "high"
            findings.append("No endpoint protection or EDR tool identified in clinical systems inventory.")

    # 20. Log Review
    elif cid == "VEL-LOG-REVIEW-001":
        if readiness.get("log_review_cadence"):
            status = "addressed"
            severity = "info"
            findings.append("Profile attests regular information system activity review cadence established.")
        else:
            status = "gap"
            severity = "high"
            findings.append("No formal log review cadence established.")

    # 21. Device Encryption
    elif cid == "VEL-ENCRYPT-DEVICE-001":
        if readiness.get("device_encryption") or readiness.get("storage_encryption"):
            status = "addressed"
            severity = "info"
            findings.append("Profile attests full-disk encryption active on staff endpoints and storage media.")
        else:
            managed = any("managed endpoint" in str(s.get("access_method", "")).lower() for s in systems)
            if managed:
                status = "partial"
                severity = "high"
                findings.append("Managed endpoints designated; full-disk encryption (BitLocker / FileVault) attestation and key management required.")
            else:
                status = "gap"
                severity = "high"
                findings.append("Device storage encryption not verified for endpoints accessing ePHI.")

    # 22. Asset Inventory
    elif cid == "VEL-ASSET-EXPOSURE-001":
        if systems:
            status = "addressed"
            severity = "info"
            findings.append(f"Systems and applications inventoried ({len(systems)} systems).")
        else:
            status = "gap"
            severity = "high"
            findings.append("No system asset inventory documented.")

    # 23. Vendor Inventory
    elif cid == "VEL-VENDOR-INV-001":
        if readiness.get("vendor_inventory") and vendors:
            status = "addressed"
            severity = "info"
            findings.append(f"Profile attests vendor inventory maintained across {len(vendors)} vendors.")
        elif vendors:
            status = "partial"
            severity = "high"
            findings.append(f"Vendor list contains {len(vendors)} vendors; formal inventory review required.")
        else:
            status = "gap"
            severity = "high"
            findings.append("Vendor inventory incomplete or missing.")

    # 24. BAA Status
    elif cid == "VEL-BAA-STATUS-001":
        ephi_vendors = [v for v in vendors if v.get("touches_ephi")]
        signed_vendors = [v for v in ephi_vendors if str(v.get("baa_status", "")).lower() == "signed"]
        if not ephi_vendors:
            status = "addressed" if readiness.get("baa_register") else "partial"
            severity = "info" if status == "addressed" else "medium"
            findings.append("No vendors currently identified as touching ePHI.")
        elif len(signed_vendors) == len(ephi_vendors) and readiness.get("baa_register"):
            status = "addressed"
            severity = "info"
            findings.append(f"Profile attests BAA register complete; all {len(ephi_vendors)} ePHI vendors have signed BAAs.")
        else:
            status = "gap" if not signed_vendors else "partial"
            severity = "critical"
            unsigned_count = len(ephi_vendors) - len(signed_vendors)
            findings.append(f"BAA verification incomplete: {unsigned_count} of {len(ephi_vendors)} ePHI vendors lack verified signed BAAs.")

    # 25. Vendor Security Evidence
    elif cid == "VEL-VENDOR-EVIDENCE-001":
        if not vendors:
            status = "partial"
            severity = "medium"
            findings.append("No vendors in scope to evaluate security attestations.")
        else:
            attested_vendors = [
                v for v in vendors
                if str(v.get("soc2_status", "")).lower() not in {"not provided", "unknown", "none", ""}
                or str(v.get("hitrust_status", "")).lower() not in {"not provided", "unknown", "none", ""}
            ]
            if len(attested_vendors) == len(vendors):
                status = "addressed"
                severity = "info"
                findings.append(f"Security attestations (SOC 2 / HITRUST) documented for all {len(vendors)} vendors.")
            elif attested_vendors:
                status = "partial"
                severity = "medium"
                findings.append(f"Security attestations (SOC 2 / HITRUST) documented for {len(attested_vendors)} of {len(vendors)} vendors.")
            else:
                status = "gap"
                severity = "medium"
                findings.append(f"Security attestations (SOC 2 / HITRUST) not provided for any of the {len(vendors)} vendors.")

    # 26. Vendor Incident Notice Terms
    elif cid == "VEL-VENDOR-TERMS-001":
        ephi_vendors = [v for v in vendors if v.get("touches_ephi")]
        if not ephi_vendors:
            status = "addressed" if readiness.get("baa_register") else "partial"
            severity = "info" if status == "addressed" else "medium"
            findings.append("No ePHI vendors in scope to evaluate breach notification terms.")
        else:
            verified_terms = [
                v for v in ephi_vendors
                if str(v.get("incident_notification_terms", "")).lower() not in {"unknown", "not provided", "missing", "tbd", "none", ""}
            ]
            if len(verified_terms) == len(ephi_vendors):
                status = "addressed"
                severity = "info"
                findings.append(f"Profile attests breach notification terms documented across all {len(ephi_vendors)} ePHI vendors.")
            else:
                status = "gap" if not verified_terms else "partial"
                severity = "high"
                unverified_count = len(ephi_vendors) - len(verified_terms)
                findings.append(f"Vendor breach notification terms unverified for {unverified_count} of {len(ephi_vendors)} ePHI vendor(s).")

    # 27. AI Tool Inventory & Workflow Decision
    elif cid == "VEL-AI-INVENTORY-001":
        ai_systems = [s for s in systems if "ai" in str(s.get("category", "")).lower()]
        if not ai_systems and not ai_workflows:
            status = "not_applicable"
            severity = "info"
            findings.append("No AI tools or automated clinical assistants in practice scope.")
        else:
            unapproved = []
            for w in ai_workflows:
                dec = str(w.get("decision", "")).lower()
                if dec not in {"allowed", "approved", "authorized"}:
                    unapproved.append(str(w.get("name", "Workflow")))
            for s in ai_systems:
                if "pilot" in str(s.get("name", "")).lower() or "pilot" in str(s.get("evidence_needed", "")).lower():
                    unapproved.append(str(s.get("name", "System")))
            if unapproved:
                status = "partial"
                severity = "high"
                count_total = len(ai_systems) or len(ai_workflows)
                findings.append(f"AI tools identified ({count_total}); {len(unapproved)} unapproved/pilot tool(s) or workflows require formal approval before ePHI exposure.")
            else:
                count_total = len(ai_systems) or len(ai_workflows)
                status = "addressed"
                severity = "info"
                findings.append(f"All {count_total} AI tools have recorded approved usage guidelines.")

    # 28. AI Data Use & Model Training
    elif cid == "VEL-AI-DATA-USE-001":
        ai_systems = [s for s in systems if "ai" in str(s.get("category", "")).lower()]
        if not ai_systems and not ai_workflows:
            status = "not_applicable"
            severity = "info"
            findings.append("No AI workflows in practice scope.")
        else:
            ai_vendor_names = {str(s.get("vendor", "")).lower() for s in ai_systems if s.get("vendor")}
            ai_vendors = [v for v in vendors if str(v.get("name", "")).lower() in ai_vendor_names or "ai" in str(v.get("service", "")).lower()]
            unverified_training = []
            for v in ai_vendors:
                use = str(v.get("ai_training_use", "")).lower()
                if "prohibit" not in use and "no" not in use:
                    unverified_training.append(str(v.get("name", "Vendor")))
            for s in ai_systems:
                role = str(s.get("ephi_role", "")).lower()
                if "prohibit" not in role and "no phi" not in role:
                    s_name = str(s.get("name", "AI System"))
                    if s_name not in unverified_training:
                        unverified_training.append(s_name)
            if unverified_training:
                status = "gap" if len(unverified_training) >= (len(ai_vendors) + len(ai_systems)) else "partial"
                severity = "high"
                findings.append(f"Patient data training prohibition unverified for: {', '.join(unverified_training[:3])}.")
            else:
                status = "addressed"
                severity = "info"
                findings.append("Explicit prohibition of patient data for model training confirmed across AI tools and vendor terms.")

    # 29. Physical Access Basics
    elif cid == "VEL-PHYSICAL-ACCESS-001":
        raw_locs = practice.get("locations", 1)
        try:
            locs = int(raw_locs)
        except (ValueError, TypeError):
            locs = 1
        if readiness.get("facility_access_controls") or readiness.get("workstation_physical_security"):
            status = "addressed"
            severity = "info"
            findings.append(f"Profile attests facility access and workstation physical controls active across {locs} location(s).")
        else:
            status = "partial"
            severity = "medium"
            findings.append(f"Physical facility scope recorded ({locs} location(s)); formal facility access controls and workstation security procedures require written documentation under 45 CFR § 164.310.")

    # 30. Device / Media Disposal
    elif cid == "VEL-MEDIA-DISPOSAL-001":
        if readiness.get("media_disposal") or readiness.get("device_sanitization"):
            status = "addressed"
            severity = "info"
            findings.append("Profile attests media sanitization and disposal procedures in place.")
        else:
            status = "partial"
            severity = "medium"
            findings.append("Media sanitization and device disposal procedures require documented policy under 45 CFR § 164.310(d)(2).")

    return ControlEvaluation(
        control_id=cid,
        control_name=cname,
        control_family=family,
        risk_area=risk_area,
        cfr_citation=cfr_citation,
        cfr_designation=cfr_designation,
        nist_ref=nist_ref,
        hicp_practice=hicp_practice,
        status=status,
        severity=severity,
        accountable_owner=owner,
        findings=findings,
        acceptable_evidence=acceptable_evidence,
        next_action=next_action,
        linked_connectors=linked_connectors,
    )


def generate_audit_gap_report(
    profile: dict[str, Any],
    connector_evidence: list[dict[str, Any]] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    gen_time = generated_at or datetime.now(timezone.utc).isoformat()
    catalog_controls = load_control_evidence_catalog()

    evaluations: list[ControlEvaluation] = []
    for ctrl in catalog_controls:
        evaluations.append(evaluate_practice_control(ctrl, profile, connector_evidence))

    status_counts = Counter(e.status for e in evaluations)
    addressed = status_counts["addressed"]
    partial = status_counts["partial"]
    gaps = status_counts["gap"]
    na = status_counts["not_applicable"]
    total = len(evaluations)
    applicable = total - na
    readiness_pct = round(((addressed + (partial * 0.5)) / applicable * 100), 1) if applicable > 0 else 100.0

    # Required vs Addressable breakdown:
    # Exclude not_applicable from the calculation denominators
    # Count only 'addressed' as met (per 45 CFR § 164.306(d), addressable items require implementation or documented equivalent)
    req_evals = [e for e in evaluations if "Required" in e.cfr_designation and e.status != "not_applicable"]
    req_total = len(req_evals)
    req_addressed = sum(1 for e in req_evals if e.status == "addressed")

    addr_evals = [e for e in evaluations if e.cfr_designation == "Addressable" and e.status != "not_applicable"]
    addr_total = len(addr_evals)
    addr_addressed = sum(1 for e in addr_evals if e.status == "addressed")

    crit_gaps = sum(1 for e in evaluations if e.status in {"gap", "partial"} and e.severity == "critical")
    high_gaps = sum(1 for e in evaluations if e.status in {"gap", "partial"} and e.severity == "high")

    # Family breakdown
    by_family: dict[str, dict[str, int]] = {}
    for e in evaluations:
        fam = e.control_family
        if fam not in by_family:
            by_family[fam] = {"total": 0, "addressed": 0, "partial": 0, "gap": 0, "not_applicable": 0}
        by_family[fam]["total"] += 1
        by_family[fam][e.status] = by_family[fam].get(e.status, 0) + 1

    # HICP breakdown: parse all practice numbers
    by_hicp: dict[str, dict[str, int]] = {}
    for e in evaluations:
        practice_nums = set(int(m) for m in re.findall(r"(?:Practice|Sub-Practice)\s+(\d+)", e.hicp_practice))
        if not practice_nums:
            practice_nums = {10}
        for pnum in sorted(practice_nums):
            pname = HICP_CORE_PRACTICE_NAMES.get(pnum, f"Practice {pnum}")
            if pname not in by_hicp:
                by_hicp[pname] = {"total": 0, "addressed": 0, "partial": 0, "gap": 0, "not_applicable": 0}
            by_hicp[pname]["total"] += 1
            by_hicp[pname][e.status] = by_hicp[pname].get(e.status, 0) + 1

    practice = profile.get("practice", {}) if isinstance(profile.get("practice"), dict) else {}
    raw_staff = practice.get("staff_count", 0)
    try:
        staff_count = int(raw_staff)
    except (ValueError, TypeError):
        staff_count = 0

    summary = AuditReportSummary(
        practice_name=str(practice.get("name", "Healthcare Practice")),
        practice_type=str(practice.get("type", "General")),
        staff_count=staff_count,
        review_period=str(practice.get("review_period", "Current")),
        generated_at=gen_time,
        total_controls=total,
        addressed_count=addressed,
        partial_count=partial,
        gap_count=gaps,
        not_applicable_count=na,
        readiness_percentage=readiness_pct,
        required_addressed_ratio=f"{req_addressed}/{req_total}" if req_total > 0 else "N/A",
        addressable_addressed_ratio=f"{addr_addressed}/{addr_total}" if addr_total > 0 else "N/A",
        critical_gaps_count=crit_gaps,
        high_gaps_count=high_gaps,
        by_family=by_family,
        by_hicp_practice=by_hicp,
    )

    return {
        "summary": asdict(summary),
        "controls": [asdict(e) for e in evaluations],
        "unaddressed_gaps": [asdict(e) for e in evaluations if e.status in {"gap", "partial"}],
    }


def render_audit_report_text(report: dict[str, Any], gaps_only: bool = False) -> str:
    s = report["summary"]
    lines = [
        "=" * 80,
        f"  SMALL PRACTICE SECURITY AUDIT GAP REPORT: {s['practice_name'].upper()}",
        f"  Practice Type: {s['practice_type']} | Staff: {s['staff_count']} | Period: {s['review_period']}",
        "=" * 80,
        "",
        "EXECUTIVE SUMMARY:",
        f"  Total Controls Evaluated : {s['total_controls']}",
        f"  Addressed / Implemented  : {s['addressed_count']}",
        f"  Partially Addressed      : {s['partial_count']}",
        f"  Unaddressed Gaps         : {s['gap_count']}",
        f"  Not Applicable           : {s['not_applicable_count']}",
        f"  Overall Readiness Score  : {s['readiness_percentage']}%",
        "",
        "PROFILE IMPLEMENTATION & STATUTORY RATIOS:",
        f"  45 CFR § 164 Required Controls    : {s['required_addressed_ratio']} addressed",
        f"  45 CFR § 164 Addressable Controls : {s['addressable_addressed_ratio']} addressed (implementation/equivalent required)",
        f"  High & Critical Action Gaps       : {s['critical_gaps_count']} critical, {s['high_gaps_count']} high",
        "",
        "-" * 80,
    ]

    target_controls = report["unaddressed_gaps"] if gaps_only else report["controls"]
    header_label = "UNADDRESSED AUDIT GAPS (ACTION REQUIRED)" if gaps_only else "FULL CONTROL AUDIT EVALUATION"
    lines.append(f"{header_label}:")
    lines.append("-" * 80)

    for c in target_controls:
        badge = f"[{c['status'].upper()}]"
        sev_badge = f"[{c['severity'].upper()}]" if c["status"] in {"gap", "partial"} else ""
        lines.append(f"\n* {c['control_id']}: {c['control_name']} {badge} {sev_badge}".rstrip())
        citation_str = c["cfr_citation"]
        if f"({c['cfr_designation']})" not in citation_str:
            citation_str = f"{citation_str} ({c['cfr_designation']})"
        lines.append(f"  Citation : {citation_str}")
        lines.append(f"  Framework: {c['nist_ref']} | {c['hicp_practice']}")
        lines.append(f"  Owner    : {c['accountable_owner']}")
        for f in c["findings"]:
            lines.append(f"  Finding  : {f}")
        if c.get("linked_connectors"):
            lines.append(f"  Evidence : Connectors: {', '.join(c['linked_connectors'])}")
        if c["status"] in {"gap", "partial"}:
            lines.append(f"  Action   : {c['next_action']}")
            if c["acceptable_evidence"]:
                lines.append(f"  Acceptable: {'; '.join(c['acceptable_evidence'][:3])}")

    lines.append("\n" + "=" * 80)
    return "\n".join(lines)


def render_audit_report_markdown(report: dict[str, Any], gaps_only: bool = False) -> str:
    s = report["summary"]
    lines = [
        f"# Security Audit Gap Report: {_sanitize_md_cell(s['practice_name'])}",
        "",
        f"**Practice Type:** {_sanitize_md_cell(s['practice_type'])} | **Staff Count:** {s['staff_count']} | **Review Period:** {_sanitize_md_cell(s['review_period'])} | **Generated:** {s['generated_at'][:10]}",
        "",
        "## Executive Scorecard",
        "",
        "| Metric | Result | Target |",
        "| --- | --- | --- |",
        f"| **Overall Readiness Score** | **{s['readiness_percentage']}%** | 100% |",
        f"| **Addressed Controls** | {s['addressed_count']} / {s['total_controls']} | {s['total_controls']} |",
        f"| **Partially Addressed** | {s['partial_count']} | 0 |",
        f"| **Unaddressed Gaps** | {s['gap_count']} | 0 |",
        f"| **45 CFR Required Controls** | {s['required_addressed_ratio']} | Full |",
        f"| **45 CFR Addressable Controls** | {s['addressable_addressed_ratio']} | Full |",
        f"| **Critical & High Priority Gaps** | {s['critical_gaps_count']} critical, {s['high_gaps_count']} high | 0 |",
        "",
        "## Safeguard Family Breakdown",
        "",
        "| Family | Total | Addressed | Partial | Gap | N/A |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for fam, counts in s["by_family"].items():
        lines.append(
            f"| {_sanitize_md_cell(fam)} | {counts['total']} | {counts.get('addressed', 0)} | "
            f"{counts.get('partial', 0)} | {counts.get('gap', 0)} | {counts.get('not_applicable', 0)} |"
        )

    lines.append("")
    lines.append("## Unaddressed Audit Gaps & Required Actions" if gaps_only else "## Control Evidence Matrix Evaluation")
    lines.append("")
    lines.append("| Control ID | Control Name | Status | Severity | Citation | Accountable Owner | Finding & Next Action |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")

    target_controls = report["unaddressed_gaps"] if gaps_only else report["controls"]
    for c in target_controls:
        status_md = f"**{c['status'].upper()}**"
        sev_md = f"`{c['severity']}`" if c["status"] in {"gap", "partial"} else "ok"
        finding_text = "<br>".join(_sanitize_md_cell(f) for f in c["findings"])
        if c.get("linked_connectors"):
            finding_text += f"<br><em>Connectors:</em> {', '.join(_sanitize_md_cell(conn) for conn in c['linked_connectors'])}"
        if c["status"] in {"gap", "partial"}:
            finding_text += f"<br><em>Action:</em> {_sanitize_md_cell(c['next_action'])}"
        lines.append(
            f"| `{_sanitize_md_cell(c['control_id'])}` | {_sanitize_md_cell(c['control_name'])} | {status_md} | {sev_md} | {_sanitize_md_cell(c['cfr_citation'])} | `{_sanitize_md_cell(c['accountable_owner'])}` | {finding_text} |"
        )

    lines.append("")
    lines.append("> [!NOTE]")
    lines.append("> This audit gap report is prepared for internal compliance readiness under HIPAA (45 CFR § 164), NIST SP 800-66r2, and HHS 405(d) HICP. All technical evidence is metadata-only without storing or transmitting raw patient records.")
    return "\n".join(lines)


def render_audit_report_csv(report: dict[str, Any], gaps_only: bool = False) -> str:
    output = io.StringIO()
    fields = [
        "control_id",
        "control_name",
        "control_family",
        "risk_area",
        "cfr_citation",
        "cfr_designation",
        "nist_ref",
        "hicp_practice",
        "status",
        "severity",
        "accountable_owner",
        "findings",
        "linked_connectors",
        "next_action",
    ]
    writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    target_controls = report["unaddressed_gaps"] if gaps_only else report["controls"]
    for c in target_controls:
        writer.writerow({
            "control_id": _sanitize_csv_cell(c["control_id"]),
            "control_name": _sanitize_csv_cell(c["control_name"]),
            "control_family": _sanitize_csv_cell(c["control_family"]),
            "risk_area": _sanitize_csv_cell(c["risk_area"]),
            "cfr_citation": _sanitize_csv_cell(c["cfr_citation"]),
            "cfr_designation": _sanitize_csv_cell(c["cfr_designation"]),
            "nist_ref": _sanitize_csv_cell(c["nist_ref"]),
            "hicp_practice": _sanitize_csv_cell(c["hicp_practice"]),
            "status": _sanitize_csv_cell(c["status"]),
            "severity": _sanitize_csv_cell(c["severity"]),
            "accountable_owner": _sanitize_csv_cell(c["accountable_owner"]),
            "findings": _sanitize_csv_cell(" | ".join(c["findings"])),
            "linked_connectors": _sanitize_csv_cell(", ".join(c.get("linked_connectors", []))),
            "next_action": _sanitize_csv_cell(c["next_action"]),
        })
    return output.getvalue()


def render_audit_report_json(report: dict[str, Any], gaps_only: bool = False) -> str:
    if gaps_only:
        filtered = dict(report)
        filtered["controls"] = report.get("unaddressed_gaps", [])
        return json.dumps(filtered, indent=2, sort_keys=True) + "\n"
    return json.dumps(report, indent=2, sort_keys=True) + "\n"
