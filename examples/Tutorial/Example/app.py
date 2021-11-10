import os
from trame import start, change, update_state, get_state, update_layout
from trame.layouts import SinglePageWithDrawer
from trame.html import Div, vtk, vuetify, widgets

from vtkmodules.vtkCommonDataModel import (
    vtkDataObject,
)
from vtkmodules.vtkIOXML import (
    vtkXMLUnstructuredGridReader,
)
from vtkmodules.vtkRenderingAnnotation import (
    vtkCubeAxesActor,
)
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
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

Points = 0
Wireframe = 1
Surface = 2
SurfaceWithEdges = 3

representations = [
    {"text": "Points", "value": 0},
    {"text": "Wireframe", "value": 1},
    {"text": "Surface", "value": 2},
    {"text": "SurfaceWithEdges", "value": 3},
]
update_state("representations", representations)

Rainbow = 0
Inverted_Rainbow = 1
Greyscale = 2
Inverted_Greyscale = 3

colormaps = [
    {"text": "Rainbow", "value": 0},
    {"text": "Inv Rainbow", "value": 1},
    {"text": "Greyscale", "value": 2},
    {"text": "Inv Greyscale", "value": 3},
]
update_state("colormaps", colormaps)

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

arrayData = []
update_state("arrayData", arrayData)
if numberOfPointArrays > 0:
    for i in range(numberOfPointArrays):
        array = reader.GetOutput().GetPointData().GetArray(i)
        array_name = array.GetName()
        array_range = array.GetRange()
        arrayData.append(
            {
            "text": array_name, 
            "value": i, 
            "min": array_range[0], 
            "max": array_range[1], 
            "type": vtkDataObject.FIELD_ASSOCIATION_POINTS
            }
        )
if numberOfCellArrays > 0:
    cellNames = []
    for i in range(numberOfCellArrays):
        array = reader.GetOutput().GetCellData().GetArray(i)
        array_name = array.GetName()
        array_range = array.GetRange()
        arrayData.append(
            {
            "text": array_name, 
            "value": i, 
            "min": array_range[0], 
            "max": array_range[1], 
            "type": vtkDataObject.FIELD_ASSOCIATION_CELLS
            }
        )

# Mesh Actor

meshMapper = vtkDataSetMapper()
meshMapper.SetInputConnection(reader.GetOutputPort())

meshLUT = meshMapper.GetLookupTable()
update_state("meshColormap", Rainbow)
meshLUT.SetHueRange(0.666, 0.0)
meshLUT.SetSaturationRange(1.0, 1.0)
meshLUT.SetRange(float(arrayData[0]["min"]), float(arrayData[0]["max"]))
update_state("meshColorByName", 0)
meshMapper.SelectColorArray(arrayData[0]["text"])
meshMapper.SetScalarModeToUsePointFieldData()
meshMapper.SetScalarVisibility(True)
meshMapper.SetUseLookupTableScalarRange(True)

meshActor = vtkActor()
meshActor.SetMapper(meshMapper)
update_state("meshVisibility", True)
meshActor.SetVisibility(True)
update_state("meshRepresentation", Surface)
meshActor.GetProperty().SetRepresentationToSurface()
meshActor.GetProperty().EdgeVisibilityOff()
update_state("meshOpacity", 1.0)
meshActor.GetProperty().SetOpacity(1.0)

# Cube Axes Actor
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
update_state("cubeAxesVisibility", True)
cubeAxesActor.SetVisibility(True)

# Contour Actor
contour = vtkContourFilter()
update_state("contourBy", 0)
contour.SetInputArrayToProcess(0, 0, 0, arrayData[0]["type"], arrayData[0]["text"])
contour.SetInputConnection(reader.GetOutputPort())
update_state("contourMin", float(arrayData[0]["min"]))
update_state("contourMax", float(arrayData[0]["max"]))
contourStep = 0.01 * (arrayData[0]["max"] - arrayData[0]["min"])
update_state("contourStep", contourStep)
contourValue = 0.5 * (arrayData[0]["max"] + arrayData[0]["min"])
update_state("contourValue", contourValue)
contour.SetValue(0, contourValue)

contourMapper = vtkPolyDataMapper()
contourMapper.SetInputConnection(contour.GetOutputPort())

