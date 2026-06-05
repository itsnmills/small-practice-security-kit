from __future__ import annotations

from collections import Counter
from datetime import date, timedelta
from typing import Any

from .external_precheck import (
    EXTERNAL_PRECHECK_ARTIFACT,
    external_finding_id,
    external_finding_owner,
    external_finding_severity,
    external_finding_title,
    external_precheck_findings,
)


LIFECYCLE_STATUSES = {
    "missing",
    "requested",
    "partial",
    "provided",
    "reviewed",
    "stale",
    "outdated",
    "blocked",
    "closed",
    "not_applicable",
}

CLOSEOUT_STATES = {"blocked", "needs_evidence", "ready_for_review", "closed", "not_applicable"}

STATUS_ALIASES = {
    "": "requested",
    "needed": "requested",
    "needs review": "requested",
    "needs_review": "requested",
    "open": "requested",
    "requested": "requested",
    "unknown": "missing",
    "not recorded": "missing",
    "not_recorded": "missing",
    "not documented": "missing",
    "not_documented": "missing",
    "not run": "missing",
    "not_run": "missing",
    "not provided": "missing",
    "not_provided": "missing",
    "absent": "missing",
    "missing": "missing",
    "missing review date": "stale",
    "missing_review_date": "stale",
    "outdated": "stale",
    "stale": "stale",
    "partial": "partial",
    "observed": "provided",
    "provided": "provided",
    "reviewed": "reviewed",
    "signed": "provided",
    "documented": "provided",
    "complete": "closed",
    "completed": "closed",
    "closed": "closed",
    "ready": "provided",
    "allowed": "closed",
    "prohibited": "blocked",
    "blocked": "blocked",
    "not applicable": "not_applicable",
    "not_applicable": "not_applicable",
    "not needed": "not_applicable",
    "not_needed": "not_applicable",
}

STATUS_LABELS = {
    "missing": "Missing",
    "requested": "Requested",
    "partial": "Partial",
    "provided": "Provided",
    "reviewed": "Reviewed",
    "stale": "Stale",
    "outdated": "Stale",
    "blocked": "Blocked",
    "closed": "Closed",
    "not_applicable": "Not applicable",
}

CLOSEOUT_LABELS = {
    "blocked": "Blocked",
    "needs_evidence": "Needs evidence",
    "ready_for_review": "Ready for review",
    "closed": "Closed",
    "not_applicable": "Not applicable",
}

DEFAULT_UNSAFE_INPUTS = [
    "PHI",
    "patient identifiers",
    "credentials",
    "private URLs",
    "raw logs",
    "screenshots with sensitive data",
    "raw contracts",
    "real incident details",
]


def slug(value: Any) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in str(value).lower()).strip("_") or "item"


def normalize_lifecycle_status(value: Any, *, default: str = "requested") -> str:
    raw = str(value if value is not None else default).strip().lower().replace("-", "_")
    raw = raw.replace(" ", "_")
    status = STATUS_ALIASES.get(raw, STATUS_ALIASES.get(raw.replace("_", " "), raw))
    return status if status in LIFECYCLE_STATUSES else default


def closeout_state_for(status: str, *, risk: str = "medium", reviewer_needed: bool = False) -> str:
    normalized = normalize_lifecycle_status(status)
    risk_level = str(risk or "medium").lower()
    if normalized == "not_applicable":
        return "not_applicable"
    if normalized == "closed":
        return "closed"
    if normalized == "blocked":
        return "blocked"
    if normalized in {"missing", "stale", "outdated"}:
        return "blocked" if risk_level in {"high", "critical"} else "needs_evidence"
    if normalized in {"requested", "partial"}:
        return "needs_evidence"
    if normalized in {"provided", "reviewed"}:
        return "ready_for_review" if reviewer_needed or risk_level in {"high", "critical"} else "closed"
    return "needs_evidence"


