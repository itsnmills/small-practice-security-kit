from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from small_practice_security_kit.packet import build_packet


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/build.py samples/family_dental_clinic.yaml")
        return 1
    out_dir = build_packet(Path(sys.argv[1]))
    print(f"Built review packet in {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
