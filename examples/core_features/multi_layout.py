from trame.app import get_server
from trame.widgets import html
from trame.ui.html import DivLayout

# -----------------------------------------------------------------------------
# Trame app
# -----------------------------------------------------------------------------

server = get_server()

# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

with DivLayout(server):
    html.A("Open UI(a)", href="/?ui=a", target="_blank")
    html.Br()
    html.A("Open UI(b)", href="/?ui=b", target="_blank")

with DivLayout(server, "a"):
    html.Div("UI for A")

with DivLayout(server, "b"):
    html.Div("UI for B")

# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
