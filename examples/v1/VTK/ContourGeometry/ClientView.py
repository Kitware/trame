import os

from trame import change
from trame.html import vuetify, vtk
from trame.layouts import SinglePage

from vtkmodules.vtkIOXML import vtkXMLImageDataReader
from vtkmodules.vtkFiltersCore import vtkContourFilter

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

# Configure contour with valid values
contour.SetNumberOfContours(1)
contour.SetValue(0, contour_value)


# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


@change("contour_value")
def update_contour(contour_value, **kwargs):
    contour.SetValue(0, contour_value)
    html_polydata.update()


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------
html_polydata = vtk.VtkPolyData("contour", dataset=contour)

layout = SinglePage("VTK contour - Remote/Local rendering", on_ready=update_contour)
layout.title.set_text("Contour Application - Local rendering")

layout.state = {
    "data_range": data_range,
}

with layout.toolbar:
    vuetify.VSpacer()
    vuetify.VSlider(
        value=("contour_value", contour_value),
        min=("data_range[0]",),
        max=("data_range[1]",),
        hide_details=True,
        dense=True,
        style="max-width: 300px",
        change="contour_value = Number($event)",
    )
    vuetify.VSwitch(
        v_model="$vuetify.theme.dark",
        hide_details=True,
    )

    with vuetify.VBtn(icon=True, click="$refs.view.resetCamera()"):
        vuetify.VIcon("mdi-crop-free")

    vuetify.VProgressLinear(
        indeterminate=True,
        absolute=True,
        bottom=True,
        active=("busy",),
    )

with layout.content:
    with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
        with vtk.VtkView() as view:
            layout.logo.click = view.reset_camera
            vtk.VtkGeometryRepresentation([html_polydata])

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
