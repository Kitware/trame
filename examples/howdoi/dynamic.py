import asyncio
from trame import state
from trame.layouts import SinglePage
from trame.html import vuetify

coundown_init = 10

# Timer to dynamically change shared state "countdown"
async def start_countdown():
    try:
        state.countdown = int(state.countdown)
    except:
        state.countdown = coundown_init

    while state.countdown > 0:
        await asyncio.sleep(0.5)
        state.countdown -= 1
        state.flush("countdown")


layout = SinglePage("Coundown")
layout.title.set_text("Countdown")

with layout.toolbar:
    vuetify.VSpacer()
    vuetify.VBtn(
        "Start countdown",
        click=start_countdown,
    )

with layout.content:
    vuetify.VTextField(
        v_model=("countdown", coundown_init),
        classes="ma-8",
    )

if __name__ == "__main__":
    layout.start()
