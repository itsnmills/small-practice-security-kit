from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .connectors.base import flatten_evidence, load_connector_bundles, utc_now


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _hash_observations(item: dict[str, Any]) -> str:
    payload = {
        "status": item.get("status"),
        "confidence": item.get("confidence"),
        "observations": item.get("observations") or item.get("counts") or {},
        "next_action": item.get("next_action"),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def build_refresh_report(
    current_paths: list[Path],
    *,
    previous_paths: list[Path] | None = None,
    stale_after_days: int = 90,
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated = generated_at or utc_now()
    current_items = flatten_evidence(load_connector_bundles(current_paths))
    previous_items = flatten_evidence(load_connector_bundles(previous_paths or []))
    previous_by_id = {str(item["evidence_id"]): item for item in previous_items}
    now = _parse_time(generated)
    rows = []
    for item in current_items:
        evidence_id = str(item["evidence_id"])
        collected_at = str(item.get("collected_at", generated))
        age_days = max(0, (now - _parse_time(collected_at)).days)
        previous = previous_by_id.get(evidence_id)
        change = "new" if not previous else "changed" if _hash_observations(previous) != _hash_observations(item) else "unchanged"
        freshness = "stale" if age_days > stale_after_days else "current"
        rows.append(
            {
                "evidence_id": evidence_id,
                "title": str(item.get("title", evidence_id)),
                "source_system": str(item.get("source_system", "")),
                "owner_lane": str(item.get("owner_lane", "")),
                "status": str(item.get("status", "")),
                "confidence": str(item.get("confidence", "")),
                "confidence_score": int(item.get("confidence_score", 0)),
                "collected_at": collected_at,
                "age_days": age_days,
                "freshness": freshness,
                "change": change,
                "next_action": str(item.get("next_action", "")),
            }
        )
    return {
        "schema_version": "2026-05-19",
        "generated_at": generated,
        "stale_after_days": stale_after_days,
        "total_items": len(rows),
        "stale_items": sum(1 for row in rows if row["freshness"] == "stale"),
        "changed_items": sum(1 for row in rows if row["change"] == "changed"),
        "new_items": sum(1 for row in rows if row["change"] == "new"),
        "removed_items": sorted(set(previous_by_id) - {str(item["evidence_id"]) for item in current_items}),
        "rows": rows,
        "data_boundary": "metadata_only_no_phi_expected",
    }


def write_refresh_report(report: dict[str, Any], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_path

