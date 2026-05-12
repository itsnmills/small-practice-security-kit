from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
CATALOG_DIR = ROOT / "catalogs"


def _load_yaml(name: str) -> dict[str, Any]:
    with (CATALOG_DIR / name).open(encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


@lru_cache(maxsize=1)
def load_catalogs() -> dict[str, Any]:
    return {
        "practice_presets": _load_yaml("practice_presets.yaml"),
        "system_catalog": _load_yaml("system_catalog.yaml"),
        "vendor_catalog": _load_yaml("vendor_catalog.yaml"),
        "evidence_catalog": _load_yaml("evidence_catalog.yaml"),
        "flow_templates": _load_yaml("flow_templates.yaml"),
    }


def presets() -> dict[str, Any]:
    return load_catalogs()["practice_presets"]["presets"]


def size_tiers() -> dict[str, Any]:
    return load_catalogs()["practice_presets"]["size_tiers"]


def systems() -> dict[str, Any]:
    return load_catalogs()["system_catalog"]["systems"]


def vendors() -> dict[str, Any]:
    return load_catalogs()["vendor_catalog"]["vendors"]


def evidence_types() -> dict[str, Any]:
    return load_catalogs()["evidence_catalog"]["evidence_types"]


def flow_templates() -> list[dict[str, Any]]:
    return load_catalogs()["flow_templates"]["flows"]
