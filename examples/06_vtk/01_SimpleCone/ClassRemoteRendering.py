r"""
Installation requirements:
    pip install trame trame-vuetify trame-vtk vtk
"""

from trame.app import get_server
from trame.decorators import TrameApp, change
from trame.widgets import vuetify, vtk as vtk_widgets
from trame.ui.vuetify import SinglePageLayout

from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkPolyDataMapper,
    vtkActor,
)

# VTK factory initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa
import vtkmodules.vtkRenderingOpenGL2  # noqa

# -----------------------------------------------------------------------------


@TrameApp()
class Cone:
    def __init__(self, server_or_name=None):
        self.server = get_server(server_or_name, client_type="vue2")
        self._vtk_rw, self._vtk_cone = self._vtk_setup()
        self.ui = self._generate_ui()

    @property
    def ctrl(self):
        return self.server.controller

    @property
    def state(self):
        return self.server.state

    @change("resolution")
    def on_resolution_change(self, resolution, **kwargs):
        self._vtk_cone.SetResolution(resolution)
        self.ctrl.view_update()

    @property
    def resolution(self):
        return self.state.resolution

    @resolution.setter
    def resolution(self, v):
        with self.state:
            self.state.resolution = v

    def reset_resolution(self):
        self.resolution = 6

    def _vtk_setup(self):
        renderer = vtkRenderer()
        renderWindow = vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindow.OffScreenRenderingOn()

        renderWindowInteractor = vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)
        renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

        cone_source = vtkConeSource()
        mapper = vtkPolyDataMapper()
        actor = vtkActor()
        mapper.SetInputConnection(cone_source.GetOutputPort())
        actor.SetMapper(mapper)
        renderer.AddActor(actor)
        renderer.ResetCamera()
        renderWindow.Render()

        return renderWindow, cone_source

    def _generate_ui(self):
        with SinglePageLayout(self.server) as layout:
            layout.title.set_text("Trame demo")
            with layout.toolbar as toolbar:
                toolbar.dense = True
                vuetify.VSpacer()
                vuetify.VSlider(
                    v_model=("resolution", 6),
                    min=3,
                    max=60,
                    step=1,
                    hide_details=True,
                    style="max-width: 300px;",
                )
                with vuetify.VBtn(icon=True, click=self.reset_resolution):
                    vuetify.VIcon("mdi-lock-reset")
                with vuetify.VBtn(icon=True, click=self.ctrl.view_reset_camera):
                    vuetify.VIcon("mdi-crop-free")

            with layout.content:
                with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                    view = vtk_widgets.VtkRemoteView(self._vtk_rw)
                    self.ctrl.view_update = view.update
                    self.ctrl.view_reset_camera = view.reset_camera

            return layout


def main(**kwargs):
    cone = Cone()
    cone.server.start(**kwargs)


if __name__ == "__main__":
    main()
