from __future__ import annotations

import html
import re
from pathlib import Path

from .profile import load_profile, slugify


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out"


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
    system_rows = [[s["name"], s["category"], s["ephi_role"], s["vendor"], s["evidence_needed"]] for s in profile["systems"]]
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
        [
            v["name"],
            v["service"],
            yn(v["touches_ephi"]),
            v["baa_status"],
            v["ai_training_use"],
            v["subcontractors_known"],
            v["incident_notification_terms"],
            v["risk"],
        ]
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
    rows = [[w["name"], w["proposed_use"], w["data_used"], w["vendor"], w["decision"], w["evidence_needed"]] for w in profile["ai_workflows"]]
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
    for evidence in profile.get("evidence", []):
        rows.append(
            [
                evidence.get("id", evidence.get("title", "Evidence")),
                evidence.get("area", evidence.get("type", "Evidence")),
                evidence.get("title", "Evidence reference") + (f" - {evidence.get('reference')}" if evidence.get("reference") else ""),
                "03-hipaa-evidence-binder",
            ]
        )
    for flow in profile["flows"]:
        rows.append([flow["id"], "ePHI flow", flow["evidence_needed"], "03-hipaa-evidence-binder"])
    for vendor in profile["vendors"]:
        rows.append([vendor["name"], "Vendor/BAA", f"BAA, security contact, AI data-use review for {vendor['name']}", "04-vendor-baa-review"])
    rows.extend(
        [
            ["ACCESS-QTR", "Access", "Quarterly access review for EHR, billing, email, remote access", "03-hipaa-evidence-binder"],
            ["BACKUP-RESTORE", "Backup", "Restore test record for EHR, billing, shared drive, key workstation", "06-downtime-ransomware-tabletop"],
            ["AI-POLICY", "AI workflow", "Allowed/prohibited AI use guidance and staff acknowledgement", "05-ai-workflow-review"],
        ]
    )
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


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    return re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", escaped)


def render_table(lines: list[str]) -> str:
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        tag = "th" if not rows else "td"
        rows.append("<tr>" + "".join(f"<{tag}>{inline_markdown(cell)}</{tag}>" for cell in cells) + f"</tr>")
    return "<div class='table-wrap'><table>" + "".join(rows) + "</table></div>"


def render_html(markdown: str, profile: dict) -> str:
    blocks: list[str] = []
    table_buffer: list[str] = []
    list_buffer: list[str] = []

    def flush_table() -> None:
        nonlocal table_buffer
        if table_buffer:
            blocks.append(render_table(table_buffer))
            table_buffer = []

    def flush_list() -> None:
        nonlocal list_buffer
        if list_buffer:
            blocks.append("<ul>" + "".join(f"<li>{inline_markdown(item)}</li>" for item in list_buffer) + "</ul>")
            list_buffer = []

    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            flush_list()
            table_buffer.append(stripped)
            continue
        flush_table()
        if stripped.startswith("- "):
            list_buffer.append(stripped[2:])
            continue
        flush_list()
        if not stripped:
            continue
        if stripped == "---":
            blocks.append("<hr>")
        elif stripped.startswith("# "):
            blocks.append(f"<section class='packet-section'><h1>{inline_markdown(stripped[2:])}</h1>")
        elif stripped.startswith("## "):
            blocks.append(f"<h2>{inline_markdown(stripped[3:])}</h2>")
        else:
            blocks.append(f"<p>{inline_markdown(stripped)}</p>")
    flush_table()
    flush_list()
    practice = profile["practice"]
    title = f"{practice['name']} Security Review Packet"
    body = "\n".join(blocks)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{ --ink: #17211b; --muted: #5b685f; --paper: #fbfaf6; --line: #cbd7cc; --accent: #0f6b57; --accent-soft: #e3f2eb; --warn: #9b4d13; --warn-soft: #fff0dd; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--paper); color: var(--ink); font-family: Georgia, "Times New Roman", serif; line-height: 1.55; }}
    .shell {{ max-width: 1120px; margin: 0 auto; padding: 32px 22px 56px; }}
    .cover {{ border-top: 8px solid var(--accent); padding: 28px 0 22px; display: grid; gap: 8px; }}
    .kicker {{ color: var(--accent); font-family: Arial, sans-serif; font-weight: 700; text-transform: uppercase; font-size: 12px; }}
    h1, h2 {{ line-height: 1.12; letter-spacing: 0; }}
    .cover h1 {{ font-size: clamp(34px, 5vw, 60px); margin: 0; max-width: 900px; }}
    .meta {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; margin-top: 18px; font-family: Arial, sans-serif; }}
    .meta div {{ border: 1px solid var(--line); padding: 10px; background: #fffdf8; }}
    .meta strong {{ display: block; font-size: 12px; color: var(--muted); margin-bottom: 3px; }}
    .notice {{ background: var(--warn-soft); border-left: 4px solid var(--warn); padding: 12px 14px; margin: 22px 0; font-family: Arial, sans-serif; font-size: 14px; }}
    .packet-section {{ display: block; padding: 24px 0 12px; border-top: 1px solid var(--line); }}
    .packet-section h1 {{ font-size: 30px; margin: 0 0 12px; }}
    h2 {{ font-size: 20px; margin: 22px 0 10px; color: var(--accent); }}
    p, li {{ font-size: 15px; }}
    .table-wrap {{ overflow-x: auto; margin: 12px 0 20px; border: 1px solid var(--line); background: white; }}
    table {{ width: 100%; border-collapse: collapse; min-width: 760px; font-family: Arial, sans-serif; font-size: 13px; }}
    th {{ text-align: left; background: var(--accent-soft); color: var(--ink); }}
    th, td {{ border-bottom: 1px solid var(--line); padding: 9px 10px; vertical-align: top; }}
    tr:last-child td {{ border-bottom: 0; }}
    hr {{ border: 0; border-top: 1px solid var(--line); margin: 28px 0; }}
    @media print {{ body {{ background: white; }} .shell {{ max-width: none; padding: 0.4in; }} .table-wrap {{ overflow: visible; }} table {{ min-width: 0; font-size: 10px; }} .packet-section {{ page-break-inside: avoid; }} }}
    @media (max-width: 760px) {{ .meta {{ grid-template-columns: 1fr; }} .cover h1 {{ font-size: 34px; }} }}
  </style>
</head>
<body>
  <main class="shell">
    <header class="cover">
      <div class="kicker">Small Practice Security Kit</div>
      <h1>{html.escape(title)}</h1>
      <div class="meta">
        <div><strong>Practice Type</strong>{html.escape(str(practice['type']))}</div>
        <div><strong>Review Period</strong>{html.escape(str(practice['review_period']))}</div>
        <div><strong>Security Owner</strong>{html.escape(str(practice['security_owner']))}</div>
        <div><strong>Technical Owner</strong>{html.escape(str(practice['technical_owner']))}</div>
      </div>
    </header>
    <div class="notice">This packet is an operational planning aid. It is not legal advice, HIPAA certification, breach determination, or a substitute for qualified review. Do not include PHI, secrets, credentials, or real incident details.</div>
    {body}
  </main>
</body>
</html>
"""


def build_packet(profile_path: Path, output_root: Path = OUT) -> Path:
    profile = load_profile(profile_path)
    out_dir = output_root / slugify(profile["practice"]["name"])
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
    (out_dir / "review-packet.html").write_text(render_html(packet, profile), encoding="utf-8", newline="\n")
    return out_dir
