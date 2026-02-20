from ignis.widgets import Widget
import subprocess


def power_button() -> Widget.Button:
    def on_click(_btn):
        options = "⏻ Shutdown\n Reboot\n⏾ Suspend\n Lock"
        try:
            result = subprocess.run(
                ["fuzzel", "--dmenu", "--prompt=Power: ", "--lines=4"],
                input=options,
                capture_output=True,
                text=True,
            )
            choice = result.stdout.strip()
            if "Shutdown" in choice:
                subprocess.Popen(["systemctl", "poweroff"])
            elif "Reboot" in choice:
                subprocess.Popen(["systemctl", "reboot"])
            elif "Suspend" in choice:
                subprocess.Popen(["systemctl", "suspend"])
            elif "Lock" in choice:
                subprocess.Popen(["swaylock"])
        except Exception:
            pass

    return Widget.Button(
        css_classes=["power-button"],
        on_click=on_click,
        child=Widget.Icon(image="system-shutdown-symbolic", pixel_size=22, css_classes=["power-icon"], halign="center"),
    )
