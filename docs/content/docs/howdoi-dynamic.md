# How do I render dynamic content?
<!--
from trame import start, update_state, get_state
from trame.layouts import SinglePage
from trame.html import vuetify

countdown_start = 10

button = vuetify.VInput(
    v_model=("countdown", countdown_start),  # Shared state reference with initial value
    classes="ma-8",  # spacing
)

layout = SinglePage("Counting down")
layout.title.content = "Counting down"
layout.content.children += [button]


async def change_timer():
    while True:
        await asyncio.sleep(1)
        (countdown,) = get_state("countdown")
        update_state("countdown", countdown - 1)


if __name__ == "__main__":
    start(layout)

    change_timer()
-->
