import time

import trame.widgets.vuetify3 as v3
from trame.app import get_server, asynchronous
from trame.ui.vuetify3 import VAppLayout


# -------------------------------------------------------------------
# Helper
# -------------------------------------------------------------------


class AsyncTracker:
    def __init__(self, server, name):
        self.name = name
        self.server = server
        self.state = server.state

    async def __aenter__(self):
        with self.state:
            self.state[self.name] = True
        await self.server.network_completion

    async def __aexit__(self, exc_t, exc_v, exc_tb):
        with self.state:
            self.state[self.name] = False
        await self.server.network_completion


# -------------------------------------------------------------------


def long_task():
    time.sleep(2)
    print("Finished")


async def run_long_task():
    async with AsyncTracker(server, "loading"):
        long_task()


def run_task():
    asynchronous.create_task(run_long_task())


# -------------------------------------------------------------------

server = get_server()
state = server.state

with VAppLayout(server) as layout:
    with layout:
        with v3.Template():
            with v3.VOverlay(
                v_model=("loading", False),
                classes="align-center justify-center",
                close_on_content_click=False,
                persistent=True,
                style="z-index: 10000;",
            ):
                v3.VProgressCircular(color="primary", size=64, indeterminate=True)
        v3.VBtn("Long task (no tracking)", click=long_task)
        v3.VBtn("Long task (tracking)", click=run_task)


if __name__ == "__main__":
    server.start()
