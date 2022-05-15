from trame.app import get_server
from trame.widgets import vuetify, vtk
from trame.ui.vuetify import SinglePageLayout

import time

from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkRenderingCore import (
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkDataSetMapper,
    vtkActor,
)

# VTK factory initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa
import vtkmodules.vtkRenderingOpenGL2  # noqa

# -----------------------------------------------------------------------------
# Trame initialization
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller

state.trame__title = "Geometry export"

# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

DEFAULT_RESOLUTION = 10

renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

source = vtkRTAnalyticSource()
filter = vtkGeometryFilter()
filter.SetInputConnection(source.GetOutputPort())
mapper = vtkDataSetMapper()
actor = vtkActor()
mapper.SetInputConnection(filter.GetOutputPort())
actor.SetMapper(mapper)
renderer.AddActor(actor)
renderer.ResetCamera()
renderWindow.Render()

filter.Update()
_min, _max = filter.GetOutput().GetPointData().GetScalars().GetRange()
mapper.SetScalarRange(_min, _max)
actor.GetProperty().SetEdgeVisibility(1)
actor.GetProperty().SetEdgeColor(1, 1, 1)

# -----------------------------------------------------------------------------


def update_view():
    t0 = time.time()
    ctrl.view_update()
    t1 = time.time()
    print(f"Server: Updated scene in {t1-t0:.3f}s")


@state.change("resolution")
def update_resolution(resolution=DEFAULT_RESOLUTION, **kwargs):
    source.SetWholeExtent(
        -resolution, resolution, -resolution, resolution, -resolution, resolution
    )
    ctrl.view_reset_camera()
    update_view()


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

with SinglePageLayout(server) as layout:
    layout.icon.click = ctrl.view_reset_camera
    layout.title.set_text("Geometry export")

    with layout.toolbar as tb:
        vuetify.VSpacer()
        tb.add_child("{{ resolution }}")
        vuetify.VSlider(
            v_model=("resolution", DEFAULT_RESOLUTION),
            min=10,
            max=100,
            step=1,
            hide_details=True,
            dense=True,
            style="max-width: 300px",
        )
        vuetify.VBtn("Update", click=update_view)

    with layout.content:
        with vuetify.VContainer(
            fluid=True,
            classes="pa-0 fill-height",
        ):
            # view = vtk.VtkLocalView(renderWindow)
            # view = vtk.VtkRemoteView(renderWindow)
            view = vtk.VtkRemoteLocalView(renderWindow, mode="local")
            ctrl.view_update = view.update
            ctrl.view_reset_camera = view.reset_camera


ctrl.on_server_ready.add(ctrl.view_update)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