contourLUT = contourMapper.GetLookupTable()
update_state("contourColormap", Rainbow)
contourLUT.SetHueRange(0.666, 0.0)
contourLUT.SetSaturationRange(1.0, 1.0)
contourLUT.SetRange(float(arrayData[0]["min"]), float(arrayData[0]["max"]))
update_state("contourColorByName", 0)
contourMapper.SelectColorArray(arrayData[0]["text"])
contourMapper.SetScalarModeToUsePointFieldData()
contourMapper.SetScalarVisibility(True)
contourMapper.SetUseLookupTableScalarRange(True)

contourActor = vtkActor()
contourActor.SetMapper(contourMapper)
update_state("contourVisibility", True)
contourActor.SetVisibility(True)
update_state("contourRepresentation", Surface)
contourActor.GetProperty().SetRepresentationToSurface()
contourActor.GetProperty().EdgeVisibilityOff()
update_state("contourOpacity", 1.0)
contourActor.GetProperty().SetOpacity(1.0)

renderer.AddActor(meshActor)
renderer.AddActor(cubeAxesActor)
renderer.AddActor(contourActor)

renderer.ResetCamera()
renderWindow.Render()

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------


def update_view(**kwargs):
    html_view.update()

local_view = vtk.VtkLocalView(renderWindow)
remote_view = vtk.VtkRemoteView(renderWindow, interactive_ratio=(1,))
html_view = local_view
update_state("local_vs_remote", True)

@change("local_vs_remote")
def update_local_vs_remote(**kwargs):
    global html_view
    lvr, = get_state("local_vs_remote")
    if lvr:
        html_view = local_view
    else:
        html_view = remote_view
    layout.content.children[0].children[0] = html_view
    update_layout(layout)
    update_view()

@change("meshRepresentation")
def update_mesh_representation(**kwargs):
    r, = get_state("meshRepresentation")
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

@change("meshColorByName")
def update_mesh_color_by_name(**kwargs):
    c, = get_state("meshColorByName")
    meshMapper.SelectColorArray(arrayData[c]["text"])
    meshLUT.SetRange(float(arrayData[c]["min"]), float(arrayData[c]["max"]))
    update_view()

@change("meshColormap")
def update_mesh_colormap(**kwargs):
    c, = get_state("meshColormap")
    if c == Rainbow:
        meshLUT.SetHueRange(0.666, 0.0)
        meshLUT.SetSaturationRange(1.0, 1.0)
        meshLUT.SetValueRange(1.0, 1.0)
    elif c == Inverted_Rainbow:
        meshLUT.SetHueRange(0.0, 0.666)
        meshLUT.SetSaturationRange(1.0, 1.0)
        meshLUT.SetValueRange(1.0, 1.0)
    elif c == Greyscale:
        meshLUT.SetHueRange(0.0, 0.0)
        meshLUT.SetSaturationRange(0.0, 0.0)
        meshLUT.SetValueRange(0.0, 1.0)
    elif c == Inverted_Greyscale:
        meshLUT.SetHueRange(0.0, 0.666)
        meshLUT.SetSaturationRange(0.0, 0.0)
        meshLUT.SetValueRange(1.0, 0.0)
    meshLUT.Build()
    update_view()

@change("meshOpacity")
def update_mesh_opacity(**kwargs):
    o, = get_state("meshOpacity")
    meshActor.GetProperty().SetOpacity(o)
    update_view()

@change("contourBy")
def update_contour_by(**kwargs):
    c, = get_state("contourBy")
    contour.SetInputArrayToProcess(0, 0, 0, arrayData[c]["type"], arrayData[c]["text"])
    update_state("contourMin", float(arrayData[c]["min"]))
    update_state("contourMax", float(arrayData[c]["max"]))
    contourStep = 0.01 * (arrayData[c]["max"] - arrayData[c]["min"])
    update_state("contourStep", contourStep)
    contourValue = 0.5 * (arrayData[c]["max"] + arrayData[c]["min"])
    update_state("contourValue", contourValue)
    contour.SetValue(0, contourValue)
    update_view()

@change("contourValue")
def update_contourValue(**kwargs):
    c, = get_state("contourValue")
    contour.SetValue(0, c)
    update_view()

