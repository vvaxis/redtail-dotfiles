from ignis.widgets import Widget
import subprocess


def network() -> Widget.EventBox:
    try:
        from ignis.services.network import NetworkService
        net = NetworkService.get_default()
        has_service = True
    except Exception:
        has_service = False

    icon = Widget.Icon(
        image="network-wireless-signal-excellent-symbolic",
        pixel_size=20,
        css_classes=["module-icon", "network-icon"],
        halign="center",
    )
    state_label = Widget.Label(
        label="--",
        css_classes=["module-value", "network-value"],
        halign="center",
    )

    if has_service:
        def update(*_args):
            if net.wifi.is_connected:
                icon.image = "network-wireless-signal-excellent-symbolic"
                icon.set_css_classes(["module-icon", "network-icon", "connected"])
                state_label.set_label("on")
                state_label.set_css_classes(["module-value", "network-value"])
                try:
                    for dev in net.wifi.devices:
                        if dev.ap and dev.ap.ssid:
                            box.set_tooltip_text(dev.ap.ssid)
                            return
                except Exception:
                    pass
                box.set_tooltip_text("Wi-Fi connected")
            elif net.ethernet.is_connected:
                icon.image = "network-wired-symbolic"
                icon.set_css_classes(["module-icon", "network-icon", "connected"])
                state_label.set_label("on")
                state_label.set_css_classes(["module-value", "network-value"])
                box.set_tooltip_text("Ethernet")
            else:
                icon.image = "network-wireless-offline-symbolic"
                icon.set_css_classes(["module-icon", "network-icon", "disconnected"])
                state_label.set_label("off")
                state_label.set_css_classes(["module-value", "network-value", "disconnected"])
                box.set_tooltip_text("Disconnected")

        net.wifi.connect("notify::is-connected", update)

    def on_click(_box):
        subprocess.Popen(["networkmanager_dmenu"])

    def on_right_click(_box):
        subprocess.Popen(["nm-connection-editor"])

    box = Widget.EventBox(
        vertical=True,
        css_classes=["module", "network"],
        child=[icon, state_label],
        on_click=on_click,
        on_right_click=on_right_click,
    )

    if has_service:
        update()
    return box
