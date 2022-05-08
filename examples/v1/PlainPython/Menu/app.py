from trame import state
from trame.html import vuetify
from trame.layouts import SinglePage

layout = SinglePage("Menu example")

state.menu_items = ["one", "two", "three"]


def print_item(item):
    print("Clicked on", item)


with layout.toolbar:
    vuetify.VSpacer()
    with vuetify.VMenu():
        with vuetify.Template(v_slot_activator="{ on, attrs }"):
            with vuetify.VBtn(icon=True, v_bind="attrs", v_on="on", v_on_click="test"):
                vuetify.VIcon("mdi-dots-vertical")
        with vuetify.VList(), vuetify.VListItem(
            v_for="(item, i) in menu_items",
            key="i",
            value=["item"],
        ):
            vuetify.VBtn(
                "{{ item }}",
                click=(print_item, "[item]"),
            )

if __name__ == "__main__":
    layout.start()
