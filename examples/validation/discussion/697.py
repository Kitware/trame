from trame.app import get_server
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3 as vuetify

server = get_server(client_type="vue3")
state, ctrl = server.state, server.controller

# Adding missing font
server.enable_module(
    {"styles": ["https://fonts.googleapis.com/css?family=Roboto:300,400,500"]}
)

with SinglePageLayout(server) as layout:
    with layout.content:
        with vuetify.VContainer(
            fluid=True,
            classes="d-flex justify-center align-center",
            style="height: 100%;",
        ):
            with vuetify.VCard():
                with vuetify.VCardTitle(
                    "Centered Card",
                    classes="d-flex align-center flex-wrap",
                    # style="font-weight: 500 !important"
                ):
                    vuetify.VSpacer()
                    vuetify.VBtn(icon="mdi-refresh", density="compact")
                vuetify.VDivider()
                with vuetify.VCardText():
                    vuetify.VTextField(
                        v_model=("text_value", ""),
                        label="Some text",
                        placeholder="Type here...",
                        variant="outlined",
                    )

    # print(layout)

server.start()
