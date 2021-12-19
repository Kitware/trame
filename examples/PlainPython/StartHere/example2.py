from trame import state
from trame.layouts import SinglePage
from trame.html import Div, vuetify

# Mode
initial_number = 5


# Updates
def increment():
    state.myNumber += 1


def decrement():
    state.myNumber -= 1


@state.change("myNumber")
def validate_input(myNumber, **kwargs):
    try:
        state.myNumber = int(myNumber)
    except:
        state.myNumber = initial_number


layout = SinglePage("Counter")
layout.title.set_text("Simple Counter Demo")

with layout.content:
    with Div(classes="ma-8"):
        vuetify.VBtn("Increment", click=increment)
        vuetify.VTextField(v_model=("myNumber", initial_number))
        vuetify.VBtn("Decrement", click=decrement)

if __name__ == "__main__":
    layout.start()
