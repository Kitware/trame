from trame.app import get_server
from trame.widgets import html, trame, vtk
from trame.ui.html import DivLayout

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
# Web App setup
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller

with DivLayout(server) as layout:
    container = layout.root
    trame.LifeCycleMonitor(events=("['created']",))
    container.style = "width: 100vw; height: 100vh;"
    view = vtk.VtkRemoteView(renderWindow)
    ctrl.view_update = view.update
    html.Input(
        type="range",
        min=3,
        max=60,
        step=1,
        v_model=("resolution", 6),
        style="position: absolute; top: 20px; left: 20px; z-index: 1; width: 25%; min-width: 300px;",
    )


@state.change("resolution")
def update_resolution(resolution, **kwargs):
    cone_source.SetResolution(int(resolution))
    ctrl.view_update()


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
