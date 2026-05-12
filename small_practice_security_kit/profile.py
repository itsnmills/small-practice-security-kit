from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .validation import validate_profile


def load_profile(path: Path, *, validate: bool = True) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        profile = yaml.safe_load(handle) or {}
    if validate:
        validate_profile(profile)
    return profile


def write_profile(profile: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(profile, sort_keys=False), encoding="utf-8", newline="\n")


def slugify(name: str) -> str:
    return "".join(char.lower() if char.isalnum() else "_" for char in name).strip("_")
