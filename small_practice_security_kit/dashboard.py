from __future__ import annotations

import html
from datetime import date
from pathlib import Path
from typing import Iterable

from .brand import VELARI_CSS_VARIABLES
from .ephi_map import build_ephi_map
from .evidence_lifecycle import build_evidence_lifecycle, closeout_label, lifecycle_label, summarize_lifecycle, trace_label
from .packet import OUT, _incident_profile, render_html, risk_level
from .profile import load_profile, slugify
from .vendor_evidence import vendor_hitrust_status, vendor_soc2_status


STATUS_LABELS = {
    "done": "Ready",
    "review": "Needs review",
    "blocked": "Needs action",
    "unknown": "Unknown",
    "needs_evidence": "Needs evidence",
    "ready_for_review": "Ready for review",
    "closed": "Closed",
    "not_applicable": "Not applicable",
}


def esc(value: object) -> str:
    return html.escape(str(value or ""))


def yes_no(value: bool) -> str:
    return "Yes" if value else "No"


def title_case(value: str) -> str:
    return value.replace("_", " ").title()


def status_class(value: str) -> str:
    normalized = str(value or "").lower()
    if normalized in {"high", "missing", "stale", "outdated", "blocked", "prohibited", "false", "not documented", "not run"}:
        return "blocked"
    if normalized in {"medium", "restricted", "unknown", "partial", "requested", "needs review", "needs_evidence", "ready_for_review", "missing review date", "not reviewed", "not provided", "absent", ""}:
        return "review"
    if normalized in {"low", "signed", "provided", "reviewed", "allowed", "true", "ready", "complete", "completed", "closed", "not_applicable"}:
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
    mapped = build_ephi_map(profile)
    if mapped["high_risk_outside"]:
        first = mapped["high_risk_outside"][0]
        actions.append(
            f"Assign an owner for high-risk patient-data flow {first['id']} ({first['source']} -> {first['destination']}), which {first['ehr_lane_label'].lower()}."
        )
    if profile["downtime"]["downtime_plan_status"] != "documented":
        actions.append("Assign downtime owners and document manual workarounds.")
    deduped: list[str] = []
    for action in actions:
        if action not in deduped:
            deduped.append(action)
    return deduped[:8] or ["Review the packet with the practice owner and record signoff."]


