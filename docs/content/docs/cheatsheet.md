# Cheatsheet

The working application below manage to capture the fundamentals of __trame__ in less than 45 lines.
In that sense, it could be seen as a cheatsheet on how to use __trame__ as it is mostly self explanatory.

```python
from trame import state, controller as ctrl # state + controller
from trame.layouts import SinglePage        # UI layout
from trame.html import vuetify, vtk         # UI components

# Reset resolution variable to 6
def reset_resolution():          
    state.resolution = 6

# When resolution change, execute fn
@state.change("resolution")      
def resolution_change(resolution, **kwargs):
    print(f"Slider updating resolution to {resolution}")

# Initialize application layout/ui
layout = SinglePage("VTK.js")    

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

# Start application
layout.start()               
```

## Result


<p style="text-align:center;display: flex;align-items: center;">
    <img src="/trame/images/trame-cheatsheet-app.jpg" alt="Application" style="width: 45%; height: 45%">
    <img src="/trame/images/trame-cheatsheet-output.jpg" alt="Output" style="width: 45%; height: 45%">
</p>

## Things to understand

### State

Read variable from shared state

```python
value = state.var_name
value = state["var_name"]
```

Write variable to the shared state

```python
state.var_name = value
state["var_name"] = value
```

Write several variables at once in the shared state

```python
state.update({
    "var_name": value,
    "var_name_2": value,
})
```

Bind a method/function to a state variable change

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

Initialise a variable from the UI definition with an initial value. 
Use a tuple to define the value of a given attribute where the first entry is a string with the variable name and the second entry is its initial value.

```python
vuetify.VTextField(v_model=("var_name", "initial value"))
vuetify.VSlider(v_model=("resolution", 6), min=1)
```

Provide a JavaScript expression as attribute. We still provide a tuple but with no initial value.

```python
vuetify.VTextField(value=("'Hello' + var_name", ))
```

### Method binding

Method can be passed to events attribute of your UI elements. By default, the function will be called with no arguments.

If you want to control its arguments you can use a tuple where the second entry represents the __args__ and the third represents the __kwargs__. If you only want to provide args without kwargs, just provide a tuple with 2 entries. __$event__ is a reserved name to reprensent the event object.

```python
vuetify.VBtn("Click me", click=ctrl.do_something))
vuetify.VBtn("Click me", click=(ctrl.do_something, "['hello', $event]"))
vuetify.VBtn("Click me", click=(ctrl.do_something, "[index, $event]", "{ a: 12 }"))
```

### Controller

The controller from trame is just a dynamic container for methods or functions that can be get or set in either order.

```python
vuetify.VBtn("Click me", click=ctrl.do_something)

def fn():
    pass

ctrl.do_something = fn
```

## Conclusion

The remaining part to learn is all the components available for displaying other 3D graphics, charts, maps and more. But right now you've learn the fundamentals on how trame works which should let you build your application simply. For more details, please refer to the [tutorial](https://kitware.github.io/trame/docs/tutorial.html) or [API](https://trame.readthedocs.io/en/latest/index.html).

Trame is a powerful framework for building any kind of application in plain Python. From prototypes to professional applications, trame offers an innovative approach for “write once and run anywhere” by allowing your app to migrate from your desktop to a cloud service.