import os
from enum import Enum

from trame import change, update_state
from trame.layouts import SinglePageWithDrawer
from trame.html import vtk, vuetify, widgets
from trame.state.core import get_state

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
# Constants
# -----------------------------------------------------------------------------


class Representation:
    Points = 0
    Wireframe = 1
    Surface = 2
    SurfaceWithEdges = 3


class LookupTable:
    Rainbow = 0
    Inverted_Rainbow = 1
    Greyscale = 2
    Inverted_Greyscale = 3


# -----------------------------------------------------------------------------
# VTK helpers
# -----------------------------------------------------------------------------


def create_representation(input):
    mapper = vtkDataSetMapper()
    mapper.SetInputConnection(input.GetOutputPort())
    actor = vtkActor()
    actor.SetMapper(mapper)
    return actor


def use_preset(actor, preset):
    lut = actor.GetMapper().GetLookupTable()
    if preset == LookupTable.Rainbow:
        lut.SetHueRange(0.666, 0.0)
        lut.SetSaturationRange(1.0, 1.0)
        lut.SetValueRange(1.0, 1.0)
    elif preset == LookupTable.Inverted_Rainbow:
        lut.SetHueRange(0.0, 0.666)
        lut.SetSaturationRange(1.0, 1.0)
        lut.SetValueRange(1.0, 1.0)
    elif preset == LookupTable.Greyscale:
        lut.SetHueRange(0.0, 0.0)
        lut.SetSaturationRange(0.0, 0.0)
        lut.SetValueRange(0.0, 1.0)
    elif preset == LookupTable.Inverted_Greyscale:
        lut.SetHueRange(0.0, 0.666)
        lut.SetSaturationRange(0.0, 0.0)
        lut.SetValueRange(1.0, 0.0)
    lut.Build()


def color_by_array(actor, array):
    _min, _max = array.get("range")
    mapper = actor.GetMapper()
    mapper.GetLookupTable().SetRange(_min, _max)
    mapper.SelectColorArray(array.get("text"))
    mapper.SetScalarModeToUsePointFieldData()
    mapper.SetScalarVisibility(True)
    mapper.SetUseLookupTableScalarRange(True)


def update_representation(actor, mode):
    property = actor.GetProperty()
    if mode == Representation.Points:
        property.SetRepresentationToPoints()
        property.SetPointSize(5)
        property.EdgeVisibilityOff()
    elif mode == Representation.Wireframe:
        property.SetRepresentationToWireframe()
        property.SetPointSize(1)
        property.EdgeVisibilityOff()
    elif mode == Representation.Surface:
        property.SetRepresentationToSurface()
        property.SetPointSize(1)
        property.EdgeVisibilityOff()
    elif mode == Representation.SurfaceWithEdges:
        property.SetRepresentationToSurface()
        property.SetPointSize(1)
        property.EdgeVisibilityOn()


def contour_by_array(filter, array, reset_value=True):
    _min, _max = array.get("range")
    step = 0.01 * (_max - _min)
    value = 0.5 * (_max + _min)
    filter.SetInputArrayToProcess(0, 0, 0, array.get("type"), array.get("text"))
    if reset_value:
        filter.SetValue(0, value)
    return value, step


# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(os.path.join(CURRENT_DIRECTORY, "../../../data/disk_out_ref.vtu"))
reader.Update()
dataset = reader.GetOutput()

# Extract arrays informations
dataset_arrays = []
fields = [
    (dataset.GetPointData(), vtkDataObject.FIELD_ASSOCIATION_POINTS),
    (dataset.GetCellData(), vtkDataObject.FIELD_ASSOCIATION_CELLS),
]
for field in fields:
    field_arrays, association = field
    for i in range(field_arrays.GetNumberOfArrays()):
        array = field_arrays.GetArray(i)
        array_range = array.GetRange()
        dataset_arrays.append(
            {
                "text": array.GetName(),
                "value": i,
                "range": list(array_range),
                "type": association,
            }
        )
default_array = dataset_arrays[0]

# Mesh
mesh_actor = create_representation(reader)
update_representation(mesh_actor, Representation.Surface)
use_preset(mesh_actor, LookupTable.Rainbow)
color_by_array(mesh_actor, default_array)
renderer.AddActor(mesh_actor)

# Keep track of pipeline elements
pipeline_server = {
    "1": {
        "actor": mesh_actor,
        "ui": "mesh",
        "shared": {
            "representation": Representation.Surface,
            "color_preset": LookupTable.Rainbow,
            "color_array_idx": 0,
            "contour_by_array_idx": 0,
            "opacity": 1.0,
        },
    }
}
pipeline_client = [{"id": "1", "parent": "0", "visible": 1, "name": "Mesh"}]

