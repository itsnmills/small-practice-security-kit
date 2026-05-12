from __future__ import annotations

import html
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out"


def load_profile(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def slugify(name: str) -> str:
    return "".join(char.lower() if char.isalnum() else "_" for char in name).strip("_")


def yn(value: bool) -> str:
    return "Yes" if value else "No"


def risk_level(profile: dict) -> tuple[str, list[str]]:
    readiness = profile["readiness"]
    gaps = []
    if not readiness["mfa_ehr"]:
        gaps.append("Enable MFA for EHR access.")
    if not readiness["quarterly_access_review"]:
        gaps.append("Run and record a quarterly access review.")
    if not readiness["tested_backups"]:
        gaps.append("Run a restore test and record evidence.")
    if not readiness["baa_register"]:
        gaps.append("Complete the BAA register and review dates.")
    if not readiness["downtime_plan"]:
        gaps.append("Document downtime procedures for critical systems.")
    if not readiness["log_review_cadence"]:
        gaps.append("Set a monthly log review cadence.")
    if len(gaps) >= 5:
        return "High", gaps
    if len(gaps) >= 3:
        return "Medium", gaps
    return "Low", gaps


def table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def readiness_review(profile: dict) -> str:
    risk, gaps = risk_level(profile)
    readiness = profile["readiness"]
    rows = [
        ["Email MFA", yn(readiness["mfa_email"]), "Access"],
        ["EHR MFA", yn(readiness["mfa_ehr"]), "Access"],
        ["Unique accounts", yn(readiness["unique_accounts"]), "Access"],
        ["Quarterly access review", yn(readiness["quarterly_access_review"]), "Evidence"],
        ["Tested backups", yn(readiness["tested_backups"]), "Resilience"],
        ["Vendor inventory", yn(readiness["vendor_inventory"]), "Vendor"],
        ["BAA register", yn(readiness["baa_register"]), "Vendor"],
        ["Incident contact list", yn(readiness["incident_contact_list"]), "Incident"],
        ["Downtime plan", yn(readiness["downtime_plan"]), "Resilience"],
        ["Training current", yn(readiness["security_training_current"]), "Workforce"],
        ["Log review cadence", yn(readiness["log_review_cadence"]), "Monitoring"],
    ]
    return f"""# Readiness Review

Practice: {profile['practice']['name']}

Overall initial risk: **{risk}**

{table(['Item', 'Ready?', 'Area'], rows)}

## Priority Gaps

{chr(10).join(f'- {gap}' for gap in gaps) if gaps else '- No priority gaps found.'}
"""


def ephi_flow_map(profile: dict) -> str:
    system_rows = [
        [s["name"], s["category"], s["ephi_role"], s["vendor"], s["evidence_needed"]]
        for s in profile["systems"]
    ]
    flow_rows = [
        [f["id"], f["source"], f["destination"], f["vendor"], f["ephi_type"], yn(f["baa_needed"]), f["risk"], f["evidence_needed"]]
        for f in profile["flows"]
    ]
    return f"""# ePHI Flow Map

## Systems

{table(['System', 'Category', 'ePHI Role', 'Vendor', 'Evidence Needed'], system_rows)}

## Flows

{table(['Flow', 'Source', 'Destination', 'Vendor', 'ePHI Type', 'BAA Needed', 'Risk', 'Evidence Needed'], flow_rows)}
"""


def vendor_review(profile: dict) -> str:
    rows = [
        [v["name"], v["service"], yn(v["touches_ephi"]), v["baa_status"], v["ai_training_use"], v["subcontractors_known"], v["incident_notification_terms"], v["risk"]]
        for v in profile["vendors"]
    ]
    return f"""# Vendor and BAA Review

{table(['Vendor', 'Service', 'Touches ePHI?', 'BAA Status', 'AI Training Use', 'Subcontractors', 'Incident Terms', 'Risk'], rows)}

## Next Evidence

- Confirm BAA review date for each vendor touching ePHI.
- Record incident notification terms.
- Ask AI/data-use questions for any vendor using automation or model training.
"""


def ai_review(profile: dict) -> str:
    rows = [
        [w["name"], w["proposed_use"], w["data_used"], w["vendor"], w["decision"], w["evidence_needed"]]
        for w in profile["ai_workflows"]
    ]
    return f"""# AI Workflow Review

{table(['Workflow', 'Use', 'Data Used', 'Vendor', 'Decision', 'Evidence Needed'], rows)}

## Rules of Thumb

- Allowed: generic administrative drafting with no patient or clinical details.
- Restricted: workflows involving claim, treatment, billing, or operationally sensitive data.
- Prohibited: pasting patient-level notes or identifiers into tools without approved safeguards and a reviewed vendor relationship.
"""


def downtime_packet(profile: dict) -> str:
    downtime = profile["downtime"]
    rows = [[system, "Needs downtime owner", "Needs restore or manual workaround evidence"] for system in downtime["critical_systems"]]
    return f"""# Downtime and Ransomware Tabletop

Downtime plan status: **{downtime['downtime_plan_status']}**

Restore test status: **{downtime['last_restore_test'] or 'not recorded'}**

Tabletop status: **{downtime['tabletop_status']}**

{table(['Critical System', 'Downtime Owner', 'Evidence Needed'], rows)}

## Tabletop Scenario

Run a 30-minute walkthrough: EHR unavailable at 8:30 AM, phones are working, billing portal is delayed, and staff need to continue patient care safely.
"""


def evidence_index(profile: dict) -> str:
    rows = []
    for flow in profile["flows"]:
        rows.append([flow["id"], "ePHI flow", flow["evidence_needed"], "03-hipaa-evidence-binder"])
    for vendor in profile["vendors"]:
        rows.append([vendor["name"], "Vendor/BAA", f"BAA, security contact, AI data-use review for {vendor['name']}", "04-vendor-baa-review"])
    rows.extend([
        ["ACCESS-QTR", "Access", "Quarterly access review for EHR, billing, email, remote access", "03-hipaa-evidence-binder"],
        ["BACKUP-RESTORE", "Backup", "Restore test record for EHR, billing, shared drive, key workstation", "06-downtime-ransomware-tabletop"],
        ["AI-POLICY", "AI workflow", "Allowed/prohibited AI use guidance and staff acknowledgement", "05-ai-workflow-review"],
    ])
    return f"""# Evidence Binder Index

{table(['Evidence ID', 'Area', 'Evidence Needed', 'Module'], rows)}
"""


def roadmap(profile: dict) -> str:
    risk, gaps = risk_level(profile)
    thirty = gaps[:3] or ["Review generated packet with practice owner and MSP."]
    sixty = gaps[3:6] or ["Validate evidence references and update vendor review dates."]
    ninety = [
        "Run a tabletop exercise and record lessons learned.",
        "Repeat access/vendor/backup evidence review.",
        "Prepare management signoff packet.",
    ]
    return f"""# 30-60-90 Roadmap

Initial risk level: **{risk}**

## First 30 Days

{chr(10).join(f'- {item}' for item in thirty)}

## Days 31-60

{chr(10).join(f'- {item}' for item in sixty)}

## Days 61-90

{chr(10).join(f'- {item}' for item in ninety)}
"""


def render_html(markdown: str) -> str:
    body = "\n".join(
        f"<h1>{html.escape(line[2:])}</h1>" if line.startswith("# ") else
        f"<h2>{html.escape(line[3:])}</h2>" if line.startswith("## ") else
        f"<p>{html.escape(line)}</p>" if line.strip() else ""
        for line in markdown.splitlines()
    )
    return f"<!doctype html><html><head><meta charset='utf-8'><title>Review Packet</title><style>body{{font-family:Arial,sans-serif;max-width:960px;margin:40px auto;line-height:1.5}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:6px}}</style></head><body>{body}</body></html>"


def build(profile_path: Path) -> Path:
    profile = load_profile(profile_path)
    out_dir = OUT / slugify(profile["practice"]["name"])
    out_dir.mkdir(parents=True, exist_ok=True)
    docs = {
        "readiness-review.md": readiness_review(profile),
        "ephi-flow-map.md": ephi_flow_map(profile),
        "vendor-baa-review.md": vendor_review(profile),
        "ai-workflow-review.md": ai_review(profile),
        "downtime-ransomware-tabletop.md": downtime_packet(profile),
        "evidence-binder-index.md": evidence_index(profile),
        "30-60-90-roadmap.md": roadmap(profile),
    }
    for name, content in docs.items():
        (out_dir / name).write_text(content, encoding="utf-8", newline="\n")
    packet = "\n\n---\n\n".join(docs.values())
    (out_dir / "review-packet.md").write_text(packet, encoding="utf-8", newline="\n")
    (out_dir / "review-packet.html").write_text(render_html(packet), encoding="utf-8", newline="\n")
    return out_dir


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/build.py samples/family_dental_clinic.yaml")
        return 1
    out_dir = build(Path(sys.argv[1]))
    print(f"Built review packet in {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
