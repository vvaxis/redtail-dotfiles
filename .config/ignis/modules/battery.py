from ignis.widgets import Widget


def _battery_icon(percent: float, charging: bool) -> str:
    level = round(percent / 10) * 10
    level = max(0, min(100, level))
    if charging:
        return f"battery-level-{level}-charging-symbolic"
    return f"battery-level-{level}-symbolic"


def battery() -> Widget.Box:
    try:
        from ignis.services.upower import UPowerService
    except Exception:
        return Widget.Box(
            vertical=True,
            css_classes=["module", "battery"],
            child=[Widget.Icon(image="battery-level-0-symbolic", pixel_size=20, css_classes=["module-icon", "battery-icon"], halign="center")],
        )

    upower = UPowerService.get_default()
    device = upower.display_device

    icon = Widget.Icon(
        image=_battery_icon(device.percent, device.charging),
        pixel_size=20,
        css_classes=["module-icon", "battery-icon"],
        halign="center",
    )
    value_label = Widget.Label(
        label=str(round(device.percent)),
        css_classes=["module-value", "battery-value"],
        halign="center",
    )

    def _format_time(seconds: int) -> str:
        if seconds <= 0:
            return ""
        h = seconds // 3600
        m = (seconds % 3600) // 60
        if h > 0:
            return f"{h}h{m:02d}m"
        return f"{m}m"

    def update(*_args):
        percent = device.percent
        charging = device.charging
        icon.image = _battery_icon(percent, charging)
        value_label.set_label(str(round(percent)))

        classes = ["module-value", "battery-value"]
        if percent <= 10:
            classes.append("critical")
        elif percent <= 20:
            classes.append("low")
        elif charging:
            classes.append("charging")
        value_label.set_css_classes(classes)

        rate = device.energy_rate
        time_str = _format_time(device.time_remaining)
        tip_parts = [f"{round(percent)}%"]
        if rate > 0:
            tip_parts.append(f"{rate / 1000:.1f}W")
        if time_str:
            status = "until full" if charging else "remaining"
            tip_parts.append(f"{time_str} {status}")
        box.set_tooltip_text(" · ".join(tip_parts))

    device.connect("notify::percent", update)
    device.connect("notify::charging", update)
    device.connect("notify::energy-rate", update)

    box = Widget.Box(
        vertical=True,
        css_classes=["module", "battery"],
        child=[icon, value_label],
    )

    update()
    return box
