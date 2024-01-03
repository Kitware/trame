from trame.app import get_server
from trame.widgets import html, vuetify
from trame.ui.vuetify import SinglePageLayout

from trame_server.utils.hot_reload import hot_reload

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# Can do `export TRAME_HOT_RELOAD=1` instead
server.hot_reload = True

# Way to enable widgets when UI creation is deferred after server.start()
html.initialize(server)
vuetify.initialize(server)


# -----------------------------------------------------------------------------
# Dynamically modify any `ChangeMe` to see the new code execute while
# interacting with the app.
# -----------------------------------------------------------------------------
@ctrl.set("number_reset")
def reset_number():
    print("reset_number::ChangeMe")
    state.number = 6
    state.size = 1
    do_someting()


@state.change("number")
def update_number(number, **kwargs):
    print("update_number::ChangeMe", number)
    do_someting()


@hot_reload
def do_someting():
    print("do_someting::ChangeMe")


@ctrl.add("on_server_bind")  # on_server_bind => fn(aiohttp_server)
@ctrl.add("on_server_reload")  # on_server_reload => fn()
def setup_ui(*_):
    with SinglePageLayout(server) as layout:
        layout.title.set_text("Hot Reload - ChangeMe")
        layout.toolbar.dense = True

        # Toolbar
        with layout.toolbar as toolbar:
            vuetify.VSpacer()
            vuetify.VSlider(
                hide_details=True,
                v_model=("number", 6),
                max=60,
                min=3,
                step=1,
                style="max-width: 300px;",
            )
            vuetify.VSlider(
                label="size",
                hide_details=True,
                v_model=("size", 2),
                max=10,
                min=1,
                step=1,
                style="max-width: 300px;",
            )
            with vuetify.VBtn(icon=True, click=ctrl.number_reset):
                vuetify.VIcon("mdi-undo")

        with layout.content:
            with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                with vuetify.VCol():
                    html.Div(
                        "{{ number }} x {{ i }} = {{ number * i }}",
                        v_for="i in size",
                        key="i",
                        classes="mx-auto text-h6 text-center",
                    )


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
