r"""
Version for trame 1.x - https://github.com/Kitware/trame/blob/release-v1/examples/VTK/ContourGeometry/DynamicLocalRemoteRendering.py
Delta v1..v2          - https://github.com/Kitware/trame/commit/3852cba56cd63f6efa684d5e5fb00881a6111e81

Installation requirements:
    pip install trame trame-vuetify trame-vtk vtk
"""

from pathlib import Path

import vtkmodules.vtkRenderingOpenGL2  # noqa
from vtkmodules.vtkFiltersCore import vtkContourFilter

# VTK factory initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa
from vtkmodules.vtkIOXML import vtkXMLImageDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vtk as vtk_widgets
from trame.widgets import vuetify

# -----------------------------------------------------------------------------
# Trame initialization
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

state.trame__title = "VTK contour"
ctrl.on_server_ready.add(ctrl.view_update)

# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

data_directory = Path(__file__).parent.parent.with_name("data")
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
    ctrl.view_update_image()


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

modes = (
    ("auto", "mdi-autorenew"),
    ("local", "mdi-rotate-3d"),
    ("remote", "mdi-image"),
)


with SinglePageLayout(server) as layout:
    layout.title.set_text("Contour")
    layout.icon.click = ctrl.view_reset_camera

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
            change=ctrl.view_update,
        )
        vuetify.VSwitch(
            v_model="$vuetify.theme.dark",
            hide_details=True,
        )

        with vuetify.VBtn(icon=True, click=ctrl.view_reset_camera):
            vuetify.VIcon("mdi-crop-free")

        vuetify.VProgressLinear(
            indeterminate=True,
            absolute=True,
            bottom=True,
            active=("trame__busy",),
        )

    with layout.content:
        with vuetify.VContainer(
            fluid=True,
            classes="pa-0 fill-height",
        ):
            view = vtk_widgets.VtkRemoteLocalView(
                renderWindow,
                namespace="demo",
                # second arg is to force the view to start in "local" mode
                mode=("override === 'auto' ? demoMode : override", "local"),
            )
            ctrl.view_reset_camera = view.reset_camera
            ctrl.view_update = view.update
            ctrl.view_update_image = view.update_image

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
