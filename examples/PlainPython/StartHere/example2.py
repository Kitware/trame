from trame import change, update_state, get_state
from trame.layouts import SinglePage
from trame.html.vuetify import VBtn, VTextField
from trame.html import Div


# Mode
initial_number = 5


# Updates
def increment():
    (number,) = get_state("myNumber")
    update_state("myNumber", number + 1)


def decrement():
    (number,) = get_state("myNumber")
    update_state("myNumber", number - 1)


@change("myNumber")
def validateMyNumber(myNumber, **kwargs):
    try:
        newNumber = int(myNumber)
        update_state("myNumber", newNumber)
    except:
        update_state("myNumber", initial_number)


# Views
controls = [
    VBtn("Increment", click=increment),
    VTextField(v_model=("myNumber", initial_number)),
    VBtn("Decrement", click=decrement),
]


layout = SinglePage("Counter")
layout.title.content = "Simple Counter Demo"
layout.content.children += [
    Div(
        controls,
        classes="ma-8",
    )
]


if __name__ == "__main__":
    layout.start()
