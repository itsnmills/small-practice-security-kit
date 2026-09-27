from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .validation import validate_profile


ROOT = Path(__file__).resolve().parent.parent
PROFILES = ROOT / "profiles"


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


class WorkspaceError(ValueError):
    pass


def ensure_workspace_dirs(root: Path = ROOT) -> dict[str, Path]:
    base = root.resolve()
    dirs = {
        "profiles": base / "profiles",
        "backups": base / "profiles" / ".backups",
        "logs": base / "profiles" / ".logs",
    }
    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)
    return dirs


def safe_profile_path(practice_name: str, root: Path = ROOT) -> Path:
    clean = "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in practice_name.strip().lower())
    clean = clean.strip("_") or "practice_profile"
    dirs = ensure_workspace_dirs(root)
    resolved = (dirs["profiles"] / f"{clean}.yaml").resolve()
    profiles_root = dirs["profiles"].resolve()
    if profiles_root not in resolved.parents:
        raise WorkspaceError("Invalid practice name caused directory escape")
    return resolved


def atomic_write_profile(
    profile: dict[str, Any],
    path: Path,
    root: Path = ROOT,
    action: str = "save",
    warnings: list[dict[str, str]] | None = None,
) -> None:
    validate_profile(profile)
    dirs = ensure_workspace_dirs(root)
    resolved = path.resolve()
    profiles_root = dirs["profiles"].resolve()
    if profiles_root not in resolved.parents:
        raise WorkspaceError("Refusing to write profile outside profiles directory")
    if resolved.exists():
        backup = dirs["backups"] / f"{resolved.stem}-{utc_stamp()}.yaml"
        backup.write_text(resolved.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    profile.setdefault("workspace", {})["updated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    tmp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            dir=resolved.parent,
            prefix=f".{resolved.stem}-",
            suffix=".tmp",
            delete=False,
            encoding="utf-8",
            newline="\n",
        ) as tmp:
            tmp_path = Path(tmp.name)
            yaml.safe_dump(profile, tmp, sort_keys=False)
        os.replace(tmp_path, resolved)
    except BaseException:
        # Security decision: never leave a plaintext profile in a stray tmp file.
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)
        raise
    log_entry = {
        "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "action": action,
        "profile": resolved.name,
        "warning_rule_ids": sorted({warning["rule_id"] for warning in warnings or []}),
    }
    log_path = dirs["logs"] / "profile_changes.jsonl"
    with log_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(log_entry) + "\n")
