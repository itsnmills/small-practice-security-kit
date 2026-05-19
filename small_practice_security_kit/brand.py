from __future__ import annotations


VELARI_PALETTE = {
    "near_black": "#050A10",
    "navy_deep": "#0A1620",
    "navy_rich": "#112433",
    "blue_steel": "#1C3B51",
    "slate": "#64748B",
    "slate_light": "#94A3B8",
    "gold_warm": "#C9A84C",
    "gold_soft": "#DCC076",
    "surface_off_white": "#E9F0F7",
    "surface_white": "#F8FAFC",
}


VELARI_SEMANTIC_COLORS = {
    "color/bg/app": VELARI_PALETTE["near_black"],
    "color/bg/surface": VELARI_PALETTE["navy_deep"],
    "color/bg/elevated": VELARI_PALETTE["navy_rich"],
    "color/border/default": VELARI_PALETTE["blue_steel"],
    "color/action/primary": VELARI_PALETTE["gold_warm"],
    "color/action/primary-hover": VELARI_PALETTE["gold_soft"],
    "color/text/strong": VELARI_PALETTE["surface_white"],
    "color/text/muted": VELARI_PALETTE["slate_light"],
    "color/surface/light": VELARI_PALETTE["surface_off_white"],
    "color/text/on-light": VELARI_PALETTE["near_black"],
    "focus/ring/color": VELARI_PALETTE["gold_soft"],
}


VELARI_CSS_VARIABLES = """
      --bg: #e9f0f7;
      --app-bg: #050a10;
      --surface: #f8fafc;
      --surface-strong: #f8fafc;
      --panel: #f8fafc;
      --elevated: #112433;
      --ink: #050a10;
      --ink-inverse: #f8fafc;
      --muted: #64748b;
      --muted-inverse: #94a3b8;
      --subtle: #94a3b8;
      --line: #94a3b8;
      --line-strong: #1c3b51;
      --primary: #0a1620;
      --primary-hover: #112433;
      --primary-strong: #050a10;
      --primary-2: #1c3b51;
      --primary-soft: #e9f0f7;
      --blue-soft: #e9f0f7;
      --action: #c9a84c;
      --action-hover: #dcc076;
      --gold: #c9a84c;
      --gold-soft: #dcc076;
      --surface-light: #e9f0f7;
      --surface-white: #f8fafc;
      --text-on-light: #050a10;
      --text-on-dark: #f8fafc;
      --focus-ring: #dcc076;
      --success: #1c3b51;
      --success-soft: #e9f0f7;
      --warning: #c9a84c;
      --warning-soft: #e9f0f7;
      --danger: #1c3b51;
      --danger-soft: #e9f0f7;
      --unknown: #64748b;
      --unknown-soft: #e9f0f7;
      --paper: var(--bg);
      --accent: var(--primary);
      --accent-2: var(--gold);
      --accent-soft: var(--primary-soft);
      --warn: var(--warning);
      --warn-soft: var(--warning-soft);
      --ok: var(--success);
      --soft: var(--primary-soft);
      --radius: 8px;
      --shadow: 0 16px 36px rgba(5, 10, 16, 0.08);
""".strip()
