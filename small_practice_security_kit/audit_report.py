from __future__ import annotations

import csv
import io
import json
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


def _extract_cfr_info(refs: list[str]) -> tuple[str, str]:
    for ref in refs:
        if "45 CFR § 164." in ref:
            designation = "Required" if "(Required)" in ref else "Addressable" if "(Addressable)" in ref else "Unspecified"
            return ref, designation
    return "45 CFR § 164 (General)", "Required"


def _extract_nist_ref(refs: list[str]) -> str:
    for ref in refs:
        if "NIST SP 800-66r2" in ref:
            return ref
    for ref in refs:
        if "NIST" in ref:
            return ref
    return "NIST SP 800-66r2"


def _extract_hicp_ref(refs: list[str]) -> str:
    for ref in refs:
        if "HHS 405(d) HICP" in ref:
            return ref
    return "HHS 405(d) HICP"


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
    owner = str(control.get("accountable_owner") or control.get("evidence_owner") or "practice_owner")

    readiness = profile.get("readiness", {})
    practice = profile.get("practice", {})
    systems = profile.get("systems", [])
    flows = profile.get("flows", [])
    vendors = profile.get("vendors", [])
    ai_workflows = profile.get("ai_workflows", [])

    status = "gap"
    severity = "high"
    findings: list[str] = []
    linked_connectors: list[str] = []

    # Correlate with connector evidence if available
    connector_items = connector_evidence or []
    for item in connector_items:
        src = str(item.get("source_system") or item.get("source") or "").lower()
        if cid == "VEL-MFA-REMOTE-001" and ("google" in src or "microsoft" in src or "m365" in src):
            linked_connectors.append(src)
        elif cid == "VEL-ACCESS-REVIEW-001" and ("csv" in src or "users" in src or "google" in src or "microsoft" in src):
            linked_connectors.append(src)
        elif "backup" in cid.lower() and "backup" in src:
            linked_connectors.append(src)
        elif "dns" in src and "MFA" in cid:
            linked_connectors.append(src)
        elif "vendor" in src and "VENDOR" in cid:
            linked_connectors.append(src)

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
            findings.append("Formal Security Risk Analysis recorded as complete.")
        elif practice.get("review_period"):
            status = "partial"
            severity = "high"
            findings.append(f"Review period {practice.get('review_period')} established; formal SRA documentation required.")
        else:
            status = "gap"
            severity = "critical"
            findings.append("No Security Risk Analysis record on file.")

    # 3. Risk Treatment & Corrective Action Register
    elif cid == "VEL-GOV-RISK-001":
        if readiness.get("risk_analysis") and readiness.get("tested_backups") and readiness.get("mfa_ehr"):
            status = "addressed"
            severity = "info"
            findings.append("Core risk items mitigated.")
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
            findings.append("Security policy set confirmed current.")
        elif practice.get("review_period"):
            status = "partial"
            severity = "medium"
            findings.append(f"Practice review period is {practice.get('review_period')}; annual policy signoff needed.")
        else:
            status = "gap"
            severity = "high"
            findings.append("Security policies not confirmed as reviewed within the last 12 months.")

    # 5. Workforce Security Training
    elif cid == "VEL-WORKFORCE-TRAIN-001":
        if readiness.get("security_training_current"):
            status = "addressed"
            severity = "info"
            findings.append(f"Workforce security training current for {practice.get('staff_count', 'all')} staff.")
        else:
            status = "gap"
            severity = "high"
            findings.append("Workforce security awareness and training not verified as current.")

    # 6. Incident Response Plan & Contacts
    elif cid == "VEL-IR-CONTACT-001":
        if readiness.get("incident_contact_list"):
            status = "addressed"
            severity = "info"
            findings.append("Incident response contact list and escalation tree confirmed.")
        else:
            status = "gap"
            severity = "high"
            findings.append("Incident response plan contact tree is unverified or missing.")

    # 7. Contingency / Downtime / DR Plan
    elif cid == "VEL-DR-DOWNTIME-001":
        if readiness.get("downtime_plan"):
            status = "addressed"
            severity = "info"
            findings.append("Downtime procedures documented for clinical operations.")
        else:
            status = "gap"
            severity = "high"
            findings.append("Downtime operational procedures for EHR/critical systems missing.")

    # 8. Evidence Freshness Report
    elif cid == "VEL-EVID-FRESHNESS-001":
        if connector_items or profile.get("evidence"):
            status = "addressed"
            severity = "info"
            findings.append(f"Evidence inventory tracked with {len(connector_items) + len(profile.get('evidence', []))} items.")
        else:
            status = "partial"
            severity = "medium"
            findings.append("Evidence tracking active; connector automation recommended.")

    # 9. MFA Coverage
    elif cid == "VEL-MFA-REMOTE-001":
        mfa_email = readiness.get("mfa_email", False)
        mfa_ehr = readiness.get("mfa_ehr", False)
        if mfa_email and mfa_ehr:
            status = "addressed"
            severity = "info"
            findings.append("MFA verified active across both email and EHR access.")
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
            findings.append("Quarterly access reviews established for ePHI systems.")
        else:
            status = "gap"
            severity = "high"
            findings.append("No quarterly access review cadence established.")

    # 11. Termination Procedures
    elif cid == "VEL-OFFBOARDING-001":
        if readiness.get("unique_accounts"):
            status = "addressed"
            severity = "info"
            findings.append("Unique user accounts enforced; offboarding revocation procedure in place.")
        else:
            status = "gap"
            severity = "high"
            findings.append("Shared accounts in use or termination revocation procedures not verified.")

    # 12. Privileged Account Inventory
    elif cid == "VEL-PRIV-ACCOUNTS-001":
        tech_owner = str(practice.get("technical_owner", "")).strip()
        if tech_owner:
            status = "addressed"
            severity = "info"
            findings.append(f"Technical lead and administrator authority assigned: {tech_owner}")
        else:
            status = "gap"
            severity = "medium"
            findings.append("No technical owner / administrative authority assigned.")

    # 13. Vendor Remote Access
    elif cid == "VEL-VENDOR-REMOTE-001":
        remote_support = any("vendor support" in str(s.get("access_method", "")).lower() for s in systems)
        if remote_support:
            status = "partial"
            severity = "medium"
            findings.append("Vendor support remote sessions identified in systems inventory; authorization bounds needed.")
        else:
            status = "addressed"
            severity = "info"
            findings.append("No unmanaged vendor remote access detected.")

    # 14. Emergency Access / Break-Glass
    elif cid == "VEL-BREAKGLASS-001":
        if readiness.get("downtime_plan"):
            status = "addressed"
            severity = "info"
            findings.append("Emergency break-glass procedure covered under downtime plan.")
        else:
            status = "gap"
            severity = "medium"
            findings.append("Emergency access procedures not formally documented.")

    # 15. Backup Scope
    elif cid == "VEL-BACKUP-SCOPE-001":
        ephi_systems = [s for s in systems if "maintains" in str(s.get("ephi_role", "")).lower()]
        backup_refs = [s for s in ephi_systems if "backup" in str(s.get("evidence_needed", "")).lower()]
        if backup_refs:
            status = "addressed" if readiness.get("tested_backups") else "partial"
            severity = "info" if status == "addressed" else "high"
            findings.append(f"Backup scope identified across {len(backup_refs)} ePHI-maintaining systems.")
        else:
            status = "gap"
            severity = "high"
            findings.append("Backup scope not documented for all ePHI storage systems.")

    # 16. Backup Restore Testing
    elif cid == "VEL-BACKUP-RESTORE-001":
        if readiness.get("tested_backups"):
            status = "addressed"
            severity = "info"
            findings.append("Regular backup restore testing confirmed.")
        else:
            status = "gap"
            severity = "critical"
            findings.append("No recorded backup restoration tests.")

    # 17. Patch Management
    elif cid == "VEL-PATCH-MGMT-001":
        tech_owner = str(practice.get("technical_owner", "")).lower()
        if "msp" in tech_owner or "it" in tech_owner:
            status = "addressed"
            severity = "info"
            findings.append(f"Patch management managed by {practice.get('technical_owner')}.")
        else:
            status = "partial"
            severity = "medium"
            findings.append("Workstation and software patch management cadence needs formal record.")

    # 18. Vulnerability Management
    elif cid == "VEL-VULN-MGMT-001":
        if flows:
            status = "addressed"
            severity = "info"
            findings.append(f"Data flow perimeter mapped ({len(flows)} flows) with HTTPS transmission checks.")
        else:
            status = "partial"
            severity = "medium"
            findings.append("Vulnerability exposure review needed.")

    # 19. Endpoint Protection / EDR
    elif cid == "VEL-EDR-STATUS-001":
        tech_owner = str(practice.get("technical_owner", "")).lower()
        if "msp" in tech_owner:
            status = "addressed"
            severity = "info"
            findings.append(f"Managed endpoint protection administered by {practice.get('technical_owner')}.")
        else:
            status = "partial"
            severity = "high"
            findings.append("Endpoint protection / antivirus attestation required across staff endpoints.")

    # 20. Log Review
    elif cid == "VEL-LOG-REVIEW-001":
        if readiness.get("log_review_cadence"):
            status = "addressed"
            severity = "info"
            findings.append("Regular information system activity review cadence established.")
        else:
            status = "gap"
            severity = "high"
            findings.append("No formal log review cadence established.")

    # 21. Device Encryption
    elif cid == "VEL-ENCRYPT-DEVICE-001":
        managed = any("managed endpoint" in str(s.get("access_method", "")).lower() for s in systems)
        if managed:
            status = "addressed"
            severity = "info"
            findings.append("Managed endpoints designated for ePHI access with storage encryption.")
        else:
            status = "partial"
            severity = "high"
            findings.append("Device encryption (BitLocker / FileVault) attestation required.")

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
        if readiness.get("vendor_inventory") and systems:
            status = "addressed"
            severity = "info"
            findings.append(f"Vendor inventory maintained across {len(systems)} systems.")
        else:
            status = "gap"
            severity = "high"
            findings.append("Vendor inventory incomplete or missing.")

    # 24. BAA Status
    elif cid == "VEL-BAA-STATUS-001":
        ephi_vendors = [s.get("vendor") for s in systems if "transmits" in str(s.get("ephi_role", "")).lower() or "maintains" in str(s.get("ephi_role", "")).lower()]
        if readiness.get("baa_register"):
            status = "addressed"
            severity = "info"
            findings.append("Business Associate Agreement register complete and reviewed.")
        else:
            status = "gap"
            severity = "critical"
            findings.append(f"BAA register not complete; {len(set(ephi_vendors))} ePHI vendors require signed BAA verification.")

    # 25. Vendor Security Evidence
    elif cid == "VEL-VENDOR-EVIDENCE-001":
        if vendors:
            status = "addressed"
            severity = "info"
            findings.append(f"Security attestations tracked for {len(vendors)} vendors.")
        else:
            status = "partial"
            severity = "medium"
            findings.append("Vendor SOC 2 / HITRUST / security attestations need gathering.")

    # 26. Vendor Incident Notice Terms
    elif cid == "VEL-VENDOR-TERMS-001":
        if readiness.get("baa_register"):
            status = "addressed"
            severity = "info"
            findings.append("Vendor breach notification requirements governed under BAAs.")
        else:
            status = "gap"
            severity = "high"
            findings.append("Vendor breach notification and retention terms unverified.")

    # 27. AI Tool Inventory & Workflow Decision
    elif cid == "VEL-AI-INVENTORY-001":
        ai_systems = [s for s in systems if "ai" in str(s.get("category", "")).lower()]
        if not ai_systems and not ai_workflows:
            status = "not_applicable"
            severity = "info"
            findings.append("No AI tools or automated assistants in practice scope.")
        else:
            unapproved = [s for s in ai_systems if "pilot" in str(s.get("name", "")).lower() or "pilot" in str(s.get("evidence_needed", "")).lower()]
            if unapproved:
                status = "partial"
                severity = "high"
                findings.append(f"AI tools identified ({len(ai_systems)}); {len(unapproved)} pilot tool(s) require formal approval before ePHI exposure.")
            else:
                status = "addressed"
                severity = "info"
                findings.append(f"All {len(ai_systems)} AI tools have approved usage guidelines.")

    # 28. AI Data Use & Model Training
    elif cid == "VEL-AI-DATA-USE-001":
        ai_systems = [s for s in systems if "ai" in str(s.get("category", "")).lower()]
        if not ai_systems and not ai_workflows:
            status = "not_applicable"
            severity = "info"
            findings.append("No AI workflows in practice scope.")
        else:
            training_prohibited = any("no phi" in str(s.get("ephi_role", "")).lower() for s in ai_systems)
            if training_prohibited:
                status = "addressed"
                severity = "info"
                findings.append("Prohibition of patient data for model training confirmed in staff guidance.")
            else:
                status = "gap"
                severity = "high"
                findings.append("Verification required that vendor does not train models on practice ePHI.")

    # 29. Physical Access Basics
    elif cid == "VEL-PHYSICAL-ACCESS-001":
        locs = practice.get("locations", 1)
        if locs > 0:
            status = "addressed"
            severity = "info"
            findings.append(f"Physical access scope bounded to {locs} clinic facility location(s).")
        else:
            status = "gap"
            severity = "medium"
            findings.append("Practice physical facility location count undefined.")

    # 30. Device / Media Disposal
    elif cid == "VEL-MEDIA-DISPOSAL-001":
        if readiness.get("unique_accounts") and practice.get("technical_owner"):
            status = "addressed"
            severity = "info"
            findings.append("Media disposal and device retirement overseen by technical lead.")
        else:
            status = "partial"
            severity = "medium"
            findings.append("Media sanitization and disposal procedures require formal policy.")

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

    # Required vs Addressable breakdown
    req_total = sum(1 for e in evaluations if e.cfr_designation == "Required")
    req_addressed = sum(1 for e in evaluations if e.cfr_designation == "Required" and e.status == "addressed")
    addr_total = sum(1 for e in evaluations if e.cfr_designation == "Addressable")
    addr_addressed = sum(1 for e in evaluations if e.cfr_designation == "Addressable" and e.status in {"addressed", "partial"})

    crit_gaps = sum(1 for e in evaluations if e.status in {"gap", "partial"} and e.severity == "critical")
    high_gaps = sum(1 for e in evaluations if e.status in {"gap", "partial"} and e.severity == "high")

    # Family breakdown
    by_family: dict[str, dict[str, int]] = {}
    for e in evaluations:
        fam = e.control_family
        if fam not in by_family:
            by_family[fam] = {"total": 0, "addressed": 0, "partial": 0, "gap": 0}
        by_family[fam]["total"] += 1
        by_family[fam][e.status] = by_family[fam].get(e.status, 0) + 1

    # HICP breakdown
    by_hicp: dict[str, dict[str, int]] = {}
    for e in evaluations:
        hicp = e.hicp_practice.split(" - ")[0] if " - " in e.hicp_practice else e.hicp_practice
        if hicp not in by_hicp:
            by_hicp[hicp] = {"total": 0, "addressed": 0, "partial": 0, "gap": 0}
        by_hicp[hicp]["total"] += 1
        by_hicp[hicp][e.status] = by_hicp[hicp].get(e.status, 0) + 1

    practice = profile.get("practice", {})
    summary = AuditReportSummary(
        practice_name=str(practice.get("name", "Healthcare Practice")),
        practice_type=str(practice.get("type", "General")),
        staff_count=int(practice.get("staff_count", 0)),
        review_period=str(practice.get("review_period", "Current")),
        generated_at=gen_time,
        total_controls=total,
        addressed_count=addressed,
        partial_count=partial,
        gap_count=gaps,
        not_applicable_count=na,
        readiness_percentage=readiness_pct,
        required_addressed_ratio=f"{req_addressed}/{req_total}",
        addressable_addressed_ratio=f"{addr_addressed}/{addr_total}",
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
        "REGULATORY STATUTORY COMPLIANCE RATIOS:",
        f"  45 CFR § 164 Required Controls    : {s['required_addressed_ratio']} addressed",
        f"  45 CFR § 164 Addressable Controls : {s['addressable_addressed_ratio']} implemented/partial",
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
        lines.append(f"\n* {c['control_id']}: {c['control_name']} {badge} {sev_badge}")
        # Cleanly print citation without duplicate designation if already embedded
        citation_str = c["cfr_citation"]
        if f"({c['cfr_designation']})" not in citation_str:
            citation_str = f"{citation_str} ({c['cfr_designation']})"
        lines.append(f"  Citation : {citation_str}")
        lines.append(f"  Framework: {c['nist_ref']} | {c['hicp_practice']}")
        lines.append(f"  Owner    : {c['accountable_owner']}")
        for f in c["findings"]:
            lines.append(f"  Finding  : {f}")
        if c["status"] in {"gap", "partial"}:
            lines.append(f"  Action   : {c['next_action']}")
            if c["acceptable_evidence"]:
                lines.append(f"  Evidence : {'; '.join(c['acceptable_evidence'][:3])}")

    lines.append("\n" + "=" * 80)
    return "\n".join(lines)


def render_audit_report_markdown(report: dict[str, Any], gaps_only: bool = False) -> str:
    s = report["summary"]
    lines = [
        f"# Security Audit Gap Report: {s['practice_name']}",
        "",
        f"**Practice Type:** {s['practice_type']} | **Staff Count:** {s['staff_count']} | **Review Period:** {s['review_period']} | **Generated:** {s['generated_at'][:10]}",
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
        "| Family | Total | Addressed | Partial | Gap |",
        "| --- | --- | --- | --- | --- |",
    ]
    for fam, counts in s["by_family"].items():
        lines.append(f"| {fam} | {counts['total']} | {counts.get('addressed', 0)} | {counts.get('partial', 0)} | {counts.get('gap', 0)} |")

    lines.append("")
    lines.append("## Unaddressed Audit Gaps & Required Actions" if gaps_only else "## Control Evidence Matrix Evaluation")
    lines.append("")
    lines.append("| Control ID | Control Name | Status | Severity | Citation | Accountable Owner | Finding & Next Action |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")

    target_controls = report["unaddressed_gaps"] if gaps_only else report["controls"]
    for c in target_controls:
        status_md = f"**{c['status'].upper()}**"
        sev_md = f"`{c['severity']}`" if c["status"] in {"gap", "partial"} else "ok"
        finding_text = "<br>".join(c["findings"])
        if c["status"] in {"gap", "partial"}:
            finding_text += f"<br><em>Action:</em> {c['next_action']}"
        lines.append(
            f"| `{c['control_id']}` | {c['control_name']} | {status_md} | {sev_md} | {c['cfr_citation']} | `{c['accountable_owner']}` | {finding_text} |"
        )

    lines.append("")
    lines.append("> [!NOTE]")
    lines.append("> This audit gap report is prepared for internal compliance readiness under HIPAA (45 CFR § 164), NIST SP 800-66r2, and HHS 405(d) HICP. All technical evidence is metadata-only without storing or transmitting raw patient records.")
    return "\n".join(lines)


def render_audit_report_csv(report: dict[str, Any]) -> str:
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
        "next_action",
    ]
    writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for c in report["controls"]:
        writer.writerow({
            "control_id": c["control_id"],
            "control_name": c["control_name"],
            "control_family": c["control_family"],
            "risk_area": c["risk_area"],
            "cfr_citation": c["cfr_citation"],
            "cfr_designation": c["cfr_designation"],
            "nist_ref": c["nist_ref"],
            "hicp_practice": c["hicp_practice"],
            "status": c["status"],
            "severity": c["severity"],
            "accountable_owner": c["accountable_owner"],
            "findings": " | ".join(c["findings"]),
            "next_action": c["next_action"],
        })
    return output.getvalue()


def render_audit_report_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True) + "\n"
