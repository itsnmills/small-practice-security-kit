from __future__ import annotations

from pathlib import Path
from typing import Any

from .sensitive_data import blocking_findings, find_sensitive_data


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


def inventory_folder(path: Path, *, max_files: int = 300) -> dict[str, Any]:
    root = path.expanduser().resolve()
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
