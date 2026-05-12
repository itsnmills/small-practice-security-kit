from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from small_practice_security_kit.adapters.evidence_binder import export_binder_index


def main() -> int:
    parser = argparse.ArgumentParser(description="Export evidence needs for hipaa-evidence-binder-template.")
    parser.add_argument("profile")
    parser.add_argument("--output")
    args = parser.parse_args()
    out = export_binder_index(Path(args.profile), Path(args.output) if args.output else None)
    print(f"Exported evidence binder index to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
