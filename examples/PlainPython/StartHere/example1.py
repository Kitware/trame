from trame import update_state, get_state
from trame.layouts import SinglePage
from trame.html.vuetify import VBtn, VTextField
from trame.html import Div


# Model
initial_number = 5


# Updates
def increment():
    (number,) = get_state("myNumber")
    update_state("myNumber", number + 1)


def decrement():
    (number,) = get_state("myNumber")
    update_state("myNumber", number - 1)


# Views
controls = [
    VBtn("Increment", click=increment),
    VTextField(v_model=("myNumber", initial_number), readonly=True),
    VBtn("Decrement", click=decrement),
]


layout = SinglePage("Counter")
layout.title.set_text("Simple Counter Demo")
layout.content.children += [
    Div(
        controls,
        classes="ma-8",
    )
]


if __name__ == "__main__":
    layout.start()