@change("contourRepresentation")
def update_contour_representation(**kwargs):
    r, = get_state("contourRepresentation")
    if r == Points:
        contourActor.GetProperty().SetRepresentationToPoints()
        contourActor.GetProperty().SetPointSize(5)
        contourActor.GetProperty().EdgeVisibilityOff()
    elif r == Wireframe:
        contourActor.GetProperty().SetRepresentationToWireframe()
        contourActor.GetProperty().SetPointSize(1)
        contourActor.GetProperty().EdgeVisibilityOff()
    elif r == Surface:
        contourActor.GetProperty().SetRepresentationToSurface()
        contourActor.GetProperty().SetPointSize(1)
        contourActor.GetProperty().EdgeVisibilityOff()
    elif r == SurfaceWithEdges:
        contourActor.GetProperty().SetRepresentationToSurface()
        contourActor.GetProperty().SetPointSize(1)
        contourActor.GetProperty().EdgeVisibilityOn()
    update_view()

@change("contourColorByName")
def update_contour_color_by_name(**kwargs):
    c, = get_state("contourColorByName")
    contourMapper.SelectColorArray(arrayData[c]["text"])
    contourLUT.SetRange(float(arrayData[c]["min"]), float(arrayData[c]["max"]))
    update_view()

@change("contourColormap")
def update_contour_colormap(**kwargs):
    c, = get_state("contourColormap")
    if c == Rainbow:
        contourLUT.SetHueRange(0.666, 0.0)
        contourLUT.SetSaturationRange(1.0, 1.0)
        contourLUT.SetValueRange(1.0, 1.0)
    elif c == Inverted_Rainbow:
        contourLUT.SetHueRange(0.0, 0.666)
        contourLUT.SetSaturationRange(1.0, 1.0)
        contourLUT.SetValueRange(1.0, 1.0)
    elif c == Greyscale:
        contourLUT.SetHueRange(0.0, 0.0)
        contourLUT.SetSaturationRange(0.0, 0.0)
        contourLUT.SetValueRange(0.0, 1.0)
    elif c == Inverted_Greyscale:
        contourLUT.SetHueRange(0.0, 0.666)
        contourLUT.SetSaturationRange(0.0, 0.0)
        contourLUT.SetValueRange(1.0, 0.0)
    contourLUT.Build()
    update_view()

@change("contourOpacity")
def update_contour_opacity(**kwargs):
    o, = get_state("contourOpacity")
    contourActor.GetProperty().SetOpacity(o)
    update_view()

def actives_change(ids):
    (_id,) = ids
    (pipeline,) = get_state("pipeline")
    for item in pipeline:
        if item.get("id") == _id:
            update_state("active_card", item.get("name"))

def visibility_change(event):
    if int(event["id"]) == 1:
        update_state("cubeAxesVisibility", event["visible"])
        cubeAxesActor.SetVisibility(event["visible"])
        update_view()
    elif int(event["id"]) == 2:
        update_state("meshVisibility", event["visible"])
        meshActor.SetVisibility(event["visible"])
        update_view()
    elif int(event["id"]) == 3:
        update_state("contourVisibility", event["visible"])
        contourActor.SetVisibility(event["visible"])
        update_view()

# -----------------------------------------------------------------------------
# GUI Cards
# -----------------------------------------------------------------------------

<<<<<<< HEAD
layout = SinglePageWithDrawer("Trame Viewer", on_ready=update_view)
layout.title.set_text("Viewer")

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
=======
def pipeline_viewer():
>>>>>>> ff7ee51 (docs(tutorial): update app)
    widgets.GitTree(
        sources=(
            "pipeline",
            [
                {"id": "1", "parent": "0", "visible": 1, "name": "Cube Axes"},
                {"id": "2", "parent": "0", "visible": 1, "name": "Mesh"},
                {"id": "3", "parent": "0", "visible": 1, "name": "Contour"},
            ],
        ),
        selection=("pipeline_selection", []),
        actives_change=(actives_change, "[$event]"),
        visibility_change=(visibility_change, "[$event]"),
    )

def cube_axes_card():
    with vuetify.VCard(
        classes="ma-4 rounded elevation-8", v_show="active_card == 'Cube Axes'"
    ):
        with vuetify.VCardTitle(
            classes="grey lighten-1 py-0 grey--text text--darken-3",
            style="user-select: none; cursor: pointer",
        ):
            Div("Cube Axes")
        vuetify.VCardText(
            classes="pb-0 mb-n2 px-0",
        )
        vuetify.VCardActions(
            classes="pa-0 pb-3",
        )

