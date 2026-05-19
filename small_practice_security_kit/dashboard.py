from __future__ import annotations

import html
from pathlib import Path
from typing import Iterable

from .brand import VELARI_CSS_VARIABLES
from .packet import OUT, render_html, risk_level
from .profile import load_profile, slugify
from .vendor_evidence import vendor_hitrust_status, vendor_soc2_status


STATUS_LABELS = {
    "done": "Ready",
    "review": "Needs review",
    "blocked": "Needs action",
    "unknown": "Unknown",
}


def esc(value: object) -> str:
    return html.escape(str(value or ""))


def yes_no(value: bool) -> str:
    return "Yes" if value else "No"


def title_case(value: str) -> str:
    return value.replace("_", " ").title()


def status_class(value: str) -> str:
    normalized = str(value or "").lower()
    if normalized in {"high", "missing", "prohibited", "false", "not documented", "not run"}:
        return "blocked"
    if normalized in {"medium", "restricted", "unknown", "partial", "missing review date", "not reviewed", "not provided", "absent", ""}:
        return "review"
    if normalized in {"low", "signed", "allowed", "true", "ready", "complete", "completed"}:
        return "done"
    return "unknown"


def badge(value: str, *, kind: str | None = None) -> str:
    css = kind or status_class(value)
    return f"<span class='badge badge-{esc(css)}'>{esc(value)}</span>"


def metric(label: str, value: object, hint: str, css: str = "") -> str:
    return f"""
      <article class="metric {esc(css)}">
        <span>{esc(label)}</span>
        <strong>{esc(value)}</strong>
        <small>{esc(hint)}</small>
      </article>
    """


def table(headers: list[str], rows: Iterable[list[object]]) -> str:
    header_html = "".join(f"<th>{esc(header)}</th>" for header in headers)
    row_html = []
    for row in rows:
        row_html.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>")
    return f"""
      <div class="table-wrap">
        <table>
          <thead><tr>{header_html}</tr></thead>
          <tbody>{''.join(row_html)}</tbody>
        </table>
      </div>
    """


def task_row(name: str, hint: str, state: str, href: str) -> str:
    label = STATUS_LABELS.get(state, "Unknown")
    return f"""
      <a class="task-row" href="{esc(href)}">
        <span class="task-state task-{esc(state)}" aria-hidden="true"></span>
        <span>
          <strong>{esc(name)}</strong>
          <small>{esc(hint)}</small>
        </span>
        {badge(label, kind=state)}
      </a>
    """


def readiness_rows(profile: dict) -> list[list[object]]:
    readiness = profile["readiness"]
    rows = []
    for key, value in readiness.items():
        state = "done" if value else "blocked"
        rows.append([esc(title_case(key)), badge(yes_no(value), kind=state), esc("Readiness evidence")])
    return rows


def next_actions(profile: dict) -> list[str]:
    _, gaps = risk_level(profile)
    actions = list(gaps[:5])
    for vendor in profile["vendors"]:
        if vendor["touches_ephi"] and vendor["baa_status"] != "signed":
            actions.append(f"Confirm BAA status and review date for {vendor['name']}.")
        if vendor["ai_training_use"] in {"unknown", "not reviewed"}:
            actions.append(f"Ask {vendor['name']} whether customer data is used for AI training.")
    for workflow in profile["ai_workflows"]:
        if workflow["decision"] in {"restricted", "prohibited"}:
            actions.append(f"Create staff guidance for AI workflow: {workflow['name']}.")
    if profile["downtime"]["downtime_plan_status"] != "documented":
        actions.append("Assign downtime owners and document manual workarounds.")
    deduped: list[str] = []
    for action in actions:
        if action not in deduped:
            deduped.append(action)
    return deduped[:8] or ["Review the packet with the practice owner and record signoff."]


def evidence_rows(profile: dict) -> list[list[object]]:
    rows: list[list[object]] = []
    for evidence in profile.get("evidence", []):
        rows.append(
            [
                esc(evidence.get("id", evidence.get("title", "Evidence"))),
                esc(evidence.get("area", evidence.get("type", "Evidence"))),
                esc(evidence.get("title", "Evidence reference")),
                badge(evidence.get("status", "needed"), kind="review" if evidence.get("status") in {"needed", "requested", ""} else "done"),
            ]
        )
    for flow in profile["flows"]:
        rows.append([esc(flow["id"]), esc("ePHI flow"), esc(flow["evidence_needed"]), badge(flow["risk"])])
    for vendor in profile["vendors"]:
        rows.append(
            [
                esc(vendor["name"]),
                esc("Vendor/BAA"),
                esc(f"BAA, SOC 2/HITRUST status, incident terms, security contact, AI data-use review for {vendor['name']}"),
                badge(vendor["risk"]),
            ]
        )
    rows.append([esc("BACKUP-RESTORE"), esc("Resilience"), esc("Restore test record and owner signoff"), badge("review", kind="review")])
    rows.append([esc("AI-POLICY"), esc("AI workflow"), esc("Allowed, restricted, and prohibited AI use guidance"), badge("review", kind="review")])
    return rows


