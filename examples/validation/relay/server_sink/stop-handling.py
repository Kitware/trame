from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")


async def stop_server():
    await server.stop()


# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

layout = SinglePageLayout(server)

with layout:
    # Title
    layout.title.set_text("Clean exit")

    # Toolbar
    with layout.toolbar as toolbar:
        toolbar.dense = True
        vuetify.VSpacer()
        vuetify.VBtn("Stop server", click=stop_server)

# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
