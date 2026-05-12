from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .catalogs import evidence_types, flow_templates, presets, size_tiers, systems, vendors
from .validation import validate_profile


DEFAULT_READINESS = {
    "mfa_email": False,
    "mfa_ehr": False,
    "unique_accounts": True,
    "quarterly_access_review": False,
    "tested_backups": False,
    "vendor_inventory": True,
    "baa_register": False,
    "incident_contact_list": False,
    "downtime_plan": False,
    "security_training_current": False,
    "log_review_cadence": False,
}


AI_WORKFLOW_LIBRARY = {
    "marketing_drafting": {
        "name": "Marketing email drafting",
        "proposed_use": "Draft generic outreach or newsletter copy",
        "data_used": "No patient data",
        "vendor": "Public AI / chatbot usage",
        "decision": "allowed",
        "evidence_needed": "Staff guidance and prohibited data examples",
    },
    "billing_appeal": {
        "name": "Billing appeal drafter",
        "proposed_use": "Draft payer appeal language",
        "data_used": "Claim and treatment details unless redacted",
        "vendor": "Public AI / chatbot usage",
        "decision": "restricted",
        "evidence_needed": "BAA review, redaction workflow, owner approval",
    },
    "clinical_note_public_chatbot": {
        "name": "Paste visit note into public chatbot",
        "proposed_use": "Summarize a clinical note",
        "data_used": "Clinical note or patient-level identifiers",
        "vendor": "Public AI / chatbot usage",
        "decision": "prohibited",
        "evidence_needed": "Training reminder and AI use policy",
    },
    "visit_summary": {
        "name": "AI visit summary workflow",
        "proposed_use": "Draft or summarize visit information",
        "data_used": "Clinical details or encounter information",
        "vendor": "AI assistant or AI scribe vendor",
        "decision": "restricted",
        "evidence_needed": "Vendor BAA, data-use review, clinician review checklist",
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _vendor_name(vendor_key: str) -> str:
    return f"Example {vendors()[vendor_key]['label']}"


def build_system(system_key: str) -> dict[str, Any]:
    item = systems()[system_key]
    return {
        "id": f"system-{system_key}",
        "catalog_key": system_key,
        "name": item["name"],
        "category": item["category"],
        "ephi_role": item["ephi_role"],
        "owner": item["owner"],
        "vendor": _vendor_name(item["vendor_category"]),
        "vendor_category": item["vendor_category"],
        "access_method": item["access_method"],
        "evidence_needed": item["evidence_needed"],
        "selected": True,
    }


def build_vendor(vendor_key: str) -> dict[str, Any]:
    item = vendors()[vendor_key]
    return {
        "id": f"vendor-{vendor_key}",
        "category": vendor_key,
        "name": _vendor_name(vendor_key),
        "service": item["service"],
        "touches_ephi": bool(item["touches_ephi"]),
        "baa_status": item["baa_status"],
        "ai_training_use": item["ai_training_use"],
        "subcontractors_known": item["subcontractors_known"],
        "incident_notification_terms": item["incident_notification_terms"],
        "risk": item["risk"],
    }


def suggest_flows(selected_system_keys: list[str]) -> list[dict[str, Any]]:
    selected = set(selected_system_keys)
    results: list[dict[str, Any]] = []
    for template in flow_templates():
        required = set(template["requires"])
        if required.issubset(selected):
            results.append(dict(template))
    return results


def build_flows(selected_system_keys: list[str]) -> list[dict[str, Any]]:
    selected_systems = {key: systems()[key] for key in selected_system_keys}
    flows: list[dict[str, Any]] = []
    for index, template in enumerate(suggest_flows(selected_system_keys), start=1):
        vendor = ""
        for key in reversed(template["requires"]):
            if key in selected_systems:
                vendor = _vendor_name(selected_systems[key]["vendor_category"])
                break
        flows.append(
            {
                "id": f"FLOW-{index:03d}",
                "template_key": template["key"],
                "source": template["source"],
                "destination": template["destination"],
                "ephi_type": template["ephi_type"],
                "vendor": vendor,
                "transmission": template["transmission"],
                "baa_needed": bool(template["baa_needed"]),
                "risk": template["risk"],
                "evidence_needed": template["evidence_needed"],
                "suggested_by": list(template["requires"]),
                "confirmed": True,
            }
        )
    return flows


def build_evidence_references(profile: dict[str, Any]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    evidence_catalog = evidence_types()
    for vendor in profile["vendors"]:
        if vendor["touches_ephi"]:
            refs.append(
                {
                    "id": f"EVID-BAA-{vendor['id'].replace('vendor-', '').upper()}",
                    "title": f"{vendor['name']} signed BAA",
                    "type": "signed_baa",
                    "area": evidence_catalog["signed_baa"]["area"],
                    "owner": "Office Manager",
                    "reference": "",
                    "status": "needed",
                    "related": vendor["id"],
                    "stores_sensitive_content": False,
                    "notes": "Reference the BAA location and review date. Do not store PHI here.",
                }
            )
    refs.extend(
        [
            {
                "id": "EVID-ACCESS-REVIEW",
                "title": "Quarterly access review",
                "type": "user_access_review",
                "area": "Access",
                "owner": "Security Owner",
                "reference": "",
                "status": "needed",
                "related": "readiness.quarterly_access_review",
                "stores_sensitive_content": False,
                "notes": "Record review signoff location, not user secrets.",
            },
            {
                "id": "EVID-RESTORE-TEST",
                "title": "Restore test result",
                "type": "restore_test",
                "area": "Resilience",
                "owner": "MSP Lead",
                "reference": "",
                "status": "needed",
                "related": "readiness.tested_backups",
                "stores_sensitive_content": False,
                "notes": "Reference restore-test evidence and next action.",
            },
            {
                "id": "EVID-AI-POLICY",
                "title": "AI use policy and prohibited data examples",
                "type": "ai_policy",
                "area": "AI workflow",
                "owner": "Security Owner",
                "reference": "",
                "status": "needed",
                "related": "ai_workflows",
                "stores_sensitive_content": False,
                "notes": "Use examples only; do not include patient details.",
            },
        ]
    )
    return refs


def create_profile_from_preset(practice_name: str, preset_key: str = "dental", size_key: str = "small") -> dict[str, Any]:
    preset_map = presets()
    size_map = size_tiers()
    if preset_key not in preset_map:
        raise KeyError(f"Unknown practice preset: {preset_key}")
    if size_key not in size_map:
        raise KeyError(f"Unknown size tier: {size_key}")
    preset = preset_map[preset_key]
    size = size_map[size_key]
    selected_systems = list(preset["systems"])
    built_systems = [build_system(system_key) for system_key in selected_systems]
    vendor_keys = []
    for system in built_systems:
        key = system["vendor_category"]
        if key not in vendor_keys:
            vendor_keys.append(key)
    built_vendors = [build_vendor(key) for key in vendor_keys]
    profile = {
        "workspace": {
            "id": practice_name.lower().replace(" ", "-"),
            "created_at": utc_now(),
            "updated_at": utc_now(),
            "source": "local-intake",
            "profile_version": "3.0",
            "local_only": True,
        },
        "intake": {
            "preset": preset_key,
            "size_tier": size_key,
            "status": {
                "basics": "complete",
                "systems": "needs_review",
                "vendors": "needs_review",
                "flows": "needs_review",
                "readiness": "not_started",
                "ai": "needs_review",
                "downtime": "needs_review",
                "evidence": "needs_review",
            },
            "dismissed_suggestions": [],
        },
        "practice": {
            "name": practice_name,
            "type": preset["name"],
            "staff_count": size["staff_count"],
            "locations": size["locations"],
            "review_period": "Initial local intake",
            "security_owner": "Office Manager",
            "technical_owner": "MSP Lead",
        },
        "readiness": dict(DEFAULT_READINESS),
        "systems": built_systems,
        "flows": build_flows(selected_systems),
        "vendors": built_vendors,
        "ai_workflows": [dict(AI_WORKFLOW_LIBRARY[key]) for key in preset.get("ai_workflows", [])],
        "downtime": {
            "critical_systems": [
                system["name"]
                for system in built_systems
                if system["catalog_key"] in {"ehr", "billing", "phones", "shared_drive", "backup", "telehealth"}
            ],
            "last_restore_test": "",
            "downtime_plan_status": "not documented",
            "tabletop_status": "not run",
        },
    }
    profile["evidence"] = build_evidence_references(profile)
    validate_profile(profile)
    return profile


def rebuild_profile_suggestions(profile: dict[str, Any]) -> dict[str, Any]:
    selected_systems = [system.get("catalog_key") for system in profile.get("systems", []) if system.get("catalog_key")]
    profile["flows"] = build_flows(selected_systems)
    known_vendor_categories = {vendor.get("category") for vendor in profile.get("vendors", [])}
    for system in profile.get("systems", []):
        vendor_category = system.get("vendor_category")
        if vendor_category and vendor_category not in known_vendor_categories:
            profile.setdefault("vendors", []).append(build_vendor(vendor_category))
            known_vendor_categories.add(vendor_category)
    profile["evidence"] = build_evidence_references(profile)
    return profile
