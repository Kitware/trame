import os
import logging
import logging.handlers
from pathlib import Path

# Trame
from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vtk, vuetify, trame

# VTK
from vtkmodules.vtkCommonDataModel import vtkDataObject, vtkPolyData
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingAnnotation import vtkCubeAxesActor, vtkScalarBarActor
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

# Required for interactor initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa

# Required for rendering initialization, not necessary for
# local rendering, but doesn't hurt to include it
import vtkmodules.vtkRenderingOpenGL2  # noqa


# -----------------------------------------------------------------------------
# Globals
# -----------------------------------------------------------------------------


class Representation:
    Surface = 2
    SurfaceWithEdges = 3


class LookupTable:
    Rainbow = 0


def read_source(path: str, supported_arrays=None):
    if not os.path.isfile(path):
        raise Exception(f"File not found at '{path}'")
    logging.debug(f"Reading source from '{path}'")
    vtk_source = vtkXMLUnstructuredGridReader()
    vtk_source.SetFileName(path)
    vtk_source.Update()

    # Extract Array/Field information from source
    logging.debug(f"Extracting fields information from source")
    dataset_arrays = []
    fields = [
        (vtk_source.GetOutput().GetPointData(), vtkDataObject.FIELD_ASSOCIATION_POINTS),
        (vtk_source.GetOutput().GetCellData(), vtkDataObject.FIELD_ASSOCIATION_CELLS),
    ]
    for field in fields:
        field_arrays, association = field
        for i in range(field_arrays.GetNumberOfArrays()):
            array = field_arrays.GetArray(i)
            if supported_arrays:
                if array.GetName() in supported_arrays:
                    logging.debug(f"Appending field '{array.GetName()}'")
                    array_range = array.GetRange()
                    _text = array.GetName()
                    dataset_arrays.append(
                        {
                            "text": _text,
                            "variable_name": array.GetName(),
                            "value": i,
                            "range": list(array_range),
                            "type": association,
                        }
                    )
            else:
                _text = array.GetName()
                array_range = array.GetRange()
                dataset_arrays.append(
                    {
                        "text": _text,
                        "variable_name": array.GetName(),
                        "value": i,
                        "range": list(array_range),
                        "type": association,
                    }
                )
    if not dataset_arrays:
        raise Exception("Error reading data")
    logging.debug("Extracted fields: [")
    for arr in dataset_arrays:
        logging.debug(
            f"\t[index: {arr['value']}, variable: {arr['variable_name']}, range: {arr['range']}, type: {arr['text']}],"
        )
    logging.debug("]")

    # Sort ascending by field 'variable_name'
    logging.info("Sorting arrays by alphabetic ascending")
    dataset_arrays = sorted(
        dataset_arrays, key=lambda d: d["variable_name"]
    )  # ascending
    # Update index after sorting
    logging.info("Updating index after sorting")
    for index, arr in enumerate(dataset_arrays):
        dataset_arrays[index]["value"] = int(index)
    logging.debug("Sorted fields: [")
    for arr in dataset_arrays:
        logging.debug(
            f"\t[index: {arr['value']}, variable: {arr['variable_name']}, range: {arr['range']}, type: {arr['text']}],"
        )
    logging.debug("]")

    # Append solid color
    dataset_arrays.append(
        {
            "text": "Solid Color",
            "variable_name": "solid_color",
            "value": len(dataset_arrays),
            "range": [0, 1],
            "type": vtkDataObject.FIELD_ASSOCIATION_POINTS,
        }
    )
    return vtk_source, dataset_arrays


def getBounds(reader_port):
    # Get data center and bounds
    geometryFilter = vtkGeometryFilter()
    geometryFilter.SetInputConnection(reader_port)
    geometryFilter.Update()
    polyData = geometryFilter.GetOutput()
    polyDataBounds = [0, 0, 0, 0, 0, 0]  # [xmin, xmax, ymin, ymax, zmin, zmax]
    polyData.GetCellsBounds(polyDataBounds)  # modifies the 'polyDataBounds' variable
    return polyData, polyDataBounds


def set_color_preset(lut, value):
    # Set HSV values
    if value == LookupTable.Rainbow:
        lut.SetHueRange(0.666, 0.0)  # H - hue
        lut.SetSaturationRange(1.0, 1.0)  # S - saturation
        lut.SetValueRange(1.0, 1.0)  # V - value
    lut.Build()
    return lut


def get_default_array(arrays, reader_port):
    existing_field_names = []
    for i in range(len(arrays)):
        existing_field_names.append(arrays[i].get("variable_name"))
    default_array_idx = 0
    default_array = arrays[default_array_idx]
    del existing_field_names
    logging.debug(f"Getting bounds")
    abs_min, abs_max = default_array.get("range")
    polyData, polyDataBounds = getBounds(reader_port)
    return default_array, default_array_idx, abs_min, abs_max, polyData, polyDataBounds


# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------
logging.debug("Setting up Trame")
server = get_server(client_type="vue2")
state, ctrl, ui = server.state, server.controller, server.ui
state.setdefault("active_ui", None)  # set the default active UI

# -----------------------------------------------------------------------------
# State management
# -----------------------------------------------------------------------------
TITLE = "Trame test"
state.trame__title = TITLE
# Set defaults
state.update(
    {
        # Common parameters
        "color_preset": LookupTable.Rainbow,
        "dataset_arrays": [],
        "default_color_array_idx": None,
        "color_array_idx": None,
        # Mesh
        "mesh_opacity": 1.0,
    }
)

# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------
# ***** Create renderer *****
logging.debug("Creating renderer")
renderer = vtkRenderer()
renderer.GradientBackgroundOn()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window_interactor = vtkRenderWindowInteractor()
interactor_style = vtkInteractorStyleTrackballCamera()
render_window_interactor.SetInteractorStyle(interactor_style)
render_window_interactor.SetRenderWindow(render_window)

# Initialize actors and mappers
dataset_mapper = vtkDataSetMapper()
mesh_actor = vtkActor()
scalarBarActor = vtkScalarBarActor()
axes_actor = vtkCubeAxesActor()
polyData = vtkPolyData()
polyDataBounds = [0, 0, 0, 0, 0, 0]  # [xmin, xmax, ymin, ymax, zmin, zmax]

# ***** Read source, extract fields and compute some values (min, max and bounds) *****
input_file_path = str(Path(__file__).with_name("patch_antenna.vtu").resolve())
vtk_source, dataset_arrays = read_source(path=input_file_path)
(
    default_array,
    default_array_idx,
    abs_min,
    abs_max,
    polyData,
    polyDataBounds,
) = get_default_array(
    dataset_arrays,
    vtk_source.GetOutputPort(),
)
# Update state
state.dataset_arrays = dataset_arrays
logging.debug("Setting the default array index")
state.default_color_array_idx = default_array_idx
state.color_array_idx = default_array_idx
logging.debug(f"Setting some values of the default array to state")
# Initialize absolute min and max values
state.abs_min = abs_min
state.abs_max = abs_max
logging.debug(
    f"New values to state: [abs_min,abs_max]=[{state.abs_min}, {state.abs_max}]"
)
state.bounds = polyDataBounds
logging.debug(f"New values to state: bounds={state.bounds}")

# ***** Dataset, color map and scalar bar *****
# ***** Dataset *****
logging.debug(f"Configuring dataset mapper")
dataset_mapper.SetInputConnection(vtk_source.GetOutputPort())
dataset_mapper.ScalarVisibilityOn()
scalar_range = vtk_source.GetOutput().GetScalarRange()
dataset_mapper.SetScalarRange(scalar_range)
# Color map
logging.debug(f"Configuring color map")
dataset_lut = set_color_preset(dataset_mapper.GetLookupTable(), LookupTable.Rainbow)
dataset_mapper.SetLookupTable(dataset_lut)

# ***** Mesh *****
logging.debug(f"Configuring mesh actor")
mesh_actor.SetMapper(dataset_mapper)
# Mesh: Setup default representation to surface
mesh_actor.GetProperty().SetRepresentationToSurface()
mesh_actor.GetProperty().SetPointSize(1)
mesh_actor.GetProperty().EdgeVisibilityOn()
renderer.AddActor(mesh_actor)

