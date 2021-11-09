from trame import change, update_state, get_state
from trame.layouts import SinglePage
from trame.html import Div, vuetify


# Model
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
    vuetify.VBtn("Increment", click=increment),
    vuetify.VTextField(v_model=("myNumber", initial_number)),
    vuetify.VBtn("Decrement", click=decrement),
    vuetify.VSlider(v_model=("myNumber",)),
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
