from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .profile import slugify
from .validation import validate_profile


ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "profiles"


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


class WorkspaceError(ValueError):
    pass


def ensure_workspace_dirs(root: Path = ROOT) -> dict[str, Path]:
    profiles = root / "profiles"
    backups = profiles / ".backups"
    logs = profiles / ".logs"
    profiles.mkdir(parents=True, exist_ok=True)
    backups.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    return {"profiles": profiles, "backups": backups, "logs": logs}


def safe_profile_path(name: str, root: Path = ROOT) -> Path:
    dirs = ensure_workspace_dirs(root)
    slug = slugify(name) or "practice"
    path = dirs["profiles"] / f"{slug}.yaml"
    resolved = path.resolve()
    profiles_root = dirs["profiles"].resolve()
    if profiles_root not in resolved.parents:
        raise WorkspaceError("Profile path escaped profiles directory")
    return resolved


def atomic_write_profile(profile: dict[str, Any], path: Path, *, action: str = "save", warnings: list[dict[str, str]] | None = None) -> None:
    validate_profile(profile)
    dirs = ensure_workspace_dirs(ROOT)
    resolved = path.resolve()
    profiles_root = dirs["profiles"].resolve()
    if profiles_root not in resolved.parents:
        raise WorkspaceError("Refusing to write profile outside profiles directory")
    if resolved.exists():
        backup = dirs["backups"] / f"{resolved.stem}-{utc_stamp()}.yaml"
        backup.write_text(resolved.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    profile.setdefault("workspace", {})["updated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    tmp = resolved.with_suffix(".yaml.tmp")
    tmp.write_text(yaml.safe_dump(profile, sort_keys=False), encoding="utf-8", newline="\n")
    os.replace(tmp, resolved)
    log_entry = {
        "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "action": action,
        "profile": resolved.name,
        "warning_rule_ids": sorted({warning["rule_id"] for warning in warnings or []}),
    }
    with (dirs["logs"] / "profile_changes.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(log_entry, sort_keys=True) + "\n")
