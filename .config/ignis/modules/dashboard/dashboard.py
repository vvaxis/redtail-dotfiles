from gi.repository import Gtk, Gdk
from ignis.widgets import Widget

from .calendar import calendar_card, handle_key as calendar_handle_key
from .events import events_card, fetch_events_for_date
from .weather import weather_card
from .notes import notes_card
from .music import music_card


def dashboard_window():
    events = events_card()

    left_panel = Widget.Box(
        vertical=True,
        spacing=24,
        css_classes=["dashboard-panel", "dashboard-left"],
        valign="center",
        hexpand=False,
        child=[
            calendar_card(on_day_selected=fetch_events_for_date),
            events,
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
        child=[left_panel, right_panel],
    )

    window = Widget.Window(
        namespace="ignis-dashboard",
        exclusivity="ignore",
        layer="overlay",
        kb_mode="on_demand",
        popup=False,
        visible=False,
        monitor=0,
        css_classes=["dashboard-window"],
        child=content,
    )

    # Keyboard navigation
    def _on_key_pressed(_ctrl, keyval, _keycode, _state):
        if keyval == Gdk.KEY_Escape:
            window.set_visible(False)
            return True
        return calendar_handle_key(keyval)

    key_ctrl = Gtk.EventControllerKey()
    key_ctrl.connect("key-pressed", _on_key_pressed)
    window.add_controller(key_ctrl)

    return window
