from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

state.visibilityList = [True, False, True, False]


def update_visibility(index, visibility):
    state.visibilityList[index] = visibility
    state.dirty("visibilityList")
    print(f"Toggle {index} to {visibility}")


with SinglePageLayout(server) as layout:
    with layout.content:
        with vuetify.VContainer(fluid=True, classes="fill-height pa-0 ma-0"):
            with vuetify.VCol():
                vuetify.VCheckbox(
                    v_for="v, i in visibilityList",
                    key="i",
                    label=("`Hello ${i}`",),
                    v_model=("visibilityList[i]",),
                    change=(update_visibility, "[i, $event]"),
                )


if __name__ == "__main__":
    server.start()
