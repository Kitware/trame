# VTK 
The Visualization Toolkit renders 3D images and volumes in Trame. For more Python Vtk examples, see [here](https://kitware.github.io/vtk-examples/site/Python/).  

[...example]

## VtkRemoteView
The VtkRemoteView component relies on the server for rendering by sending images to the client by simply binding your vtkRenderWindow to it. This component gives you controls to the image size and quality to reduce latency while interacting. 

The component allows you to directly tap into a vtk.js interactor events so you can bind your own method from python to them. The list of available events can be found [here](https://github.com/Kitware/vtk-js/blob/b92ad5463150b88514fcb5020c1fa6c7fcfe2a4f/Sources/Rendering/Core/RenderWindowInteractor/index.js#L23-L60). 

The component also provides a convenient method for forcing a render to the client when you're modifying your scences on the python side.

```python
from trame.html import vtk

def end():
  pass

remote_view = vtk.vtkRemoteView(
  view=...,               # Instance of vtkRenderWindow (required)
  ref=...,                # Identifier for this component
  interactive_quality=60, # [0, 100] 0 for fastest render, 100 for best quality
  interactive_ratio=...,  # [0.1, 1] Image size scale factor while interacting
  interactor_events=(     # Enable vtk.js interactor events for method binding
    "events", 
    ['EndAnimation'],
  ),
  EndAnimation=end,       # Bind method to the enabled event
)

remote_view.update()  # Force image to be pushed to client
```
## VtkLocalView
[...]
<!--
The VtkLocalView component builds a geometry on the server but renders on the client.

The component allows you to directly tap into a vtk.js interactor events so you can bind your own method from python to them. The list of available events can be found [here](https://github.com/Kitware/vtk-js/blob/b92ad5463150b88514fcb5020c1fa6c7fcfe2a4f/Sources/Rendering/Core/RenderWindowInteractor/index.js#L23-L60). 

The component also provides a convenient method to push a render to the client when you're modifying your scences on the python side.

The component can take a list of settings to configure how the mouse and camera will interact. 

```python
from trame.html import vtk

def end():
  pass

local_view = vtk.VtkLocalView(
  view=...,                # Instance of vtkRenderWindow (required)
  ref=...,                 # Identifier for this component
  context_name=...,        # Namespace for geometry cache
  interactor_settings=..., # Options for camera controls. See below.
  interactor_events=(      # Enable vtk.js interactor events for method binding
    "events", 
    ['EndAnimation'],
  ),
  EndAnimation=end,        # Bind method to the enabled event

)

local_view.update()  # Force geometry to be pushed
```

### interactorSettings 
For the interactorSettings we expect a list of mouse event type linked to an action. The example below is what is used as default:

```
interactorSettings=[
  {
    button: 1,
    action: 'Rotate',
  }, {
    button: 2,
    action: 'Pan',
  }, {
    button: 3,
    action: 'Zoom',
    scrollEnabled: true,
  }, {
    button: 1,
    action: 'Pan',
    shift: true,
  }, {
    button: 1,
    action: 'Zoom',
    alt: true,
  }, {
    button: 1,
    action: 'ZoomToMouse',
    control: true,
  }, {
    button: 1,
    action: 'Roll',
    alt: true,
    shift: true,
  }
]
```

A mouse event can be identified with the following set of properties:

    button: 1/2/3 # Which button should be down
    shift: True/False # Is the Shift key down
    alt: True/False # Is the Alt key down
    control: True/False # Is the Ctrl key down
    scrollEnabled: True/False # Some action could also be triggered by scroll
    dragEnabled: True/False # Mostly used to disable default drag behavior

And the action could be one of the following:

    Pan: Will pan the object on the plane normal to the camera
    Zoom: Will zoom closer or further from the object based on the drag direction
    Roll: Will rotate the object around the view direction
    ZoomToMouse: Will zoom while keeping the location that was initially under the mouse at the same spot

-->
## VtkRemoteLocalView
[...]
<!--
The VtkRemoteLocalView can change between remote and local rendering modes.

It will create several Trame variables and events which can control which mode it is currently or to track animations.

```python
from trame.html import vtk

def end():
  pass

rl_view = vtk.VtkRemoteLocalView(
  view=...,                # Instance of vtkRenderWindow (required)
  interactor_events=(      # Enable vtk.js interactor events for method binding
    "events", 
    ['EndAnimation'],
  ),
  EndAnimation=end,        # Bind method to the enabled event

  # Just VtkRemoteView params
  interactive_ratio=...,   # [0.1, 1] Image size scale factor while interacting

  # Just VtkLocalView params
  context_name=...,        # Namespace for geometry cache
  interactor_settings=..., # Options for camera controls

  # Just VtkRemoteLocalView params
  namespace=...,           # Prefix for variables and triggers. See below.
  mode="local",            # Decide between local or remote. See below.
)

rl_view.update_geometry()  # Force update to geometry
rl_view.update_image()     # Force update to image
rl_view.view()             # Get linked vtkRenderWindow instance
```

### Namespace parameter
Constructing a VtkRemoteLocalView will set several Trame keys, optinally prefixed by a namespace:

    "mode" # This will store "local" or "remote"
    "id"   # This identifies the view 

Constructing a VtkRemoteLocalView will also set several Trame triggers, optinally prefixed by a namespace:

    "camera"       # [...]
    "animateStop"  # [...]
    "animateStart" # [...]


### Mode parameter
When constructing a vtkRemoteLocalView, the "mode" parameter can take several values.
1) mode="local" or mode="remote"
This will set the (optionally namespaced) shared state key "mode" to that particular mode.


2) mode=("...js expression",)
Passing a tuple with length 1 will interpret the value in the tuple as a javascript expression and use the result of that expression when looking up the mode. See example [here](https://github.com/Kitware/trame/blob/f6594a02ed7e1ecc24058ffac527e010e8181e22/examples/VTK/ContourGeometry/DynamicLocalRemoteRendering.py#L88).


3) mode=("...js expression", `initial_mode`)
This will do the same as 2) above, but it will also ensure the initial mode is set to `initial_mode`.
-->

<!--
# VtkAlgorithm
## Properties
#### `port`
#### `vtk_class`
#### `state`

# VtkCellData

# VtkDataArray
## Properties
#### `name`
#### `registration`
#### `type`
#### `values`
#### `number_of_components`

# VtkFieldData

# VtkGeometryRepresentation
## Properties
#### `id`
#### `color_map_preset`
#### `color_data_range`
#### `actor`
#### `mapper`
#### `property`

# VtkGlyphRepresentation
## Properties
#### `color_map_preset`
#### `color_data_range`
#### `actor`
#### `mapper`
#### `property`

# VtkMesh
## Properties
#### `port`
#### `state`

# VtkPointData

# VtkPolyData
## Properties
#### `port`
#### `verts`
#### `lines`
#### `polys`
#### `strips`
#### `connectivity`

#### set_dataset(self, dataset)
#### update(self)


# VtkReader
## Properties
#### `parse_as_array_buffer`
#### `parse_as_text`
#### `port`
#### `render_on_update`
#### `reset_camera_on_update`
#### `url`
#### `vtk_class`


# VtkShareDataset
## Properties
#### `port`
#### `name`

# VtkSyncView
## Properties
#### `ref`
#### `wsClient`
#### `view_state`
#### `interactor_events`
#### `interactor_settings`
#### `context_name`
#### update

## Events
#### `interactor_events`

# VtkView
## Properties
#### `ref`
#### `background`
#### `cube_axes_style`
#### `interactor_settings`
#### `picking_modes`
#### `show_cube_axes` -->
