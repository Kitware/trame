# VTK 
The Visualization Toolkit renders 3D images and volumes in Trame. For more Python Vtk examples, see [here](https://kitware.github.io/vtk-examples/site/Python/).  

# remoteview, localview, localremoteview 

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

# Force image to be pushed to client
remote_view.update() 
```

# The rest 

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

# VtkRemoteLocalView
## Properties
#### `context_name`
#### `interactive_ratio`
#### `interactor_events`
#### `interactor_settings`
#### `namespace`
#### update_geometry
#### update_image
#### view

## Events
#### `interactor_events`

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

# VtkLocalView

# VtkView
## Properties
#### `ref`
#### `background`
#### `cube_axes_style`
#### `interactor_settings`
#### `picking_modes`
#### `show_cube_axes` -->
