from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, Callable

from .base import build_bundle, make_evidence_item, utc_now


RecordResolver = Callable[[str, str], list[str]]


def _dig_resolver(name: str, record_type: str) -> list[str]:
    command = ["dig", "+short", record_type, name]
    try:
        completed = subprocess.run(command, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=8)
    except (OSError, subprocess.TimeoutExpired):
        return []
    if completed.returncode != 0:
        return []
    return [line.strip().strip('"') for line in completed.stdout.splitlines() if line.strip()]


def _txt_contains(records: list[str], needle: str) -> bool:
    joined = " ".join(records).lower()
    return needle.lower() in joined


def _dmarc_policy(records: list[str]) -> str:
    joined = " ".join(records).lower()
    if "p=reject" in joined:
        return "reject"
    if "p=quarantine" in joined:
        return "quarantine"
    if "p=none" in joined:
        return "none"
    return "missing"


def collect_dns_email_auth(
    domain: str,
    *,
    generated_at: str | None = None,
    resolver: RecordResolver | None = None,
) -> dict[str, Any]:
    collected_at = generated_at or utc_now()
    resolve = resolver or _dig_resolver
    clean_domain = domain.strip().lower().rstrip(".")
    if not clean_domain or "/" in clean_domain or "@" in clean_domain:
        raise ValueError("domain must be a bare DNS name, for example exampleclinic.com")

    mx_records = resolve(clean_domain, "MX")
    txt_records = resolve(clean_domain, "TXT")
    dmarc_records = resolve(f"_dmarc.{clean_domain}", "TXT")
    dkim_selectors = ["google", "selector1", "selector2", "default", "k1"]
    dkim_hits = [selector for selector in dkim_selectors if resolve(f"{selector}._domainkey.{clean_domain}", "TXT")]
    has_spf = _txt_contains(txt_records, "v=spf1")
    policy = _dmarc_policy(dmarc_records)

    evidence: list[dict[str, Any]] = [
        make_evidence_item(
            evidence_id="CONN-DNS-MX-001",
            title="Mail exchanger record summary",
            source_system="dns",
            source_type="public_lookup",
            collected_at=collected_at,
            control_area="email_authentication",
            subject="mx_records",
            summary=f"{len(mx_records)} MX records observed for {clean_domain}. Record values are not included in owner-facing outputs.",
            status="observed" if mx_records else "missing",
            confidence="observed_from_public_dns",
            owner_lane="msp",
            recommended_question="Can the MSP confirm the practice's mail provider and whether email security controls match the production mail flow?",
            acceptable_evidence=["MX lookup date", "mail provider name", "email security gateway status", "owner/MSP confirmation"],
            next_action="Confirm the mail provider and email-security owner before relying on SPF, DKIM, or DMARC findings.",
            stage_id="access_offboarding_review",
            priority="medium" if not mx_records else "low",
            counts={"mx_record_count": len(mx_records)},
            unsafe_fields_excluded=["mailbox contents", "private mail routing consoles", "credentials", "raw message headers"],
        ),
        make_evidence_item(
            evidence_id="CONN-DNS-SPF-001",
            title="SPF record presence summary",
            source_system="dns",
            source_type="public_lookup",
            collected_at=collected_at,
            control_area="email_authentication",
            subject="spf_record",
            summary=f"SPF record {'observed' if has_spf else 'not observed'} for {clean_domain}.",
            status="observed" if has_spf else "missing",
            confidence="observed_from_public_dns",
            owner_lane="msp",
            recommended_question="Can the MSP confirm SPF includes only authorized senders for patient-facing and business email domains?",
            acceptable_evidence=["SPF lookup date", "authorized sender list", "email vendor list", "MSP confirmation"],
            next_action="Ask the MSP to confirm or remediate SPF for the production email domain.",
            stage_id="access_offboarding_review",
            priority="high" if not has_spf else "low",
            counts={"spf_record_present": int(has_spf)},
            unsafe_fields_excluded=["mailbox contents", "private DNS provider credentials", "raw email contents"],
        ),
        make_evidence_item(
            evidence_id="CONN-DNS-DMARC-001",
            title="DMARC policy summary",
            source_system="dns",
            source_type="public_lookup",
            collected_at=collected_at,
            control_area="email_authentication",
            subject="dmarc_policy",
            summary=f"DMARC policy for {clean_domain}: {policy}.",
            status="missing" if policy == "missing" else "needs_review" if policy == "none" else "observed",
            confidence="observed_from_public_dns",
            owner_lane="msp",
            recommended_question="Can the MSP confirm whether DMARC should move from monitoring to quarantine or reject after sender alignment is reviewed?",
            acceptable_evidence=["DMARC lookup date", "policy value", "aggregate report owner", "authorized sender review", "MSP confirmation"],
            next_action="Review DMARC posture with the MSP and document whether monitoring-only is intentional.",
            stage_id="access_offboarding_review",
            priority="high" if policy == "missing" else "medium" if policy == "none" else "low",
            counts={"dmarc_record_count": len(dmarc_records), "dmarc_monitoring_only": int(policy == "none")},
            unsafe_fields_excluded=["raw email contents", "mailbox contents", "private DNS provider credentials"],
        ),
        make_evidence_item(
            evidence_id="CONN-DNS-DKIM-001",
            title="DKIM selector check summary",
            source_system="dns",
            source_type="public_lookup",
            collected_at=collected_at,
            control_area="email_authentication",
            subject="dkim_selector_presence",
            summary=f"{len(dkim_hits)} common DKIM selectors responded for {clean_domain}. Absence of common selectors is not proof DKIM is disabled.",
            status="observed" if dkim_hits else "requested",
            confidence="observed_from_public_dns",
            owner_lane="msp",
            recommended_question="Can the MSP confirm the actual DKIM selector and signing status from the email admin console?",
            acceptable_evidence=["DKIM admin-console status", "selector name", "date observed", "MSP confirmation"],
            next_action="Ask the MSP to confirm DKIM signing in the mail admin console because selectors cannot always be discovered publicly.",
            stage_id="access_offboarding_review",
            priority="medium" if not dkim_hits else "low",
            counts={"common_dkim_selectors_found": len(dkim_hits)},
            unsafe_fields_excluded=["raw email contents", "mailbox contents", "private DNS provider credentials"],
        ),
    ]

    return build_bundle(
        connector="dns_email_auth",
        mode="public_dns_metadata",
        input_ref=clean_domain,
        evidence=evidence,
        generated_at=collected_at,
    )
