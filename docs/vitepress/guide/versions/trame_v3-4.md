# From v3 to v4

Trame v4 adds a second, first-class client type: `client_type="react"`. Where
you previously wrote `client_type="vue3"`, you can now target React instead —
and everything else about how you build a trame app stays the same. Same
`TrameApp` base class, same reactive `state`, same event/trigger model, same
Python-only workflow.

Here's a small example using [MUI](https://mui.com/), one of the most widely
adopted React component libraries, driven entirely from Python:

```python
from trame.app import TrameApp
from trame.ui.html import DivLayout
from trame.widgets import mui, react


class MuiDemo(TrameApp):
    def __init__(self, server=None):
        super().__init__(server, client_type="react")
        
        with DivLayout(self.server) as self.ui:
            with mui.Card(elevation=4), mui.CardContent():
                mui.Typography(["count = ", react.Bind("count", count=3)], variant="h5")
                mui.Slider(
                    value=react.Bind("count"),
                    on_change=react.Callback("count = Number($event.target.value)"),
                    min=0, max=10, step=1,
                )
                mui.Button("Reset", variant="contained", on_click=react.Callback(self.reset))

    def reset(self):
        self.state.count = 0
        
```

![](../../assets/images/examples/trame-mui.png)
