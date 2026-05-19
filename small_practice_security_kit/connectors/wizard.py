from __future__ import annotations

from pathlib import Path

from ..brand import VELARI_CSS_VARIABLES


def render_connector_wizard() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Velari Connector Wizard</title>
  <style>
    :root {
{velari_css}
    }
    body { font-family: Inter, Avenir Next, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 0; background: var(--bg); color: var(--ink); }
    header, main { max-width: 1040px; margin: 0 auto; padding: 32px 20px; }
    header { padding-bottom: 8px; }
    h1 { margin: 0 0 8px; font-size: 34px; }
    p { line-height: 1.5; }
    .grid { display: grid; gap: 14px; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }
    .card { background: var(--surface-strong); border: 1px solid var(--line); border-radius: 8px; padding: 18px; box-shadow: var(--shadow); }
    .tag { display: inline-flex; padding: 4px 8px; border-radius: 999px; background: var(--gold-soft); color: var(--primary); border: 1px solid #ecd8a6; font-size: 12px; font-weight: 800; }
    code { display: block; white-space: pre-wrap; background: var(--primary-strong); color: #eef5fb; padding: 12px; border-radius: 6px; font-size: 13px; overflow-x: auto; }
    button { border: 0; border-radius: 6px; background: var(--primary); color: white; padding: 10px 12px; font-weight: 700; cursor: pointer; }
    small { color: var(--muted); display: block; margin-top: 8px; }
  </style>
</head>
<body>
  <header>
    <span class="tag">Local connector setup</span>
    <h1>Connect the systems, then build the packet</h1>
    <p>Velari official connectors use read-only metadata scopes. They do not request PHI, credentials, mailbox contents, Drive/SharePoint contents, raw logs, patient screenshots, or raw contracts.</p>
  </header>
  <main class="grid">
    <section class="card">
      <h2>Google Workspace</h2>
      <p>Use a Google OAuth desktop client with Admin SDK Directory API enabled.</p>
      <code>python -m small_practice_security_kit connect google-workspace --client-id "$VELARI_GOOGLE_CLIENT_ID"
python -m small_practice_security_kit collect google-workspace --out evidence/google-workspace.json</code>
      <button data-copy="google">Copy commands</button>
      <small>Scope: admin.directory.user.readonly. Stores token in Keychain when available.</small>
    </section>
    <section class="card">
      <h2>Microsoft 365</h2>
      <p>Use a Microsoft Entra public client app with localhost redirect URI.</p>
      <code>python -m small_practice_security_kit connect microsoft-365 --client-id "$VELARI_MICROSOFT_CLIENT_ID"
python -m small_practice_security_kit collect microsoft-365 --out evidence/microsoft-365.json</code>
      <button data-copy="microsoft">Copy commands</button>
      <small>Scopes: User.Read.All, AuditLog.Read.All, offline_access. Stores token in Keychain when available.</small>
    </section>
    <section class="card">
      <h2>Build the owner packet</h2>
      <p>After connectors run, build one packet from every evidence bundle.</p>
      <code>python -m small_practice_security_kit generate msp-request --profile samples/family_dental_clinic.yaml --evidence evidence/*.json --out out/msp-request.md
python -m small_practice_security_kit build samples/family_dental_clinic.yaml --evidence evidence/*.json --output-root out</code>
      <button data-copy="build">Copy commands</button>
      <small>Outputs owner, MSP, vendor, reviewer, risk, freshness, and evidence views.</small>
    </section>
  </main>
  <script>
    document.querySelectorAll("button[data-copy]").forEach((button) => {
      button.addEventListener("click", async () => {
        await navigator.clipboard.writeText(button.parentElement.querySelector("code").innerText);
        button.innerText = "Copied";
      });
    });
  </script>
</body>
</html>
""".replace("{velari_css}", VELARI_CSS_VARIABLES)


def write_connector_wizard(output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_connector_wizard(), encoding="utf-8")
    return output_path