# Cube Axes
cube_axes = vtkCubeAxesActor()
cube_axes.SetBounds(mesh_actor.GetBounds())
cube_axes.SetCamera(renderer.GetActiveCamera())
cube_axes.SetXLabelFormat("%6.1f")
cube_axes.SetYLabelFormat("%6.1f")
cube_axes.SetZLabelFormat("%6.1f")
cube_axes.SetFlyModeToOuterEdges()
renderer.AddActor(cube_axes)

# Contour(s)
for i in range(4):
    array = dataset_arrays[i]
    contour = vtkContourFilter()
    contour.SetInputConnection(reader.GetOutputPort())
    contour_value, contour_step = contour_by_array(contour, array)
    contour_actor = create_representation(contour)
    contour_min, contour_max = array.get("range")
    update_representation(contour_actor, Representation.Surface)
    use_preset(contour_actor, LookupTable.Rainbow)
    color_by_array(contour_actor, array)
    renderer.AddActor(contour_actor)

    # Register actor and definition in pipeline
    _id = f"{i+2}"
    pipeline_server[_id] = {
        "actor": contour_actor,
        "ui": "contour",
        "filter": contour,
        "shared": {
            "representation": Representation.Surface,
            "color_preset": LookupTable.Rainbow,
            "color_array_idx": i,
            "opacity": 1.0,
            # contour add-on
            "contour_by_array_idx": i,
            "contour_value": contour_value,
            "contour_min": contour_min,
            "contour_max": contour_max,
            "contour_step": contour_step,
        },
    }
    pipeline_client.append(
        {
            "id": _id,
            "parent": "1",
            "visible": 1,
            "name": f"Contour {i + 1}",
        }
    )


renderer.ResetCamera()

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

html_view = vtk.VtkRemoteLocalView(
    renderWindow,
    namespace="view",
    mode=("viewMode", "local"),
    interactive_ratio=1,
)


def update_view():
    (is_local,) = get_state("local_vs_remote")
    if is_local:
        html_view.update_geometry()
    else:
        html_view.update_image()


html_view.update = update_view


@change("cube_axes_visibility")
def update_cube_axes_visibility(cube_axes_visibility, **kwargs):
    cube_axes.SetVisibility(cube_axes_visibility)
    html_view.update()


@change("local_vs_remote")
def update_local_vs_remote(local_vs_remote, **kwargs):
    update_state("viewMode", "local" if local_vs_remote else "remote")


@change("representation")
def update_active_representation(active_id, representation, **kwargs):
    active_item = pipeline_server.get(active_id)
    if not active_item:
        return

    active_item["shared"]["representation"] = representation
    update_representation(active_item["actor"], representation)
    html_view.update()


@change("color_array_idx")
def update_active_color_by_name(active_id, color_array_idx, **kwargs):
    array = dataset_arrays[color_array_idx]
    active_item = pipeline_server.get(active_id)
    if not active_item:
        return

    active_item["shared"]["color_array_idx"] = color_array_idx
    color_by_array(active_item["actor"], array)
    html_view.update()


@change("color_preset")
def update_active_color_preset(active_id, color_preset, **kwargs):
    active_item = pipeline_server.get(active_id)
    if not active_item:
        return

    active_item["shared"]["color_preset"] = color_preset
    use_preset(active_item["actor"], color_preset)
    html_view.update()


@change("opacity")
def update_active_opacity(active_id, opacity, **kwargs):
    active_item = pipeline_server.get(active_id)
    if not active_item:
        return

    active_item["shared"]["opacity"] = opacity
    active_item["actor"].GetProperty().SetOpacity(opacity)
    html_view.update()


@change("contour_by_array_idx")
def update_contour_by(active_id, contour_by_array_idx, **kwargs):
    active_item = pipeline_server.get(active_id)
    if not active_item:
        return

    contour = active_item.get("filter")
    array = dataset_arrays[contour_by_array_idx]
    contour_value, contour_step = contour_by_array(contour, array)
    contour_min, contour_max = array.get("range")

    active_item["shared"]["contour_by_array_idx"] = contour_by_array_idx
    active_item["shared"]["contour_min"] = contour_min
    active_item["shared"]["contour_max"] = contour_max
    active_item["shared"]["contour_step"] = contour_step
    active_item["shared"]["contour_value"] = contour_value
    update_state(active_item["shared"])  # let client know about contour edited params

    html_view.update()


@change("contour_value")
def update_contour_value(active_id, contour_value, **kwargs):
    active_item = pipeline_server.get(active_id)
    if not active_item:
        return

    active_item["shared"]["contour_value"] = contour_value
    contour = active_item.get("filter")
    contour.SetValue(0, float(contour_value))

    html_view.update()


# Called by pipeline when selection change
def actives_change(ids):
    _id = update_state("active_id", ids[0])
    selected_pipeline = pipeline_server[_id]
    update_state("active_ui", selected_pipeline.get("ui"))
    update_state(selected_pipeline.get("shared"))


