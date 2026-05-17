from __future__ import annotations

from typing import Any


SOC2_STATUS_FIELD = "soc2_status"
HITRUST_STATUS_FIELD = "hitrust_status"
DEFAULT_EVIDENCE_STATUS = "not provided"


def vendor_evidence_status(vendor: dict[str, Any], field: str) -> str:
    value = str(vendor.get(field) or "").strip()
    return value or DEFAULT_EVIDENCE_STATUS


def vendor_soc2_status(vendor: dict[str, Any]) -> str:
    return vendor_evidence_status(vendor, SOC2_STATUS_FIELD)


def vendor_hitrust_status(vendor: dict[str, Any]) -> str:
    return vendor_evidence_status(vendor, HITRUST_STATUS_FIELD)
