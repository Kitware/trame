from trame.app import get_server
from trame.widgets import vtk, trame, vuetify, html
from trame.ui.vuetify import SinglePageLayout

# -----------------------------------------------------------------------------
# VTK
# -----------------------------------------------------------------------------

from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkPolyDataMapper,
    vtkActor,
)
import vtkmodules.vtkRenderingOpenGL2  # noqa
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa

DEFAULT_RESOLUTION = 6

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

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller


def reset_resolution():
    state.resolution = 6


@state.change("resolution")
def update_resolution(resolution, **kwargs):
    cone_source.SetResolution(int(resolution))
    ctrl.view_update()


# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

layout = SinglePageLayout(server)

with layout:
    # Validate client life cycle
    trame.LifeCycleMonitor(events=("['created']",))

    layout.icon.click = ctrl.reset_camera
    layout.title.set_text("Cone")
    layout.toolbar.dense = True

    # Toolbar
    with layout.toolbar as toolbar:
        vuetify.VSpacer()
        html.Div("Test size", classes="text-h6")
        vuetify.VSlider(
            hide_details=True,
            v_model=("resolution", 6),
            max=60,
            min=3,
            step=1,
            style="max-width: 300px;",
        )
        vuetify.VSwitch(
            hide_details=True,
            v_model=("$vuetify.theme.dark",),
        )
        with vuetify.VBtn(icon=True, click=reset_resolution):
            vuetify.VIcon("mdi-undo")

    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            view = vtk.VtkRemoteView(renderWindow, interactive_ratio=1)
            ctrl.view_update = view.update
            ctrl.reset_camera = view.reset_camera


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start(exec_mode="desktop")
