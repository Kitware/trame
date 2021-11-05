import os
from trame import start, change, update_state, get_state
from trame.layouts import SinglePageWithDrawer
from trame.html import Div, vtk, vuetify, widgets

from vtkmodules.vtkIOXML import (
    vtkXMLUnstructuredGridReader,
)
from vtkmodules.vtkRenderingAnnotation import (
    vtkCubeAxesActor,
)
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
)
from vtkmodules.vtkFiltersExtraction import (
    vtkExtractGeometry,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkDataSetMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

# Required for interacter factory initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa

# Required for remote rendering factory initialization, not necessary for
# local rendering, but doesn't hurt to include it

import vtkmodules.vtkRenderingOpenGL2  # noqa

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

# -----------------------------------------------------------------------------
# Globals
# -----------------------------------------------------------------------------

DEFAULT_RESOLUTION = 6
Points = 0
Wireframe = 1
Surface = 2
SurfaceWithEdges = 3

# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()
renderWindowInteractor.EnableRenderOff()

reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(os.path.join(CURRENT_DIRECTORY, "../data/disk_out_ref.vtu"))
reader.Update()

numberOfPointArrays = reader.GetOutput().GetPointData().GetNumberOfArrays()
numberOfCellArrays = reader.GetOutput().GetCellData().GetNumberOfArrays()

arrayNames = []
if numberOfPointArrays > 0:

    for i in range(numberOfPointArrays):
        array = reader.GetOutput().GetPointData().GetArray(i)
        array_name = array.GetName()
        arrayNames.append({"text": array_name, "value": i})

if numberOfCellArrays > 0:
    cellNames = []
    for i in range(numberOfCellArrays):
        array = reader.GetOutput().GetCellData().GetArray(i)
        array_name = array.GetName()
        arrayNames.append({"text": array_name, "value": i})

meshMapper = vtkDataSetMapper()
meshMapper.SetInputConnection(reader.GetOutputPort())
update_state("meshVisibility", True)
meshActor = vtkActor()
meshActor.SetMapper(meshMapper)
meshActor.SetVisibility(True)
update_state("meshRepresentation", Surface)
representations = [
    {"text": "Points", "value": 0},
    {"text": "Wireframe", "value": 1},
    {"text": "Surface", "value": 2},
    {"text": "SurfaceWithEdges", "value": 3},
]
update_state("representations", representations)
meshActor.GetProperty().SetRepresentationToSurface()
meshActor.GetProperty().EdgeVisibilityOff()

# Cube Axes Actor
update_state("cubeAxesVisibility", True)
cubeAxesActor = vtkCubeAxesActor()
bounds = meshMapper.GetBounds()
cubeAxesActor.SetBounds(
    bounds[0], bounds[1], bounds[2], bounds[3], bounds[4], bounds[5]
)
cubeAxesActor.SetCamera(renderer.GetActiveCamera())
cubeAxesActor.SetXLabelFormat("%6.1f")
cubeAxesActor.SetYLabelFormat("%6.1f")
cubeAxesActor.SetZLabelFormat("%6.1f")
cubeAxesActor.SetFlyModeToOuterEdges()
cubeAxesActor.SetVisibility(True)

# contour filter for temperature data
# contour = vtkContourFilter()
# contour.SetInputConnection(reader.GetOutputPort())
# contour.GenerateValues()
# contourMapper = vtkPolyDataMapper()
# contourMapper.SetInputConnection(contour.GetOutputPort())
# contourActor = vtkActor()
# contourActor.SetMapper(contourMapper)

# extract skin filter
# skin = vtkExtractGeometry()
# skin.SetInputConnection(reader.GetOutputPort())
# skin.Update()
# skinMapper = vtkPolyDataMapper()
# skinMapper.SetInputConnection(skin.GetOutputPort())
# skinActor = vtkActor()
# skinActor.SetMapper(skinMapper)

renderer.AddActor(meshActor)
renderer.AddActor(cubeAxesActor)
# renderer.AddActor(contourActor)
# renderer.AddActor(skinActor)
renderer.ResetCamera()
renderWindow.Render()

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------


def update_view(**kwargs):
    html_view.update()


@change("cubeAxesVisibility")
def update_cube_axes_visibitily(**kwargs):
    (v,) = get_state("cubeAxesVisibility")
    cubeAxesActor.SetVisibility(v)
    update_view()


@change("meshVisibility")
def update_cube_axes_visibitily(**kwargs):
    (v,) = get_state("meshVisibility")
    meshActor.SetVisibility(v)
    update_view()


@change("meshRepresentation")
def update_mesh_representation(**kwargs):
    (r,) = get_state("meshRepresentation")
    if r == Points:
        meshActor.GetProperty().SetRepresentationToPoints()
        meshActor.GetProperty().SetPointSize(5)
        meshActor.GetProperty().EdgeVisibilityOff()
    elif r == Wireframe:
        meshActor.GetProperty().SetRepresentationToWireframe()
        meshActor.GetProperty().SetPointSize(1)
        meshActor.GetProperty().EdgeVisibilityOff()
    elif r == Surface:
        meshActor.GetProperty().SetRepresentationToSurface()
        meshActor.GetProperty().SetPointSize(1)
        meshActor.GetProperty().EdgeVisibilityOff()
    elif r == SurfaceWithEdges:
        meshActor.GetProperty().SetRepresentationToSurface()
        meshActor.GetProperty().SetPointSize(1)
        meshActor.GetProperty().EdgeVisibilityOn()
    update_view()


def actives_change(ids):
    (_id,) = ids
    (pipeline,) = get_state("pipeline")
    for item in pipeline:
        if item.get("id") == _id:
            update_state("active_card", item.get("name"))


def visibility_change(event):
    print("visibility_change", event)


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

layout = SinglePageWithDrawer("Trame Viewer")
layout.title.content = "Viewer"

with layout.toolbar:
    vuetify.VSpacer()
    vuetify.VDivider(vertical=True, classes="mx-2")
    vuetify.VSwitch(
        v_model="$vuetify.theme.dark",
        hide_details=True,
    )
    with vuetify.VBtn(
        icon=True,
        click="$refs.view.resetCamera()",
    ):
        vuetify.VIcon("mdi-crop-free")

with layout.drawer:
    widgets.GitTree(
        sources=(
            "pipeline",
            [
                {"id": "1", "parent": "0", "visible": 1, "name": "Cube Axes"},
                {"id": "2", "parent": "0", "visible": 1, "name": "Mesh"},
            ],
        ),
        selection=("pipeline_selection", []),
        actives_change=(actives_change, "[$event]"),
        visibility_change=(visibility_change, "[$event]"),
    )
    with vuetify.VCard(
        classes="ma-4 rounded elevation-8", v_show="active_card == 'Cube Axes'"
    ):
        with vuetify.VCardTitle(
            classes="grey lighten-1 py-0 grey--text text--darken-3",
            style="user-select: none; cursor: pointer",
        ):
            vuetify.VCheckbox(
                hide_details=True,
                classes="ma-0 pa-0 float-left",
                v_model="cubeAxesVisibility",
                color="#ffd600",
                off_icon="mdi-eye-off",
                on_icon="mdi-eye",
                value=True,
            )
            Div("Cube Axes")
        vuetify.VCardText(
            classes="pb-0 mb-n2 px-0",
        )
        vuetify.VCardActions(
            classes="pa-0 pb-3",
        )
    with vuetify.VCard(
        classes="ma-4 rounded elevation-8", v_show="active_card == 'Mesh'"
    ):
        with vuetify.VCardTitle(
            classes="grey lighten-1 py-0 grey--text text--darken-3",
            style="user-select: none; cursor: pointer",
            dense=True,
        ):
            vuetify.VCheckbox(
                hide_details=True,
                classes="ma-0 pa-0 float-left",
                v_model="meshVisibility",
                color="#ffd600",
                off_icon="mdi-eye-off",
                on_icon="mdi-eye",
                value=True,
            )
            Div("Mesh")
        with vuetify.VCardText(
            classes="pb-0 mb-n2 px-0",
        ):
            vuetify.VSelect(
                v_model="meshRepresentation",
                items=["representations"],
                hide_details=True,
                dense=True,
                outlined=True,
            )
        vuetify.VCardActions(
            classes="pa-0 pb-3",
        )

html_view = vtk.VtkLocalView(renderWindow)

with layout.content:
    vuetify.VContainer(
        fluid=True,
        classes="pa-0 fill-height",
        children=[html_view],
    )


layout.state = {
    "active_card": "",
}

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    start(layout, on_ready=update_view)
