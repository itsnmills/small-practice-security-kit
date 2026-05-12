from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROHIBITED = [
    re.compile(r"\bMRN\s*[:=]", re.IGNORECASE),
    re.compile(r"\bPatient Name\s*[:=]", re.IGNORECASE),
    re.compile(r"\bDOB\s*[:=]", re.IGNORECASE),
    re.compile(r"\bapi[_ -]?key\s*[:=]", re.IGNORECASE),
    re.compile(r"-----BEGIN .*PRIVATE KEY-----"),
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def main() -> None:
    required = [
        ROOT / "README.md",
        ROOT / "samples" / "family_dental_clinic.yaml",
        ROOT / "scripts" / "build.py",
        ROOT / "out" / "family_dental_clinic" / "review-packet.md",
        ROOT / "out" / "family_dental_clinic" / "ephi-flow-map.md",
        ROOT / "out" / "family_dental_clinic" / "vendor-baa-review.md",
        ROOT / "out" / "family_dental_clinic" / "ai-workflow-review.md",
    ]
    for path in required:
        if not path.exists() or path.stat().st_size < 100:
            fail(f"missing or too small: {path}")
    for path in list((ROOT / "samples").rglob("*")) + list((ROOT / "out").rglob("*")):
        if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".csv", ".json", ".html"}:
            text = path.read_text(encoding="utf-8")
            for pattern in PROHIBITED:
                if pattern.search(text):
                    fail(f"possible sensitive pattern in {path}: {pattern.pattern}")
    print("Content validation passed")


if __name__ == "__main__":
    main()