# *****  Scalar bar *****
logging.debug(f"Configuring scalar bar")
scalarBarActor.SetLookupTable(dataset_mapper.GetLookupTable())
scalarBarActor.SetNumberOfLabels(7)
scalarBarActor.UnconstrainedFontSizeOn()
scalarBarActor.SetMaximumWidthInPixels(100)
scalarBarActor.SetMaximumHeightInPixels(800 // 3)
scalarBarActor.SetTitle(default_array.get("text"))
renderer.AddActor2D(scalarBarActor)

# ***** Axes - boundaries, camera, and styling *****
logging.debug(f"Configuring axes")
axes_actor.SetBounds(mesh_actor.GetBounds())
axes_actor.SetCamera(renderer.GetActiveCamera())
axes_actor.SetXLabelFormat("%6.1f")
axes_actor.SetYLabelFormat("%6.1f")
axes_actor.SetZLabelFormat("%6.1f")
axes_actor.SetFlyModeToOuterEdges()
renderer.AddActor(axes_actor)


# -----------------------------------------------------------------------------
# Useful methods
# -----------------------------------------------------------------------------
def reset():
    state.update(
        {
            "color_preset": LookupTable.Rainbow,
            "default_color_array_idx": 0,
            "color_array_idx": 0,
        }
    )
    state.active_ui = "colormap"  # the default active UI
    set_default_visibility()
    ctrl.view_update()
    ctrl.view_reset_camera()


# Visibility
def set_default_visibility():
    scalarBarActor.SetVisibility(True)
    mesh_actor.SetVisibility(True)


def visibility_change(event):
    _id = event["id"]
    _visibility = event["visible"]
    if _id == "1":  # Color Map
        scalarBarActor.SetVisibility(_visibility)
        if _visibility:  # If colormap has been enabled, color by the default array
            update_color_by_name(state.default_color_array_idx)
            state.active_ui = "colormap"
        else:  # If colormap has been disabled, color by a solid color
            update_color_by_name(len(state.dataset_arrays) - 1)
            state.active_ui = "nothing"
            # Disable scalar bar
            scalarBarActor.SetVisibility(False)
    elif _id == "2":  # Mesh
        mesh_actor.SetVisibility(_visibility)
        state.active_ui = "mesh" if _visibility else "nothing"

    ctrl.view_update()


# Color By Callbacks
def update_colormap(actor, arr):
    logging.debug("INIT update_colormap")
    logging.debug(f"Setting colormap for field '{arr.get('text')}'")
    _min, _max = arr.get("range")
    # Update dataset mapper
    mapper = actor.GetMapper()
    if not mapper:
        return
    mapper.SelectColorArray(arr.get("variable_name"))
    print("SetScalarRange", _min, _max)
    mapper.SetScalarRange([_min, _max])
    if arr.get("type") == vtkDataObject.FIELD_ASSOCIATION_POINTS:
        mapper.SetScalarModeToUsePointFieldData()
    else:
        mapper.SetScalarModeToUseCellFieldData()
    # Update mesh actor
    logging.debug("END update_colormap")


# Selection
def actives_change(ids):
    _id = ids[0]
    if _id == "1" and scalarBarActor.GetVisibility():  # Color Map
        state.active_ui = "colormap"
    elif _id == "2" and mesh_actor.GetVisibility():  # Mesh
        state.active_ui = "mesh"
    else:
        state.active_ui = "nothing"


# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------
# ** INIT Common callbacks **
@state.change("color_array_idx")
def update_color_by_name(color_array_idx, **kwargs):
    logging.debug("INIT update_color_by_name")
    if (
        mesh_actor.GetMapper()
    ):  # only if some geometry was loaded (after initializing the GUI)
        # Get the array (field) for the given index
        logging.debug(f"Getting array with index '{color_array_idx}'")
        _array = state.dataset_arrays[color_array_idx]
        # Disable/Enable scalar bar according to the selected field: disable scalar bar is solid color was chosen
        if color_array_idx == (len(state.dataset_arrays) - 1):  # disable scalar bar
            scalarBarActor.SetVisibility(False)
        else:  # enable scalar bar
            scalarBarActor.SetVisibility(True)
        # Update scalar bar title
        logging.debug(f"Updating scalar bar title to '{_array.get('text')}'")
        scalarBarActor.SetTitle(_array.get("text"))
        # Update color map for mesh
        logging.debug(f"Updating colormap for mesh actor")
        update_colormap(mesh_actor, _array)
        # Update scalar bar actor
        scalarBarActor.SetLookupTable(mesh_actor.GetMapper().GetLookupTable())
        # Update state
        state.color_array_idx = color_array_idx
        # Initialize custom min and max to absolute min and max
        logging.debug(f"Updating bounds")
        # Initialize absolute min and max values
        _min, _max = _array.get("range")
        state.abs_min = _min
        state.abs_max = _max
        logging.debug(
            f"New values to state: [abs_min,abs_max]=[{state.abs_min}, {state.abs_max}]"
        )

        # Update view
        logging.debug(f"Updating view")
        ctrl.view_update()

    logging.debug("END update_color_by_name")


@state.change("color_preset")
def update_color_preset(color_preset, **kwargs):
    logging.debug("INIT update_color_preset")
    logging.debug(f"Updating color preset to '{color_preset}'")
    if mesh_actor.GetMapper():
        mesh_actor.GetMapper().SetLookupTable(
            set_color_preset(mesh_actor.GetMapper().GetLookupTable(), color_preset)
        )
    ctrl.view_update()
    logging.debug("END update_color_preset")


# ** END Common callbacks **


# ** INIT Axes callbacks **
@state.change("axes_visibility")
def update_axes_visibility(axes_visibility: bool, **kwargs):
    logging.debug("INIT update_axes_visibility")
    logging.debug(f"Updating axes visibility to '{axes_visibility}'")
    axes_actor.SetVisibility(axes_visibility)
    ctrl.view_update()
    logging.debug("END update_axes_visibility")


# ** END Axes callbacks **


# ** INIT Mesh callbacks **
@state.change("mesh_representation")
def update_mesh_representation(mesh_representation, **kwargs):
    logging.debug(f"Updating mesh representation to '{mesh_representation}'")
    update_representation(mesh_actor, mesh_representation)
    ctrl.view_update()


def update_representation(actor, mode):
    logging.debug("INIT update_representation")
    _property = actor.GetProperty()
    if mode == Representation.Surface:
        _property.SetRepresentationToSurface()
        _property.SetPointSize(1)
        _property.EdgeVisibilityOff()
    elif mode == Representation.SurfaceWithEdges:
        _property.SetRepresentationToSurface()
        _property.SetPointSize(1)
        _property.EdgeVisibilityOn()
    logging.debug("END update_representation")


# Opacity Callbacks
@state.change("mesh_opacity")
def update_mesh_opacity(mesh_opacity, **kwargs):
    logging.debug(f"Updating mesh opacity to '{mesh_opacity}'")
    mesh_actor.GetProperty().SetOpacity(mesh_opacity)
    ctrl.view_update()


# ** END Mesh callbacks **


# -----------------------------------------------------------------------------
# GUI ELEMENTS
# -----------------------------------------------------------------------------
def standard_buttons():
    vuetify.VCheckbox(
        v_model=("axes_visibility", True),
        on_icon="mdi-cube-outline",
        off_icon="mdi-cube-off-outline",
        classes="mx-1",
        hide_details=True,
        dense=True,
    )
    with vuetify.VBtn(icon=True, click="$refs.view.resetCamera()"):
        vuetify.VIcon("mdi-crop-free")


def ui_card(title, ui_name):
    with vuetify.VCard(v_show=f"active_ui == '{ui_name}'"):
        vuetify.VCardTitle(
            title,
            classes="grey lighten-1 py-1 grey--text text--darken-3",
            style="user-select: none; cursor: pointer",
            hide_details=True,
            dense=True,
        )
        content = vuetify.VCardText(classes="py-2")
    return content


def colormap_card():
    with ui_card(title="Color Map", ui_name="colormap"):
        # Field and colormap
        with vuetify.VRow(classes="pt-2", dense=True):
            with vuetify.VCol(cols="12"):
                vuetify.VSelect(
                    # Color By
                    label="Field",
                    v_model=("color_array_idx", state.default_color_array_idx),
                    items=("array_list", state.dataset_arrays),
                    hide_details=True,
                    dense=True,
                    outlined=True,
                    classes="pt-1",
                )


def mesh_card():
    with ui_card(title="Geometry", ui_name="mesh"):
        # Representation
        with vuetify.VRow(classes="pt-2", dense=True):
            vuetify.VSelect(
                v_model=("mesh_representation", Representation.Surface),
                items=(
                    "representations",
                    [{"text": "Surface", "value": 2}, {"text": "Mesh", "value": 3}],
                ),
                label="Representation",
                hide_details=True,
                dense=True,
                outlined=True,
                classes="pt-1",
            )
        # Opacity
        vuetify.VSlider(
            v_model=("mesh_opacity", state.mesh_opacity),
            min=0,
            max=1,
            step=0.01,
            label="Opacity",
            classes="mt-1",
            hide_details=True,
            dense=True,
        )


def left_menu():
    trame.GitTree(
        sources=(
            "pipeline",
            [
                {"id": "1", "parent": "0", "visible": 1, "name": "Color Map"},
                {"id": "2", "parent": "1", "visible": 1, "name": "Geometry"},
            ],
        ),
        actives_change=(actives_change, "[$event]"),
        visibility_change=(visibility_change, "[$event]"),
    )
    vuetify.VDivider(classes="mb-2")
    colormap_card()
    mesh_card()


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------
set_default_visibility()
renderer.ResetCamera()

# Layout content
logging.debug(f"Configuring GUI")
with SinglePageWithDrawerLayout(server) as layout:
    # -----------------------------------------------------------------------------
    # Toolbar
    # -----------------------------------------------------------------------------
    # Toolbar title
    layout.title.set_text("Trame test")
    layout.icon.click = reset  # call reset() function

    # Toolbar right-side buttons
    with layout.toolbar as toolbar:
        vuetify.VSpacer()
        vuetify.VDivider(vertical=True, classes="mx-2")
        standard_buttons()
        # Loading bar
        vuetify.VProgressLinear(
            indeterminate=True,
            absolute=True,
            bottom=True,
            active=("trame__busy",),
        )

    # Drawer components
    with layout.drawer as drawer:
        drawer.width = 325
        left_menu()

    # Content
    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            # view = vtk.VtkLocalView(render_window, interactive_ratio=1)
            view = vtk.VtkRemoteView(render_window, interactive_ratio=1)
            ctrl.view_update = view.update
            ctrl.view_reset_camera = view.reset_camera
            ctrl.on_server_ready.add(view.update)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
