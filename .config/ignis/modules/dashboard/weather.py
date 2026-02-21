import json
import subprocess

from ignis.widgets import Widget
from ignis.utils import Poll

WEATHER_SCRIPT = "/home/vvaxis/.config/ignis/scripts/weather.py"

# Module-level references
_temp_ref = None
_highlow_ref = None
_condition_ref = None
_icon_ref = None
_feels_ref = None
_pop_ref = None
_hourly_ref = None


def _fetch_weather() -> dict:
    try:
        result = subprocess.run(
            [WEATHER_SCRIPT],
            capture_output=True,
            text=True,
            timeout=15,
        )
        return json.loads(result.stdout)
    except Exception:
        return {
            "temp": "--", "high": "--", "low": "--",
            "feels_like": "--", "condition": "Erro",
            "icon": "\ue374", "humidity": 0, "pop": 0,
            "hourly": [],
        }


def _make_hourly_slot(slot: dict) -> Widget.Box:
    children = [
        Widget.Label(label=slot.get("time", ""), css_classes=["hourly-time"]),
        Widget.Label(label=slot.get("icon", ""), css_classes=["hourly-icon"]),
        Widget.Label(label=f"{slot.get('temp', '--')}°", css_classes=["hourly-temp"]),
    ]
    pop = slot.get("pop", 0)
    if pop > 0:
        children.append(
            Widget.Label(label=f"{pop}%", css_classes=["hourly-pop"])
        )
    return Widget.Box(
        vertical=True,
        spacing=4,
        css_classes=["hourly-slot"],
        child=children,
    )


def _update_weather(data: dict):
    if _temp_ref:
        _temp_ref.set_label(f"{data.get('temp', '--')}°C")
    if _highlow_ref:
        _highlow_ref.set_label(f"↑{data.get('high', '--')}° ↓{data.get('low', '--')}°")
    if _condition_ref:
        _condition_ref.set_label(str(data.get("condition", "...")))
    if _icon_ref:
        _icon_ref.set_label(str(data.get("icon", "")))
    if _feels_ref:
        _feels_ref.set_label(f"Sensação {data.get('feels_like', '--')}°")
    if _pop_ref:
        _pop_ref.set_label(f"Chance de chuva {data.get('pop', 0)}%")
    if _hourly_ref:
        hourly = data.get("hourly", [])
        _hourly_ref.child = [_make_hourly_slot(s) for s in hourly[:4]]


def _poll_callback(poll):
    data = _fetch_weather()
    _update_weather(data)


def weather_card() -> Widget.Box:
    global _temp_ref, _highlow_ref, _condition_ref, _icon_ref
    global _feels_ref, _pop_ref, _hourly_ref

    _temp_ref = Widget.Label(
        label="--°C", css_classes=["weather-temp"], halign="start",
    )
    _highlow_ref = Widget.Label(
        label="↑--° ↓--°", css_classes=["weather-highlow"], halign="start",
    )
    _condition_ref = Widget.Label(
        label="...", css_classes=["weather-condition"], halign="start",
    )
    _icon_ref = Widget.Label(
        label="", css_classes=["weather-icon"],
        halign="end",
        valign="center",
        hexpand=True,
    )
    _feels_ref = Widget.Label(
        label="Sensação --°", css_classes=["weather-detail"],
    )
    _pop_ref = Widget.Label(
        label="Chance de chuva 0%", css_classes=["weather-detail"],
    )

    current_left = Widget.Box(
        vertical=True,
        child=[
            Widget.Box(
                spacing=10,
                child=[_temp_ref, _highlow_ref],
            ),
            _condition_ref,
        ],
    )

    current = Widget.Box(
        spacing=12,
        css_classes=["weather-current"],
        child=[current_left, _icon_ref],
    )

    details = Widget.Box(
        spacing=20,
        css_classes=["weather-details"],
        child=[_feels_ref, _pop_ref],
    )

    _hourly_ref = Widget.Box(
        spacing=8,
        homogeneous=True,
        css_classes=["weather-hourly"],
        child=[],
    )

    # Start polling (15 min = 900000 ms)
    Poll(900_000, _poll_callback)
    # Also fetch immediately
    from ignis.utils import ThreadTask
    task = ThreadTask(
        target=_fetch_weather,
        callback=lambda data: _update_weather(data),
    )
    task.run()

    return Widget.Box(
        vertical=True,
        css_classes=["card", "weather-card"],
        child=[
            Widget.Label(
                label="󰖙  Clima",
                css_classes=["section-header"],
                halign="start",
            ),
            current,
            details,
            _hourly_ref,
        ],
    )
