import vtkmodules.vtkRenderingOpenGL2  # noqa
from vtkmodules.vtkFiltersSources import vtkConeSource

# VTK factory initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import html, vtk, vuetify3
from trame.decorators import change


class Cone(TrameApp):
    def __init__(self, name=None):
        super().__init__(server=name)
        self._setup_vtk()
        self._build_ui()

    def _setup_vtk(self):
        renderer = vtkRenderer()
        render_window = vtkRenderWindow()
        render_window.AddRenderer(renderer)
        render_window.OffScreenRenderingOn()

        render_window_interactor = vtkRenderWindowInteractor()
        render_window_interactor.SetRenderWindow(render_window)
        render_window_interactor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

        cone_source = vtkConeSource()
        mapper = vtkPolyDataMapper()
        actor = vtkActor()
        mapper.SetInputConnection(cone_source.GetOutputPort())
        actor.SetMapper(mapper)
        renderer.AddActor(actor)
        renderer.ResetCamera()
        render_window.Render()

        self.cone_source = cone_source
        self.render_window = render_window

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
            self.ui.icon.click = self.ctrl.view_reset_camera
            with self.ui.toolbar:
                html.Div("resolution: {{ resolution }}")
                vuetify3.VSpacer()
                vuetify3.VSlider(
                    v_model=("resolution", 6), min=3, max=60, step=1, hide_details=True
                )
                vuetify3.VBtn("Reset", click=self.reset_resolution)
            with self.ui.content:
                with vtk.VtkRemoteView(
                    self.render_window,
                    interactive_ratio=1,
                ) as view:
                    self.ctrl.view_update = view.update
                    self.ctrl.view_reset_camera = view.reset_camera

    @change("resolution")
    def _on_resolution(self, resolution, **_):
        self.cone_source.SetResolution(resolution)
        self.ctrl.view_update()


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    app = Cone()
    app.server.start()
