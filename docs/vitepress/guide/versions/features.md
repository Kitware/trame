# Features by versions

## Version 3.10

This version is bringing a new tool around VTK for debugging remote rendering deployment.
More information are captured [here](https://trame.readthedocs.io/en/latest/tools.vtk.html).

## Version 3.9

This version is bringing new classes to help with application or component setup.

Here is an example for on how to use them.

```python
from trame.app import TrameApp
from trame.decorators import change, controller, life_cycle, trigger
from trame.ui.html import DivLayout
from trame.widgets import html


class App(TrameApp):
    def __init__(self, name=None):
        super().__init__(name)
        self._build_ui()

    @trigger("exec")
    def method_call(self, msg):
        print("method_called", msg)

    @controller.set("hello")
    def method_on_ctrl(self, *args):
        print("method_on_ctrl", args)

    @change("resolution")
    def one_slider(self, resolution, **kwargs):
        print("Slider value 1", resolution)

    @life_cycle.server_ready
    def on_ready(self, *args, **kwargs):
        print("on_ready")

    def _build_ui(self):
        with DivLayout(self.server) as self.ui:
            html.Input(
                type="range",
                min=3,
                max=60,
                step=1,
                v_model_number=("resolution", 6),
            )
            html.Button("trigger", click="trigger('exec', ['trigger'])")
            html.Button("method", click=(self.method_call, "['method']"))
            html.Button("ctrl", click=self.ctrl.hello)


if __name__ == "__main__":
    app = App()
    app.server.start()
```

On top of those classes, some improvements have been made for handling properties and events regardless of them being registered.
Here are some examples on how to make use of them. Also widgets support method decorators like the TrameApp base class.

```python
html.Div(
    v_on_click_prevent_stop="...", # => @click.prevent.stop="..."
    v_bind_hello_world="...", # => :hello.world="..."
)
```

## Version 3.8

The @TrameApp decorator now support inheritance. 

## Version 3.7

DeepReactive available in `client` for vue3 only.

## Version 3.6

New network layer relying on binary message exchange with automatic chunking to enable large data exchange without timeout or proxy disconnection. 

## Version 3.5

vue3 is the new default in get_server and docker setup.

## Version 3.4

Infrastructure for enabling namespace isolation via child_server.

## Version 3.3

A new tool is available for serving an application for multiple users from a single process. The documentation is available [here](https://trame.readthedocs.io/en/latest/tools.serve.html) and for it to work, the application needs to expect a server in its constructor.

```bash
# Assuming the code from 3.1 exist in a MyApp.py file
# you can run it with the following command line

python -m trame.tools.serve --exec MyApp:App
```

## Version 3.2

A new tool is available for generating widgets from a YAML description file. The usage documentation is available [here](https://trame.readthedocs.io/en/latest/tools.widgets.html). 


## Version 3.1

A new @TrameApp() decorator is available to help creating classes with method decorator. The following example illustrate such usage.

```python
from trame.app import get_server
from trame.decorators import TrameApp, change, controller, life_cycle, trigger
from trame.ui.html import DivLayout
from trame.widgets import html


@TrameApp()
class App:
    def __init__(self, name=None):
        self.server = get_server(name)
        self.ui()

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    @trigger("exec")
    def method_call(self, msg):
        print("method_called", msg)

    @controller.set("hello")
    def method_on_ctrl(self, *args):
        print("method_on_ctrl", args)

    @change("resolution")
    def one_slider(self, resolution, **kwargs):
        print("Slider value 1", resolution)

    @life_cycle.server_ready
    def on_ready(self, *args, **kwargs):
        print("on_ready")

    def ui(self):
        with DivLayout(self.server):
            html.Input(
                type="range",
                min=3,
                max=60,
                step=1,
                v_model_number=("resolution", 6),
            )
            html.Button("trigger", click="trigger('exec', ['trigger'])")
            html.Button("method", click=(self.method_call, "['method']"))
            html.Button("ctrl", click=self.ctrl.hello)


if __name__ == "__main__":
    app = App()
    app.server.start()
```