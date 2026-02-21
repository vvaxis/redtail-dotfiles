from ignis.widgets import Widget
import subprocess


def _volume_icon(percent: int, muted: bool) -> str:
    if muted or percent <= 0:
        return "audio-volume-muted-symbolic"
    if percent < 33:
        return "audio-volume-low-symbolic"
    if percent < 66:
        return "audio-volume-medium-symbolic"
    return "audio-volume-high-symbolic"


def _to_percent(vol: float) -> int:
    """Handle both 0.0-1.0 and 0-100 ranges."""
    if vol <= 1.0:
        return round(vol * 100)
    return round(vol)


def volume() -> Widget.EventBox:
    try:
        from ignis.services.audio import AudioService
    except Exception:
        return Widget.EventBox(
            vertical=True,
            css_classes=["module", "volume"],
            child=[Widget.Icon(image="audio-volume-muted-symbolic", pixel_size=22, css_classes=["module-icon", "volume-icon"], halign="center")],
        )

    audio = AudioService.get_default()
    speaker = audio.speaker

    icon = Widget.Icon(
        image=_volume_icon(_to_percent(speaker.volume), speaker.is_muted),
        pixel_size=22,
        css_classes=["module-icon", "volume-icon"],
        halign="center",
    )
    value_label = Widget.Label(
        label=str(_to_percent(speaker.volume)),
        css_classes=["module-value", "volume-value"],
        halign="center",
    )

    def update(*_args):
        vol = speaker.volume
        muted = speaker.is_muted
        pct = _to_percent(vol)
        icon.image = _volume_icon(pct, muted)
        value_label.set_label(str(pct))

        classes = ["module-value", "volume-value"]
        if muted:
            classes.append("muted")
        value_label.set_css_classes(classes)

    speaker.connect("notify::volume", update)
    speaker.connect("notify::is-muted", update)

    def toggle_mute(_box):
        speaker.is_muted = not speaker.is_muted

    def open_mixer(_box):
        subprocess.Popen(["pwvucontrol"])

    def scroll_up(_box):
        vol = speaker.volume
        step = 0.05 if vol <= 1.0 else 5
        speaker.volume = min(1.0 if vol <= 1.0 else 100, vol + step)

    def scroll_down(_box):
        vol = speaker.volume
        step = 0.05 if vol <= 1.0 else 5
        speaker.volume = max(0.0, vol - step)

    return Widget.EventBox(
        vertical=True,
        css_classes=["module", "volume"],
        child=[icon, value_label],
        on_click=toggle_mute,
        on_right_click=open_mixer,
        on_scroll_up=scroll_up,
        on_scroll_down=scroll_down,
    )
