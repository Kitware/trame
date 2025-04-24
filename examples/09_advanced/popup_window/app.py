from trame.app import get_server
from trame.ui.vuetify3 import SinglePageLayout, VAppLayout
from trame.widgets import vuetify3


class MultiWindow:
    def __init__(self, server=None, table_size=10):
        self.server = get_server(server, client_type="vue3")

        # Create local variable for JS side
        self.state.update(dict(window_hello=None, window_world=None))
        self.state.client_only("window_hello", "window_world")

        # Force ui creation
        self.ui = self.ui_main
        self.popup_hello = self.ui_hello
        self.popup_world = self.ui_world

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    @property
    def ui_main(self):
        with SinglePageLayout(self.server, full_height=True) as layout:
            with layout.toolbar.clear():
                vuetify3.VToolbarTitle("Multi Window example")
                vuetify3.VSpacer()
                vuetify3.VBtn(
                    "Open Hello",
                    disabled=("window_hello",),
                    click="""
                        window_hello = window.open(
                            '/?ui=hello',
                            target='_blank',
                            'popup,width=200,height=200,left=10,top=10'
                        )
                    """,
                )
                vuetify3.VBtn(
                    "Close Hello", click="window_hello.close(); window_hello = null;"
                )
                vuetify3.VBtn(
                    "Open World",
                    disabled=("window_world",),
                    click="""
                        window_world = window.open(
                            '/?ui=world',
                            target='_blank',
                            'popup,width=200,height=200,left=100,top=100'
                        )
                    """,
                )
                vuetify3.VBtn(
                    "Close World", click="window_world.close(); window_world = null;"
                )
            with layout.content:
                with vuetify3.VContainer():
                    with vuetify3.VCard():
                        vuetify3.VCardTitle("Main Page")

    @property
    def ui_hello(self):
        with VAppLayout(self.server, template_name="hello", full_height=True):
            with vuetify3.VContainer():
                with vuetify3.VCard():
                    vuetify3.VCardTitle("Hello Page")

    @property
    def ui_world(self):
        with VAppLayout(self.server, template_name="world", full_height=True):
            with vuetify3.VContainer():
                with vuetify3.VCard():
                    vuetify3.VCardTitle("World Page")


def main():
    app = MultiWindow()
    app.server.start()


if __name__ == "__main__":
    main()
