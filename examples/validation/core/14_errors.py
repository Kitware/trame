import asyncio
import sys
from trame.app import get_server
from trame.widgets import trame, vuetify
from trame.ui.vuetify import SinglePageLayout

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller


def kill_server():
    sys.exit(0)


def throw_exception():
    raise Exception("That is an expected error")


async def fake_busy():
    print("start busy...")
    asyncio.sleep(5)
    print("end busy...")


ctrl.on_client_mounted.add(fake_busy)

# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

layout = SinglePageLayout(server)

with layout:
    # Validate client life cycle
    trame.LifeCycleMonitor(events=("['created']",))

    # Title
    layout.title.set_text("Cone")

    # Toolbar
    with layout.toolbar as toolbar:
        toolbar.dense = True
        vuetify.VSpacer()
        vuetify.VBtn("Kill server", click=kill_server)
        vuetify.VBtn("Server exception", click=throw_exception)
        vuetify.VBtn("JS Error", click="console.error('test')")

# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
