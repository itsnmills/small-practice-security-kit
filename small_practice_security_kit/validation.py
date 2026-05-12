from __future__ import annotations

from typing import Any


class ValidationError(ValueError):
    """Raised when a public profile or import file is structurally invalid."""


REQUIRED_TOP_LEVEL = ["practice", "readiness", "systems", "flows", "vendors", "ai_workflows", "downtime"]
REQUIRED_PRACTICE = ["name", "type", "staff_count", "locations", "review_period", "security_owner", "technical_owner"]
REQUIRED_READINESS = [
    "mfa_email",
    "mfa_ehr",
    "unique_accounts",
    "quarterly_access_review",
    "tested_backups",
    "vendor_inventory",
    "baa_register",
    "incident_contact_list",
    "downtime_plan",
    "security_training_current",
    "log_review_cadence",
]
REQUIRED_SYSTEM = ["name", "category", "ephi_role", "owner", "vendor", "access_method", "evidence_needed"]
REQUIRED_FLOW = ["id", "source", "destination", "ephi_type", "vendor", "transmission", "baa_needed", "risk", "evidence_needed"]
REQUIRED_VENDOR = [
    "name",
    "service",
    "touches_ephi",
    "baa_status",
    "ai_training_use",
    "subcontractors_known",
    "incident_notification_terms",
    "risk",
]
REQUIRED_AI_WORKFLOW = ["name", "proposed_use", "data_used", "vendor", "decision", "evidence_needed"]
REQUIRED_DOWNTIME = ["critical_systems", "last_restore_test", "downtime_plan_status", "tabletop_status"]

VALID_RISKS = {"low", "medium", "high", "critical"}
VALID_AI_DECISIONS = {"allowed", "restricted", "prohibited"}


def require_fields(mapping: dict[str, Any], fields: list[str], context: str) -> None:
    missing = [field for field in fields if field not in mapping]
    if missing:
        raise ValidationError(f"{context} missing required field(s): {', '.join(missing)}")


def require_list(profile: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = profile.get(key)
    if not isinstance(value, list):
        raise ValidationError(f"{key} must be a list")
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValidationError(f"{key}[{index}] must be an object")
    return value


def require_bool(value: Any, context: str) -> None:
    if not isinstance(value, bool):
        raise ValidationError(f"{context} must be true or false")


def validate_profile(profile: dict[str, Any]) -> None:
    if not isinstance(profile, dict):
        raise ValidationError("profile must be a YAML object")
    require_fields(profile, REQUIRED_TOP_LEVEL, "profile")
    require_fields(profile["practice"], REQUIRED_PRACTICE, "practice")
    require_fields(profile["readiness"], REQUIRED_READINESS, "readiness")

    for field in REQUIRED_READINESS:
        require_bool(profile["readiness"][field], f"readiness.{field}")

    for index, system in enumerate(require_list(profile, "systems")):
        require_fields(system, REQUIRED_SYSTEM, f"systems[{index}]")

    for index, flow in enumerate(require_list(profile, "flows")):
        require_fields(flow, REQUIRED_FLOW, f"flows[{index}]")
        require_bool(flow["baa_needed"], f"flows[{index}].baa_needed")
        validate_risk(flow["risk"], f"flows[{index}].risk")

    for index, vendor in enumerate(require_list(profile, "vendors")):
        require_fields(vendor, REQUIRED_VENDOR, f"vendors[{index}]")
        require_bool(vendor["touches_ephi"], f"vendors[{index}].touches_ephi")
        validate_risk(vendor["risk"], f"vendors[{index}].risk")

    for index, workflow in enumerate(require_list(profile, "ai_workflows")):
        require_fields(workflow, REQUIRED_AI_WORKFLOW, f"ai_workflows[{index}]")
        if workflow["decision"] not in VALID_AI_DECISIONS:
            raise ValidationError(f"ai_workflows[{index}].decision must be one of {', '.join(sorted(VALID_AI_DECISIONS))}")

    require_fields(profile["downtime"], REQUIRED_DOWNTIME, "downtime")
    if not isinstance(profile["downtime"]["critical_systems"], list):
        raise ValidationError("downtime.critical_systems must be a list")


def validate_risk(value: Any, context: str) -> None:
    if value not in VALID_RISKS:
        raise ValidationError(f"{context} must be one of {', '.join(sorted(VALID_RISKS))}")


def validate_required_columns(headers: set[str], required: list[str], context: str) -> None:
    missing = [field for field in required if field not in headers]
    if missing:
        raise ValidationError(f"{context} missing required column(s): {', '.join(missing)}")


def parse_bool(value: str, context: str) -> bool:
    lowered = str(value).strip().lower()
    if lowered in {"true", "yes", "1"}:
        return True
    if lowered in {"false", "no", "0"}:
        return False
    raise ValidationError(f"{context} must be true/false or yes/no")
