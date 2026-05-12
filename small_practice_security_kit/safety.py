from __future__ import annotations

import re
from pathlib import Path


SENSITIVE_PATTERNS = [
    re.compile(r"\bMRN\s*[:=]\s*[A-Za-z0-9-]{3,}", re.IGNORECASE),
    re.compile(r"\bPatient Name\s*[:=]\s*[A-Za-z][A-Za-z ,.'-]+", re.IGNORECASE),
    re.compile(r"\bDOB\s*[:=]\s*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", re.IGNORECASE),
    re.compile(r"\bdiagnosis\s*[:=]\s*[A-Za-z][A-Za-z ,.'-]+", re.IGNORECASE),
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    re.compile(r"\b(api[_ -]?key|password|token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{8,}", re.IGNORECASE),
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY-----"),
]

SAFE_SUFFIXES = {".md", ".yaml", ".yml", ".csv", ".json", ".html", ".txt"}


def find_sensitive_patterns(text: str) -> list[str]:
    findings: list[str] = []
    for pattern in SENSITIVE_PATTERNS:
        if pattern.search(text):
            findings.append(pattern.pattern)
    return findings


def scan_file(path: Path) -> list[str]:
    if path.suffix.lower() not in SAFE_SUFFIXES:
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    return [f"{path}: {pattern}" for pattern in find_sensitive_patterns(text)]


def scan_tree(path: Path) -> list[str]:
    if path.is_file():
        return scan_file(path)
    findings: list[str] = []
    if not path.exists():
        return findings
    for child in path.rglob("*"):
        if child.is_file():
            findings.extend(scan_file(child))
    return findings


def assert_safe_tree(path: Path) -> None:
    findings = scan_tree(path)
    if findings:
        raise ValueError("possible sensitive content found:\n" + "\n".join(findings))
