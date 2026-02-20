from ignis.widgets import Widget
from ignis.services.niri import NiriService


def workspaces() -> Widget.Box:
    niri = NiriService.get_default()
    container = Widget.Box(
        vertical=True,
        css_classes=["workspaces"],
    )

    def make_dot(ws):
        classes = ["ws-dot"]
        if ws.is_focused:
            classes.append("focused")
        elif ws.is_active:
            classes.append("active")

        return Widget.Button(
            css_classes=classes,
            on_click=lambda _btn, ws_ref=ws: ws_ref.switch_to(),
            child=Widget.Label(label=""),
        )

    def rebuild(*_args):
        children = []
        for ws in niri.workspaces:
            children.append(make_dot(ws))
        container.set_child(children)

    def refresh_active(*_args):
        ws_list = niri.workspaces
        for i, child in enumerate(container):
            if i >= len(ws_list):
                break
            ws = ws_list[i]
            classes = ["ws-dot"]
            if ws.is_focused:
                classes.append("focused")
            elif ws.is_active:
                classes.append("active")
            child.set_css_classes(classes)

    niri.connect("notify::workspaces", rebuild)
    niri.connect("notify::active-window", refresh_active)

    rebuild()
    return container
