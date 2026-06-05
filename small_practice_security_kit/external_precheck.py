from __future__ import annotations

from typing import Any


EXTERNAL_PRECHECK_STAGE = "external_evidence_precheck"
EXTERNAL_PRECHECK_SECTION = "external_evidence_precheck"
EXTERNAL_PRECHECK_ARTIFACT = "external-evidence-precheck.md"


def external_precheck_profile(profile: dict[str, Any]) -> dict[str, Any]:
    value = profile.get("external_precheck") or {}
    return value if isinstance(value, dict) else {}


def external_precheck_findings(profile: dict[str, Any]) -> list[dict[str, Any]]:
    findings = external_precheck_profile(profile).get("findings") or []
    return [item for item in findings if isinstance(item, dict)]


def external_precheck_scope(profile: dict[str, Any]) -> dict[str, Any]:
    scope = external_precheck_profile(profile).get("scope") or {}
    return scope if isinstance(scope, dict) else {}


def external_precheck_enabled(profile: dict[str, Any]) -> bool:
    return bool(external_precheck_findings(profile) or external_precheck_scope(profile))


def external_finding_id(item: dict[str, Any], index: int) -> str:
    value = str(item.get("id") or "").strip()
    return value or f"EXT-PRECHECK-{index:03d}"


def external_finding_title(item: dict[str, Any]) -> str:
    value = str(item.get("title") or "").strip()
    if value:
        return value
    category = str(item.get("category") or "external evidence").replace("_", " ")
    page = str(item.get("page_label") or item.get("workflow") or "patient-facing workflow")
    return f"{category.title()} needs review for {page}"


def external_finding_severity(item: dict[str, Any]) -> str:
    severity = str(item.get("severity") or item.get("risk") or "medium").strip().lower()
    return severity if severity in {"low", "medium", "high", "critical"} else "medium"


def external_finding_recipient(item: dict[str, Any]) -> str:
    category = str(item.get("category") or "").lower()
    title = external_finding_title(item).lower()
    if item.get("recipient"):
        return str(item["recipient"])
    if "tracker" in category or "tracker" in title or "pixel" in title or "analytics" in title:
        return "Vendor/legal/compliance reviewer"
    if "tls" in category or "certificate" in title or "https" in title:
        return "MSP"
    return "Owner/MSP"


def external_finding_owner(item: dict[str, Any], profile: dict[str, Any]) -> str:
    if item.get("owner"):
        return str(item["owner"])
    category = str(item.get("category") or "").lower()
    if "tls" in category or "certificate" in external_finding_title(item).lower():
        return str(profile.get("practice", {}).get("technical_owner") or "MSP Lead")
    return str(profile.get("practice", {}).get("security_owner") or "Office Manager")


def external_precheck_counts(profile: dict[str, Any]) -> dict[str, int]:
    findings = external_precheck_findings(profile)
    tracker = 0
    tls = 0
    other = 0
    high = 0
    for item in findings:
        title = external_finding_title(item).lower()
        category = str(item.get("category") or "").lower()
        if "tracker" in category or "tracker" in title or "pixel" in title or "analytics" in title:
            tracker += 1
        elif "tls" in category or "certificate" in title or "https" in title:
            tls += 1
        else:
            other += 1
        if external_finding_severity(item) in {"high", "critical"}:
            high += 1
    return {
        "findings": len(findings),
        "tracker_findings": tracker,
        "tls_findings": tls,
        "other_findings": other,
        "high_or_critical": high,
    }
