from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from small_practice_security_kit.adapters.ephi_mapper import import_flows


def main() -> int:
    parser = argparse.ArgumentParser(description="Import ePHI flow rows into a practice profile.")
    parser.add_argument("csv")
    parser.add_argument("--base", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--append", action="store_true")
    args = parser.parse_args()
    out = import_flows(Path(args.csv), Path(args.base), Path(args.output), append=args.append)
    print(f"Imported ePHI flows into {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
