from trame.app import get_server
from trame.widgets import trame, vuetify, html
from trame.ui.vuetify import SinglePageLayout

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state = server.state

CURSORS = [
    "auto",
    "default",
    "none",
    "context-menu",
    "help",
    "pointer",
    "progress",
    "wait",
    "cell",
    "crosshair",
    "text",
    "vertical-text",
    "alias",
    "copy",
    "move",
    "no-drop",
    "not-allowed",
    "grab",
    "grabbing",
    "e-resize",
    "n-resize",
    "ne-resize",
    "nw-resize",
    "s-resize",
    "se-resize",
    "sw-resize",
    "w-resize",
    "ew-resize",
    "ns-resize",
    "nesw-resize",
    "nwse-resize",
    "col-resize",
    "row-resize",
    "all-scroll",
    "zoom-in",
    "zoom-out",
]

# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

with SinglePageLayout(server) as layout:
    layout.icon.click = f"active = (active + 1) % {len(CURSORS)}"
    layout.title.set_text("Toggle Cursor")

    trame.Cursor(
        active=("active", 0),
        cursors=("options", CURSORS),
    )

    with layout.toolbar:
        trame.Cursor(
            active=("active + 1",),
            cursors=("options", CURSORS),
        )
        html.Div(
            "({{ options[active + 1] }})",
            classes="ml-2",
            style="text-overflow: ellipsis;",
        )
        vuetify.VSpacer()
        vuetify.VChip("{{ active }}")
        vuetify.VSlider(
            dense=True,
            hide_details=True,
            v_model="active",
            min=0,
            max=len(CURSORS) - 1,
            style="max-width: 200px;",
        )

    with layout.content:
        with vuetify.VContainer(fluid=True):
            with vuetify.VCol():
                with vuetify.VRow(style="background: red;"):
                    html.Div("{{ options[active + 2] }}", classes="pa-6")
                    trame.Cursor(
                        active=("active + 2",),
                        cursors=("options", CURSORS),
                    )
                with vuetify.VRow():
                    html.Div("{{ options[active] }}", classes="pa-6")


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
