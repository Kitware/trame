r"""
Installation requirements:
    pip install trame trame-vuetify trame-vtk trame-components trame-plotly
"""

import pandas as pd

# Plotly/chart imports
import plotly.express as px
import vtkmodules.vtkRenderingOpenGL2  # noqa
from vtkmodules.numpy_interface import dataset_adapter as dsa
from vtkmodules.vtkCommonCore import vtkIdTypeArray
from vtkmodules.vtkCommonDataModel import vtkDataObject, vtkSelection, vtkSelectionNode
from vtkmodules.vtkFiltersExtraction import vtkExtractSelection
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkInteractionStyle import (
    vtkInteractorStyleRubberBandPick,
)  # noqa

# VTK imports
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkHardwareSelector,
    vtkRenderedAreaPicker,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

# Trame imports
from trame.app import get_server
from trame.assets.remote import HttpFile
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import plotly, trame, vuetify
from trame.widgets import vtk as vtk_widgets

# -----------------------------------------------------------------------------
# Data file information
# -----------------------------------------------------------------------------

dataset_file = HttpFile(
    "./data/disk_out_ref.vtu",
    "https://github.com/Kitware/trame/raw/master/examples/data/disk_out_ref.vtu",
    __file__,
)

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller


# -----------------------------------------------------------------------------
# VTK
# -----------------------------------------------------------------------------

reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(dataset_file.path)
reader.Update()
dataset = reader.GetOutput()

renderer = vtkRenderer()
renderer.SetBackground(1, 1, 1)
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)

rw_interactor = vtkRenderWindowInteractor()
rw_interactor.SetRenderWindow(render_window)
rw_interactor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

interactor_trackball = rw_interactor.GetInteractorStyle()
interactor_selection = vtkInteractorStyleRubberBandPick()
area_picker = vtkRenderedAreaPicker()
rw_interactor.SetPicker(area_picker)

surface_filter = vtkGeometryFilter()
surface_filter.SetInputConnection(reader.GetOutputPort())
surface_filter.SetPassThroughPointIds(True)

mapper = vtkDataSetMapper()
mapper.SetInputConnection(surface_filter.GetOutputPort())
actor = vtkActor()
actor.GetProperty().SetOpacity(0.5)
actor.SetMapper(mapper)

# Selection
selection_extract = vtkExtractSelection()
selection_mapper = vtkDataSetMapper()
selection_mapper.SetInputConnection(selection_extract.GetOutputPort())
selection_actor = vtkActor()
selection_actor.GetProperty().SetColor(1, 0, 1)
selection_actor.GetProperty().SetPointSize(5)
selection_actor.SetMapper(selection_mapper)
selection_actor.SetVisibility(0)

renderer.AddActor(actor)
renderer.AddActor(selection_actor)
renderer.ResetCamera()

selector = vtkHardwareSelector()
selector.SetRenderer(renderer)
selector.SetFieldAssociation(vtkDataObject.FIELD_ASSOCIATION_POINTS)

# vtkDataSet to DataFrame
py_ds = dsa.WrapDataObject(dataset)
pt_data = py_ds.PointData
cols = {}
for name in pt_data.keys():
    array = pt_data[name]
    shp = array.shape
    if len(shp) == 1:
        cols[name] = array
    else:
        for i in range(shp[1]):
            cols[name + "_%d" % i] = array[:, i]
DATAFRAME = pd.DataFrame(cols)
FIELD_NAMES = list(cols.keys())
SELECTED_IDX = []

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


@state.change("figure_size", "scatter_x", "scatter_y")
def update_figure(figure_size, scatter_x, scatter_y, **kwargs):
    if figure_size is None:
        return

    # Generate figure
    bounds = figure_size.get("size", {})
    fig = px.scatter(
        DATAFRAME,
        x=scatter_x,
        y=scatter_y,
        width=bounds.get("width", 200),
        height=bounds.get("height", 200),
    )

    # Update selection settings
    fig.data[0].update(
        selectedpoints=SELECTED_IDX,
        selected={"marker": {"color": "red"}},
        unselected={"marker": {"opacity": 0.5}},
    )

    # Update chart
    ctrl.update_figure(fig)


# -----------------------------------------------------------------------------


@state.change("vtk_selection")
def update_interactor(vtk_selection, **kwargs):
    if vtk_selection:
        # remote view
        rw_interactor.SetInteractorStyle(interactor_selection)
        interactor_selection.StartSelect()
        # local view
        state.interactorSettings = VIEW_SELECT
    else:
        # remote view
        rw_interactor.SetInteractorStyle(interactor_trackball)
        # local view
        state.interactorSettings = VIEW_INTERACT


# -----------------------------------------------------------------------------


def on_chart_selection(selected_point_idxs):
    global SELECTED_IDX
    SELECTED_IDX = selected_point_idxs if selected_point_idxs else []
    npts = len(SELECTED_IDX)

    ids = vtkIdTypeArray()
    ids.SetNumberOfTuples(npts)
    for idx, p_id in enumerate(SELECTED_IDX):
        ids.SetTuple1(idx, p_id)
        idx += 1

    sel_node = vtkSelectionNode()
    sel_node.GetProperties().Set(
        vtkSelectionNode.CONTENT_TYPE(), vtkSelectionNode.INDICES
    )
    sel_node.GetProperties().Set(vtkSelectionNode.FIELD_TYPE(), vtkSelectionNode.POINT)
    sel_node.SetSelectionList(ids)
    sel = vtkSelection()
    sel.AddNode(sel_node)

    selection_extract.SetInputDataObject(0, py_ds.VTKObject)
    selection_extract.SetInputDataObject(1, sel)
    selection_extract.Update()
    selection_actor.SetVisibility(1)

    # Update 3D view
    ctrl.view_update()


