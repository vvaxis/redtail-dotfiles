import json
import subprocess
from datetime import date

from ignis.widgets import Widget
from ignis.utils import ThreadTask

VENV_PYTHON = "/home/vvaxis/Projects/dashboard/eww/scripts/.venv/bin/python3"
GCAL_SCRIPT = "/home/vvaxis/Projects/dashboard/eww/scripts/gcal-events.py"

# Module-level references
_header_ref = None
_list_ref = None


def _make_event_row(event: dict) -> Widget.Box:
    return Widget.Box(
        spacing=10,
        css_classes=["event-row"],
        child=[
            Widget.Label(
                label=event.get("time", ""),
                css_classes=["event-time"],
            ),
            Widget.Label(
                label=event.get("title", "(sem título)"),
                css_classes=["event-title"],
                halign="start",
                hexpand=True,
                ellipsize="end",
                max_width_chars=32,
            ),
        ],
    )


def _show_loading():
    if _list_ref is not None:
        _list_ref.child = [
            Widget.Label(
                label="Carregando...",
                css_classes=["events-empty"],
                halign="start",
            )
        ]


def _show_events(data: dict):
    if _header_ref is not None:
        label = data.get("dateLabel", "Eventos")
        _header_ref.set_label(f"󰃮  {label}" if label else "󰃮  Eventos")

    if _list_ref is None:
        return

    events = data.get("events", [])
    error = data.get("error")

    if error:
        _list_ref.child = [
            Widget.Label(label=error, css_classes=["events-empty"], halign="start")
        ]
    elif not events:
        _list_ref.child = [
            Widget.Label(
                label="Nenhum evento",
                css_classes=["events-empty"],
                halign="start",
            )
        ]
    else:
        _list_ref.child = [_make_event_row(e) for e in events]


def _fetch_thread(date_str: str) -> dict:
    try:
        result = subprocess.run(
            [VENV_PYTHON, GCAL_SCRIPT, date_str],
            capture_output=True,
            text=True,
            timeout=15,
        )
        return json.loads(result.stdout)
    except Exception as e:
        return {
            "date": date_str,
            "dateLabel": "",
            "events": [],
            "count": 0,
            "error": str(e),
        }


def fetch_events_for_date(d: date):
    _show_loading()
    ThreadTask(
        target=lambda: _fetch_thread(d.isoformat()),
        callback=lambda _task, result: _show_events(result),
    )


def events_card() -> Widget.Box:
    global _header_ref, _list_ref

    header = Widget.Label(
        label="󰃮  Eventos",
        css_classes=["section-header"],
        halign="start",
    )
    _header_ref = header

    event_list = Widget.Box(
        vertical=True,
        spacing=6,
        css_classes=["events-content"],
        child=[
            Widget.Label(
                label="Selecione um dia",
                css_classes=["events-empty"],
                halign="start",
            )
        ],
    )
    _list_ref = event_list

    return Widget.Box(
        vertical=True,
        css_classes=["card", "events-card"],
        child=[header, event_list],
    )
