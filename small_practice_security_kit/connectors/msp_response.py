from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .base import build_bundle, make_evidence_item, utc_now


SAFE_STATUSES = {"provided", "needs_followup", "not_applicable", "scheduled", "exception_requested"}


def collect_msp_response(response_path: Path, *, generated_at: str | None = None) -> dict[str, Any]:
    collected_at = generated_at or utc_now()
    payload = yaml.safe_load(response_path.read_text(encoding="utf-8")) or {}
    responses = payload.get("responses", [])
    if not isinstance(responses, list):
        raise ValueError("MSP response file must contain a responses list.")
    evidence = []
    for index, response in enumerate(responses, start=1):
        if not isinstance(response, dict):
            raise ValueError("Each MSP response must be an object.")
        source_id = str(response.get("evidence_id") or f"MSP-RESPONSE-{index:03d}")
        status_label = str(response.get("status") or "needs_followup")
        if status_label not in SAFE_STATUSES:
            raise ValueError(f"Unsupported MSP response status '{status_label}'.")
        provided = status_label in {"provided", "not_applicable"}
        title = str(response.get("title") or f"MSP response for {source_id}")
        reference = str(response.get("reference") or "MSP response reference")
        owner = str(response.get("owner") or "msp")
        evidence.append(
            make_evidence_item(
                evidence_id=f"CONN-MSP-RESPONSE-{index:03d}",
                title=title,
                source_system="msp_response",
                source_type="msp_response",
                collected_at=collected_at,
                control_area=str(response.get("control_area") or "msp_evidence_response"),
                subject=source_id,
                summary=f"MSP response status for {source_id}: {status_label}. Reference captured without raw logs or private URLs.",
                status="observed" if provided else "needs_review",
                confidence="imported_from_msp_response",
                owner_lane=owner if owner in {"owner", "office_manager", "msp", "vendor", "legal_compliance"} else "msp",
                recommended_question=str(response.get("recommended_question") or "Can the MSP confirm scope, date observed, exceptions, and next due date?"),
                acceptable_evidence=list(response.get("acceptable_evidence") or ["ticket/reference ID", "date observed", "scope covered", "reviewer/contact", "exceptions and due dates"]),
                next_action=str(response.get("next_action") or "Review the MSP response, close supported evidence gaps, and route exceptions to the owner."),
                stage_id=str(response.get("stage_id") or "owner_msp_handoff"),
                priority=str(response.get("priority") or ("low" if provided else "medium")),
                observations={
                    "source_evidence_id": source_id,
                    "msp_status": status_label,
                    "reference": reference,
                    "scope": str(response.get("scope") or "not provided"),
                    "date_observed": str(response.get("date_observed") or collected_at[:10]),
                    "raw_logs_stored": False,
                    "private_urls_stored": False,
                },
                unsafe_fields_excluded=["PHI", "credentials", "private admin URLs", "raw logs", "patient screenshots", "raw contracts"],
                source_refs=[reference],
            )
        )
    return build_bundle(
        connector="msp_response_import",
        mode="msp_response_metadata_import",
        input_ref=response_path.name,
        evidence=evidence,
        generated_at=collected_at,
    )

