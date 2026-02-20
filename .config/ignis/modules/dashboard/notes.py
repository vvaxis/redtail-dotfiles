import os
import subprocess

from ignis.widgets import Widget
from ignis.utils import Poll

NOTES_PATH = os.path.expanduser("~/.local/share/dashboard/notes.md")

_content_ref = None


def _read_notes() -> str:
    try:
        with open(NOTES_PATH, "r") as f:
            lines = f.readlines()
        # Show last 8 lines, strip trailing whitespace
        tail = lines[-8:] if len(lines) > 8 else lines
        text = "".join(tail).rstrip()
        return text if text else ""
    except FileNotFoundError:
        return ""
    except Exception:
        return ""


def _poll_callback(poll):
    text = _read_notes()
    if _content_ref:
        _content_ref.set_label(text if text else "Clique para adicionar notas...")
        classes = ["notes-content"]
        if not text:
            classes.append("notes-empty-text")
        _content_ref.set_css_classes(classes)


def notes_card() -> Widget.Box:
    global _content_ref

    text = _read_notes()
    _content_ref = Widget.Label(
        label=text if text else "Clique para adicionar notas...",
        css_classes=["notes-content"] + (["notes-empty-text"] if not text else []),
        halign="start",
        valign="start",
        wrap=True,
    )

    def open_notes(_box):
        subprocess.Popen(["foot", "micro", NOTES_PATH])

    # Poll every 5 seconds
    Poll(5_000, _poll_callback)

    return Widget.EventBox(
        css_classes=["card", "notes-card"],
        on_click=open_notes,
        child=[
            Widget.Box(
                vertical=True,
                child=[
                    Widget.Label(
                        label="󰏫  Notas",
                        css_classes=["section-header"],
                        halign="start",
                    ),
                    _content_ref,
                ],
            ),
        ],
    )
