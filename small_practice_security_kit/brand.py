from __future__ import annotations


VELARI_PALETTE = {
    "navy": "#12395B",
    "blue": "#1F5D8B",
    "gold": "#C9A55B",
    "bg": "#F3F6F9",
    "surface": "#FBFDFF",
    "panel": "#F6FBFF",
    "line": "#D9E2EC",
    "ink": "#1F2937",
    "muted": "#52606D",
}


VELARI_CSS_VARIABLES = """
      --bg: #f3f6f9;
      --surface: #fbfdff;
      --surface-strong: #ffffff;
      --panel: #fbfdff;
      --ink: #1f2937;
      --muted: #52606d;
      --line: #d9e2ec;
      --primary: #12395b;
      --primary-strong: #0b2944;
      --primary-2: #1f5d8b;
      --primary-soft: #eef5fb;
      --blue-soft: #f6fbff;
      --gold: #c9a55b;
      --gold-soft: #fff8ec;
      --success: #2f6f43;
      --success-soft: #e8f3e7;
      --warning: #8a5a14;
      --warning-soft: #fff8ec;
      --danger: #a13d32;
      --danger-soft: #fde8e4;
      --unknown: #667085;
      --unknown-soft: #eef0f2;
      --paper: var(--bg);
      --accent: var(--primary);
      --accent-2: var(--gold);
      --accent-soft: var(--primary-soft);
      --warn: var(--warning);
      --warn-soft: var(--warning-soft);
      --ok: var(--success);
      --soft: var(--primary-soft);
      --radius: 8px;
      --shadow: 0 18px 45px rgba(18, 57, 91, 0.08);
""".strip()
