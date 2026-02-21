import json
import subprocess
import time
from datetime import date

from ignis.widgets import Widget
from ignis.utils import ThreadTask

VENV_PYTHON = "/home/vvaxis/.config/ignis/scripts/.venv/bin/python3"
GCAL_SCRIPT = "/home/vvaxis/.config/ignis/scripts/gcal-events.py"

CACHE_TTL = 300  # 5 minutes for other days; today expires only on restart

# Module-level references
_header_ref = None
_list_ref = None
_current_date = None  # date currently displayed — guards against stale async responses

# In-memory cache: {date_str: {"data": dict, "ts": float}}
_cache = {}


def _open_link(link: str):
    if link:
        subprocess.Popen(["xdg-open", link])


def _make_event_row(event: dict) -> Widget.EventBox:
    link = event.get("link", "")
    return Widget.EventBox(
        css_classes=["event-row"],
        on_click=lambda *_: _open_link(link),
        child=[
            Widget.Box(
                spacing=10,
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


def _show_events(data: dict, date_str: str = ""):
    # Store in cache
    if date_str:
        _cache[date_str] = {"data": data, "ts": time.time()}

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
    global _current_date
    date_str = d.isoformat()
    _current_date = date_str
    is_today = (d == date.today())

    # Check cache — today never expires (cleared on restart), other days 5min TTL
    cached = _cache.get(date_str)
    if cached and (is_today or (time.time() - cached["ts"]) < CACHE_TTL):
        _show_events(cached["data"])
        return

    # Cache miss or stale — show loading and fetch
    _show_loading()

    def _on_result(result):
        # Always cache the result
        _cache[date_str] = {"data": result, "ts": time.time()}
        # Only update UI if user hasn't navigated away
        if _current_date == date_str:
            _show_events(result)

    task = ThreadTask(
        target=lambda: _fetch_thread(date_str),
        callback=_on_result,
    )
    task.run()


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
