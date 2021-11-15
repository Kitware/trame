# Paraview

ParaView is based on the Visualization Toolkit to process images and create 3D computer graphics. To learn more about ParaView and see how it can be user via Python, see its [User Guide](https://docs.paraview.org/en/latest/).

ParaView integration in trame allow you to create reach visualization and data processing applications by leveraging the Python infrastructure of ParaView. Several components are available so you can leverage ParaView either for its data processing and/or rendering. trame lets you choose whether you want to leverage Remote Rendering or whether the client should do the rendering by leveraging vtk.js under the hood.

[![ParaView Guide](/trame/images/module-paraview.jpg)](https://docs.paraview.org/en/latest/)

## VtkRemoteView

The VtkRemoteView component relies on the server for rendering by sending images to the client by simply binding your view proxy to it. This component gives you controls to the image size reduction and quality to reduce latency while interacting.

### How to use it?

The component allows you to directly tap into a vtk.js interactor's events so you can bind your own method from Python to them. The list of available events can be found [here](https://github.com/Kitware/vtk-js/blob/b92ad5463150b88514fcb5020c1fa6c7fcfe2a4f/Sources/Rendering/Core/RenderWindowInteractor/index.js#L23-L60).

The component also provides a convenient method for pushing a new image to the client when you're modifying your scene on the Python side.

```python
from trame.html import vtk

def end():
  pass

remote_view = vtk.vtkRemoteView(
  view=...,               # Instance of view proxy (required)
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

### Examples

- [ParaView/SimpleCone/RemoteRendering](https://github.com/Kitware/trame/blob/master/examples/ParaView/SimpleCone/RemoteRendering.py)


## VtkLocalView

The VtkLocalView component relies on the server for defining the `view` but then only the geometry is exchanged with the client. The server does not need a GPU as no rendering is happening on the server. The view proxy is only used to retrieve the scene data and parameters (coloring by, representations, ...). By relying on the same api, you can easily switch from a `VtkRemoteView` to a `VtkLocalView` or vice-versa. This component gives you controls on how you want to map mouse interaction with the camera. The default setting mimic default VTK interactor style so you will rarely have to override to the `interactor_settings`.

### How to use it?

The component allows you to directly tap into a vtk.js interactor's events so you can bind your own method from Python to them. The list of available events can be found [here](https://github.com/Kitware/vtk-js/blob/b92ad5463150b88514fcb5020c1fa6c7fcfe2a4f/Sources/Rendering/Core/RenderWindowInteractor/index.js#L23-L60).

The component also provides a convenient method to push the scene to the client when you're modifying your scene on the Python side.

```python
from trame.html import vtk

def end():
  pass

local_view = vtk.VtkLocalView(
  view=...,                # Instance of view proxy (required)
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


#### Interactor Settings

For the `interactor_settings` we expect a list of mouse event type linked to an action. The example below is what is used as a default:

```javascript
interactor_settings=[
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

| Attribute     | Value      | Description                                   |
| ------------- | ---------- | --------------------------------------------- |
| button        | 1, 2, 3    | Which button should be down                   |
| shift         | true/false | Is the Shift key down                         |
| alt           | true/false | Is the Alt key down                           |
| control       | true/false | Is the Ctrl key down                          |
| scrollEnabled | true/false | Some action could also be triggered by scroll |
| dragEnabled   | true/false | Mostly used to disable default drag behavior  |


And the action could be one of the following:

| Action      |  Description                                                                             |
| ----------- | ---------------------------------------------------------------------------------------- |
| Pan         | Will pan the object on the plane normal to the camera                                    |
| Zoom        | Will zoom closer or further from the object based on the drag direction                  |
| Roll        | Will rotate the object around the view direction                                         |
| ZoomToMouse | Will zoom while keeping the location that was initially under the mouse at the same spot |

### Examples

- [ParaView/SimpleCone/LocalRendering](https://github.com/Kitware/trame/blob/master/examples/ParaView/SimpleCone/LocalRendering.py)

## VtkRemoteLocalView

The VtkRemoteLocalView component is a blend of `VtkLocalView` and `VtkRemoteView` where the user can choose dynamically which mode he/she wants to be in. When instantiating a `VtkRemoteLocalView` several variables and triggers will be created for you to more easily control your view.

### How to use it?

```python
from trame.html import vtk

rl_view = vtk.VtkRemoteLocalView(
  view=...,                # Instance of view proxy (required)

  # Just VtkRemoteLocalView params
  namespace=...,           # Prefix for variables and triggers. See below. (required)
  mode="local",            # Decide between local or remote. See below.

  # VtkRemoteView params
  **remote_view_params,

  # VtkLocalView params
  **local_view_params,
)

rl_view.update_geometry()  # Force update to geometry
rl_view.update_image()     # Force update to image
rl_view.view()             # Get linked vtkRenderWindow instance
```

#### Namespace parameter

Constructing a VtkRemoteLocalView will set several variables, prefixed by a namespace. In the example below we used `namespace="view"`.

| Variable | Description                                                       |
| -------- | ----------------------------------------------------------------- |
| viewId   | `str` representing the vtkRenderWindow id                         |
| viewMode | `local`or `remote` to control which View is displayed to the user |


Constructing a VtkRemoteLocalView will also set several trame triggers.

| Trigger          | Description                                                                |
| ---------------- | -------------------------------------------------------------------------- |
| viewCamera       | When call with no arguments, the server will push its camera to the client |
| viewAnimateStart | Start the animation loop for constantly rendering                          |
| viewAnimateStop  | Stop the animation loop                                                    |

The `namespace` will also be used as `ref=` unless provided by the user.

#### Mode parameter

The mode is driven by the variable `{namespace}Mode` but can be provided when instantiated so the default can be overriden and a JavaScript expression can be used instead of the default variable. This attribute behaves the same way as any trame one except we won't register the left side as a state entry since we already have one under `{namespace}Mode`. This means we will evaluate the left side of the expression assuming a tuple is provided and the right side of the tuple is used to set its inital value.

### Examples

- [API](https://trame.readthedocs.io/en/latest/trame.html.paraview.html)
- to come...
