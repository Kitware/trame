import time

from trame.app import get_server
from trame.ui.html import DivLayout
from trame.widgets import html

# -----------------------------------------------------------------------------
# Trame app
# -----------------------------------------------------------------------------

server = get_server()
count = 1


def make_server_busy():
    time.sleep(1)


def update_title():
    global count
    server.state.trame__title = f"T({count})"
    count += 1


def update_favicon():
    global count
    server.state.trame__favicon = f"https://picsum.photos/id/{count}/32/32"
    count += 10


# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

with DivLayout(server) as layout:
    html.Div("trame__busy: {{ trame__busy }}")
    html.Button("Make server busy", click=make_server_busy)
    html.Button("Update title", click=update_title)
    html.Button("Update favicon", click=update_favicon)


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
