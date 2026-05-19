from __future__ import annotations

import re
import urllib.error
import urllib.request
from typing import Any, Callable

from .base import build_bundle, make_evidence_item, utc_now


FetchResult = tuple[int, str]
PublicPageFetcher = Callable[[str], FetchResult]

PUBLIC_VENDOR_PATHS = ["/", "/security", "/privacy", "/hipaa", "/trust", "/subprocessors", "/terms"]

TERM_GROUPS = {
    "security_terms": ["security", "soc 2", "soc2", "hitrust", "iso 27001", "encryption"],
    "hipaa_baa_terms": ["hipaa", "business associate", "baa"],
    "ai_data_terms": ["artificial intelligence", "machine learning", "model training", "customer data", "data use"],
    "subprocessor_terms": ["subprocessor", "sub-processors", "subprocessors"],
    "incident_terms": ["security incident", "breach notification", "incident response"],
}


def _clean_domain(domain: str) -> str:
    clean = domain.strip().lower().rstrip(".")
    if not re.fullmatch(r"[a-z0-9][a-z0-9.-]*[a-z0-9]", clean) or ".." in clean:
        raise ValueError("domain must be a bare public DNS name, for example abridge.com")
    return clean


def _default_fetcher(url: str) -> FetchResult:
    request = urllib.request.Request(url, headers={"User-Agent": "VelariSecurityKit/0.1 metadata-only"})
    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            status = int(getattr(response, "status", 200))
            body = response.read(64_000).decode("utf-8", errors="ignore")
            return status, body
    except urllib.error.HTTPError as exc:
        body = exc.read(8_000).decode("utf-8", errors="ignore")
        return int(exc.code), body


def _term_hits(text: str) -> dict[str, bool]:
    lowered = text.lower()
    return {group: any(term in lowered for term in terms) for group, terms in TERM_GROUPS.items()}


def collect_vendor_public(
    vendor: str,
    domain: str,
    *,
    generated_at: str | None = None,
    fetcher: PublicPageFetcher | None = None,
) -> dict[str, Any]:
    collected_at = generated_at or utc_now()
    clean_vendor = vendor.strip()
    if not clean_vendor:
        raise ValueError("vendor is required")
    clean_domain = _clean_domain(domain)
    fetch = fetcher or _default_fetcher

    reachable_paths: list[str] = []
    warnings: list[str] = []
    aggregate_hits = {group: False for group in TERM_GROUPS}
    for path in PUBLIC_VENDOR_PATHS:
        url = f"https://{clean_domain}{path}"
        try:
            status, text = fetch(url)
        except (OSError, TimeoutError, ValueError, urllib.error.URLError):
            warnings.append(f"Could not reach public vendor path {path}.")
            continue
        if 200 <= status < 400 and text:
            reachable_paths.append(path)
            for group, found in _term_hits(text).items():
                aggregate_hits[group] = aggregate_hits[group] or found
        elif status in {401, 403}:
            warnings.append(f"Public vendor path {path} requires review because it returned {status}.")

    missing_review_signals = [label for label, found in aggregate_hits.items() if not found]
    if not reachable_paths:
        status = "requested"
        priority = "high"
        summary = (
            f"No standard public evidence pages were reachable for {clean_vendor} at {clean_domain}. "
            "Treat this as a request for vendor-owner follow-up, not a compliance conclusion."
        )
    else:
        status = "needs_review"
        priority = "high" if "hipaa_baa_terms" in missing_review_signals else "medium"
        found_labels = ", ".join(label.replace("_", " ") for label, found in aggregate_hits.items() if found) or "no standard review terms"
        summary = (
            f"Public vendor review for {clean_vendor} found {len(reachable_paths)} reachable standard page(s) "
            f"and these review signals: {found_labels}. Public pages are triage evidence only."
        )

    observations = {
        "vendor": clean_vendor,
        "domain": clean_domain,
        "pages_checked": PUBLIC_VENDOR_PATHS,
        "reachable_page_count": len(reachable_paths),
        "reachable_pages": reachable_paths,
        "security_terms_found": aggregate_hits["security_terms"],
        "hipaa_baa_terms_found": aggregate_hits["hipaa_baa_terms"],
        "ai_data_terms_found": aggregate_hits["ai_data_terms"],
        "subprocessor_terms_found": aggregate_hits["subprocessor_terms"],
        "incident_terms_found": aggregate_hits["incident_terms"],
        "missing_review_signals": missing_review_signals,
        "raw_page_text_stored": False,
    }

    evidence = [
        make_evidence_item(
            evidence_id="CONN-VENDOR-PUBLIC-001",
            title=f"{clean_vendor} public vendor evidence triage",
            source_system="vendor_public_web",
            source_type="public_lookup",
            collected_at=collected_at,
            control_area="vendor_baa_ai",
            subject="public_vendor_evidence",
            summary=summary,
            status=status,
            confidence="observed_from_public_web" if reachable_paths else "unknown",
            owner_lane="vendor",
            recommended_question=(
                "Can the vendor owner confirm BAA status, security-review evidence, incident notice terms, "
                "subprocessors, retention/deletion handling, and whether customer data is used for AI or model training?"
            ),
            acceptable_evidence=[
                "vendor security or trust page snapshot",
                "vendor BAA status confirmation from qualified reviewer",
                "AI/customer-data-use response",
                "subprocessor list or vendor response",
                "incident notice terms summary",
                "vendor owner signoff",
            ],
            next_action=(
                "Route the public vendor triage to the vendor owner and qualified reviewer; request missing answers "
                "without uploading raw contracts or patient examples."
            ),
            stage_id="vendor_baa_review",
            priority=priority,
            counts={
                "pages_checked": len(PUBLIC_VENDOR_PATHS),
                "reachable_pages": len(reachable_paths),
                "missing_review_signals": len(missing_review_signals),
            },
            observations=observations,
            unsafe_fields_excluded=[
                "raw contracts",
                "patient examples",
                "credentials",
                "private vendor portal URLs",
                "raw public page text",
                "incident-sensitive details",
            ],
            source_refs=[f"{clean_domain} public web paths"],
        )
    ]
    return build_bundle(
        connector="vendor_public_web",
        mode="public_vendor_metadata",
        input_ref=clean_domain,
        evidence=evidence,
        generated_at=collected_at,
        warnings=warnings,
    )