def on_box_selection_change(selection):
    global SELECTED_IDX
    if selection.get("mode") == "remote":
        actor.GetProperty().SetOpacity(1)
        selector.SetArea(
            int(renderer.GetPickX1()),
            int(renderer.GetPickY1()),
            int(renderer.GetPickX2()),
            int(renderer.GetPickY2()),
        )
    elif selection.get("mode") == "local":
        camera = renderer.GetActiveCamera()
        camera_props = selection.get("camera")

        # Sync client view to server one
        camera.SetPosition(camera_props.get("position"))
        camera.SetFocalPoint(camera_props.get("focalPoint"))
        camera.SetViewUp(camera_props.get("viewUp"))
        camera.SetParallelProjection(camera_props.get("parallelProjection"))
        camera.SetParallelScale(camera_props.get("parallelScale"))
        camera.SetViewAngle(camera_props.get("viewAngle"))
        render_window.SetSize(selection.get("size"))

        actor.GetProperty().SetOpacity(1)
        render_window.Render()

        area = selection.get("selection")
        selector.SetArea(
            int(area[0]),
            int(area[2]),
            int(area[1]),
            int(area[3]),
        )

    # Common server selection
    s = selector.Select()
    n = s.GetNode(0)
    ids = dsa.vtkDataArrayToVTKArray(n.GetSelectionData().GetArray("SelectedIds"))
    surface = dsa.WrapDataObject(surface_filter.GetOutput())
    SELECTED_IDX = surface.PointData["vtkOriginalPointIds"][ids].tolist()

    selection_extract.SetInputConnection(surface_filter.GetOutputPort())
    selection_extract.SetInputDataObject(1, s)
    selection_extract.Update()
    selection_actor.SetVisibility(1)
    actor.GetProperty().SetOpacity(0.5)

    # Update scatter plot with selection
    update_figure(**state.to_dict())

    # Update 3D view
    ctrl.view_update()

    # disable selection mode
    state.vtk_selection = False


# -----------------------------------------------------------------------------
# Settings
# -----------------------------------------------------------------------------

DROPDOWN_STYLES = {
    "dense": True,
    "hide_details": True,
    "classes": "px-2",
    "style": "max-width: calc(25vw - 10px);",
}

CHART_STYLE = {
    "style": "position: absolute; left: 50%; transform: translateX(-50%);",
    "display_mode_bar": ("true",),
    "mode_bar_buttons_to_remove": (
        "chart_buttons",
        [
            "toImage",
            "resetScale2d",
            "zoomIn2d",
            "zoomOut2d",
            "toggleSpikelines",
            "hoverClosestCartesian",
            "hoverCompareCartesian",
        ],
    ),
    "display_logo": ("false",),
}

VTK_VIEW_SETTINGS = {
    "interactive_ratio": 1,
    "interactive_quality": 80,
}

VIEW_INTERACT = [
    {"button": 1, "action": "Rotate"},
    {"button": 2, "action": "Pan"},
    {"button": 3, "action": "Zoom", "scrollEnabled": True},
    {"button": 1, "action": "Pan", "alt": True},
    {"button": 1, "action": "Zoom", "control": True},
    {"button": 1, "action": "Pan", "shift": True},
    {"button": 1, "action": "Roll", "alt": True, "shift": True},
]

VIEW_SELECT = [{"button": 1, "action": "Select"}]


# -----------------------------------------------------------------------------
# UI
# -----------------------------------------------------------------------------

state.trame__title = "VTK selection"
ctrl.on_server_ready.add(ctrl.view_update)

with SinglePageLayout(server) as layout:
    layout.title.set_text("VTK & plotly")
    layout.icon.click = ctrl.view_reset_camera

    with layout.toolbar as tb:
        tb.dense = True
        vuetify.VSpacer()
        vuetify.VSelect(
            v_model=("scatter_y", FIELD_NAMES[1]),
            items=("fields", FIELD_NAMES),
            **DROPDOWN_STYLES,
        )
        vuetify.VSelect(
            v_model=("scatter_x", FIELD_NAMES[0]),
            items=("fields", FIELD_NAMES),
            **DROPDOWN_STYLES,
        )

    with layout.content:
        with vuetify.VContainer(fluid=True, classes="fill-height pa-0 ma-0"):
            with vuetify.VRow(dense=True, style="height: 100%;"):
                with vuetify.VCol(
                    classes="pa-0",
                    style="border-right: 1px solid #ccc; position: relative;",
                ):
                    view = vtk_widgets.VtkRemoteView(
                        # view = vtk_widgets.VtkLocalView(
                        render_window,
                        box_selection=("vtk_selection",),
                        box_selection_change=(on_box_selection_change, "[$event]"),
                        # For VtkRemoteView
                        **VTK_VIEW_SETTINGS,
                        # For VtkLocalView
                        interactor_settings=("interactorSettings", VIEW_SELECT),
                    )
                    ctrl.view_update = view.update
                    ctrl.view_reset_camera = view.reset_camera
                    vuetify.VCheckbox(
                        small=True,
                        on_icon="mdi-selection-drag",
                        off_icon="mdi-rotate-3d",
                        v_model=("vtk_selection", False),
                        style="position: absolute; top: 0; right: 0; z-index: 1;",
                        dense=True,
                        hide_details=True,
                    )
                with vuetify.VCol(classes="pa-0"):
                    with trame.SizeObserver("figure_size"):
                        html_plot = plotly.Figure(
                            selected=(
                                on_chart_selection,
                                "[$event?.points.map(({pointIndex}) => pointIndex)]",
                            ),
                            **CHART_STYLE,
                        )
                        ctrl.update_figure = html_plot.update

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
