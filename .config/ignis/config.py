import os
from ignis.widgets import Widget
from ignis.css_manager import CssInfoPath, CssManager

from modules import (
    power_button,
    workspaces,
    clock,
    system_indicators,
    volume,
    brightness,
    network,
    bluetooth,
    battery,
    dashboard_window,
)

# ── CSS ──────────────────────────────────────────────────────────────────
css = CssManager.get_default()
css.apply_css(CssInfoPath(
    name="sidebar",
    path=os.path.expanduser("~/.config/ignis/style.css"),
))

# ── Layout ───────────────────────────────────────────────────────────────
# Top section: power button + workspace dots
top = Widget.Box(
    vertical=True,
    css_classes=["section", "section-top"],
    child=[
        power_button(),
        Widget.Separator(css_classes=["section-sep"]),
        workspaces(),
    ],
)

# Center section: clock (HH over MM)
center = Widget.Box(
    vertical=True,
    css_classes=["section", "section-center"],
    child=[clock()],
)

# Bottom section: system indicators
bottom = Widget.Box(
    vertical=True,
    css_classes=["section", "section-bottom"],
    child=[
        system_indicators(),
        volume(),
        brightness(),
        network(),
        bluetooth(),
        battery(),
    ],
)

# ── Window ───────────────────────────────────────────────────────────────
Widget.Window(
    namespace="ignis-sidebar",
    anchor=["top", "bottom", "left"],
    exclusivity="exclusive",
    layer="top",
    kb_mode="none",
    monitor=0,
    child=Widget.CenterBox(
        vertical=True,
        css_classes=["sidebar"],
        start_widget=top,
        center_widget=center,
        end_widget=bottom,
    ),
)

# ── Dashboard (hidden overlay, toggled via Mod+D) ────────────────────────
dashboard_window()