def evidence_rows(profile: dict) -> list[list[object]]:
    records = build_evidence_lifecycle(profile, date.today())
    ranked = sorted(
        records,
        key=lambda record: (
            {"blocked": 0, "needs_evidence": 1, "ready_for_review": 2, "closed": 3, "not_applicable": 4}.get(record["closeout_state"], 5),
            record["evidence_id"],
        ),
    )
    rows: list[list[object]] = []
    for record in ranked:
        rows.append(
            [
                esc(record["evidence_id"]),
                esc(record["evidence_type"]),
                badge(lifecycle_label(record["lifecycle_status"]), kind=status_class(record["lifecycle_status"])),
                badge(closeout_label(record["closeout_state"]), kind=status_class(record["closeout_state"])),
                esc(record["owner"]),
                esc(trace_label(record)),
                esc(record["next_action"]),
            ]
        )
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
    ephi_map = build_ephi_map(profile)
    high_flows = sum(1 for flow in profile["flows"] if flow["risk"] == "high")
    outside_flows = ephi_map["counts"]["outside_flows"]
    restricted_ai = sum(1 for workflow in profile["ai_workflows"] if workflow["decision"] != "allowed")
    incident = _incident_profile(profile)
    incident_events = len(incident.get("timeline", []))
    incident_actions = len(incident.get("after_actions", []))
    lifecycle_records = build_evidence_lifecycle(profile, date.today())
    lifecycle_summary = summarize_lifecycle(lifecycle_records)
    evidence_task_state = "blocked" if lifecycle_summary["blocked"] else "review" if lifecycle_summary["needs_evidence"] or lifecycle_summary["ready_for_review"] else "done"

    actions = "".join(f"<li>{esc(action)}</li>" for action in next_actions(profile))
    task_list = "".join(
        [
            task_row("Readiness review", "MFA, access, backups, training, logging, and incident basics.", "review" if gaps else "done", "#readiness"),
            task_row("ePHI flow map", "Patient-data paths that leave, enter, or never touch the EHR.", "review" if outside_flows or high_flows else "done", "#flows"),
            task_row("Vendor and BAA review", "BAA status, SOC 2/HITRUST status, subcontractors, incident terms, and AI data use.", "review" if signed_baas < vendors_touching_ephi else "done", "#vendors"),
            task_row("AI workflow review", "Allowed, restricted, and prohibited AI uses.", "review" if restricted_ai else "done", "#ai"),
            task_row("Downtime packet", "Critical systems, restore tests, tabletop, and manual workarounds.", "blocked" if profile["downtime"]["downtime_plan_status"] != "documented" else "done", "#downtime"),
            task_row("Incident evidence timeline", "Sanitized event order, decision gates, evidence refs, and after-action owners.", "review" if incident_events else "unknown", "#incident"),
            task_row("Evidence lifecycle", "Evidence status, traceability, closeout rules, and owner/MSP next actions.", evidence_task_state, "#evidence"),
        ]
    )

    flow_rows = [
        [
            esc(flow["id"]),
            badge(flow["ehr_lane_label"], kind="blocked" if flow["ehr_lane"] == "outside_ehr" else "review" if flow["outside_ehr"] else "done"),
            esc(flow["outside_kind_label"]),
            esc(flow["source"]),
            esc(flow["destination"]),
            esc(flow["vendor"]),
            badge("BAA needed" if flow["baa_needed"] else "No BAA flag", kind="review" if flow["baa_needed"] else "unknown"),
            badge(flow["risk"]),
        ]
        for flow in ephi_map["flows"]
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
    incident_rows = [
        [
            esc(entry.get("time", "TBD")),
            esc(entry.get("phase", "Timeline event")),
            esc(entry.get("event", "Sanitized event category")),
            esc("; ".join(str(system) for system in entry.get("systems", []))),
            esc(entry.get("owner", "Practice owner/MSP")),
            esc(entry.get("evidence_ref", "private evidence reference")),
            badge(entry.get("status", "requested")),
        ]
        for entry in incident.get("timeline", [])
    ]
    after_action_rows = [
        [
            esc(item.get("id", "INC-AA")),
            badge(item.get("priority", "medium")),
            esc(item.get("owner", "Practice owner/MSP")),
            esc(item.get("action", "Action to complete")),
            esc(item.get("due", "30 days")),
        ]
        for item in incident.get("after_actions", [])
    ]
    companion_pages = {
        "30-60-90-roadmap.md": "30-60-90-roadmap.html",
        "evidence-binder-index.md": "evidence-binder-index.html",
        "incident-evidence-timeline.md": "incident-evidence-timeline.html",
        "incident-after-action-report.md": "incident-after-action-report.html",
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
      overflow-x: hidden;
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
    .panel, .metric, .task-row, .link-card, .local-note, .callout {{ min-width: 0; }}
    .intro {{ padding: clamp(20px, 4vw, 34px); }}
    h1, h2, h3 {{ margin: 0; line-height: 1.12; }}
    h1 {{ max-width: 820px; margin-top: 8px; font-size: 44px; letter-spacing: 0; }}
    h1, h2, h3, p, li, td, th, small, strong {{ overflow-wrap: anywhere; }}
    .lede {{ max-width: 820px; font-size: 18px; margin: 16px 0 0; }}
    .decision-card {{ padding: 22px; display: grid; gap: 16px; background: var(--primary); color: var(--text-on-dark); }}
    .decision-card .eyebrow {{ color: var(--gold-soft); }}
    .decision-card .action-list {{ color: var(--text-on-dark); }}
    .decision-card h2 {{ font-size: 22px; }}
    .action-list {{ margin: 0; padding-left: 20px; display: grid; gap: 9px; color: var(--ink); }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin: 18px 0; }}
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
      .shell {{ display: block; width: 100vw; max-width: 100vw; overflow-x: hidden; }}
      .sidebar {{ position: relative; height: auto; border-right: 0; border-bottom: 1px solid var(--line); }}
      .nav {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .hero, .split {{ grid-template-columns: 1fr; }}
      .metrics, .links {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      h1 {{ font-size: 38px; }}
    }}
    @media (max-width: 620px) {{
      .shell, .sidebar, .main {{ width: 100%; max-width: 390px; margin-inline: 0; overflow-x: hidden; }}
      .hero, .panel, .section {{ width: 100%; max-width: 100%; overflow-x: hidden; }}
      .sidebar {{ padding: 22px 14px; }}
      .main {{ padding: 28px 14px 56px; }}
      .metrics, .links {{ grid-template-columns: 1fr; }}
      .section, .intro, .decision-card {{ padding: 16px; }}
      .task-row {{ grid-template-columns: 12px minmax(0, 1fr); }}
      .task-row .badge {{ grid-column: 2; justify-self: start; }}
      h1 {{ max-width: calc(100vw - 60px); font-size: 29px; line-height: 1.08; }}
      .lede {{ font-size: 16px; }}
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
        <a href="#incident">Incident</a>
        <a href="#evidence">Closeout</a>
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
        {metric("Outside the EHR", outside_flows, f"{ephi_map['counts']['never_touches']} never touch the chart", "blocked" if ephi_map["counts"]["high_risk_outside"] else "")}
        {metric("AI workflows", restricted_ai, "restricted or prohibited")}
        {metric("Incident actions", incident_actions, f"{incident_events} timeline events")}
        {metric("Evidence closeout", f"{lifecycle_summary['closed']}/{lifecycle_summary['total']}", f"{lifecycle_summary['blocked']} blocked, {lifecycle_summary['needs_evidence']} need evidence")}
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
        <div class="section-head"><div><h2>Patient data outside the EHR</h2><p>The EHR is one system. This map is the rest: email, shared files, imaging exports, messaging, billing, AI, and other sidecar paths.</p></div>{badge(f"{outside_flows} outside-EHR flows")}</div>
        {table(["Flow", "Lane", "Location", "Source", "Destination", "Vendor", "BAA", "Risk"], flow_rows)}
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
        <div class="section-head"><div><h2>Evidence lifecycle and closeout</h2><p>The dashboard does not need PHI. It points to evidence references, owner decisions, trace context, closeout rules, and exports that should live in a binder.</p></div>{badge(f"{lifecycle_summary['blocked']} blocked", kind='blocked' if lifecycle_summary['blocked'] else 'done')}</div>
        {table(["Evidence ID", "Area", "Lifecycle", "Closeout", "Owner", "Trace", "Next action"], evidence_rows(profile))}
      </section>
      <section id="incident" class="panel section">
        <div class="section-head"><div><h2>Incident evidence timeline</h2><p>A sanitized event sequence for tabletop, suspicious-access, downtime, vendor-notice, or ransomware concern handoffs. It tracks evidence references and decision gates without copying raw evidence.</p></div>{badge(incident.get('scenario_type', 'tabletop'))}</div>
        {table(["Time", "Phase", "Event category", "System/workflow", "Owner", "Evidence ref", "Status"], incident_rows)}
        <h3>After-action queue</h3>
        {table(["ID", "Priority", "Owner", "Action", "Due"], after_action_rows)}
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
          <a class="link-card" href="incident-evidence-timeline.html"><strong>Incident timeline</strong><small>Decision gates and evidence refs</small></a>
          <a class="link-card" href="incident-after-action-report.html"><strong>After-action report</strong><small>Remediation owners</small></a>
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
