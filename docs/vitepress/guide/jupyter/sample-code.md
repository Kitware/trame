# Sample code

In the introduction we just imported an existing example application, but let's look at its internal and explain it.

::: code-group
<<< @/../../trame/app/demo.py
:::

## Key take away

When a trame application is laid out like above, you can just run the following inside a cell to access it.

```python
from module import App

app = App()
await app.ui.ready
app.ui
```

And in case you want to have a second instance independent of the first one, you can do

```python
app2 = App('v2')
await app2.ui.ready
app2.ui
```

## Changing application state

In trame you simply can change a state variable to see the change reflected in the UI. But when doing that in another cell, it does not seems to work. 
The reason is the same as when you update a state variable from an asynchronous task, you need to be explicit when the state synchronization needs to happen. A simpler way to do that is to use the state as context manager like below.

```python
with app.state:
    app.state.resolution = 24
```

That is why in our setter we added such logic which allow us to simply call from anywhere

```python
app.resolution = 32
```

## Create several small UI

```python
from trame.app import get_server
from trame.widgets import html
from trame.ui.html import DivLayout

server = get_server()
state = server.state

def reset_slider():
    state.slider_a = 2

@state.change("slider_a")
def udpate_result(slider_a, **_):
    state.result = slider_a / 2

with DivLayout(server, 'a', height=30) as ui_a:
    html.Input(
        type="range", 
        min=-1, 
        max=50, 
        step=0.1, 
        v_model_number=("slider_a", 2), 
        style="width: 100%;",
    )

await ui_a.ready
ui_a
```

Then you can create more ui on the same server

```python
with DivLayout(server, 'b', height=30) as ui_b:
    html.Button(
        "Reset Value", 
        click=reset_slider,
    )
    html.Span("{{ slider_a }} / 2 = {{ result }}", style="margin-left: 2rem")

ui_b
```

![Multi-UI in Jupyter](/assets/images/jupyter/multi-ui.png)
