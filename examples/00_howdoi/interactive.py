r"""
Installation requirements:
    pip install trame trame-vuetify
"""

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import html, vuetify

server = get_server(client_type="vue2")
state = server.state

# Initial state values
DEFAULT_VALUE = 5
state.trame_title = "Counter"


# Updates
def increment():
    state.my_number += 1


def decrement():
    state.my_number -= 1


@state.change("my_number")
def validate_my_number(my_number, **kwargs):
    if isinstance(my_number, int):
        # Prevent infinite loop
        return

    try:
        state.my_number = int(my_number)
    except:
        state.my_number = DEFAULT_VALUE


with SinglePageLayout(server) as layout:
    layout.title.set_text("Simple Counter Demo")

    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VBtn("-", click=decrement)
        vuetify.VBtn("+", click=increment)

    with layout.content:
        with html.Div(classes="ma-8"):
            vuetify.VTextField(v_model=("my_number", DEFAULT_VALUE))
            vuetify.VSlider(v_model=("my_number",))


if __name__ == "__main__":
    server.start()
