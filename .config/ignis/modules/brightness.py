from ignis.widgets import Widget


def brightness() -> Widget.EventBox:
    try:
        from ignis.services.backlight import BacklightService
        bl = BacklightService.get_default()
    except Exception:
        return Widget.EventBox(visible=False)

    if not bl.available:
        return Widget.EventBox(visible=False)

    def _percent() -> int:
        if bl.max_brightness <= 0:
            return 0
        return round(bl.brightness / bl.max_brightness * 100)

    icon = Widget.Icon(
        image="display-brightness-symbolic",
        pixel_size=20,
        css_classes=["module-icon", "brightness-icon"],
        halign="center",
    )
    value_label = Widget.Label(
        label=str(_percent()),
        css_classes=["module-value", "brightness-value"],
        halign="center",
    )

    def update(*_args):
        value_label.set_label(str(_percent()))

    bl.connect("notify::brightness", update)

    def scroll_up(_box):
        step = max(1, bl.max_brightness // 20)
        bl.set_brightness_async(min(bl.max_brightness, bl.brightness + step))

    def scroll_down(_box):
        step = max(1, bl.max_brightness // 20)
        bl.set_brightness_async(max(0, bl.brightness - step))

    return Widget.EventBox(
        vertical=True,
        css_classes=["module", "brightness"],
        child=[icon, value_label],
        on_scroll_up=scroll_up,
        on_scroll_down=scroll_down,
    )
