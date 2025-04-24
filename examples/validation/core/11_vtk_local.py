from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vtk, vuetify

# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

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
# trame
# -----------------------------------------------------------------------------

server = get_server(
    client_type="vue2",
    # log_network="/Users/sebastien.jourdain/Documents/code/open-source/Web/trame-next/test-examples/logs",
)
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


@state.change("resolution")
def update_cone(resolution=DEFAULT_RESOLUTION, **kwargs):
    cone_source.SetResolution(resolution)
    ctrl.view_update()


def update_reset_resolution():
    state.resolution = DEFAULT_RESOLUTION


# Bind on life cycle method
ctrl.on_server_ready.add(update_cone)

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

layout = SinglePageLayout(server)
with layout:
    layout.title.set_text("Cone Application")
    layout.icon.click = ctrl.view_reset_camera

    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VSlider(
            v_model=("resolution", DEFAULT_RESOLUTION),
            min=3,
            max=60,
            step=1,
            hide_details=True,
            dense=True,
            style="max-width: 300px",
        )
        vuetify.VDivider(vertical=True, classes="mx-2")
        with vuetify.VBtn(icon=True, click=update_reset_resolution):
            vuetify.VIcon("mdi-undo-variant")

    with layout.content:
        with vuetify.VContainer(
            fluid=True,
            classes="pa-0 fill-height",
        ):
            view = vtk.VtkLocalView(renderWindow, ref="view")
            ctrl.view_update = view.update
            ctrl.view_reset_camera = view.reset_camera


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
