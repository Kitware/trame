r"""
Version for trame 1.x - https://github.com/Kitware/trame/blob/release-v1/examples/howdoi/dynamic.py
Delta v1..v2          - https://github.com/Kitware/trame/commit/3ee54ce5b663bf2af12b3fbdda7aab944fb86298

Installation requirements:
    pip install trame trame-vuetify
"""

import asyncio
from trame.app import get_server, asynchronous
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify

coundown_init = 10

server = get_server()
state = server.state
state.trame__title = "Coundown"


@asynchronous.task
async def start_countdown():
    try:
        state.countdown = int(state.countdown)
    except:
        state.countdown = coundown_init

    while state.countdown > 0:
        with state:
            await asyncio.sleep(0.5)
            state.countdown -= 1


with SinglePageLayout(server) as layout:
    layout.title.set_text("Countdown")

    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VBtn(
            "Start countdown",
            click=start_countdown,
        )

    with layout.content:
        vuetify.VTextField(
            v_model=("countdown", coundown_init),
            classes="ma-8",
        )

if __name__ == "__main__":
    server.start()
