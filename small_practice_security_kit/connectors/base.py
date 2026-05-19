from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

from ..manifest import slug
from ..sensitive_data import blocking_findings


CONNECTOR_SCHEMA_VERSION = "2026-05-19"
CONNECTOR_VERSION = "0.1.0"
ROOT = Path(__file__).resolve().parents[2]
SAFETY_MANIFEST_PATH = ROOT / "catalogs" / "connector_safety_manifests.yaml"

DEFAULT_UNSAFE_INPUTS = [
    "PHI or patient identifiers",
    "credentials",
    "private admin URLs",
    "raw logs",
    "patient screenshots",
    "full private contracts",
    "mailbox or drive file contents",
    "incident-sensitive details",
]

STATUS_TO_EVIDENCE_INDEX = {
    "observed": "reviewed",
    "current": "reviewed",
    "missing": "missing",
    "stale": "outdated",
    "needs_review": "partial",
    "requested": "requested",
    "not_applicable": "not_applicable",
}

STATUS_TO_RISK_EVIDENCE = {
    "observed": "referenced",
    "current": "referenced",
    "missing": "missing",
    "stale": "stale",
    "needs_review": "requested",
    "requested": "requested",
    "not_applicable": "referenced",
}


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _date_plus(generated_at: str, days: int) -> str:
    observed = datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
    return (observed + timedelta(days=days)).date().isoformat()


def _safe_input_ref(path: Path | str) -> str:
    raw = Path(path)
    try:
        return raw.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return raw.name


