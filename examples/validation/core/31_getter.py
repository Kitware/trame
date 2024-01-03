from trame.app import get_server
from trame.widgets import client, vuetify
from trame.ui.vuetify import SinglePageLayout

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

state.message_1 = "Hello 1"
state.message_2 = "Hello 2"
state.message_3 = "Hello 3"

state.list_1 = [True, False, False]
state.list_2 = [False, True, False]
state.list_3 = [False, False, True]

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
                    with client.Getter(
                        name=("`message_${msg_idx}`",), key_name="var_key"
                    ):
                        with vuetify.VCard(style="height: 200px;"):
                            vuetify.VCardTitle("getter {{ var_key }}")
                            vuetify.VDivider()
                            vuetify.VCardText(">>> {{ value }}")

                with vuetify.VCol():
                    with vuetify.VCard(style="height: 200px;"):
                        vuetify.VCardTitle("getter with rename")
                        vuetify.VDivider()
                        with client.Getter(
                            name=("`message_${msg_idx}`",),
                            value_name="msg",
                            key_name="name",
                        ):
                            vuetify.VCardText(">>> {{ name }}={{ msg }}")

            with vuetify.VRow():
                with vuetify.VCol():
                    with client.Getter(
                        name=("`list_${msg_idx}`",),
                        key_name="name",
                        update_nested_name="update",
                    ):
                        with vuetify.VCard():
                            vuetify.VCardTitle("List {{ name }}")
                            vuetify.VDivider()
                            with vuetify.VCardText():
                                with vuetify.VList():
                                    with vuetify.VListItem(
                                        v_for="v, i in value", key="i"
                                    ):
                                        vuetify.VIcon(
                                            v_text="v ? 'mdi-eye' : 'mdi-eye-off'",
                                            click="update(i, !v)",
                                        )


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
