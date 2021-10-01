import os

from trame import html, start, update_state, change, get_state
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


@change("contour_value", "interactive")
def update_contour(contour_value, interactive, force=False, **kwargs):
    if interactive or force:
        contour.SetValue(0, contour_value)
        html_view.update()


def commit_changes():
    cv, i = get_state("contour_value", "interactive")
    update_contour(force=True, contour_value=cv, interactive=i)


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------
html_view = vtk.VtkSyncView(renderWindow)  # Only change compare to RemoteRendering

layout = SinglePage("VTK contour - Remote/Local rendering")
layout.title.content = "Contour Application - Remote rendering"
layout.logo.content = "mdi-virus-outline"
layout.logo.click = "$refs.view.resetCamera()"
layout.toolbar.children += [
    vuetify.VSpacer(),
    vuetify.VSwitch(
        v_model=("interactive", False),
        hide_details=True,
        label="Update while dragging",
    ),
    vuetify.VSlider(
        v_model=("contour_value", contour_value),
        change=commit_changes,
        min=["data_range[0]"],
        max=["data_range[1]"],
        hide_details=True,
        dense=True,
        style="max-width: 300px",
    ),
    vuetify.VSwitch(
        v_model="$vuetify.theme.dark",
        hide_details=True,
    ),
    vuetify.VBtn(
        vuetify.VIcon("mdi-crop-free"),
        icon=True,
        click="$refs.view.resetCamera()",
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
        classes="pa-0 fill-height",
        children=[html_view],
    )
]

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # print(layout.html)
    start(layout, on_ready=html_view.update)
