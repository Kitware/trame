# Cheatsheet

The working application below captures the fundamentals of __trame__ in less than 45 lines. Consider this as a cheatsheet on how to use __trame__ as it is mostly self explanatory.

```python
from trame.app import get_server               # Entry point to trame
from trame.ui.vuetify import SinglePageLayout  # UI layout
from trame.widgets import vuetify, vtk         # UI widgets

server = get_server()                          # Create/retrieve default server
server.client_type = "vue2"                    # Choose between vue2 and vue3
state, ctrl = server.state, server.controller  # Extract server state and controller

# Reset resolution variable to 6
def reset_resolution():
    state.resolution = 6

# When resolution change, execute fn
@state.change("resolution")
def resolution_change(resolution, **kwargs):
    print(f"Slider updating resolution to {resolution}")

# Initialize application layout/ui
with SinglePageLayout(server) as layout:
    # Toolbar customization (add-on)
    with layout.toolbar as toolbar:
        toolbar.dense = True            # Update toolbar attribute
        vuetify.VSpacer()               # Push things to the right
        vuetify.VSlider(                # Add slider
            v_model=("resolution", 6),     # bind variable with an initial value of 6
            min=3, max=60,                 # slider range
            dense=True, hide_details=True, # presentation setup
        )
        # Bind methods to 2 icon buttons
        with vuetify.VBtn(icon=True, click=ctrl.reset_camera):
            vuetify.VIcon("mdi-crop-free")
        with vuetify.VBtn(icon=True, click=reset_resolution):
            vuetify.VIcon("mdi-undo")

    # Content setup
    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            with vtk.VtkView() as vtk_view:               # vtk.js view for local rendering
                ctrl.reset_camera = vtk_view.reset_camera # Bind method to controller
                with vtk.VtkGeometryRepresentation():     # Add representation to vtk.js view
                    vtk.VtkAlgorithm(                     # Add ConeSource to representation
                        vtkClass="vtkConeSource",           # Set attribute value with no JS eval
                        state=("{ resolution }",)           # Set attribute value with JS eval
                    )

# Start server
server.start()
```

## Results


<p style="text-align:center;display: flex;align-items: center;">
    <img src="/trame/images/trame-cheatsheet-app.jpg" alt="Application" style="width: 45%; height: 45%">
    <img src="/trame/images/trame-cheatsheet-output.jpg" alt="Output" style="width: 45%; height: 45%">
</p>

## Explanatory Details

### State

Read a variable from shared state:

```python
value = state.var_name
value = state["var_name"]
```

Write a variable to shared state:

```python
state.var_name = value
state["var_name"] = value
```

Write several variables at once to the shared state:

```python
state.update({
    "var_name": value,
    "var_name_2": value,
})
```

Bind a method/function to a state variable change:

```python
@state.change("var_name")
def change_detected(var_name, **kwargs):
    # Called with full state as kwargs when "var_name"
    # gets modified regardless if it is coming from Python or UI
    print(f"New var_name value is {var_name}")

@state.change("var_name", "var_name_1")
def change_detected(**kwargs):
    print(f"Either var_name or var_name_1 is modified")
```

Specify an initial value for a UI variable. Use a tuple to define the value of a given attribute, where the first entry is a string with the variable name and the second entry is its initial value.

```python
vuetify.VTextField(v_model=("var_name", "initial value"))
vuetify.VSlider(v_model=("resolution", 6), min=1)
```

Provide a JavaScript expression as an attribute value. We still provide a tuple but with no initial value.

```python
vuetify.VTextField(value=("'Hello' + var_name", ))
```

### Method binding

Methods can be passed to the events attribute of your UI elements. By default, the function will be called with no arguments.

If you want to control its arguments you can use a tuple where the second entry represents the __args__ and the third represents the __kwargs__. If you only want to provide args without kwargs, just provide a tuple with 2 entries. __$event__ is a reserved name to represent the event object.

```python
vuetify.VBtn("Click me", click=ctrl.do_something))
vuetify.VBtn("Click me", click=(ctrl.do_something, "['hello', $event]"))
vuetify.VBtn("Click me", click=(ctrl.do_something, "[index, $event]", "{ a: 12 }"))
```

### Controller

The trame controller is just a dynamic container for methods or functions that can be set or get in either order.

```python
vuetify.VBtn("Click me", click=ctrl.do_something)

def fn():
    pass

ctrl.do_something = fn
```

## Life Cycle

* on_server_ready : All protocols initialized and available for the client to connect.
* on_client_connected : Connection established to server.
* on_client_exited : Linked to browser "beforeunload" event.
* on_server_exited : Trame is exiting its event loop.
* on_server_reload : If callback registered it is used to reload server side modules.

```python

ctrl.on_server_ready.add(lambda **_: print("server ready"))
ctrl.on_server_ready.add(lambda **_: print("Staring Factory - Launcher barrier"))

ctrl.on_client_exited = lambda **_: print("Someone is gone...")
```

## Conclusion and Next Steps

At this point the fundamentals of trame have been presented. To build fully-fledged applications, the next steps are to learn the various components available for displaying 3D graphics, charts, maps and more. For more details, please refer to the [tutorial](https://kitware.github.io/trame/docs/tutorial.html) or [API](https://trame.readthedocs.io/en/latest/index.html).

Trame is a powerful Pyton-based integration framework for creating visual analytics applications. From prototypes to professional applications, trame offers an innovative approach to “write once and run anywhere” through applications that run from a desktop to a cloud service using a standard web browser.
