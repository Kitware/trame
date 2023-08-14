r"""
Version for trame 1.x - https://github.com/Kitware/trame/blob/release-v1/examples/VTK/ContourGeometry/RemoteDynamic.py
Delta v1..v2          - https://github.com/Kitware/trame/commit/3852cba56cd63f6efa684d5e5fb00881a6111e81

Installation requirements:
    pip install trame trame-vuetify trame-vtk
"""

from pathlib import Path

from trame.app import get_server
from trame.widgets import vuetify, vtk as vtk_widgets
from trame.ui.vuetify import SinglePageLayout

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
# Trame initialization
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller

state.trame__title = "VTK contour - Remote/Local rendering"

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


# share state with client
state.data_range = data_range

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


def get_html_view(remote_view):
    if remote_view:
        return html_remote_view
    return html_local_view


@state.change("contour_value", "interactive")
def update_contour(contour_value, interactive, remote_view, force=False, **kwargs):
    if interactive or force:
        contour.SetValue(0, contour_value)
        get_html_view(remote_view).update()


@state.change("remote_view")
def update_view_type(remote_view, **kwargs):
    elem = get_html_view(remote_view)
    with layout:
        html_view_container.clear()
        html_view_container.add_child(elem)
        ctrl.view_reset_camera = elem.reset_camera
    commit_changes()


def commit_changes():
    update_contour(
        contour_value=state.contour_value,
        interactive=state.interactive,
        remote_view=state.remote_view,
        force=True,
    )


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

html_remote_view = vtk_widgets.VtkRemoteView(renderWindow, trame_server=server)
html_local_view = vtk_widgets.VtkLocalView(renderWindow, trame_server=server)


layout = SinglePageLayout(server)

with layout:
    layout.title.set_text("Contour Application - Remote rendering")
    layout.icon.click = ctrl.view_reset_camera

    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VSwitch(
            v_model=("remote_view", False),
            hide_details=True,
            label="RemoteView",
            classes="mx-2",
        )
        vuetify.VSwitch(
            v_model=("interactive", False),
            hide_details=True,
            label="Update while dragging",
            classes="mx-2",
        )
        vuetify.VSlider(
            v_model=("contour_value", contour_value),
            change=commit_changes,
            min=("data_range[0]",),
            max=("data_range[1]",),
            hide_details=True,
            dense=True,
            style="max-width: 300px",
        )
        vuetify.VSwitch(
            v_model="$vuetify.theme.dark",
            hide_details=True,
        )
        with vuetify.VBtn(
            icon=True,
            click=ctrl.view_reset_camera,
        ):
            vuetify.VIcon("mdi-crop-free")

        vuetify.VProgressLinear(
            indeterminate=True,
            absolute=True,
            bottom=True,
            active=("trame__busy",),
        )

    with layout.content:
        html_view_container = vuetify.VContainer(
            fluid=True,
            classes="pa-0 fill-height",
        )

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
