from pathlib import Path

from trame import state
from trame.html import vuetify, vtk
from trame.layouts import SinglePage

from vtkmodules.vtkIOXML import vtkXMLImageDataReader
from vtkmodules.vtkFiltersCore import vtkContourFilter
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
# VTK pipeline
# -----------------------------------------------------------------------------

data_directory = Path(__file__).parent.parent.parent.with_name("data")
head_vti = data_directory / "head.vti"

reader = vtkXMLImageDataReader()
reader.SetFileName(head_vti)
reader.Update()

contour = vtkContourFilter()
contour.SetInputConnection(reader.GetOutputPort())
contour.SetComputeNormals(1)
contour.SetComputeScalars(0)

# Extract data range => Update store/state
data_range = reader.GetOutput().GetPointData().GetScalars().GetRange()
contour_value = 0.5 * (data_range[0] + data_range[1])
state.data_range = data_range
state.contour_value = contour_value

# Configure contour with valid values
contour.SetNumberOfContours(1)
contour.SetValue(0, contour_value)

# Rendering setup
renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

mapper = vtkPolyDataMapper()
actor = vtkActor()
mapper.SetInputConnection(contour.GetOutputPort())
actor.SetMapper(mapper)
renderer.AddActor(actor)
renderer.ResetCamera()
renderWindow.Render()

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


@state.change("contour_value")
def update_contour(contour_value, **kwargs):
    contour.SetValue(0, contour_value)
    html_view.update_image()


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------
html_view = vtk.VtkRemoteLocalView(
    renderWindow,
    namespace="demo",
    # second arg is to force the view to start in "local" mode
    mode=("override === 'auto' ? demoMode : override", "local"),
)

layout = SinglePage("VTK contour", on_ready=html_view.update_geometry)
layout.title.content = "Contour"
layout.logo.click = html_view.reset_camera

modes = (
    ("auto", "mdi-autorenew"),
    ("local", "mdi-rotate-3d"),
    ("remote", "mdi-image"),
)

with layout.toolbar:
    vuetify.VSpacer()

    with vuetify.VBtnToggle(
        v_model=("override", "auto"),
        dense=True,
        mandatory=True,
    ):
        for entry in modes:
            with vuetify.VBtn(value=entry[0]):
                vuetify.VIcon(entry[1])

    vuetify.VSpacer()
    vuetify.VSlider(
        v_model="contour_value",
        min=("data_range[0]",),
        max=("data_range[1]",),
        hide_details=True,
        dense=True,
        style="max-width: 300px",
        start="trigger('demoAnimateStart')",
        end="trigger('demoAnimateStop')",
    )
    vuetify.VSwitch(
        v_model="$vuetify.theme.dark",
        hide_details=True,
    )

    with vuetify.VBtn(icon=True, click=html_view.reset_camera):
        vuetify.VIcon("mdi-crop-free")

    vuetify.VProgressLinear(
        indeterminate=True,
        absolute=True,
        bottom=True,
        active=("busy",),
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
