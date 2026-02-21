from ignis.widgets import Widget
from gi.repository import GLib
import subprocess


def _bt_state():
    """Read bluetooth state from bluetoothctl."""
    try:
        result = subprocess.run(
            ["bluetoothctl", "show"],
            capture_output=True, text=True, timeout=2,
        )
        powered = "Powered: yes" in result.stdout
    except Exception:
        return "off", []

    if not powered:
        return "off", []

    try:
        result = subprocess.run(
            ["bluetoothctl", "devices", "Connected"],
            capture_output=True, text=True, timeout=2,
        )
        devices = []
        for line in result.stdout.strip().splitlines():
            parts = line.split(" ", 2)
            if len(parts) >= 3:
                devices.append(parts[2])
        return "on", devices
    except Exception:
        return "on", []


def bluetooth() -> Widget.EventBox:
    icon = Widget.Icon(
        image="bluetooth-active-symbolic",
        pixel_size=24,
        css_classes=["module-icon", "bluetooth-icon"],
        halign="center",
    )
    state_label = Widget.Label(
        label="--",
        css_classes=["module-value", "bluetooth-value"],
        halign="center",
    )

    def update():
        state, devices = _bt_state()
        if state == "on" and devices:
            icon.image = "bluetooth-active-symbolic"
            icon.set_css_classes(["module-icon", "bluetooth-icon", "connected"])
            state_label.set_label("on")
            state_label.set_css_classes(["module-value", "bluetooth-value"])
            box.set_tooltip_text(", ".join(devices))
        elif state == "on":
            icon.image = "bluetooth-active-symbolic"
            icon.set_css_classes(["module-icon", "bluetooth-icon"])
            state_label.set_label("on")
            state_label.set_css_classes(["module-value", "bluetooth-value"])
            box.set_tooltip_text("Bluetooth on")
        else:
            icon.image = "bluetooth-disabled-symbolic"
            icon.set_css_classes(["module-icon", "bluetooth-icon", "off"])
            state_label.set_label("off")
            state_label.set_css_classes(["module-value", "bluetooth-value", "off"])
            box.set_tooltip_text("Bluetooth off")
        return True

    def on_click(_box):
        subprocess.Popen(["blueman-manager"])

    box = Widget.EventBox(
        vertical=True,
        css_classes=["module", "bluetooth"],
        child=[icon, state_label],
        on_click=on_click,
    )

    update()
    GLib.timeout_add_seconds(5, update)
    return box
