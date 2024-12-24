from trame.app import get_server
from trame.widgets import vtk as tvtk, vuetify
from trame.ui.vuetify import SinglePageWithDrawerLayout

import json

server = get_server(client_type="vue2")
state = server.state
ctrl = server.controller

state.sgnodeList = json.loads(
    """[
    {
        "name": "First",
        "visible": false,
        "selfcolor": "#ff643d",
        "selected": true
    },
    {
        "name": "Second",
        "visible": true,
        "selfcolor": "green",
        "selected": false
    }
]"""
)


def changeSelected():
    print("changing selected")


with SinglePageWithDrawerLayout(server, style="overflow: hidden") as layout:
    layout.title.set_text("My App")

    with layout.drawer:
        with vuetify.VList(shaped=True):
            with vuetify.VListItem(v_for="val, idx in sgnodeList", key="idx"):
                vuetify.VSwitch(
                    v_model=("val.visible",),
                    color=("val.selfcolor",),
                )
                with vuetify.VListItemContent():
                    vuetify.VListItemTitle("{{val.name}}")

                vuetify.VCheckbox(
                    v_model=("val.selected",),
                    click=changeSelected,
                )

if __name__ == "__main__":
    server.start()
