from ignis.widgets import Widget
from services.system_stats import SystemStatsService
import subprocess


def _open_btop(_box):
    subprocess.Popen(["foot", "-e", "btop"])


def system_indicators() -> Widget.Box:
    stats = SystemStatsService()

    cpu_icon = Widget.Icon(image="am-cpu-symbolic", pixel_size=16, css_classes=["module-icon", "cpu-icon"], halign="center")
    cpu_value = Widget.Label(
        label=str(stats.cpu_percent),
        css_classes=["module-value", "cpu-value"],
        halign="center",
    )
    cpu_box = Widget.EventBox(
        vertical=True,
        css_classes=["module", "cpu"],
        child=[cpu_icon, cpu_value],
        on_click=_open_btop,
    )

    ram_icon = Widget.Icon(image="am-memory-symbolic", pixel_size=18, css_classes=["module-icon", "ram-icon"], halign="center")
    ram_value = Widget.Label(
        label=str(stats.ram_percent),
        css_classes=["module-value", "ram-value"],
        halign="center",
    )
    ram_box = Widget.EventBox(
        vertical=True,
        css_classes=["module", "ram"],
        child=[ram_icon, ram_value],
        on_click=_open_btop,
    )

    stats.on_cpu_change(lambda v: cpu_value.set_label(str(v)))
    stats.on_ram_change(lambda v: ram_value.set_label(str(v)))

    return Widget.Box(
        vertical=True,
        css_classes=["system-indicators"],
        child=[cpu_box, ram_box],
    )
