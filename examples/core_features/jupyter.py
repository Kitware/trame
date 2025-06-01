from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import html, vtk, vuetify3


class Cone(TrameApp):
    def __init__(self, name=None):
        super().__init__(server=name)
        self._build_ui()

    @property
    def resolution(self):
        return self.state.resolution

    @resolution.setter
    def resolution(self, v):
        with self.state:
            self.state.resolution = v

    def reset_resolution(self):
        self.resolution = 6

    def _build_ui(self):
        with SinglePageLayout(self.server) as self.ui:
            self.ui.icon.click = self.ctrl.reset_camera
            with self.ui.toolbar:
                html.Div("resolution: {{ resolution }}")
                vuetify3.VSpacer()
                vuetify3.VSlider(
                    v_model=("resolution", 6), min=3, max=60, step=1, hide_details=True
                )
                vuetify3.VBtn("Reset", click=self.reset_resolution)
            with self.ui.content:
                with vuetify3.VContainer(fluid=True, classes="pa-0 fill-height"):
                    with vtk.VtkView() as vtk_view:
                        self.ctrl.reset_camera = vtk_view.reset_camera
                        with vtk.VtkGeometryRepresentation():
                            vtk.VtkAlgorithm(
                                vtkClass="vtkConeSource", state=("{ resolution }",)
                            )
