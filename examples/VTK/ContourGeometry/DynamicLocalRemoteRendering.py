import os

from trame import html, start, update_state, change, get_app_instance
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
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch

# Grab implementation
import vtkmodules.vtkRenderingOpenGL2

# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

data_directory = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
)
head_vti = os.path.join(data_directory, "head.vti")

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
update_state("data_range", data_range)
update_state("contour_value", contour_value)

# Configure contour with valid values
contour.SetNumberOfContours(1)
contour.SetValue(0, contour_value)

# Rendering setup
renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.SetSize(300, 300)
renderWindow.SetWindowName("rendering")
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()
renderWindowInteractor.EnableRenderOff()

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


@change("contour_value")
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

layout = SinglePage("VTK contour - Remote/Local rendering")
layout.title.content = "Contour Application - Remote rendering"
layout.logo.content = "mdi-virus-outline"
layout.logo.click = "$refs.demo.resetCamera()"
layout.toolbar.children += [
    vuetify.VSpacer(),
    vuetify.VBtnToggle(
        v_model=("override", "auto"),
        dense=True,
        mandatory=True,
        children=[
            vuetify.VBtn(vuetify.VIcon("mdi-autorenew"), value="auto"),
            vuetify.VBtn(vuetify.VIcon("mdi-rotate-3d"), value="local"),
            vuetify.VBtn(vuetify.VIcon("mdi-image"), value="remote"),
        ],
    ),
    vuetify.VSpacer(),
    vuetify.VSlider(
        v_model="contour_value",
        min=["data_range[0]"],
        max=["data_range[1]"],
        hide_details=True,
        dense=True,
        style="max-width: 300px",
        start="trigger('demoAnimateStart')",
        end="trigger('demoAnimateStop')",
    ),
    vuetify.VSwitch(
        v_model="$vuetify.theme.dark",
        hide_details=True,
    ),
    vuetify.VBtn(
        vuetify.VIcon("mdi-crop-free"),
        icon=True,
        click="$refs.demo.resetCamera()",
    ),
    vuetify.VProgressLinear(
        indeterminate=True,
        absolute=True,
        bottom=True,
        active=["busy"],
    ),
]

layout.content.children += [
    vuetify.VContainer(
        fluid=True,
        fill_height=True,
        classes="pa-0",
        children=[html_view],
    )
]

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # print(layout.html)
    start(layout, on_ready=html_view.update_geometry)
