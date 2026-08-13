from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from .sensitive_data import blocking_findings, find_sensitive_data
from .workspaces import ROOT

EVIDENCE_ROOT_NAMES = ("out", "profiles", "examples", "samples")

ALLOWED_SUFFIXES = {
    ".csv",
    ".docx",
    ".html",
    ".jpeg",
    ".jpg",
    ".md",
    ".pdf",
    ".png",
    ".txt",
    ".xlsx",
    ".yaml",
    ".yml",
}


class FileInventoryError(ValueError):
    pass


def default_evidence_roots(*extra: Path) -> list[Path]:
    roots = [ROOT.resolve()]
    for name in EVIDENCE_ROOT_NAMES:
        roots.append((ROOT / name).resolve())
    for item in extra:
        roots.append(Path(item).expanduser().resolve())
    unique: list[Path] = []
    seen: set[Path] = set()
    for root in roots:
        if root not in seen:
            seen.add(root)
            unique.append(root)
    return unique


def _has_parent_segment(path: Path) -> bool:
    return ".." in path.expanduser().parts


def path_is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def resolve_allowed_path(raw: str | Path, allowed_roots: Sequence[Path]) -> Path:
    given = Path(raw).expanduser()
    if _has_parent_segment(given):
        raise FileInventoryError("Path must not contain parent-directory segments.")
    candidate = given if given.is_absolute() else (ROOT / given)
    resolved = candidate.resolve()
    if not any(path_is_within(resolved, root) for root in allowed_roots):
        raise FileInventoryError("Path is outside the allowed workspace or evidence root.")
    return resolved


def inventory_folder(path: Path, *, max_files: int = 300, allowed_roots: Sequence[Path] | None = None) -> dict[str, Any]:
    given = path.expanduser()
    if _has_parent_segment(given):
        raise FileInventoryError("Path must not contain parent-directory segments.")
    root = resolve_allowed_path(given, allowed_roots) if allowed_roots is not None else given.resolve()
    if not root.exists() or not root.is_dir():
        raise FileInventoryError("Evidence folder does not exist or is not a directory.")
    evidence = []
    skipped = []
    for file_path in sorted(root.rglob("*")):
        if len(evidence) >= max_files:
            skipped.append({"path": str(root), "reason": "max file limit reached"})
            break
        if any(part.startswith(".") for part in file_path.relative_to(root).parts):
            continue
        if not file_path.is_file():
            continue
        try:
            file_path.resolve().relative_to(root)
        except ValueError:
            skipped.append({"path": str(file_path.relative_to(root)), "reason": "outside inventory root"})
            continue
        suffix = file_path.suffix.lower()
        if suffix not in ALLOWED_SUFFIXES:
            skipped.append({"path": str(file_path), "reason": "unsupported extension"})
            continue
        relative = file_path.relative_to(root)
        item = {
            "id": f"EVID-FILE-{len(evidence) + 1:03d}",
            "title": relative.stem.replace("_", " ").replace("-", " ").title(),
            "type": "admin_settings_export",
            "area": "Imported evidence reference",
            "owner": "Security Owner",
            "reference": str(relative),
            "status": "requested",
            "related": "",
            "stores_sensitive_content": False,
            "notes": f"Metadata-only import from {root.name}; content was not read.",
            "metadata": {
                "extension": suffix,
                "size_bytes": file_path.stat().st_size,
                "modified_epoch": int(file_path.stat().st_mtime),
            },
        }
        blocked = blocking_findings({"title": item["title"], "reference": item["reference"]})
        if blocked:
            skipped.append({"path": str(relative), "reason": "sensitive-looking filename", "rule_ids": [finding.rule_id for finding in blocked]})
            continue
        evidence.append(item)
    warnings = [finding.to_dict() for finding in find_sensitive_data(evidence)]
    return {"root": str(root), "evidence": evidence, "skipped": skipped, "warnings": warnings}
