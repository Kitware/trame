# How to use trame

Trame aims to streamline the creation of visual analytics applications, with support for interactive data manipulation and visualization, through a very compact and simple API. This document describes the core API and concepts behind trame; the document is both a start up guide, but also a quick reference for those more familiar with trame.

## Core concepts

Trame allows you to easily share variables between UI components and a Python application. The resulting shared state can be modified by functions and methods invoked from the UI or application. For example, a Python function can be called when a button in the UI is clicked; or the UI can be updated in response to programmatic changes to the state. This document focuses on how you can leverage these capabilities inside your application using trame.

## Shared state

Trame mainly focuses on the Python side, therefore the variables that we aim to use across our application will be defined from Python. The following sections illustate the various ways the shared state can be modified.

![Shared state summary](/assets/images/course/state.jpg)

### UI element with a dynamic variable

The example below uses Vuetify to create a slider where the value is controlled by the slider. The variable `slider_value` is initialized with the value `8`. So variables in the shared state can be defined and initialized right were we want to use them when defining our UI elements. In this example, the slider will be able to modify that value but also will reflect its content if that value changes on the server side.

```python
from trame.widgets import vuetify

slider = vuetify.VSlider(
  label="Example",
  min=2,
  max=15,
  v_model=("slider_value", 8),
)
```

### Listening to changes

Imagine that we want to monitor the value of `slider_value` within our Python application and execute a method when that variable is updated. The code below illustate how we can annotate a function so it can be called when a value of the shared state is modified.

```python
from trame.app import get_server

server = get_server()
state = server.state

@state.change("slider_value")
def slider_value_change(slider_value, **kwargs):
  print(f"Slider is changing slider_value to {slider_value}")
```

So far, we only have the client modifying that variable. But if a function on the server were to change that variable, the function would also be called as we simply react to the fact that the variable has been updated by someone.

### Changing the value from Python

Within a Python trame application, it is possible to update the UI in response to read and even write operations to and from the shared state. The code below provides a function that will read the current value and update its content.

```python
from trame.app import get_server

server = get_server()
state = server.state

def random_update():
  state.slider_value += 1
  if state.slider_value > 15:
    state.slider_value = 2
```

### Forcing state exchange

Sometimes, the variable inside your shared state is an actual object with a nested structure. While the state on the Python side always maintains a reference to that object, when manually editing it's important to flush its contents so that the client reflects changes. In this situation, the `dirty()` method can be called with the list of variable names that should be pushed. 

Here is a simple example of what we mean by nested structure.

```python
from trame.app import get_server

server = get_server()
state = server.state

state.list_variable = []
state.dict_variable = {}

def edit_state():
  state.list_variable.append(f"new item {len(state.list_variable)}"")
  state.dict_variable["a"] = state.dict_variable.setdefault("a", 1) + 1
  state.dirty("list_variable", "dict_variable")
```

You can also decide when a state needs to be flushed using it as a context manager. 
Be aware that flushing will only work on variables that are known to be modified/dirty.
Also such flushing operation is mendatory when running in an async task or coroutine.
The code below provides a simple example.

```python
import asyncio
import time

async def update_time():
  while True:
    await asyncio.sleep(1)
    # needed because of async and will flush on exit
    with state: 
      # modification is automatically detected
      state.time = time.time()

      # dirty() is needed as we modify object in place
      # => python does not know that "list_variable" has changed
      state.list_variable.append(len(state.list_variable))
      state.dirty("list_variable")

```

## Method calls

When building a client/server application you will need to be able to trigger methods on both sides and trame has some easy ways to do that.

![Event summary](/assets/images/course/events.jpg)

### Bind method to a button click

The example below re-uses the function we had defined before but now we bind it to a button.

```python
from trame.app import get_server
from trame.widgets import vuetify

server = get_server()
state, ctrl = server.state, server.controller

change_btn = vuetify.VBtn(
  "Change slider_value",
  click=ctrl.rnd_update
)

def random_update():
  state.slider_value += 1
  if state.slider_value > 15:
    state.slider_value = 2

# Do the binding later on
ctrl.rnd_update = random_update
```

### Calling JavaScript methods

Some components in an application may have APIs that you be used and invoked from the Python side. The code below provides an example of such a use case:

```python
from trame.app import get_server
from trame.widgets import vtk

server = get_server()

html_view = vtk.VtkView(
  ref="vtkView", # Name to identify the Web component on which we want to call a method
  ...
)

def reset_camera():
  server.js_call(ref="vtkView", method="resetCamera", args=[])
```

## Layout management

Layouts are meant to define the core UI elements of an application. Think of FullScreen vs Toolbar, Drawer, Footer and so on. Layouts let you drop pieces of your UI into pre-defined locations. The layout organizes the way an application is structured. It could be defined once, or be redifined at runtime.

When creating a layout, you have the opportunity to define the Tab title along with a path to a favicon and a method to call at startup.

## HTML Elements

HTML elements in trame (trame.html.*) are just helpers for generating HTML content. But because they exist as Python objects, users can interact with them simply by setting attributes on them in plain Python.

Below are various ways that you can translate what you see on a Vue component into trame syntax.

```python
# Attribute without value (boolean)
# <v-btn outlined />
vuetify.VBtn(outlined=True)

# Bind method to event
# <v-btn @click="do_something">
def do_something():
  pass
vuetify.VBtn(click=do_something)

# Dash handling (v-model => v_model)
# <v-slider v-model="slider_value" min="0" max="100" />
vuetify.VSlider(
  v_model=("slider_value", 50), # See state section above
  min=0,
  max=50,
)
```

## Command line arguments

Since trame is used to create applications, as compared to web services that aim to serve many concurrent users, it may be important to provide information to an application on start up. For example, which ML model to load, or the file/directory that you would like to explore or process. This can be achieved by adding CLI parameters using [ArgParse](https://docs.python.org/3/library/argparse.html), like in the following example.

```python
from trame.app import get_server

server = get_server()

server.cli.add_argument("-d", "--data", help="Directory to explore", dest="data")
args = server.cli.parse_args()
print(args.data)
```

## Starting an application

The server provides a `start()` method which actually starts a trame application. Typically the following section is placed in the main script:

```python
if __name__ == "__main__":
    server.start()
```

The full API is listed below

```python
def start(
      port=None,
      thread=False,
      open_browser=True,
      show_connection_info=True,
      disableLogging=False,
      backend="aiohttp",
      exec_mode="main",
      timeout=None,
    ):
    """
    Start web server for serving your application

    Parameters
    ----------
    port    : None or Number
        Port on which the server should run on. When providing 0, the operating system will pick an available one.
    thread  : Boolean
        If true we won't listen to ctrl-c
    open_browser: Boolean
        Default True which will open your browser and connect to your local server. Using --server is similar than passing False.
    show_connection_info: Boolean
        Default True which will print server IP and port information.
    disableLogging: Boolean
        Default False which will keep the default logging setup otherwise logger will be disabled.
    exec_mode: String
      Default "main", Options ["main", "task", "coroutine", "desktop"]
      "main" will block, while "desktop" will run like main but as a standalone application
    timeout=None,
      Adjust timeout. 0 will prevent process ripper from running when no client is connected.
```
