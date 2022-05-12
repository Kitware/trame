import asyncio
from trame.app import get_server, asynchronous
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify

# -----------------------------------------------------------------------------
# Trame app
# -----------------------------------------------------------------------------

server = get_server(ws_heart_beat=5)  # 5s
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# State setup
# -----------------------------------------------------------------------------

state.count = 1
state.running_jobs = 0


@asynchronous.task  # <--- if commented the heartbeat will think the server is dead and crash server
async def start_count():
    with state:
        state.count = 0
        state.running_jobs += 1

    for i in range(int(state.delta)):
        with state:
            state.count += 1
            await asyncio.sleep(0.5)

    with state:
        state.running_jobs -= 1


ctrl.run = start_count


# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------
layout = SinglePageLayout(server)

with layout:
    with layout.toolbar as tb:
        vuetify.VSpacer()
        tb.add_child("RunningTasks({{ running_jobs }}) - CountSize({{ delta }})")
        vuetify.VSlider(
            v_model=("delta", 10),
            min=10,
            max=100,
            step=1,
            hide_details=True,
            dense=True,
            classes="mx-4",
        )
        with vuetify.VBtn(icon=True, click=ctrl.run):
            vuetify.VIcon("mdi-run")

    with layout.content:
        with vuetify.VContainer() as container:
            container.add_child("{{ count }}")

# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
