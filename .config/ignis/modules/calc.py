from ignis.widgets import Widget
import subprocess


def calc_button() -> Widget.Button:
    def on_click(_btn):
        subprocess.Popen([
            "bash", "-c",
            'expr=$(printf "" | fuzzel --dmenu --prompt="calc: "); '
            '[ -z "$expr" ] && exit 0; '
            'result=$(echo "$expr" | bc -l 2>&1); '
            '[ -z "$result" ] && exit 0; '
            'result=$(echo "$result" | sed "/\\./ s/0*$//; s/\\.$//"); '
            'echo -n "$result" | wl-copy; '
            'notify-send -t 3000 "󰃬 $expr" "= $result (copied)"'
        ])

    return Widget.Button(
        child=Widget.Label(label="󰃬", css_classes=["module-icon", "calc-icon"]),
        css_classes=["calc-button"],
        on_click=on_click,
        tooltip_text="Calculator",
    )