# Called by pipeline when visibility change
def visibility_change(event):
    _id = event["id"]
    _visibility = event["visible"]
    pipeline_server[_id].get("actor").SetVisibility(_visibility)

    # Update view of pipeline
    for item in pipeline_client:
        if item.get("id") == _id:
            item["visible"] = _visibility
    update_state("pipeline", pipeline_client, force=True)

    html_view.update()


# -----------------------------------------------------------------------------
# GUI Cards
# -----------------------------------------------------------------------------

compact_style = {
    "hide_details": True,
    "dense": True,
}

select_style = {
    **compact_style,
    "outlined": True,
    "classes": "pt-1",
}


def ui_array_selector(title, variable_name, initial_index=0, **kwargs):
    return vuetify.VSelect(
        label=title,
        v_model=(variable_name, initial_index),
        items=("array_list", dataset_arrays),
        **kwargs,
    )


def ui_card(title, ui_name):
    card_style = {}
    title_style = {
        "classes": "grey lighten-1 py-1 grey--text text--darken-3",
        "style": "user-select: none; cursor: pointer",
        **compact_style,
    }
    content_style = {"classes": "py-2"}
    with vuetify.VCard(v_show=f"active_ui == '{ui_name}'", **card_style):
        vuetify.VCardTitle(title + " ({{active_id}})", **title_style)
        content = vuetify.VCardText(**content_style)

    return content


def ui_common(rep=Representation.Surface, lut=LookupTable.Rainbow, opacity=1):
    vuetify.VSelect(
        v_model=("representation", rep),
        items=(
            "representations",
            [
                {"text": "Points", "value": 0},
                {"text": "Wireframe", "value": 1},
                {"text": "Surface", "value": 2},
                {"text": "SurfaceWithEdges", "value": 3},
            ],
        ),
        label="Representation",
        **select_style,
    )
    with vuetify.VRow(classes="pt-2", dense=True):
        with vuetify.VCol(cols="6"):
            ui_array_selector("Color by", "color_array_idx", **select_style)
        with vuetify.VCol(cols="6"):
            vuetify.VSelect(
                label="Colormap",
                v_model=("color_preset", lut),
                items=(
                    "colormaps",
                    [
                        {"text": "Rainbow", "value": 0},
                        {"text": "Inv Rainbow", "value": 1},
                        {"text": "Greyscale", "value": 2},
                        {"text": "Inv Greyscale", "value": 3},
                    ],
                ),
                **select_style,
            )
    vuetify.VSlider(
        v_model=("opacity", opacity),
        min=0,
        max=1,
        step=0.1,
        label="Opacity",
        classes="mt-1",
        **compact_style,
    )


def mesh_card():
    with ui_card("Mesh", "mesh"):
        ui_common()


def contour_card():
    with ui_card("Contour", "contour"):
        ui_array_selector("Contour by", "contour_by_array_idx", **select_style)
        vuetify.VSlider(
            v_model=("contour_value", contour_value),
            min=("contour_min", contour_min),
            max=("contour_max", contour_max),
            step=("contour_step", contour_step),
            label="Value",
            classes="my-1",
            **compact_style,
        )
        ui_common()


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

layout = SinglePageWithDrawer("MultiFilter", on_ready=html_view.update)
layout.title.set_text("Viewer")

toggle_buttons = [
    (("cube_axes_visibility", True), "mdi-cube-outline", "mdi-cube-off-outline"),
    ("$vuetify.theme.dark", "mdi-lightbulb-off-outline", "mdi-lightbulb-outline"),
    (("local_vs_remote", True), "mdi-lan-disconnect", "mdi-lan-connect"),
]

with layout.toolbar:
    vuetify.VSpacer()
    vuetify.VDivider(vertical=True, classes="mx-2")
    for model, on, off in toggle_buttons:
        vuetify.VCheckbox(
            v_model=model,
            on_icon=on,
            off_icon=off,
            classes="mx-1",
            **compact_style,
        )
    with vuetify.VBtn(icon=True, click="$refs.view.resetCamera()"):
        vuetify.VIcon("mdi-crop-free")

with layout.drawer as drawer:
    drawer.width = 325
    widgets.GitTree(
        sources=("pipeline", pipeline_client),
        actives=("[active_id]",),
        actives_change=(actives_change, "[$event]"),
        visibility_change=(visibility_change, "[$event]"),
    )
    vuetify.VDivider()
    mesh_card()
    contour_card()

with layout.content:
    vuetify.VContainer(
        fluid=True,
        classes="pa-0 fill-height",
        children=[html_view],
    )

# State use to track active pipeline element
layout.state = {
    "active_id": None,
    "active_ui": None,
}

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
