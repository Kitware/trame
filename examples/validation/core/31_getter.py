from trame.app import get_server
from trame.widgets import client, vuetify
from trame.ui.vuetify import SinglePageLayout

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller

state.message_1 = "Hello 1"
state.message_2 = "Hello 2"
state.message_3 = "Hello 3"

state.msg_idx = 1


# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

with SinglePageLayout(server) as layout:
    # Toolbar
    with layout.toolbar as toolbar:
        vuetify.VSpacer()
        vuetify.VBtn("1", click="msg_idx = 1")
        vuetify.VBtn("2", click="msg_idx = 2")
        vuetify.VBtn("3", click="msg_idx = 3")
        vuetify.VBtn(
            "Revert",
            click="""
            name = `message_${msg_idx}`;
            set(name, get(name).split('').reverse().join(''))
        """,
        )

    with layout.content:
        with vuetify.VContainer():
            with vuetify.VRow():
                with vuetify.VCol():
                    with vuetify.VCard(style="height: 200px;"):
                        vuetify.VCardTitle("get function")
                        vuetify.VDivider()
                        vuetify.VCardText(">>> {{ get(`message_${msg_idx}`) }}")

                with vuetify.VCol():
                    with vuetify.VCard(style="height: 200px;"):
                        vuetify.VCardTitle("getter")
                        vuetify.VDivider()
                        with client.Getter(name=("`message_${msg_idx}`",)):
                            vuetify.VCardText(">>> {{ value }}")

                with vuetify.VCol():
                    with vuetify.VCard(style="height: 200px;"):
                        vuetify.VCardTitle("getter with rename")
                        vuetify.VDivider()
                        with client.Getter(
                            name=("`message_${msg_idx}`",), value_name="msg"
                        ):
                            vuetify.VCardText(">>> {{ msg }}")


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
