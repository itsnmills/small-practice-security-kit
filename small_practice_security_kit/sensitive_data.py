from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SensitiveFinding:
    rule_id: str
    severity: str
    path: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "path": self.path,
            "message": self.message,
        }


RULES = [
    ("ssn", "high", re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "Looks like an SSN."),
    ("private_key", "high", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "Looks like a private key."),
    ("api_key", "high", re.compile(r"\b(sk-[A-Za-z0-9_-]{20,}|xox[baprs]-[A-Za-z0-9-]{20,}|ghp_[A-Za-z0-9]{20,})\b"), "Looks like an API token."),
    ("credit_card", "high", re.compile(r"\b(?:\d[ -]*?){13,16}\b"), "Looks like a payment card number."),
    ("password_field", "high", re.compile(r"(?i)\b(password|passcode|mfa code|recovery code)\b\s*[:=]"), "Looks like a credential."),
    ("mrn_label", "high", re.compile(r"(?i)\b(MRN|medical record number|patient id)\b[\s_:-]*[A-Za-z0-9-]{4,}"), "Looks like a patient identifier."),
    ("dob_label", "high", re.compile(r"(?i)\b(DOB|date of birth)\b\s*[:=]?\s*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"), "Looks like a date of birth."),
    ("patient_name_label", "medium", re.compile(r"(?i)(?:\bpatient\s+name\b\s*[:=]?\s*[A-Z][A-Za-z]+|\bpatient\b\s*[:=]\s*[A-Z][A-Za-z]+)"), "Looks like a patient name label."),
    ("email_address", "high", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "Contains an email address. Use role contacts or non-sensitive references."),
    ("private_url", "high", re.compile(r"(?i)https?://[^\s]+(?:token=|secret=|signature=|X-Amz-Signature|sig=|key=|password=|passcode=|presigned|private)[^\s]*"), "Looks like a private or signed URL."),
    ("bearer_or_basic_auth", "high", re.compile(r"(?i)\b(authorization:\s*)?(bearer|basic)\s+[A-Za-z0-9._~+/=-]{12,}"), "Looks like an authorization credential."),
]

CLINICAL_TERMS = re.compile(
    r"(?i)\b(diagnosis|diagnosed|medication|prescription|chief complaint|assessment|treatment plan|symptoms|blood pressure|lab result|visit note|encounter)\b"
)


def _walk(value: Any, path: str = "") -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            items.extend(_walk(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            items.extend(_walk(child, f"{path}[{index}]"))
    elif isinstance(value, str):
        items.append((path, value))
    return items


def find_sensitive_data(value: Any) -> list[SensitiveFinding]:
    findings: list[SensitiveFinding] = []
    for path, text in _walk(value):
        for rule_id, severity, pattern, message in RULES:
            if pattern.search(text):
                findings.append(SensitiveFinding(rule_id, severity, path, message))
        if len(text) > 220 and CLINICAL_TERMS.search(text):
            findings.append(
                SensitiveFinding(
                    "long_clinical_text",
                    "high",
                    path,
                    "Looks like pasted clinical text. Store a reference, not the contents.",
                )
            )
    return findings


def blocking_findings(value: Any) -> list[SensitiveFinding]:
    return [finding for finding in find_sensitive_data(value) if finding.severity == "high"]
