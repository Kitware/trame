# How to use trame

trame aims to streamline creation of graphical interfaces for interactive data manipulation and visualization with a very compact and simple API.
This document tries to capture the core API and concepts behind trame so you can use it when you get started but also as a reference once you get more familiar with trame.

## Core concept

trame allow you to easily share variables between the UI components and your Python application.
But on top of that shared state, functions and methods can be triggered from either side.
For example, you can link a Python function to be called when a button in the UI is clicked.
This document will focus on how you can leverage those two functionalities inside your application using trame.

## Shared state

trame mainly focuses on the Python side, therefore the variables that we aim to use across our application will be defined from Python.
The following sections will illustate the various way you can affect the shared state.

### UI element with a dynamic variable

The example below uses Vuetify to create a slider where the value controlled by that slider is available in our shared state behind the name `slider_value` that we initialize with the value `8`. So variables in our shared state can be defined and initialized right were we want to use them when defining our UI elements. In this example, the slider will be able to modify that value but also will reflect its content if that value changes on the server side.

```python
from trame.html import vuetify

slider = vuetify.VSlider(
  label="Example",
  min=2,
  max=15,
  v_model=("slider_value", 8),
)
```

### Listening to change

Let's pretend we want to monitor the value of `slider_value` within our Python application and execute a method when that variable gets updated.
The code below illustate how we can annotate a function so it can be called when a value of our shared state is modified.

```python
from trame import state

@state.change("slider_value")
def slider_value_change(slider_value, **kwargs):
  print(f"Slider is changing slider_value to {slider_value}")
```

So far, we only have the client modifing that variable. But if a function on the server were to change that variable, that function will also be called as we simply react to the fact that the variable has been updated by someone.

### Changing the value from Python

Within our Python application it is possible that we would like to read and even write in the shared state so the UI can reflect your changes.
The code below provides a function that will read the current value and update its content.

```python
from trame import state

def random_update():
  state.slider_value += 1
  if state.slider_value > 15:
    state.slider_value = 2
```

### Forcing state exchange

Sometimes, the variable inside your shared state is an actual object with nested structure. While the state on the Python side always keeps the same reference to that object, you are manually editing its content and you want to flush its content so the client can see your changes. In that use case we have a `flush()` method that can be called with the list of variable names that should be pushed. This is also useful in some async contexts to control when pieces of the state should be pushed to the other side. The code below provides a usage example.

```python
import asyncio
from trame import state
import time

async def update_time():
  while True:
    await asyncio.sleep(1)
    state.time = time.time()
    state.flush("time")
```

## Method calls

When building a client/server application you will need to be able to trigger methods on both side and trame has some easy ways to do that.

### Bind method to a button click

The example below re-uses the function we had defined before but now we bind it to a button.

```python
from trame.html import vuetify
from trame import state

def random_update():
  state.slider_value += 1

  if state.slider_value > 15:
    state.slider_value = 2


change_btn = vuetify.VBtn(
  "Change slider_value",
  click=random_update
)
```

### Calling JS methods

Some components in your layout may have APIs that you can use and call from the Python side.
The code below provides an example of such use case:

```python
from trame import js_call
from trame.html import vtk

html_view = vtk.VtkView(
  ref="vtkView", # Name to identify the Web component on which we want to call a method
  ...
)

def reset_camera():
  js_call(ref="vtkView", method="resetCamera", args=[])
```

## Layout management

Layouts are meant to define the core UI elements of an application. Think of FullScreen vs Toolbar, Drawer, Footer and so on.
Layouts let you drop pieces of your UI into pre-defined locations.
The layout gathers the way your application will look. It could be defined once or be redifined at runtime.

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

Since a trame application is a real application, as opposed to a service that aims to serve many concurrent users, you may want to provide some information to your application when you start it like which ML model you want to load or the file/directory that you would like to explore or process.
This can be achieved by adding CLI parameters using [ArgParse](https://docs.python.org/3/library/argparse.html), like in the following example.

```python
from trame import get_cli_parser

parser = get_cli_parser()
parser.add_argument("-d", "--data", help="Directory to explore", dest="data")
args = parser.parse_args()
print(args.data)
```

## Starting the application

trame layouts provides a `start()` method which will actually start your application.
Usually we put the following section in your main script.

```python
if __name__ == "__main__":
    layout.start())
```

The full API is listed below

```python
def start(name=None, favicon=None, on_ready=None, port=None):
    """
    Start web server for serving your application

    Parameters
    ----------
    name    : None or str
        "Title" that you can see in your tab browser.
        This will be filled automatically if a trame.layouts.* layout was provided.
    favicon : None or str
        Relative path to a png image that should be used as favicon
    port    : None or Number
        Port on which the server should run on
    on_ready: None or function
        Function called once the server is ready
```
