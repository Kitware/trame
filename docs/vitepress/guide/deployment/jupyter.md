# Jupyter

Trame applications can be imported and shown within a Jupyter cell without missing any of your application capabilities.

The [trame-cookiecutter](https://github.com/Kitware/trame-cookiecutter) provide an initial helper that live under `{package_name}/app/jupyter.py` which provide a `show()` method.

But such `show()` method can be implemented for a single file application like below when no additional parameter are required for your application:

```python
def show(**kwargs):
    from trame.app import jupyter
    jupyter.show(server, **kwargs)
```

Also the layout can be directly returned and will be displayed within Jupyter appropriately. And the server can be started as a background task by calling `await layout.ready`.

![Trame in Jupyer](/assets/images/deployment/jupyter.png)

The way such integration works is by running the trame server as an asynchronous task within Tornedo (Jupyter kernel) and opening a new port so that iframe can connect to it.
This means that everything defined within your Jupyter environment is accessible within trame and vice-versa.


## Code example

Disable trame version 3 warning.

```python
import os

os.environ["TRAME_DISABLE_V3_WARNING"] = "1"
```

Create trame application as a class so it can be instantiated several time within Jupyter.

```python

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, vtk
from trame.decorators import TrameApp, change


@TrameApp()
class Cone:
    def __init__(self, name=None):
        self.server = get_server(name)
        self.server.client_type = "vue2"
        self._ui = None

        # Build UI
        self.ui

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    @property
    def resolution(self):
        return self.state.resolution

    @resolution.setter
    def resolution(self, v):
        with self.state:
            self.state.resolution = v

    def reset_resolution(self):
        self.resolution = 6

    @change("resolution")
    def _resolution_change(self, resolution, **kwargs):
        print("New resolution", resolution)

    @property
    def ui(self):
        if self._ui is None:
            with SinglePageLayout(self.server) as layout:
                self._ui = layout
                with layout.toolbar:
                    vuetify.VSpacer()
                    vuetify.VSlider(v_model=("resolution", 6), min=3, max=60, hide_details=True)
                    vuetify.VBtn("Reset", click=self.reset_resolution)
                with layout.content:
                    with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                        with vtk.VtkView() as vtk_view:
                            self.ctrl.reset_camera = vtk_view.reset_camera
                            with vtk.VtkGeometryRepresentation():
                                vtk.VtkAlgorithm(
                                    vtkClass="vtkConeSource",
                                    state=("{ resolution }",)
                                )

        return self._ui
```

Start the server and display the application UI.

```python
cone = Cone()
await cone.ui.ready
cone.ui
```