# How to use Trame

Trame aims to streamline creation of graphical interface for interactive data manipulation and visualization with a very compact and simple API.
This document try to capture the core API and concepts behind trame so you can use it when you get started but also as reference once you get more familiar with Trame.

## Core concept

Trame allow you to easily share variables between the UI components and your Python application.
But on top of that shared state, functions and methods can be triggered from either side.
For example, you can link a Python function to be called when a button in the UI is clicked.
This document will focus on how you can leverage those two functionalities inside your application using Trame.

## Shared state

Trame mainly focus on the Python side, therefore the variables that we aim to use across our application will be defined from Python.
The following sections will illustate the various way you can affect the shared state.

### UI element with a dynamic variable

The example below use Vuetify to create a slider where the value controlled by that slider is available in our shared state behind the name `slider_value` that we initialize with the value `8`. So variables in our shared state can be defined and initialized right were we want to use them when defining our UI elements. In that example, the slider will be able to modify that value but also will reflect its content if that value change on the server side.

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

Let's pretend we want to monitor the value of `slider_value` within our Python application and execute a method when such variable gets updated.
The code below illustate how we can annotate function so they can be called when a value of our shared state is modified.

```python
from trame import change

@change("slider_value")
def slider_value_change(slider_value, **kwargs):
  print(f"Slider is changing slider_value to {slider_value}")
```

So far, we only have the client modifing that variable. But if a function on the server were to change that variable, that function will also be called as we simply react to the fact that such variable has been updated by someone.

### Changing the value from Python

Within our Python application it is possible that you would like to read and even write in that shared state so the UI can reflect your changes.
The code below provide a function that will read the current value and update its content.

```python
from trame import update_state, get_state

def random_update():
  current_value, = get_state("slider_value") # read a set of variables

  current_value += 1
  if current_value > 15:
    current_value = 2

  update_state("slider_value", current_value) # update variable with new content
```

### Forcing variable exchange

Sometime, the variable inside your shared state is an actual object with nested structure. While the state on the Python side always keeps the same reference to that object, you are manually editing its content and you want to flush its content so the client can see your changes. In that use case we have a `flush_state()` methods that can be called with the list of variable names that should be pushed. This is also useful in some async context to control when pieces of the state should be pushed to the other side. The code below provide a usage example.

```python
import asyncio
from trame import flush_state, update_state
import time

async def update_time():
  while True:
    await asyncio.sleep(1)
    update_state("time", time.time())
    flush_state("time")
```

## Method calls

When building a client/server application you will need to be able to trigger methods on both side and Trame as some easy to do that.

### Bind method to a button click

The example below re-use the function we had defined before but now we bind it to a button.

```python
from trame.html import vuetify
from trame import update_state, get_state

def random_update():
  current_value, = get_state("slider_value") # read a set of variables

  current_value += 1
  if current_value > 15:
    current_value = 2

  update_state("slider_value", current_value) # update variable with new content

change_btn = vuetify.VBtn(
  "Change slider_value",
  click=random_update
)
```

### Calling JS methods

Some components used in your layout may have some API that you can use and call from the Python side.
The code below provide an example of such use case:

```python
from trame import call
from trame.html import vtk

html_view = vtk.VtkView(
  ref="vtkView", # Name to identify the Web component on which we want to call a method
  ...
)

def reset_camera():
  call(ref="vtkView", method="resetCamera", args=[])
```

## Layout management

Layouts are meant to define the core UI elements of an application. Think of FullScreen vs Toolbar, Drawer, Footer and so on.
Layouts let you drop pieces of your UI into pre-defined locations.
The layout gather the way your application will look and it could be defined once or be redifined at runtime.

## Command line arguments

[...]

## Starting the application

[...]
