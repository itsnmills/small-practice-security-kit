from __future__ import annotations

import argparse
import sys
import webbrowser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from small_practice_security_kit.dashboard import build_dashboard
from small_practice_security_kit.local_api import AppState, LocalIntakeServer, make_handler
from small_practice_security_kit.packet import build_packet


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build and serve the local Small Practice Security Kit intake workspace.")
    parser.add_argument("--profile", default="samples/family_dental_clinic.yaml", help="Practice profile YAML to open.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind. Default: 127.0.0.1")
    parser.add_argument("--port", type=int, default=8765, help="Port to bind. Default: 8765")
    parser.add_argument("--no-open", action="store_true", help="Do not open the browser automatically.")
    parser.add_argument("--build-only", action="store_true", help="Build dashboard files without starting the local server.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    profile_path = Path(args.profile)
    if not profile_path.is_absolute():
        profile_path = ROOT / profile_path
    if not profile_path.exists():
        print(f"Profile not found: {profile_path}", file=sys.stderr)
        return 1

    out_dir = build_packet(profile_path)
    dashboard_path = build_dashboard(profile_path, out_dir)
    print(f"Built dashboard: {dashboard_path}")

    if args.build_only:
        return 0

    state = AppState(profile_path=profile_path, out_dir=out_dir, host=args.host)
    server = LocalIntakeServer((args.host, args.port), make_handler(state))
    url = f"http://{args.host}:{args.port}/"
    dashboard_url = f"http://{args.host}:{args.port}/dashboard.html"
    print(f"Intake workspace running at {url}")
    print(f"Dashboard available at {dashboard_url}")
    print("Press Ctrl+C to stop.")
    if not args.no_open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
