r"""
Installation requirements:
    pip install trame trame-vuetify
"""

from trame.app import get_server
from trame.widgets import vuetify
from trame.ui.vuetify import SinglePageLayout

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

state.menu_items = ["one", "two", "three"]


def print_item(item):
    print("Clicked on", item)


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

state.trame__title = "Menu example"

with SinglePageLayout(server) as layout:
    with layout.toolbar:
        vuetify.VSpacer()
        with vuetify.VMenu():
            with vuetify.Template(v_slot_activator="{ on, attrs }"):
                with vuetify.VBtn(icon=True, v_bind="attrs", v_on="on"):
                    vuetify.VIcon("mdi-dots-vertical")
            with vuetify.VList():
                with vuetify.VListItem(
                    v_for="(item, i) in menu_items",
                    key="i",
                    value=["item"],
                ):
                    vuetify.VBtn(
                        "{{ item }}",
                        click=(print_item, "[item]"),
                    )

if __name__ == "__main__":
    server.start()
