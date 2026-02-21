import calendar as cal
from datetime import date, timedelta

from ignis.widgets import Widget

MONTHS_PT = [
    "", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]
DAY_HEADERS = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]

# Module-level state
_state = {
    "year": date.today().year,
    "month": date.today().month,
    "selected_day": None,  # (year, month, day) tuple or None
}

_grid_ref = None
_title_ref = None
_on_day_selected = None


def _get_weeks(year: int, month: int) -> list[list[int]]:
    """Return 6 weeks of day numbers (0 = empty cell), Sunday-first."""
    c = cal.Calendar(firstweekday=6)  # Sunday first
    weeks = []
    current_week = []
    for d in c.itermonthdays(year, month):
        current_week.append(d)
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []
    if current_week:
        weeks.append(current_week + [0] * (7 - len(current_week)))
    return weeks


def _day_classes(day: int, year: int, month: int) -> list[str]:
    if day == 0:
        return ["day-cell", "day-empty"]
    classes = ["day-cell"]
    today = date.today()
    if year == today.year and month == today.month and day == today.day:
        classes.append("day-today")
    sel = _state["selected_day"]
    if sel and sel == (year, month, day):
        classes.append("day-selected")
    return classes


def _select_day(d: int):
    """Select a day and fire the callback."""
    if d > 0:
        _state["selected_day"] = (_state["year"], _state["month"], d)
        _rebuild_grid()
        if _on_day_selected:
            sel = _state["selected_day"]
            _on_day_selected(date(sel[0], sel[1], sel[2]))


def _rebuild_grid():
    if _grid_ref is None:
        return

    year = _state["year"]
    month = _state["month"]
    weeks = _get_weeks(year, month)

    cells = []
    for week in weeks:
        for day in week:
            label = str(day) if day > 0 else ""
            css = _day_classes(day, year, month)

            def make_click(d):
                def on_click(_btn):
                    _select_day(d)
                return on_click

            btn = Widget.Button(
                label=label,
                css_classes=css,
                on_click=make_click(day),
                hexpand=True,
            )
            cells.append(btn)

    _grid_ref.child = cells

    if _title_ref is not None:
        _title_ref.set_label(f"󰃭  {MONTHS_PT[month]} {year}")


def _navigate(delta: int):
    m = _state["month"] + delta
    y = _state["year"]
    if m < 1:
        m = 12
        y -= 1
    elif m > 12:
        m = 1
        y += 1
    _state["year"] = y
    _state["month"] = m
    _state["selected_day"] = None
    _rebuild_grid()


def _move_selection(days: int):
    """Move selected day by delta days, crossing month boundaries."""
    sel = _state["selected_day"]
    if not sel:
        _go_today()
        return

    current = date(sel[0], sel[1], sel[2])
    new = current + timedelta(days=days)

    if new.month != _state["month"] or new.year != _state["year"]:
        _state["year"] = new.year
        _state["month"] = new.month

    _state["selected_day"] = (new.year, new.month, new.day)
    _rebuild_grid()
    if _on_day_selected:
        _on_day_selected(new)


def _go_today():
    today = date.today()
    _state["year"] = today.year
    _state["month"] = today.month
    _state["selected_day"] = (today.year, today.month, today.day)
    _rebuild_grid()
    if _on_day_selected:
        _on_day_selected(today)


def handle_key(keyval):
    """Handle keyboard navigation. Returns True if consumed."""
    from gi.repository import Gdk

    if keyval in (Gdk.KEY_Left, Gdk.KEY_h):
        _move_selection(-1)
        return True
    elif keyval in (Gdk.KEY_Right, Gdk.KEY_l):
        _move_selection(1)
        return True
    elif keyval in (Gdk.KEY_Up, Gdk.KEY_k):
        _move_selection(-7)
        return True
    elif keyval in (Gdk.KEY_Down, Gdk.KEY_j):
        _move_selection(7)
        return True
    elif keyval == Gdk.KEY_Page_Up:
        _navigate(-1)
        return True
    elif keyval == Gdk.KEY_Page_Down:
        _navigate(1)
        return True
    elif keyval == Gdk.KEY_t:
        _go_today()
        return True
    return False


def calendar_card(on_day_selected=None) -> Widget.Box:
    global _grid_ref, _title_ref, _on_day_selected
    _on_day_selected = on_day_selected

    today = date.today()
    title_label = Widget.Label(
        label=f"󰃭  {MONTHS_PT[today.month]} {today.year}",
        css_classes=["cal-nav-title"],
        hexpand=True,
        halign="center",
    )
    _title_ref = title_label

    nav = Widget.Box(
        css_classes=["cal-nav"],
        child=[
            Widget.Button(
                label="󰅁",
                css_classes=["cal-nav-btn"],
                on_click=lambda _b: _navigate(-1),
            ),
            Widget.Button(
                child=title_label,
                css_classes=["cal-nav-title-btn"],
                hexpand=True,
                on_click=lambda _b: _go_today(),
            ),
            Widget.Button(
                label="󰅂",
                css_classes=["cal-nav-btn"],
                on_click=lambda _b: _navigate(1),
            ),
        ],
    )

    # Day name headers
    header_cells = [
        Widget.Label(label=name, css_classes=["day-name"], hexpand=True)
        for name in DAY_HEADERS
    ]
    header_row = Widget.Grid(
        column_num=7,
        css_classes=["day-names"],
        child=header_cells,
    )

    # Day grid (42 cells = 6 weeks x 7 days)
    grid = Widget.Grid(
        column_num=7,
        css_classes=["cal-grid"],
        child=[],
    )
    _grid_ref = grid
    _go_today()

    return Widget.Box(
        vertical=True,
        css_classes=["card", "calendar-card"],
        child=[nav, header_row, grid],
    )
