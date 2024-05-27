"""
pip install trame trame-vuetify
python ./495.py
"""

from trame.app import get_server
from trame.ui.vuetify3 import VAppLayout
from trame.widgets import vuetify3, html, client

server = get_server(client_type="vue3")

# 1. Grab the font
server.enable_module(
    {
        "styles": [
            "https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.2.0/dist/tabler-icons.min.css"
        ]
    }
)


with VAppLayout(server, full_height=True):
    # 2. Force .ti font-family
    client.Style(".ti:before{font-family:tabler-icons!important}")

    with vuetify3.VContainer(fluid=True, classes="full-height"):
        # MDI
        with vuetify3.VCard(classes="d-flex justify-space-around align-center ma-4"):
            vuetify3.VIcon(
                color="green-darken-2",
                icon="mdi-domain",
                size="x-small",
            )
            vuetify3.VIcon(
                color="blue-darken-2",
                icon="mdi-message-text",
                size="small",
            )
            vuetify3.VIcon(
                color="purple-darken-2",
                icon="mdi-dialpad",
                size="medium",
            )
            vuetify3.VIcon(
                color="teal-darken-2",
                icon="mdi-email",
                size="large",
            )
            vuetify3.VIcon(
                color="blue-grey-darken-2",
                icon="mdi-call-split",
                size="x-large",
            )
            vuetify3.VIcon(
                color="orange-darken-2",
                icon="mdi-arrow-up-bold-box-outline",
                size="large",
            )

        with vuetify3.VCard(classes="d-flex justify-space-around align-center  ma-4"):
            with vuetify3.VBtn("Accept", classes="ma-2", color="primary"):
                vuetify3.VIcon(icon="mdi-checkbox-marked-circle", end=True)
            with vuetify3.VBtn("Decline", classes="ma-2", color="red"):
                vuetify3.VIcon(icon="mdi-cancel", end=True)
            with vuetify3.VBtn(classes="ma-2") as btn:
                vuetify3.VIcon(icon="mdi-minus-circle", start=True)
                btn.add_child("Cancel")

            with vuetify3.VBtn(classes="ma-2", color="orange-darken-2") as btn:
                vuetify3.VIcon(icon="mdi-arrow-left", start=True)
                btn.add_child("Back")

            with html.Div():
                vuetify3.VBtn(classes="ma-2", color="purple", icon="mdi-wrench")
                vuetify3.VBtn(classes="ma-2", color="indigo", icon="mdi-cloud-upload")

            with html.Div():
                vuetify3.VBtn(
                    classes="ma-2",
                    color="blue-lighten-2",
                    icon="mdi-thumb-up",
                    variant="text",
                )
                vuetify3.VBtn(
                    classes="ma-2",
                    color="red-lighten-2",
                    icon="mdi-thumb-down",
                    variant="text",
                )

        # Tabler
        with vuetify3.VCard(classes="d-flex justify-space-around align-center ma-4"):
            vuetify3.VIcon(
                color="green-darken-2",
                icon="ti ti-ghost-2",
                size="x-small",
            )
            vuetify3.VIcon(
                color="blue-darken-2",
                icon="ti ti-ghost-3",
                size="small",
            )
            vuetify3.VIcon(
                color="purple-darken-2",
                icon="ti ti-pacman",
                size="medium",
            )
            vuetify3.VIcon(
                color="teal-darken-2",
                icon="ti ti-layout-sidebar-right",
                size="large",
            )
            vuetify3.VIcon(
                color="blue-grey-darken-2",
                icon="ti ti-layout-sidebar-right-filled",
                size="x-large",
            )
            vuetify3.VIcon(
                color="orange-darken-2",
                icon="ti ti-brand-qq",
                size="large",
            )

        with vuetify3.VCard(classes="d-flex justify-space-around ma-4"):
            with vuetify3.VBtn("Accept", classes="ma-2", color="primary"):
                vuetify3.VIcon(icon="ti ti-ghost", end=True)
            with vuetify3.VBtn("Decline", classes="ma-2", color="red"):
                vuetify3.VIcon(icon="ti ti-ghost-2", end=True)
            with vuetify3.VBtn(classes="ma-2") as btn:
                vuetify3.VIcon(icon="ti ti-arrow-roundabout-right", start=True)
                btn.add_child("Cancel")

            with vuetify3.VBtn(classes="ma-2", color="orange-darken-2") as btn:
                vuetify3.VIcon(icon="ti ti-arrow-roundabout-right", start=True)
                btn.add_child("Back")

            with html.Div():
                vuetify3.VBtn(
                    classes="ma-2", color="purple", icon="ti ti-wrecking-ball"
                )
                vuetify3.VBtn(classes="ma-2", color="indigo", icon="ti ti-cloud-upload")

            with html.Div():
                vuetify3.VBtn(
                    classes="ma-2",
                    color="blue-lighten-2",
                    icon="ti ti-thumb-up",
                    variant="text",
                )
                vuetify3.VBtn(
                    classes="ma-2",
                    color="red-lighten-2",
                    icon="ti ti-thumb-down",
                    variant="text",
                )

server.start()
