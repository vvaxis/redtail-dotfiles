from ignis.widgets import Widget

from .calendar import calendar_card
from .events import events_card, fetch_events_for_date
from .weather import weather_card
from .notes import notes_card
from .music import music_card


def dashboard_window():
    left_panel = Widget.Box(
        vertical=True,
        spacing=24,
        css_classes=["dashboard-panel", "dashboard-left"],
        valign="center",
        hexpand=False,
        child=[
            calendar_card(on_day_selected=fetch_events_for_date),
            events_card(),
        ],
    )
    left_panel.set_size_request(460, -1)

    right_panel = Widget.Box(
        vertical=True,
        spacing=24,
        css_classes=["dashboard-panel", "dashboard-right"],
        valign="center",
        hexpand=False,
        child=[
            weather_card(),
            notes_card(),
            music_card(),
        ],
    )
    right_panel.set_size_request(440, -1)

    content = Widget.Box(
        vertical=False,
        spacing=48,
        css_classes=["dashboard-content"],
        halign="center",
        valign="center",
        hexpand=True,
        vexpand=True,
        child=[left_panel, right_panel],
    )

    window = Widget.Window(
        namespace="ignis-dashboard",
        anchor=["top", "bottom", "left", "right"],
        exclusivity="ignore",
        layer="overlay",
        kb_mode="on_demand",
        popup=False,
        visible=False,
        monitor=0,
        css_classes=["dashboard-window"],
        child=content,
    )

    return window
