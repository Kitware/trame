# VTK 
The Visualization Toolkit renders 3D images and volumes in Trame. For more Python Vtk examples, see [here](https://kitware.github.io/vtk-examples/site/Python/).  

[...example]

## VtkRemoteView
The VtkRemoteView component relies on the server for rendering by sending images to the client by simply binding your vtkRenderWindow to it. This component gives you controls to the image size and quality to reduce latency while interacting. 

The component allows you to directly tap into a vtk.js interactor events so you can bind your own method from python to them. The list of available events can be found [here](https://github.com/Kitware/vtk-js/blob/b92ad5463150b88514fcb5020c1fa6c7fcfe2a4f/Sources/Rendering/Core/RenderWindowInteractor/index.js#L23-L60). 

The component also provides a convenient method for forcing a render to the client when you're modifying your scences on the python side.

```python
from trame.html import vtk

def end_interaction():
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
  EndAnimation=end_interaction, # Bind method to the enabled event
)

remote_view.update()  # Force image to be pushed to client
```
## VtkLocalView
For the interactorSettings we expect a list of mouse event type linked to an action. The example below is what is used as default:

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

## VtkRemoteLocalView
The VtkRemoteLocalView component renders on the client a geometry which is made on the server.

The component allows you to directly tap into a vtk.js interactor events so you can bind your own method from python to them. The list of available events can be found [here](https://github.com/Kitware/vtk-js/blob/b92ad5463150b88514fcb5020c1fa6c7fcfe2a4f/Sources/Rendering/Core/RenderWindowInteractor/index.js#L23-L60). 

The component also provides a convenient method for forcing a render to the client when you're modifying your scences on the python side.

```python
from trame.html import vtk

rl_view = vtk.VtkRemoteLocalView(
  view=...,                # Instance of vtkRenderWindow (required)
  mode="local",            # Decide between local or remote. See below.
  context_name=...,        # Namespace for geometry cache
  interactor_settings=..., # Options for camera controls
  namespace=...,           # Prefix for variables and triggers. See below.
  interactive_ratio=...,   # [0.1, 1] Image size scale factor while interacting
  interactor_events=(      # Enable vtk.js interactor events for method binding
    "events", 
    ['EndAnimation'],
  ),
  EndAnimation=end_interaction, # Bind method to the enabled event

)

rl_view.update_geometry()  # Force update to geometry
rl_view.update_image()     # Force update to image
rl_view.view()             # Get linked vtkRenderWindow instance
```

### Mode

1) String
Just "local" or "remote"

2) Length 1
js eval

3) Length 2
js eval, initial namespace+mode

mode = ("override", initial)

Pywebvue Vtk trame state
# init keys
self.ref_key = namespace
self.mode_key = f"{namespace}Mode" if namespace else "mode"
self.scene_key = f"{namespace}Scene" if namespace else "scene"
self.camera_key = f"{namespace}Camera" if namespace else "camera"
self.animation_key = f"{namespace}Animate" if namespace else "animate"
self.id_key = f"{namespace}Id" if namespace else "id"

# Attach annotations
self._app.set(self.id_key, self._view_id)
self._app.set(self.mode_key, mode)
self._app.trigger(self.camera_key)(self.update_camera)
self._app.trigger(f"{self.animation_key}Start")(self.start_animation)
self._app.trigger(f"{self.animation_key}Stop")(self.stop_animation)


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
