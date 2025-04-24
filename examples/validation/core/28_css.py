from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import client

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

STYLES = [
    "div { background: white; }",
    "div { background: red; }",
    "div { background: blue; }",
    "div { background: green; }",
    "div { background: gray; }",
]
STYLE_IDX = 0


def change_style():
    global STYLE_IDX
    STYLE_IDX += 1
    if len(STYLES) == STYLE_IDX:
        STYLE_IDX = 0
    ctrl.update_style(STYLES[STYLE_IDX])


# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

with SinglePageLayout(server) as layout:
    layout.icon.click = change_style
    layout.title.set_text("Toggle HTML Background")
    layout.toolbar.dense = True

    style = client.Style("div { background: orange }")
    ctrl.update_style = style.update


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
