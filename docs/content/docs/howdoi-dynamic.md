# How do I render dynamic content?

This example illustrate how the server can dynamically change the value of variable and make them reflect on the client automatically.

This example is a little bit more complicated as it involve coding some asynchronous Python logic, but the key point to keep in mind is that the variable will automatically propagate to the client when changed on the server. The `flush_state` is only required when the server modify variable in an asynchronous manner.

## Code

```python
import asyncio
from trame import start, get_state, update_state, flush_state
from trame.layouts import SinglePage
from trame.html import vuetify

coundown_init = 10

# Timer to dynamically change shared state "countdown"
async def start_countdown():
    while True:
        try:  # catch int()
            await asyncio.sleep(1)
            (countdown,) = get_state("countdown")
            countdown = int(countdown)
            if countdown < 0:
                break
            update_state("countdown", countdown - 1)
            flush_state("countdown")
        except:
            pass


text = vuetify.VTextField(v_model=("countdown", coundown_init), classes="ma-8")
button = vuetify.VBtn("Start countdown", click=start_countdown)

layout = SinglePage("Coundown")
layout.title.content = "Countdown"
layout.toolbar.children += [vuetify.VSpacer(), button]
layout.content.children += [text]

if __name__ == "__main__":
    start(layout)
```

## Example

- [Code above](https://github.com/Kitware/trame/blob/master/examples/howdoi/dynamic.py)