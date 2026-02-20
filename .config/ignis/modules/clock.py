from ignis.widgets import Widget
from gi.repository import GLib
from datetime import datetime


def clock() -> Widget.Box:
    hour_label = Widget.Label(
        label=datetime.now().strftime("%H"),
        css_classes=["clock-hour"],
        halign="center",
       
    )
    minute_label = Widget.Label(
        label=datetime.now().strftime("%M"),
        css_classes=["clock-minute"],
        halign="center",
       
    )

    def update(_user_data=None):
        now = datetime.now()
        hour_label.set_label(now.strftime("%H"))
        minute_label.set_label(now.strftime("%M"))
        return True

    GLib.timeout_add_seconds(30, update)

    return Widget.Box(
        vertical=True,
        css_classes=["clock"],
        child=[hour_label, minute_label],
    )
