# Vtk 
The Visual Tool Kit renders 3D images and volumes for Trame. For more python vtk examples, see [here](https://kitware.github.io/vtk-examples/site/Python/).
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

# VtkRemoteView

## Properties
#### `wsClient`
#### `ref`
#### `view_id`
#### `enable_picking`
#### `interactive_quality`
#### `interactive_ratio`
#### `interactor_events`
#### update
#### VtkRemoteView.push_image(view)

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
#### `show_cube_axes`
