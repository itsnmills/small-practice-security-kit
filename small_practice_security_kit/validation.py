from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError as JsonSchemaValidationError


class ValidationError(ValueError):
    """Raised when a public profile or import file is structurally invalid."""


ROOT = Path(__file__).resolve().parents[1]
PROFILE_SCHEMA_PATH = ROOT / "schemas" / "practice-profile.schema.json"

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


@lru_cache(maxsize=1)
def profile_schema() -> dict[str, Any]:
    return json.loads(PROFILE_SCHEMA_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def profile_validator() -> Draft202012Validator:
    validator = Draft202012Validator(profile_schema())
    validator.check_schema(profile_schema())
    return validator


def json_path(path: Any) -> str:
    parts = ["profile"]
    for item in path:
        if isinstance(item, int):
            parts[-1] = f"{parts[-1]}[{item}]"
        else:
            parts.append(str(item))
    return ".".join(parts)


def expected_type(schema_type: Any) -> str:
    if isinstance(schema_type, list):
        return " or ".join(str(item) for item in schema_type)
    return str(schema_type)


def required_fields_error(error: JsonSchemaValidationError) -> str:
    if isinstance(error.instance, dict):
        missing = [field for field in error.validator_value if field not in error.instance]
    else:
        missing = list(error.validator_value)
    return f"{json_path(error.absolute_path)} missing required field(s): {', '.join(str(field) for field in missing)}"


def enum_error(error: JsonSchemaValidationError) -> str:
    choices = ", ".join(str(choice) for choice in error.validator_value)
    return f"{json_path(error.absolute_path)} must be one of {choices}"


def additional_properties_error(error: JsonSchemaValidationError) -> str:
    properties = re.findall(r"'([^']+)'", error.message)
    if properties:
        return f"{json_path(error.absolute_path)} contains unknown field(s): {', '.join(properties)}"
    return f"{json_path(error.absolute_path)} contains unknown field(s)"


def format_schema_error(error: JsonSchemaValidationError) -> str:
    path = json_path(error.absolute_path)
    if error.validator == "required":
        return required_fields_error(error)
    if error.validator == "type":
        return f"{path} must be {expected_type(error.validator_value)}"
    if error.validator == "enum":
        return enum_error(error)
    if error.validator == "minLength":
        return f"{path} must not be empty"
    if error.validator == "minimum":
        return f"{path} must be at least {error.validator_value}"
    if error.validator == "additionalProperties":
        return additional_properties_error(error)
    return f"{path} failed {error.validator} validation"


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
    errors = sorted(profile_validator().iter_errors(profile), key=lambda err: [str(part) for part in err.absolute_path])
    if errors:
        formatted = [format_schema_error(error) for error in errors[:8]]
        extra = len(errors) - len(formatted)
        if extra:
            formatted.append(f"{extra} additional validation error(s)")
        raise ValidationError("profile schema validation failed:\n- " + "\n- ".join(formatted))


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