def build_dashboard(profile_path: Path, output_dir: Path | None = None) -> Path:
    profile = load_profile(profile_path)
    practice = profile["practice"]
    out_dir = output_dir or OUT / slugify(practice["name"])
    out_dir.mkdir(parents=True, exist_ok=True)

    risk, gaps = risk_level(profile)
    ready_count = sum(1 for value in profile["readiness"].values() if value)
    readiness_total = len(profile["readiness"])
    vendors_touching_ephi = sum(1 for vendor in profile["vendors"] if vendor["touches_ephi"])
    signed_baas = sum(1 for vendor in profile["vendors"] if vendor["touches_ephi"] and vendor["baa_status"] == "signed")
    high_flows = sum(1 for flow in profile["flows"] if flow["risk"] == "high")
    restricted_ai = sum(1 for workflow in profile["ai_workflows"] if workflow["decision"] != "allowed")

    actions = "".join(f"<li>{esc(action)}</li>" for action in next_actions(profile))
    task_list = "".join(
        [
            task_row("Readiness review", "MFA, access, backups, training, logging, and incident basics.", "review" if gaps else "done", "#readiness"),
            task_row("ePHI flow map", "Where ePHI enters, moves, rests, and leaves the practice.", "review" if high_flows else "done", "#flows"),
            task_row("Vendor and BAA review", "BAA status, SOC 2/HITRUST status, subcontractors, incident terms, and AI data use.", "review" if signed_baas < vendors_touching_ephi else "done", "#vendors"),
            task_row("AI workflow review", "Allowed, restricted, and prohibited AI uses.", "review" if restricted_ai else "done", "#ai"),
            task_row("Downtime packet", "Critical systems, restore tests, tabletop, and manual workarounds.", "blocked" if profile["downtime"]["downtime_plan_status"] != "documented" else "done", "#downtime"),
            task_row("Evidence queue", "The packet of evidence references to collect before review.", "review", "#evidence"),
        ]
    )

    flow_rows = [
        [
            esc(flow["id"]),
            esc(flow["source"]),
            esc(flow["destination"]),
            esc(flow["vendor"]),
            badge("BAA needed" if flow["baa_needed"] else "No BAA flag", kind="review" if flow["baa_needed"] else "unknown"),
            badge(flow["risk"]),
        ]
        for flow in profile["flows"]
    ]
    vendor_rows = [
        [
            esc(vendor["name"]),
            esc(vendor["service"]),
            badge("Touches ePHI" if vendor["touches_ephi"] else "No ePHI", kind="review" if vendor["touches_ephi"] else "unknown"),
            badge(vendor["baa_status"]),
            badge(vendor_soc2_status(vendor)),
            badge(vendor_hitrust_status(vendor)),
            badge(vendor["ai_training_use"]),
            badge(vendor["risk"]),
        ]
        for vendor in profile["vendors"]
    ]
    ai_rows = [
        [
            esc(workflow["name"]),
            esc(workflow["proposed_use"]),
            esc(workflow["data_used"]),
            esc(workflow["vendor"]),
            badge(workflow["decision"]),
        ]
        for workflow in profile["ai_workflows"]
    ]
    downtime_rows = [[esc(system), esc("Assign owner"), esc("Manual workaround and restore evidence")] for system in profile["downtime"]["critical_systems"]]
    companion_pages = {
        "30-60-90-roadmap.md": "30-60-90-roadmap.html",
        "evidence-binder-index.md": "evidence-binder-index.html",
    }
    for source_name, html_name in companion_pages.items():
        source_path = out_dir / source_name
        if source_path.exists():
            html_path = out_dir / html_name
            html_path.write_text(render_html(source_path.read_text(encoding="utf-8"), profile), encoding="utf-8", newline="\n")

    dashboard = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(practice['name'])} Local Security Dashboard</title>
  <style>
    :root {{
      {VELARI_CSS_VARIABLES}
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      color: var(--ink);
      background: linear-gradient(180deg, rgba(28, 59, 81, 0.08), transparent 280px), var(--bg);
      font-family: Avenir Next, "Segoe UI", Verdana, sans-serif;
      line-height: 1.5;
    }}
    a {{ color: inherit; }}
    .skip-link {{ position: absolute; left: -999px; top: 12px; background: var(--primary); color: var(--text-on-light); padding: 10px 12px; z-index: 20; }}
    .skip-link:focus {{ left: 12px; }}
    .shell {{ min-height: 100vh; display: grid; grid-template-columns: 280px minmax(0, 1fr); }}
    .sidebar {{ position: sticky; top: 0; height: 100vh; padding: 22px; border-right: 1px solid var(--line-strong); background: var(--app-bg); color: var(--text-on-dark); }}
    .brand {{ display: grid; gap: 6px; padding-bottom: 18px; border-bottom: 1px solid var(--line); }}
    .brand span, .eyebrow {{ color: var(--primary); font-size: 12px; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; }}
    .sidebar .brand span {{ color: var(--gold-soft); }}
    .brand strong {{ font-size: 22px; line-height: 1.15; }}
    .brand small, .nav a {{ color: var(--muted-inverse); }}
    .lede, .section-head p, .task-row small, .link-card small, .footer, .metric span, .metric small {{ color: var(--muted); }}
    .nav {{ display: grid; gap: 6px; margin: 18px 0; }}
    .nav a {{ text-decoration: none; border-radius: var(--radius); padding: 10px 11px; font-weight: 700; }}
    .nav a:hover, .nav a:focus, .task-row:hover, .task-row:focus, .link-card:hover, .link-card:focus {{ outline: 3px solid rgba(220, 192, 118, 0.36); border-color: var(--primary); }}
    .nav a:hover, .nav a:focus {{ color: var(--ink); background: var(--primary-soft); }}
    .local-note {{ padding: 12px; background: var(--surface); color: var(--ink); border: 1px solid var(--line-strong); border-radius: var(--radius); font-size: 13px; }}
    .callout {{ padding: 12px; background: var(--primary-soft); color: var(--ink); border: 1px solid var(--line); border-radius: var(--radius); font-size: 13px; }}
    .main {{ padding: 28px clamp(18px, 4vw, 48px) 56px; }}
    .hero {{ display: grid; grid-template-columns: minmax(0, 1.35fr) minmax(280px, 0.65fr); gap: 18px; align-items: stretch; margin-bottom: 18px; }}
    .panel {{ background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); box-shadow: var(--shadow); }}
    .intro {{ padding: clamp(20px, 4vw, 34px); }}
    h1, h2, h3 {{ margin: 0; line-height: 1.12; }}
    h1 {{ max-width: 820px; margin-top: 8px; font-size: clamp(32px, 4vw, 46px); letter-spacing: 0; }}
    .lede {{ max-width: 820px; font-size: 18px; margin: 16px 0 0; }}
    .decision-card {{ padding: 22px; display: grid; gap: 16px; background: var(--primary); color: var(--text-on-dark); }}
    .decision-card .eyebrow {{ color: var(--gold-soft); }}
    .decision-card .action-list {{ color: var(--text-on-dark); }}
    .decision-card h2 {{ font-size: 22px; }}
    .action-list {{ margin: 0; padding-left: 20px; display: grid; gap: 9px; color: var(--ink); }}
    .metrics {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin: 18px 0; }}
    .metric {{ padding: 16px; background: var(--surface-strong); border: 1px solid var(--line); border-radius: var(--radius); }}
    .metric span, .metric small {{ display: block; }}
    .metric strong {{ display: block; margin: 5px 0; font-size: 30px; letter-spacing: 0; overflow-wrap: anywhere; }}
    .section {{ scroll-margin-top: 24px; margin-top: 18px; padding: 22px; }}
    .section-head {{ display: flex; gap: 16px; justify-content: space-between; align-items: start; margin-bottom: 16px; }}
    .section-head p {{ margin: 8px 0 0; max-width: 760px; }}
    .task-list {{ display: grid; gap: 8px; }}
    .task-row {{ display: grid; grid-template-columns: 14px minmax(0, 1fr) auto; gap: 12px; align-items: center; padding: 13px; text-decoration: none; background: var(--surface-strong); border: 1px solid var(--line); border-radius: var(--radius); }}
    .task-row small {{ display: block; margin-top: 2px; }}
    .task-state {{ width: 12px; height: 12px; border-radius: 50%; background: var(--unknown); }}
    .task-done {{ background: var(--success); }}
    .task-review {{ background: var(--warning); }}
    .task-blocked {{ background: var(--danger); }}
    .badge {{ display: inline-flex; align-items: center; min-height: 24px; padding: 3px 9px; border-radius: 999px; font-size: 12px; font-weight: 800; white-space: nowrap; }}
    .badge-done {{ color: var(--success); background: var(--success-soft); }}
    .badge-review {{ color: var(--warning); background: var(--warning-soft); }}
    .badge-blocked {{ color: var(--danger); background: var(--danger-soft); }}
    .badge-unknown {{ color: var(--unknown); background: var(--unknown-soft); }}
    .split {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(260px, 0.4fr); gap: 14px; }}
    .callout strong {{ display: block; margin-bottom: 4px; }}
    .table-wrap {{ overflow-x: auto; border: 1px solid var(--line); border-radius: var(--radius); background: var(--surface-strong); }}
    table {{ width: 100%; border-collapse: collapse; min-width: 760px; }}
    th, td {{ padding: 11px 12px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ font-size: 12px; letter-spacing: 0.05em; text-transform: uppercase; color: var(--gold-soft); background: var(--primary-soft); }}
    tr:last-child td {{ border-bottom: 0; }}
    .links {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; }}
    .link-card {{ padding: 14px; border: 1px solid var(--line); background: var(--surface-strong); border-radius: var(--radius); text-decoration: none; }}
    .link-card strong, .link-card small {{ display: block; }}
    .link-card small {{ margin-top: 4px; }}
    .footer {{ margin-top: 20px; font-size: 13px; }}
    @media (max-width: 960px) {{
      .shell {{ display: block; }}
      .sidebar {{ position: relative; height: auto; border-right: 0; border-bottom: 1px solid var(--line); }}
      .nav {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .hero, .split {{ grid-template-columns: 1fr; }}
      .metrics, .links {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
    @media (max-width: 620px) {{
      .main {{ padding-inline: 14px; }}
      .metrics, .links {{ grid-template-columns: 1fr; }}
      .section, .intro, .decision-card {{ padding: 16px; }}
      .task-row {{ grid-template-columns: 12px minmax(0, 1fr); }}
      .task-row .badge {{ grid-column: 2; justify-self: start; }}
    }}
    @media print {{
      :root {{ --bg: #e9f0f7; --surface: #f8fafc; --surface-strong: #f8fafc; --panel: #f8fafc; --elevated: #e9f0f7; --ink: #050a10; --muted: #64748b; --line: #94a3b8; --primary-soft: #e9f0f7; --blue-soft: #e9f0f7; }}
      .sidebar {{ display: none; }}
      .shell {{ display: block; }}
      .main {{ padding: 0; }}
      .panel {{ box-shadow: none; break-inside: avoid; }}
      body {{ background: var(--surface-light); color: var(--text-on-light); }}
    }}
  </style>
</head>
<body>
  <a class="skip-link" href="#main">Skip to dashboard</a>
  <div class="shell">
    <aside class="sidebar" aria-label="Dashboard sections">
      <div class="brand">
        <span>Velari Security Kit</span>
        <strong>{esc(practice['name'])}</strong>
        <small>{esc(practice['review_period'])} local dashboard</small>
      </div>
      <nav class="nav">
        <a href="/">Intake</a>
        <a href="#overview">Overview</a>
        <a href="#readiness">Readiness</a>
        <a href="#flows">ePHI flows</a>
        <a href="#vendors">Vendors</a>
        <a href="#ai">AI workflows</a>
        <a href="#evidence">Evidence</a>
        <a href="#downtime">Downtime</a>
        <a href="#packet">Packet</a>
      </nav>
      <div class="local-note">
        <strong>Local only.</strong> This dashboard is generated from your local YAML profile. Do not enter PHI, passwords, patient details, or real incident contents.
      </div>
    </aside>
    <main id="main" class="main">
      <section id="overview" class="hero">
        <div class="panel intro">
          <span class="eyebrow">Owner dashboard</span>
          <h1>What needs to be fixed, evidenced, or reviewed before this practice is defensible?</h1>
          <p class="lede">This is the front door for the packet: readiness, ePHI movement, vendors, AI usage, downtime planning, and evidence collection in one local view.</p>
        </div>
        <aside class="panel decision-card">
          <div>
            <span class="eyebrow">Next best actions</span>
            <h2>Start here</h2>
          </div>
          <ol class="action-list">{actions}</ol>
        </aside>
      </section>
      <section class="metrics" aria-label="Practice summary metrics">
        {metric("Initial risk", risk, f"{len(gaps)} priority readiness gaps", status_class(risk))}
        {metric("Readiness", f"{ready_count}/{readiness_total}", "baseline items ready")}
        {metric("Vendor BAAs", f"{signed_baas}/{vendors_touching_ephi}", "ePHI vendors signed")}
        {metric("AI workflows", restricted_ai, "restricted or prohibited")}
      </section>
      <section class="panel section">
        <div class="section-head">
          <div><h2>Review workflow</h2><p>Use this like a practice-manager task list. Each row points to the dashboard section that explains what evidence or decision is needed.</p></div>
          {badge(risk)}
        </div>
        <div class="task-list">{task_list}</div>
      </section>
      <section id="readiness" class="panel section">
        <div class="section-head"><div><h2>Readiness</h2><p>Baseline security and evidence habits that small practices are commonly asked to prove.</p></div></div>
        {table(["Item", "Ready?", "Evidence lane"], readiness_rows(profile))}
      </section>
      <section id="flows" class="panel section">
        <div class="section-head"><div><h2>ePHI flow map</h2><p>Plain-English view of where ePHI enters, moves, rests, and leaves the practice.</p></div></div>
        {table(["Flow", "Source", "Destination", "Vendor", "BAA", "Risk"], flow_rows)}
      </section>
      <section id="vendors" class="panel section">
        <div class="section-head"><div><h2>Vendor and BAA review</h2><p>BAA status, SOC 2/HITRUST evidence status, incident terms, subcontractor visibility, and AI/customer-data questions.</p></div></div>
        {table(["Vendor", "Service", "ePHI", "BAA", "SOC 2", "HITRUST", "AI data use", "Risk"], vendor_rows)}
      </section>
      <section id="ai" class="panel section">
        <div class="section-head"><div><h2>AI workflow review</h2><p>Shows which workflows are allowed, restricted, or prohibited before staff paste anything into a tool.</p></div></div>
        {table(["Workflow", "Use", "Data", "Vendor", "Decision"], ai_rows)}
      </section>
      <section id="evidence" class="panel section">
        <div class="section-head"><div><h2>Evidence queue</h2><p>The dashboard does not need PHI. It points to evidence references, owner decisions, and exports that should live in a binder.</p></div></div>
        {table(["Evidence ID", "Area", "Evidence needed", "Priority"], evidence_rows(profile))}
      </section>
      <section id="downtime" class="panel section">
        <div class="section-head"><div><h2>Downtime and ransomware tabletop</h2><p>Critical systems that need an owner, manual workaround, restore-test evidence, and tabletop notes.</p></div>{badge(profile['downtime']['downtime_plan_status'])}</div>
        <div class="split">
          {table(["Critical system", "Owner", "Evidence needed"], downtime_rows)}
          <aside class="callout"><strong>Tabletop prompt</strong>EHR unavailable at 8:30 AM. Phones work. Billing portal is delayed. Staff need to continue patient care safely and preserve evidence.</aside>
        </div>
      </section>
      <section id="packet" class="panel section">
        <div class="section-head"><div><h2>Open packet outputs</h2><p>These files are generated locally from the same profile and are meant for owner/MSP/reviewer conversations.</p></div></div>
        <div class="links">
          <a class="link-card" href="review-packet.html"><strong>Review packet</strong><small>Full HTML packet</small></a>
          <a class="link-card" href="30-60-90-roadmap.html"><strong>30/60/90 roadmap</strong><small>Prioritized next steps</small></a>
          <a class="link-card" href="evidence-binder-index.html"><strong>Evidence index</strong><small>Binder queue</small></a>
          <a class="link-card" href="review-packet.md"><strong>Markdown packet</strong><small>Portable source file</small></a>
        </div>
      </section>
      <p class="footer">Generated locally by Velari Security Kit. This is not legal advice, does not certify any legal or regulatory requirement, does not decide incident reporting duties, and is not a substitute for qualified professional review.</p>
    </main>
  </div>
</body>
</html>
"""

    dashboard_path = out_dir / "dashboard.html"
    dashboard_path.write_text(dashboard, encoding="utf-8", newline="\n")
    return dashboard_path
