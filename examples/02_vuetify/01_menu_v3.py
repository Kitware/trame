from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3 as v3


class Demo(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)

        # Set state values
        self.state.trame__title = "Menu example"
        self.state.menu_items = ["one", "two", "three"]

        self._build_ui()

    def _build_ui(self):
        with SinglePageLayout(self.server) as self.ui:
            with self.ui.toolbar:
                v3.VSpacer()
                with v3.VMenu():
                    with v3.Template(v_slot_activator="{ props }"):
                        v3.VBtn(icon="mdi-dots-vertical", v_bind="props")

                    with v3.VList():
                        v3.VListItem(
                            v_for="(item, i) in menu_items",
                            key="i",
                            value=("item",),
                            click=(self.print_item, "[item]"),
                            title=("item",),
                        )


    def print_item(self, item):
        print("Clicked on", item)


if __name__ == "__main__":
    app = Demo()
    app.server.start()
