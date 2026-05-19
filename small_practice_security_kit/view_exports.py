from __future__ import annotations

import csv
import tempfile
from pathlib import Path
from typing import Any

from .sprint import build_sprint


LANES = {
    "owner": "Owner View",
    "msp": "MSP View",
    "vendor": "Vendor View",
    "legal_compliance": "Reviewer View",
}


def _read_risks(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _row_for_lane(row: dict[str, str], lane: str) -> bool:
    if lane == "legal_compliance":
        return bool(row.get("legal_compliance_view")) or row.get("owner_lane") == "legal_compliance"
    return row.get("owner_lane") == lane or bool(row.get(f"{lane}_view"))


def _render_lane(label: str, rows: list[dict[str, str]], lane: str) -> str:
    lines = [
        f"# {label}",
        "",
        "This is a readiness and evidence handoff view. It does not provide legal, compliance, breach, insurance, or HIPAA certification conclusions.",
        "",
        "| Priority | Finding | Question | Acceptable evidence | Do not send | Next action |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        view = row.get(f"{lane}_view") or row.get("plain_english_summary") or ""
        lines.append(
            f"| {row.get('priority','')} | {view} | {row.get('recommended_question','')} | {row.get('acceptable_evidence','')} | {row.get('unsafe_inputs','')} | {row.get('next_action','')} |"
        )
    if not rows:
        lines.append("| low | No open lane-specific actions generated. | Confirm whether any new evidence has been added. | evidence reference | PHI; credentials; private URLs; raw logs | Refresh connector evidence quarterly. |")
    return "\n".join(lines) + "\n"


def export_practice_views(profile_path: Path, output_dir: Path, *, evidence_paths: list[Path] | None = None) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temp:
        sprint_dir = build_sprint(profile_path, Path(temp), evidence_paths=evidence_paths or []).output_dir
        rows = _read_risks(sprint_dir / "risk-register.csv")
    written: list[Path] = []
    for lane, label in LANES.items():
        lane_rows = [row for row in rows if _row_for_lane(row, lane)]
        path = output_dir / f"{lane.replace('_', '-')}-view.md"
        path.write_text(_render_lane(label, lane_rows, lane), encoding="utf-8", newline="\n")
        written.append(path)
    return written

