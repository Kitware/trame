import time
from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller


@ctrl.trigger("generate_content")
def generate_content():
    return f"Hello on the server is {time.time()}"


# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

layout = SinglePageLayout(server)

with layout:
    with layout.toolbar as toolbar:
        toolbar.clear()
        vuetify.VSpacer()
        vuetify.VBtn(
            "Download",
            click="utils.download('hello.txt', trigger('generate_content'), 'text/plain')",
        )


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
