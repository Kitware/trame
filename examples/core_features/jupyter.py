r"""
Within Jupyter

```
import os
os.environ["TRAME_DISABLE_V3_WARNING"] = "1"

cone = Cone()
await cone.ui.ready
cone.ui
```

Another cell

```
cone.resolution = 4
```

"""


from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import html, vuetify, vtk
from trame.decorators import TrameApp, change


@TrameApp()
class Cone:
    def __init__(self, name=None):
        self.server = get_server(name)
        self.server.client_type = "vue2"
        self._ui = None

        self.state.a = 0

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
        self.state.a = resolution

    @property
    def ui(self):
        if self._ui is None:
            with SinglePageLayout(self.server) as layout:
                self._ui = layout
                with layout.toolbar:
                    html.Div("a: {{ a }}")
                    vuetify.VSpacer()
                    vuetify.VSlider(
                        v_model=("resolution", 6), min=3, max=60, hide_details=True
                    )
                    vuetify.VBtn("Reset", click=self.reset_resolution)
                with layout.content:
                    with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                        with vtk.VtkView() as vtk_view:
                            self.ctrl.reset_camera = vtk_view.reset_camera
                            with vtk.VtkGeometryRepresentation():
                                vtk.VtkAlgorithm(
                                    vtkClass="vtkConeSource", state=("{ resolution }",)
                                )

        return self._ui
