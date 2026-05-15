from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .adapters.evidence_binder import export_binder_index
from .demo_export import export_demo
from .packet import OUT, build_packet
from .profile import load_profile
from .sensitive_data import blocking_findings
from .validation import ValidationError


def _path(value: str) -> Path:
    return Path(value)


def validate_command(args: argparse.Namespace) -> int:
    profile = load_profile(args.profile)
    findings = blocking_findings(profile)
    if findings:
        joined = "; ".join(f"{finding.path}: {finding.message}" for finding in findings[:5])
        print(f"Sensitive data check failed: {joined}", file=sys.stderr)
        return 2
    print(f"Profile valid: {args.profile}")
    return 0


def build_command(args: argparse.Namespace) -> int:
    out_dir = build_packet(args.profile, args.output_root)
    print(f"Built review packet in {out_dir}")
    return 0


def export_binder_command(args: argparse.Namespace) -> int:
    out_dir = export_binder_index(args.profile, args.output)
    print(f"Exported evidence binder index to {out_dir}")
    return 0


def export_demo_command(args: argparse.Namespace) -> int:
    result = export_demo(
        args.profile,
        args.output,
        include_pdf=args.pdf,
        include_screenshot=not args.no_screenshot,
    )
    for warning in result.warnings:
        print(f"Warning: {warning}", file=sys.stderr)
    print(f"Exported public demo packet to {result.output_dir}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m small_practice_security_kit")
    subcommands = parser.add_subparsers(dest="command", required=True)

    validate = subcommands.add_parser("validate", help="Validate a practice profile schema and safety boundary.")
    validate.add_argument("profile", type=_path)
    validate.set_defaults(func=validate_command)

    build = subcommands.add_parser("build", help="Build a local review packet from a practice profile.")
    build.add_argument("profile", type=_path)
    build.add_argument("--output-root", type=_path, default=OUT)
    build.set_defaults(func=build_command)

    export_binder = subcommands.add_parser("export-binder", help="Export binder-compatible evidence index files.")
    export_binder.add_argument("profile", type=_path)
    export_binder.add_argument("--output", type=_path)
    export_binder.set_defaults(func=export_binder_command)

    export_demo_parser = subcommands.add_parser("export-demo", help="Export a safe public demo packet snapshot.")
    export_demo_parser.add_argument("--profile", type=_path, default=Path("samples/family_dental_clinic.yaml"))
    export_demo_parser.add_argument("--output", type=_path, default=Path("docs/demo"))
    export_demo_parser.add_argument("--pdf", action="store_true", help="Optionally render review-packet.pdf if Chrome/Chromium is installed.")
    export_demo_parser.add_argument("--no-screenshot", action="store_true", help="Skip optional Chrome/Chromium screenshot rendering.")
    export_demo_parser.set_defaults(func=export_demo_command)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
