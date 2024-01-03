import time
import asyncio
from trame.app import get_server
from trame.widgets import vuetify, html
from trame.ui.vuetify import SinglePageLayout

# -----------------------------------------------------------------------------
# Trame app
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state = server.state

# -----------------------------------------------------------------------------
# State setup
# -----------------------------------------------------------------------------

state.a = 1
state.b = 0
state.c = 1
state.d = 0


@state.change("a")
async def change_a(a, c, **kwargs):
    print(f"(a) server state {a=} {c=}")
    await asyncio.sleep(2)  # async 2s wait
    with state:
        state.b = a * 2


@state.change("c")
def change_c(a, c, **kwargs):
    print(f"(c) server state {a=} {c=}")
    time.sleep(2)  # busy 2s wait
    state.d = c * 2


# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

with SinglePageLayout(server) as layout:
    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VSlider(
            label="a",
            value=("get('a')",),
            hide_details=True,
            dense=True,
            disabled=True,
        )
        vuetify.VSlider(
            label="c",
            value=("get('c')",),
            hide_details=True,
            dense=True,
            disabled=True,
        )

    with layout.content:
        with vuetify.VContainer(fluid=True):
            html.Div("(Async) a={{a}} b={{b}} | (Busy) c={{c}} d={{d}}")
            vuetify.VSlider(v_model=("a", 0), label="Async server handling (a)")
            vuetify.VSlider(v_model=("c", 0), label="Busy server handling (c)")

# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
