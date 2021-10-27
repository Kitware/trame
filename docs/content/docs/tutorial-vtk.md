# VTK

So we want to start adding VTK visualizations to our application. 

## VTK Imports

Start with the initial *setup-vtk* `app.py`. 

**First**, we need to add is an import for `vtk` and `vuetify` from `trame.html`.

```python
from trame.html import vtk, vuetify
```

This provides us access to Trame's helper functions for vtk and vuetify. 

**Next**, we will need to import the required objects from vtk. Here we will visualize a simple cone in this example so we will need `vtkConeSource`.

```python
from vtkmodules.vtkFiltersSources import vtkConeSource
```

Other VTK objects will need to be imported based on the desired visualization pipelines. 

**Next**, we need to import the VTK rendering core

```python
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)
```

**Finally**, we need to import the required modules for the interacter factory and remote rendering factory. 

`vtkInteractorStyleSwitch` is required for interacter factory initialization.

```python
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch #noqa
```

The `vtkRenderingOpenGL2` module is required for remote rendering factory initialization. It is not necessary for local rendering, but you'll want to include it so that you can seamlessly switch between *local* and *remote* rendering.

```python
import vtkmodules.vtkRenderingOpenGL2 #noqa
```

**Note**: `#noqa` tells the linter to ignore checking this problematic line.

## VTK Pipeline

As promised, to add visualization to your Trame application you simply write VTK pipelines in Python.

There are a number of ways to learn VTK:

- [VTK User Guide](https://www.kitware.com/products/books/VTKUsersGuide.pdf)
- [VTK Textbook](https://gitlab.kitware.com/vtk/textbook/raw/master/VTKBook/VTKTextBook.pdf)
- [VTK Examples](https://kitware.github.io/vtk-examples/site/Python)
- [VTK Documentation](https://www.vtk.org/doc/nightly/html/)

This tutorial will not provide an adequate background for VTK, but we will explain the pieces and parts of the provided exmples at a high level.

**First**, we create a `vtkRenderer` and `vtkRenderWindow`. The we tie them together by adding the `renderer` to the `renderWindow`.

```python
renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)
```

**Second**, we define a `vtkRenderWindowInteractor` which provides a platform-independent interaction mechanism for mouse/key/time events. 

```python
renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()
renderWindowInteractor.EnableRenderOff()
```

We create the interactor, connect it to the `renderWindow`, set the interaction style, and disable the interactor from calling the `renderWindow` `Render` function.

**Third**, we create the desired visualization. This process requires the creation of an object, a mapper, and an actor.

```python
cone_source = vtkConeSource()
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cone_source.GetOutputPort())
actor = vtkActor()
actor.SetMapper(mapper)
```

The instantiated `vtkConeSource` is our graphics object, and we want to map that object to polydata creating a `vtkPolyDataMapper`. We must digitally create a connection from the cone to the mapper by setting the input connection. We then create an actor and connect the mapper to the actor.

**Finally**, we add all the pipelines (actors) to the `renderer`, reset the camera, and render.

```python
renderer.AddActor(actor)
renderer.ResetCamera()
renderWindow.Render()
```

The VTK specific imports and pipelines defined for a `Trame` application are precisely the specific imports and pipelines required for a Python VTK script.

## Local and Remote Rendering

Why do we care about *local* and *remote* rendering? Well each method of rendering has it's advantages and disadvantaages.

**Local Rendering**

*Advantages*

- The server doesn't need a graphics processing unit (GPU). Systems with GPUs are expensive to purchase and expensive to rent (Cloud). These costs are pushed to the end-points on end-users.
- The frames per second rendering is higher. Advancements in the browser access to local GPU resources implies that the performance is nearly as good as available to a desktop application.

*Disadvantages*

- The data to be rendered must move from the server to the client. This transfer may be too slow and it may be too large.
- Where will the data be processed into graphic primitives? The processing may increase load and latency on the server side or the client side.

**Remote Rendering**

*Advantages*

- The data to be rendered doesn't move, only the resulting image.
- Rendering can utilize parallel and distributed processing to handle larger and larger data.
- The server can serve a more diverse set of clients. From cell phone to workstation, their requirements are limited to recieving and rendering images.

*Disadvantages*

- The frames per second rendering might be capped by the speed and latency of image delivery.
- The servers have to be more capable. Remote software rendering is possible, but the framerates will be further impacted.

**Implementation**

Down in the GUI section of the application, we **first** need to select a rendering scheme 

for *local rendering*

```python
html_view = vtk.VtkLocalView(renderWindow, ref="view")
```

for *remote rendering*

```python
html_view = vtk.VtkRemoteView(renderWindow, ref="view")
```

and define a container to hold the renderer

```python
layout.content.children += [
    vuetify.VContainer(
        fluid=True,
        classes="pa-0 fill-height",
        children=[html_view],
    )
]
```

We add a **Vuetify** component to the Web application. In this case, a `VContainer`. The arguments include: fluid (to get full width container), classes (CSS stylings), and children components (the local or remote view).

More information on [vuetify](https://vuetifyjs.com/en/introduction/why-vuetify/).

## Update and Start

Once the client and server are ready, we need to update the view (`html_view`). 

**First**, one needs to provide a function to do this as follows

```python
def update_view(**kwargs):
    html_view.update()
```

**Finally**, we revist the `start` function in the `Main`. There is an option variable called `on_ready`, which takes a function name to call when the server and client are ready. So we modify our start function to look like

```python
    start(layout, on_ready=update_view)
```

## Running the Application

```bash
cd examples/Tutorial/VTK
python ./app.py --port 1234
```

Open browser to `http://localhost:1234/`

## Interaction

- Rotate: Hold down the mouse and move
- Zoom: Hold down mouse + control key and move up (out) and down (in)
- Pan: Hold down the mouse + option key and move

## Other VTK Examples

Now you can take much of the code examples at [VTK Examples](https://kitware.github.io/vtk-examples/site/Python) and port them to Trame.

Checkout [Carotid.py]().