def lifecycle_label(status: str) -> str:
    return STATUS_LABELS.get(normalize_lifecycle_status(status), str(status).replace("_", " ").title())


def closeout_label(state: str) -> str:
    return CLOSEOUT_LABELS.get(str(state), str(state).replace("_", " ").title())


def next_review_date(generated_date: date, risk: str, status: str) -> str:
    closeout = closeout_state_for(status, risk=risk)
    if closeout == "blocked":
        days = 14
    elif closeout == "needs_evidence":
        days = 30
    elif closeout == "ready_for_review":
        days = 60
    else:
        days = 90
    return (generated_date + timedelta(days=days)).isoformat()


def _split_evidence(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return [part.strip() for part in str(value or "").split(",") if part.strip()]


def _dedupe(values: list[str] | None) -> list[str]:
    deduped: list[str] = []
    for value in values or []:
        text = str(value)
        if text and text not in deduped:
            deduped.append(text)
    return deduped


def _system_lookup(profile: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(system.get("name", "")).lower(): system for system in profile.get("systems", [])}


def _flow_lookup(profile: dict[str, Any]) -> list[dict[str, Any]]:
    return list(profile.get("flows", []))


def _systems_for_flow(profile: dict[str, Any], flow: dict[str, Any]) -> list[str]:
    systems = _system_lookup(profile)
    names = []
    for key in ("source", "destination"):
        value = str(flow.get(key, ""))
        if value.lower() in systems:
            names.append(value)
    return names


def _flows_for_vendor(profile: dict[str, Any], vendor_name: str) -> list[str]:
    vendor_key = vendor_name.lower()
    return [str(flow.get("id")) for flow in _flow_lookup(profile) if str(flow.get("vendor", "")).lower() == vendor_key]


def _systems_for_vendor(profile: dict[str, Any], vendor_name: str) -> list[str]:
    vendor_key = vendor_name.lower()
    return [str(system.get("name")) for system in profile.get("systems", []) if str(system.get("vendor", "")).lower() == vendor_key]


def _flows_for_system(profile: dict[str, Any], system_name: str) -> list[str]:
    key = system_name.lower()
    matches = []
    for flow in _flow_lookup(profile):
        if key in {str(flow.get("source", "")).lower(), str(flow.get("destination", "")).lower()}:
            matches.append(str(flow.get("id")))
    return matches


def _flows_for_ai_workflow(profile: dict[str, Any], workflow: dict[str, Any]) -> list[str]:
    name = str(workflow.get("name", "")).lower()
    vendor = str(workflow.get("vendor", "")).lower()
    matches = []
    for flow in _flow_lookup(profile):
        haystack = " ".join(str(flow.get(key, "")).lower() for key in ["source", "destination", "vendor", "ephi_type"])
        vendor_matches = vendor and (vendor in haystack or haystack in vendor)
        if name in haystack or vendor_matches:
            matches.append(str(flow.get("id")))
    return _dedupe(matches)


def _record(
    *,
    evidence_id: str,
    title: str,
    evidence_type: str,
    source_kind: str,
    source_ref: str,
    source_system: str,
    owner: str,
    status: str,
    risk: str,
    generated_date: date,
    artifact_refs: list[str],
    acceptable_evidence: list[str],
    next_action: str,
    closeout_rule: str,
    notes: str = "",
    reviewer_needed: bool = False,
    unsafe_inputs: list[str] | None = None,
    flow_ids: list[str] | None = None,
    system_refs: list[str] | None = None,
    vendor_refs: list[str] | None = None,
    workflow_refs: list[str] | None = None,
    source_modules: list[str] | None = None,
) -> dict[str, Any]:
    lifecycle_status = normalize_lifecycle_status(status)
    closeout_state = closeout_state_for(lifecycle_status, risk=risk, reviewer_needed=reviewer_needed)
    artifact_refs = _dedupe(artifact_refs)
    return {
        "evidence_id": evidence_id,
        "title": title,
        "evidence_type": evidence_type,
        "source_kind": source_kind,
        "source_ref": source_ref,
        "source_system": source_system,
        "owner": owner,
        "status": lifecycle_status,
        "lifecycle_status": lifecycle_status,
        "closeout_state": closeout_state,
        "date_observed": generated_date.isoformat(),
        "next_review_date": next_review_date(generated_date, risk, lifecycle_status),
        "sensitivity_boundary": "reference_only_no_phi_no_secret",
        "artifact_refs": artifact_refs,
        "acceptable_evidence": acceptable_evidence,
        "unsafe_inputs": _dedupe(unsafe_inputs or DEFAULT_UNSAFE_INPUTS),
        "next_action": next_action,
        "closeout_rule": closeout_rule,
        "notes": notes,
        "trace": {
            "source_kind": source_kind,
            "source_ref": source_ref,
            "flow_ids": _dedupe(flow_ids),
            "system_refs": _dedupe(system_refs),
            "vendor_refs": _dedupe(vendor_refs),
            "workflow_refs": _dedupe(workflow_refs),
            "artifact_refs": artifact_refs,
            "source_modules": _dedupe(source_modules or [source_kind]),
        },
    }


def build_evidence_lifecycle(profile: dict[str, Any], generated_date: date) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    practice = profile.get("practice", {})
    security_owner = str(practice.get("security_owner") or "Office Manager")
    technical_owner = str(practice.get("technical_owner") or "MSP Lead")

    for index, item in enumerate(external_precheck_findings(profile), start=1):
        evidence_id = external_finding_id(item, index)
        title = external_finding_title(item)
        lowered = title.lower()
        category = str(item.get("category") or "external_precheck").lower()
        is_tracker = "tracker" in category or "tracker" in lowered or "pixel" in lowered or "analytics" in lowered
        is_tls = "tls" in category or "tls" in lowered or "certificate" in lowered or "https" in lowered
        acceptable = (
            [
                "tracker inventory",
                "tag manager export",
                "sanitized network request summary",
                "page/workflow label",
                "vendor BAA or authorization review note",
                "privacy reviewer disposition",
            ]
            if is_tracker
            else [
                "TLS scan summary",
                "certificate expiry and issuer",
                "HTTPS redirect evidence",
                "HSTS status",
                "covered host list",
                "MSP attestation",
            ]
            if is_tls
            else [
                "public observation summary",
                "page/workflow label",
                "date observed",
                "owner",
                "vendor/MSP/reviewer note",
            ]
        )
        unsafe = DEFAULT_UNSAFE_INPUTS + [
            "real form submissions",
            "patient-entered details",
            "full intercepted payloads with sensitive data",
            "session cookies",
            "private admin links",
        ]
        page = str(item.get("page_label") or item.get("url_label") or "public patient-facing workflow")
        destination = str(item.get("network_destination") or item.get("observed_technology") or "")
        records.append(
            _record(
                evidence_id=evidence_id,
                title=title,
                evidence_type="external_precheck",
                source_kind="external_precheck",
                source_ref=evidence_id,
                source_system=page,
                owner=external_finding_owner(item, profile),
                status=str(item.get("status") or "observed"),
                risk=external_finding_severity(item),
                generated_date=generated_date,
                artifact_refs=[EXTERNAL_PRECHECK_ARTIFACT],
                acceptable_evidence=acceptable,
                next_action=str(
                    item.get("next_action")
                    or (
                        "Route the tracker observation to the website vendor and qualified privacy reviewer before relying on the workflow."
                        if is_tracker
                        else "Ask the MSP or website vendor to confirm public-site TLS posture and record a reference-only evidence note."
                        if is_tls
                        else "Assign the observation to the right owner and collect reference-only evidence."
                    )
                ),
                closeout_rule=(
                    "Close when tracker purpose, data sent, tag placement, vendor relationship, and reviewer disposition are recorded without PHI."
                    if is_tracker
                    else "Close when TLS/certificate posture, covered hosts, redirect behavior, HSTS status, and owner acceptance or remediation are recorded."
                    if is_tls
                    else "Close when owner, evidence reference, date observed, and reviewer disposition are recorded."
                ),
                notes=f"Observation context: {destination}".strip(),
                reviewer_needed=True,
                unsafe_inputs=unsafe,
                source_modules=["external_precheck"],
            )
        )

    for item in profile.get("evidence", []):
        evidence_id = str(item.get("id") or f"EVID-{len(records) + 1:03d}")
        area = str(item.get("area") or item.get("type") or "Evidence")
        risk = "high" if area.lower() in {"access", "backup", "vendor"} else "medium"
        records.append(
            _record(
                evidence_id=evidence_id,
                title=str(item.get("title") or "Evidence reference"),
                evidence_type=slug(area),
                source_kind="evidence",
                source_ref=evidence_id,
                source_system=str(item.get("reference") or "practice evidence index"),
                owner=str(item.get("owner") or security_owner),
                status=str(item.get("status") or "requested"),
                risk=risk,
                generated_date=generated_date,
                artifact_refs=["evidence-binder-index.md"],
                acceptable_evidence=[str(item.get("title") or "reference-only evidence"), "date observed", "owner signoff", "scope covered", "exception note"],
                next_action="Collect or refresh the reference-only evidence and record owner/date/scope without uploading raw evidence.",
                closeout_rule="Close when the private evidence reference has owner, date observed, scope covered, and exception handling.",
                notes=str(item.get("notes") or ""),
                reviewer_needed=risk == "high",
                source_modules=["evidence"],
            )
        )

    readiness_map = [
        ("READINESS-MFA-EMAIL", "Email MFA evidence", "mfa_email", "Access / MFA", security_owner, "email access", "readiness-review.md", "MFA policy export, covered groups, exceptions, and date observed"),
        ("READINESS-MFA-EHR", "EHR MFA evidence", "mfa_ehr", "Access / MFA", technical_owner, "EHR access", "owner-msp-handoff.md", "MFA enforcement export, admin screenshot with date observed, covered groups, exceptions, and MSP attestation"),
        ("READINESS-UNIQUE-ACCOUNTS", "Unique account evidence", "unique_accounts", "Access review", technical_owner, "account lifecycle", "owner-msp-handoff.md", "User list export, shared-account exception list, owner signoff, and sunset dates"),
        ("READINESS-ACCESS-REVIEW", "Quarterly access review evidence", "quarterly_access_review", "Access review", technical_owner, "access review", "owner-msp-handoff.md", "User list export, admin role list, owner signoff, removed-account notes, and exception sunset dates"),
        ("READINESS-BACKUP-RESTORE", "Backup restore evidence", "tested_backups", "Backup / downtime", technical_owner, "backup and restore", "downtime-ransomware-tabletop.md", "Backup scope summary, restore-test note, date observed, recovery owner, and excluded systems"),
        ("READINESS-VENDOR-INVENTORY", "Vendor inventory evidence", "vendor_inventory", "Vendor / BAA", security_owner, "vendor register", "vendor-baa-review.md", "Vendor register, owner, service, ePHI touch status, BAA status, and review date"),
        ("READINESS-BAA-REGISTER", "BAA register evidence", "baa_register", "Vendor / BAA", security_owner, "BAA register", "vendor-baa-review.md", "BAA status, review date, vendor security page, SOC 2/HITRUST status, and incident terms"),
        ("READINESS-INCIDENT-CONTACTS", "Incident contact evidence", "incident_contact_list", "Incident readiness", security_owner, "incident contacts", "incident-decision-log.md", "Incident contact list, MSP contact, vendor contact, qualified-review contact, and review date"),
        ("READINESS-DOWNTIME-PLAN", "Downtime plan evidence", "downtime_plan", "Downtime", technical_owner, "downtime workflow", "downtime-ransomware-tabletop.md", "Downtime workflow, manual workaround owner, staff acknowledgement, and tabletop attendance"),
        ("READINESS-TRAINING", "Security training evidence", "security_training_current", "Workforce", security_owner, "staff training", "readiness-review.md", "Training roster, acknowledgement date, no-PHI AI guidance, and exception list"),
        ("READINESS-LOG-REVIEW", "Log review cadence evidence", "log_review_cadence", "Monitoring", technical_owner, "log review", "owner-msp-handoff.md", "Log source list, review cadence record, alert owner, escalation path, and date observed"),
    ]
    readiness = profile.get("readiness", {})
    for evidence_id, title, key, area, owner, source, artifact, evidence_text in readiness_map:
        present = bool(readiness.get(key))
        risk = "high" if key in {"mfa_ehr", "tested_backups", "baa_register", "downtime_plan", "log_review_cadence"} and not present else "medium"
        records.append(
            _record(
                evidence_id=evidence_id,
                title=title,
                evidence_type=slug(area),
                source_kind="readiness",
                source_ref=key,
                source_system=source,
                owner=owner,
                status="provided" if present else "missing",
                risk=risk,
                generated_date=generated_date,
                artifact_refs=[artifact, "readiness-review.md"],
                acceptable_evidence=_split_evidence(evidence_text),
                next_action="Request proof, document exceptions, and assign an owner before closeout." if not present else "Keep this evidence on a quarterly refresh cadence.",
                closeout_rule=f"Close when {evidence_text.lower()} are recorded as reference-only evidence.",
                reviewer_needed=risk == "high",
                source_modules=["readiness"],
            )
        )

    for flow in profile.get("flows", []):
        flow_id = str(flow.get("id"))
        risk = str(flow.get("risk") or "medium")
        system_refs = _systems_for_flow(profile, flow)
        records.append(
            _record(
                evidence_id=flow_id,
                title=str(flow.get("evidence_needed") or f"Evidence for {flow_id}"),
                evidence_type="ephi_flow",
                source_kind="flow",
                source_ref=flow_id,
                source_system=str(flow.get("source") or "ePHI flow"),
                owner="MSP or workflow owner",
                status="requested" if flow.get("baa_needed") or risk in {"high", "critical"} else "provided",
                risk=risk,
                generated_date=generated_date,
                artifact_refs=["ephi-flow-map.md", "evidence-binder-index.md"],
                acceptable_evidence=_split_evidence(flow.get("evidence_needed")),
                next_action="Confirm the flow owner, channel, BAA need, and private evidence reference.",
                closeout_rule="Close when owner, vendor path, BAA need, access/retention control, and private evidence reference are recorded.",
                reviewer_needed=risk in {"high", "critical"},
                flow_ids=[flow_id],
                system_refs=system_refs,
                vendor_refs=[str(flow.get("vendor"))] if flow.get("vendor") else [],
                source_modules=["flows", "systems"],
            )
        )

    for vendor in profile.get("vendors", []):
        vendor_name = str(vendor.get("name"))
        risk = str(vendor.get("risk") or "medium")
        status = vendor.get("baa_status")
        if not vendor.get("touches_ephi"):
            status = "not_applicable" if "not needed" in str(status).lower() else status
        records.append(
            _record(
                evidence_id=f"VENDOR-{slug(vendor_name).upper()}",
                title=f"Vendor evidence for {vendor_name}",
                evidence_type="vendor_baa",
                source_kind="vendor",
                source_ref=vendor_name,
                source_system=vendor_name,
                owner="Practice manager",
                status=str(status or "requested"),
                risk=risk,
                generated_date=generated_date,
                artifact_refs=["vendor-baa-review.md", "evidence-binder-index.md"],
                acceptable_evidence=["BAA status", "BAA review date", "SOC 2 or HITRUST status", "incident notification terms", "retention/deletion terms", "AI/data-use response"],
                next_action="Request vendor BAA, incident, subcontractor, retention/deletion, and AI/data-use answers without uploading raw contracts.",
                closeout_rule="Close when BAA status, review date, security evidence status, incident terms, data-use posture, and reviewer boundary are recorded.",
                notes=f"BAA status: {vendor.get('baa_status', 'unknown')}; incident terms: {vendor.get('incident_notification_terms', 'unknown')}",
                reviewer_needed=bool(vendor.get("touches_ephi")),
                flow_ids=_flows_for_vendor(profile, vendor_name),
                system_refs=_systems_for_vendor(profile, vendor_name),
                vendor_refs=[vendor_name],
                source_modules=["vendors", "flows"],
            )
        )

    for workflow in profile.get("ai_workflows", []):
        name = str(workflow.get("name"))
        decision = str(workflow.get("decision") or "restricted")
        risk = "high" if decision == "prohibited" else "medium" if decision == "restricted" else "low"
        records.append(
            _record(
                evidence_id=f"AI-{slug(name).upper()}",
                title=f"AI workflow evidence for {name}",
                evidence_type="ai_workflow",
                source_kind="ai_workflow",
                source_ref=name,
                source_system=str(workflow.get("vendor") or "AI workflow"),
                owner=security_owner,
                status="blocked" if decision == "prohibited" else "requested" if decision == "restricted" else "closed",
                risk=risk,
                generated_date=generated_date,
                artifact_refs=["ai-workflow-review.md", "evidence-binder-index.md"],
                acceptable_evidence=_split_evidence(workflow.get("evidence_needed")),
                next_action="Keep the workflow no-PHI or restricted until terms, retention, model-training use, and human review are documented.",
                closeout_rule="Close when staff guidance, allowed data classes, prohibited examples, owner approval, and vendor terms are recorded.",
                reviewer_needed=decision != "allowed",
                flow_ids=_flows_for_ai_workflow(profile, workflow),
                workflow_refs=[name],
                vendor_refs=[str(workflow.get("vendor"))] if workflow.get("vendor") else [],
                source_modules=["ai_workflows", "flows"],
            )
        )

    downtime = profile.get("downtime", {})
    downtime_status = downtime.get("downtime_plan_status") or "requested"
    restore_status = "stale" if not str(downtime.get("last_restore_test", "")).strip() else "provided"
    for system_name in downtime.get("critical_systems", []):
        system_name = str(system_name)
        status = "missing" if normalize_lifecycle_status(downtime_status) == "missing" else restore_status
        records.append(
            _record(
                evidence_id=f"DOWNTIME-{slug(system_name).upper()}",
                title=f"Downtime and restore evidence for {system_name}",
                evidence_type="downtime",
                source_kind="downtime",
                source_ref=system_name,
                source_system=system_name,
                owner=technical_owner,
                status=status,
                risk="high",
                generated_date=generated_date,
                artifact_refs=["downtime-ransomware-tabletop.md", "incident-evidence-timeline.md", "evidence-binder-index.md"],
                acceptable_evidence=["downtime workflow", "manual workaround owner", "backup scope", "restore-test note", "tabletop attendance"],
                next_action="Assign downtime owner, document manual workaround, and record restore-test/tabletop evidence references.",
                closeout_rule="Close when downtime owner, manual workaround, backup scope, restore-test evidence, and tabletop notes are recorded.",
                reviewer_needed=True,
                flow_ids=_flows_for_system(profile, system_name),
                system_refs=[system_name],
                source_modules=["downtime", "flows"],
            )
        )

    incident = profile.get("incident_timeline") or {}
    for index, entry in enumerate(incident.get("timeline", []), start=1):
        systems = [str(system) for system in entry.get("systems", [])]
        records.append(
            _record(
                evidence_id=f"INC-TIMELINE-{index:03d}",
                title=f"Incident timeline evidence for {entry.get('phase', 'timeline event')}",
                evidence_type="incident_timeline",
                source_kind="incident_timeline",
                source_ref=str(entry.get("time") or f"event-{index}"),
                source_system="; ".join(systems) or "incident tabletop",
                owner=str(entry.get("owner") or "Practice owner/MSP"),
                status=str(entry.get("status") or "requested"),
                risk="high",
                generated_date=generated_date,
                artifact_refs=["incident-evidence-timeline.md", "incident-after-action-report.md", "evidence-binder-index.md"],
                acceptable_evidence=["timeline event category", "owner", "timestamp or sequence marker", "private evidence reference", "decision gate"],
                next_action="Preserve reference-only event order and route qualified decisions to the right reviewer.",
                closeout_rule="Close when the event category, owner, private evidence reference, decision gate, and next reviewer are recorded.",
                notes=f"Private evidence reference: {entry.get('evidence_ref', 'private evidence reference')}",
                reviewer_needed=True,
                flow_ids=[flow_id for system in systems for flow_id in _flows_for_system(profile, system)],
                system_refs=systems,
                source_modules=["incident_timeline", "downtime"],
            )
        )

    for item in incident.get("after_actions", []):
        action_id = str(item.get("id") or f"INC-AA-{len(records) + 1:03d}")
        records.append(
            _record(
                evidence_id=action_id,
                title=f"Incident after-action evidence: {item.get('action', 'after-action item')}",
                evidence_type="incident_after_action",
                source_kind="incident_after_action",
                source_ref=action_id,
                source_system="incident after-action queue",
                owner=str(item.get("owner") or "Practice owner/MSP"),
                status="requested",
                risk=str(item.get("priority") or "medium"),
                generated_date=generated_date,
                artifact_refs=["incident-after-action-report.md", "incident-evidence-timeline.md", "evidence-binder-index.md"],
                acceptable_evidence=_split_evidence(item.get("evidence_needed")),
                next_action="Assign owner, due date, evidence reference, and reviewer lane before closing the after-action item.",
                closeout_rule="Close when the after-action owner, due date, evidence reference, and reviewer lane are recorded.",
                reviewer_needed=True,
                source_modules=["incident_timeline"],
            )
        )

    return records


def summarize_lifecycle(records: list[dict[str, Any]]) -> dict[str, Any]:
    by_status = Counter(str(record["lifecycle_status"]) for record in records)
    by_closeout = Counter(str(record["closeout_state"]) for record in records)
    return {
        "total": len(records),
        "by_lifecycle_status": dict(sorted(by_status.items())),
        "by_closeout_state": dict(sorted(by_closeout.items())),
        "blocked": by_closeout.get("blocked", 0),
        "needs_evidence": by_closeout.get("needs_evidence", 0),
        "ready_for_review": by_closeout.get("ready_for_review", 0),
        "closed": by_closeout.get("closed", 0),
        "traceable_to_ephi": sum(1 for record in records if record.get("trace", {}).get("flow_ids")),
    }


def trace_label(record: dict[str, Any]) -> str:
    trace = record.get("trace", {})
    parts = []
    if trace.get("flow_ids"):
        parts.append("flows " + ", ".join(trace["flow_ids"]))
    if trace.get("system_refs"):
        parts.append("systems " + ", ".join(trace["system_refs"]))
    if trace.get("vendor_refs"):
        parts.append("vendors " + ", ".join(trace["vendor_refs"]))
    if trace.get("workflow_refs"):
        parts.append("workflows " + ", ".join(trace["workflow_refs"]))
    return "; ".join(parts) if parts else str(record.get("source_ref") or record.get("source_kind") or "")


def lifecycle_by_source(records: list[dict[str, Any]], source_kind: str) -> dict[str, dict[str, Any]]:
    return {str(record["source_ref"]): record for record in records if record.get("source_kind") == source_kind}
