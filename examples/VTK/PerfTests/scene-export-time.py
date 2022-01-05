from trame import state
from trame.html import vuetify, vtk
from trame.layouts import SinglePage

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

@state.change("resolution")
def update_resolution(resolution=DEFAULT_RESOLUTION, **kwargs):
    source.SetWholeExtent(
        -resolution, resolution,
        -resolution, resolution,
        -resolution, resolution
    )
    html_view.reset_camera()
    html_view.update()

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

# html_view = vtk.VtkLocalView(renderWindow)
# html_view = vtk.VtkRemoteView(renderWindow)
html_view = vtk.VtkRemoteLocalView(renderWindow, mode="local")

layout = SinglePage("Geometry export", on_ready=html_view.update)
layout.logo.click = html_view.reset_camera
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
    vuetify.VBtn(
        "Update",
        click=html_view.update
    )

with layout.content:
    vuetify.VContainer(
        fluid=True,
        classes="pa-0 fill-height",
        children=[html_view],
    )


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