def _load_safety_catalog(path: Path = SAFETY_MANIFEST_PATH) -> dict[str, dict[str, Any]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    connectors = data.get("connectors", []) if isinstance(data, dict) else []
    return {str(item["connector"]): dict(item) for item in connectors}


def safety_manifest(connector: str) -> dict[str, Any]:
    catalog = _load_safety_catalog()
    if connector in catalog:
        return catalog[connector]
    return {
        "connector": connector,
        "default_mode": "read_only_metadata",
        "phi_expected": False,
        "forbidden_data": DEFAULT_UNSAFE_INPUTS,
        "required_scopes": [],
        "unsafe_scopes": [],
        "human_approval_required_for": ["client exports", "vendor messages", "legal/compliance or insurance outputs"],
    }


def make_run(
    *,
    connector: str,
    mode: str,
    input_ref: str,
    generated_at: str | None = None,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    completed_at = generated_at or utc_now()
    return {
        "schema_version": CONNECTOR_SCHEMA_VERSION,
        "run_id": f"run_{slug(connector)}_{completed_at[:10].replace('-', '')}",
        "connector": connector,
        "connector_version": CONNECTOR_VERSION,
        "mode": mode,
        "started_at": completed_at,
        "completed_at": completed_at,
        "input_ref": input_ref,
        "status": "completed_with_warnings" if warnings else "completed",
        "warnings": warnings or [],
        "safety_manifest": safety_manifest(connector),
    }


def make_evidence_item(
    *,
    evidence_id: str,
    title: str,
    source_system: str,
    source_type: str,
    collected_at: str,
    control_area: str,
    subject: str,
    summary: str,
    status: str,
    confidence: str,
    owner_lane: str,
    recommended_question: str,
    acceptable_evidence: list[str],
    next_action: str,
    stage_id: str,
    priority: str,
    counts: dict[str, Any] | None = None,
    observations: dict[str, Any] | None = None,
    unsafe_fields_excluded: list[str] | None = None,
    unsafe_inputs: list[str] | None = None,
    source_refs: list[str] | None = None,
    notes: str = "",
) -> dict[str, Any]:
    resolved_observations = observations if observations is not None else counts or {}
    resolved_unsafe_excluded = unsafe_fields_excluded or DEFAULT_UNSAFE_INPUTS
    item = {
        "schema_version": CONNECTOR_SCHEMA_VERSION,
        "evidence_id": evidence_id,
        "title": title,
        "source_system": source_system,
        "source_type": source_type,
        "collected_at": collected_at,
        "phi_expected": False,
        "phi_status": "metadata_only_no_phi_expected",
        "control_area": control_area,
        "subject": subject,
        "summary": summary,
        "status": status,
        "confidence": confidence,
        "counts": counts or {},
        "observations": resolved_observations,
        "owner_lane": owner_lane,
        "recommended_question": recommended_question,
        "acceptable_evidence": acceptable_evidence,
        "unsafe_inputs": unsafe_inputs or DEFAULT_UNSAFE_INPUTS,
        "unsafe_fields_excluded": resolved_unsafe_excluded,
        "unsafe_inputs_excluded": resolved_unsafe_excluded,
        "next_action": next_action,
        "recommended_action": next_action,
        "stage_id": stage_id,
        "priority": priority,
        "source_refs": source_refs or [],
        "notes": notes,
    }
    findings = blocking_findings(item)
    if findings:
        joined = "; ".join(f"{finding.path}: {finding.message}" for finding in findings[:5])
        raise ValueError(f"connector evidence contains blocked sensitive data; aggregate or reference it instead ({joined})")
    return item


def build_bundle(
    *,
    connector: str,
    mode: str,
    input_ref: str,
    evidence: list[dict[str, Any]],
    generated_at: str | None = None,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    run = make_run(
        connector=connector,
        mode=mode,
        input_ref=input_ref,
        generated_at=generated_at,
        warnings=warnings,
    )
    run["evidence_count"] = len(evidence)
    return {
        "schema_version": CONNECTOR_SCHEMA_VERSION,
        "run": run,
        "evidence": evidence,
    }


def write_connector_bundle(bundle: dict[str, Any], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_path


def _load_bundle_file(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return build_bundle(
            connector="legacy_normalized_evidence",
            mode="imported_json",
            input_ref=_safe_input_ref(path),
            evidence=data,
            generated_at=utc_now(),
            warnings=["Imported legacy list of normalized evidence items."],
        )
    if not isinstance(data, dict) or "evidence" not in data:
        raise ValueError(f"connector evidence file must contain an evidence bundle: {path}")
    return data


def load_connector_bundles(paths: list[Path] | None) -> list[dict[str, Any]]:
    bundles: list[dict[str, Any]] = []
    for path in paths or []:
        if path.is_dir():
            for child in sorted(path.glob("*.json")):
                bundles.append(_load_bundle_file(child))
        else:
            bundles.append(_load_bundle_file(path))
    return bundles


def flatten_evidence(bundles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    for bundle in bundles:
        for item in bundle.get("evidence", []):
            evidence.append(dict(item))
    return evidence


def evidence_reference(item: dict[str, Any], generated_at: str) -> dict[str, Any]:
    return {
        "evidence_id": str(item["evidence_id"]),
        "title": str(item["title"]),
        "evidence_type": str(item.get("control_area", "connector_evidence")),
        "source_system": str(item.get("source_system", "connector")),
        "owner": str(item.get("owner_lane", "msp")),
        "status": STATUS_TO_EVIDENCE_INDEX.get(str(item.get("status", "requested")), "requested"),
        "date_observed": str(item.get("collected_at", generated_at))[:10],
        "next_review_date": _date_plus(str(item.get("collected_at", generated_at)), 30),
        "sensitivity_boundary": "reference_only_no_phi_no_secret",
        "artifact_refs": ["connector-evidence-summary.json", "evidence-index.json"],
        "notes": str(item.get("summary", "")),
    }


def summarize_connector_evidence(bundles: list[dict[str, Any]]) -> dict[str, Any]:
    evidence = flatten_evidence(bundles)
    by_connector: dict[str, int] = {}
    by_status: dict[str, int] = {}
    by_confidence: dict[str, int] = {}
    by_owner_lane: dict[str, int] = {}
    by_control_area: dict[str, int] = {}
    runs: list[dict[str, Any]] = []
    for bundle in bundles:
        run = bundle.get("run", {})
        connector = str(run.get("connector", "unknown"))
        by_connector[connector] = by_connector.get(connector, 0) + len(bundle.get("evidence", []))
        runs.append(
            {
                "run_id": str(run.get("run_id", "")),
                "connector": connector,
                "mode": str(run.get("mode", "")),
                "status": str(run.get("status", "")),
                "input_ref": str(run.get("input_ref", "")),
                "evidence_count": int(run.get("evidence_count", len(bundle.get("evidence", [])))),
                "phi_expected": bool(run.get("safety_manifest", {}).get("phi_expected", False)),
                "warnings": list(run.get("warnings", [])),
            }
        )
    for item in evidence:
        status = str(item.get("status", "requested"))
        confidence = str(item.get("confidence", "unknown"))
        owner_lane = str(item.get("owner_lane", "unknown"))
        control_area = str(item.get("control_area", "general"))
        by_status[status] = by_status.get(status, 0) + 1
        by_confidence[confidence] = by_confidence.get(confidence, 0) + 1
        by_owner_lane[owner_lane] = by_owner_lane.get(owner_lane, 0) + 1
        by_control_area[control_area] = by_control_area.get(control_area, 0) + 1
    return {
        "total_items": len(evidence),
        "runs": runs,
        "by_connector": dict(sorted(by_connector.items())),
        "by_status": dict(sorted(by_status.items())),
        "by_confidence": dict(sorted(by_confidence.items())),
        "by_owner_lane": dict(sorted(by_owner_lane.items())),
        "by_control_area": dict(sorted(by_control_area.items())),
        "needs_attention": sum(by_status.get(status, 0) for status in ["missing", "stale", "needs_review", "requested"]),
        "data_boundary": "metadata_only_no_phi_expected",
    }
