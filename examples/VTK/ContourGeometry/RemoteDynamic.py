import os

import trame as tr
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


def get_html_view(remote_view):
    if remote_view:
        return html_remote_view
    return html_local_view


@tr.change("contour_value", "interactive")
def update_contour(contour_value, interactive, remote_view, force=False, **kwargs):
    if interactive or force:
        contour.SetValue(0, contour_value)
        get_html_view(remote_view).update()


@tr.change("remote_view")
def update_view_type(remote_view, **kwargs):
    elem = get_html_view(remote_view)
    html_view_container.children[0] = elem
    layout.flush_content()
    commit_changes()


def commit_changes():
    cv, i, rv = tr.get_state("contour_value", "interactive", "remote_view")
    update_contour(force=True, contour_value=cv, interactive=i, remote_view=rv)


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

html_remote_view = vtk.VtkRemoteView(renderWindow)
html_local_view = vtk.VtkLocalView(renderWindow)

html_view_container = vuetify.VContainer(
    fluid=True,
    classes="pa-0 fill-height",
    children=[html_local_view],  # start with SyncView
)

layout = SinglePage("VTK contour - Remote/Local rendering", on_ready=commit_changes)
layout.title.content = "Contour Application - Remote rendering"
layout.logo.click = "$refs.view.resetCamera()"

layout.state = {
    "data_range": data_range,
}

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
        click="$refs.view.resetCamera()",
    ):
        vuetify.VIcon("mdi-crop-free")

    vuetify.VProgressLinear(
        indeterminate=True,
        absolute=True,
        bottom=True,
        active=("busy",),
    )

layout.content.children += [html_view_container]

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
