from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from small_practice_security_kit.safety import assert_safe_tree


ROOT = Path(__file__).resolve().parents[1]


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
    for path in [ROOT / "samples", ROOT / "out", ROOT / "examples"]:
        assert_safe_tree(path)
    print("Content validation passed")


if __name__ == "__main__":
    main()