def mesh_card():
    with vuetify.VCard(
        classes="ma-4 rounded elevation-8", v_show="active_card == 'Mesh'"
    ):
        with vuetify.VCardTitle(
            classes="grey lighten-1 py-0 grey--text text--darken-3",
            style="user-select: none; cursor: pointer",
            dense=True,
        ):
            Div("Mesh")
        with vuetify.VCardText(
            classes="pb-0 mb-n2 px-0",
        ):
            vuetify.VSelect(
                classes="pt-1",
                v_model="meshRepresentation",
                items=["representations"],
                label="Representations",
                hide_details=True,
                dense=True,
                outlined=True,
            )
            with vuetify.VRow(
                classes="pa-0",
            ):
                with vuetify.VCol(
                    cols="6",
                ):
                    vuetify.VSelect(
                        classes="pt-1",
                        v_model="meshColorByName",
                        items=["arrayData"],
                        label="Color by",
                        hide_details=True,
                        dense=True,
                        outlined=True,
                    )
                with vuetify.VCol(
                    cols="6",
                ):
                    vuetify.VSelect(
                        classes="pt-1",
                        v_model="meshColormap",
                        items=["colormaps"],
                        label="Colormap",
                        hide_details=True,
                        dense=True,
                        outlined=True,
                    )
            vuetify.VSlider(
                v_model=("meshOpacity", 1.0),
                min=0,
                max=1,
                step=0.1,
                label="Opacity",
                hide_details=True,
                dense=True,
                style="max-width: 300px",
                )
        vuetify.VCardActions(
            classes="pa-0 pb-3",
        )

def contour_card():
    with vuetify.VCard(
        classes="ma-4 rounded elevation-8",
        v_show="active_card == 'Contour'"
    ):
        with vuetify.VCardTitle(
            classes="grey lighten-1 py-0 grey--text text--darken-3",
            style="user-select: none; cursor: pointer",
            dense=True,
        ):
            Div("Contour")
        with vuetify.VCardText(
            classes="pb-0 mb-n2 px-0",
        ):
            vuetify.VSelect(
                classes="pt-1",
                v_model="contourBy",
                items=["arrayData"],
                label="Contour By",
                hide_details=True,
                dense=True,
                outlined=True,
            )
            vuetify.VSlider(
                v_model="contourValue",
                min=("contourMin",),
                max=("contourMax",),
                step=("contourStep",),
                label="Value",
                hide_details=True,
                dense=True,
                style="max-width: 300px",
            )
            vuetify.VSelect(
                classes="pt-1",
                v_model="contourRepresentation",
                items=["representations"],
                label="Representation",
                hide_details=True,
                dense=True,
                outlined=True,
            )
            with vuetify.VRow(
                classes="pa-0",
            ):
                with vuetify.VCol(
                    cols="6",
                ):
                    vuetify.VSelect(
                        classes="pt-1",
                        v_model="contourColorByName",
                        items=["arrayData"],
                        label="Color by",
                        hide_details=True,
                        dense=True,
                        outlined=True,
                    )
                with vuetify.VCol(
                    cols="6",
                ):
                    vuetify.VSelect(
                        classes="pt-1",
                        v_model="contourColormap",
                        items=["colormaps"],
                        label="Colormap",
                        hide_details=True,
                        dense=True,
                        outlined=True,
                    )
            vuetify.VSlider(
                v_model=("contourOpacity", 1.0),
                min=0,
                max=1,
                step=0.1,
                label="Opacity",
                hide_details=True,
                dense=True,
                style="max-width: 300px",
            )
        vuetify.VCardActions(
            classes="pa-0 pb-3",
        )
# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

layout = SinglePageWithDrawer("Trame Viewer")
layout.title.content = "Viewer"

with layout.toolbar:
    vuetify.VSpacer()
    vuetify.VDivider(vertical=True, classes="mx-2")
    vuetify.VCheckbox(
                hide_details=True,
                classes="ma-0 pa-0 float-left",
                v_model="$vuetify.theme.dark",
                on_icon="mdi-lightbulb-off-outline",
                off_icon="mdi-lightbulb-outline",
                value=True,
    )
    vuetify.VCheckbox(
                hide_details=True,
                classes="ma-0 pa-0 float-left",
                v_model="local_vs_remote",
                on_icon="mdi-lan-disconnect",
                off_icon="mdi-lan-connect",
                value=True,
    )
    with vuetify.VBtn(
        icon=True,
        click="$refs.view.resetCamera()",
    ):
        vuetify.VIcon("mdi-crop-free")

with layout.drawer as drawer:
    drawer.width = "300px"
    pipeline_viewer()
    vuetify.VDivider(vertical=False)
    cube_axes_card()
    mesh_card()
    contour_card()

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
    layout.start()
