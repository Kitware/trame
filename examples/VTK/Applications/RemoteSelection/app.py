import os
import pandas as pd

# Plotly/chart imports
import plotly.graph_objects as go
import plotly.express as px

# Trame imports
from trame import state, controller as ctrl
from trame.layouts import SinglePage
from trame.html import Div, vuetify, plotly, vtk, observer

# VTK imports
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.numpy_interface import dataset_adapter as dsa
from vtkmodules.vtkCommonDataModel import vtkSelection, vtkSelectionNode
from vtkmodules.vtkCommonCore import vtkIdTypeArray
from vtkmodules.vtkFiltersExtraction import vtkExtractSelection
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

from vtkmodules.vtkInteractionStyle import vtkInteractorStyleRubberBandPick, vtkInteractorStyleSwitch  # noqa
import vtkmodules.vtkRenderingOpenGL2  # noqa

# -----------------------------------------------------------------------------
# Data file information
# -----------------------------------------------------------------------------

BASE_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../../data/disk_out_ref.vtu"))

# -----------------------------------------------------------------------------
# VTK
# -----------------------------------------------------------------------------

reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(FILE_PATH)
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

mapper = vtkDataSetMapper()
mapper.SetInputConnection(reader.GetOutputPort())
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
def update_figure(**kwargs):
    # Generate figure
    bounds = state.figure_size.get("size", {})
    fig = px.scatter(
        DATAFRAME,
        x=state.scatter_x,
        y=state.scatter_y,
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
    print("update_interactor", vtk_selection)
    if vtk_selection:
        print("+++ Switch to selection")
        rw_interactor.SetInteractorStyle(interactor_selection)
    else:
        print("+++ Switch to trackball")
        rw_interactor.SetInteractorStyle(interactor_trackball)

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
    ctrl.update_view()


# -----------------------------------------------------------------------------
# Settings
# -----------------------------------------------------------------------------

DROPDOWN_STYLES = {
    "dense": True,
    "hide_details": True,
    "classes": "px-2",
    "style": "max-width: calc(25vw - 10px);"
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
    "displaylogo": ("false",),
}

VTK_VIEW_SETTINGS = {
    "interactive_ratio": 1,
    "interactive_quality": 80,
}

# -----------------------------------------------------------------------------
# UI
# -----------------------------------------------------------------------------

layout = SinglePage("VTK selection", on_ready=ctrl.update_view)
layout.title.set_text("VTK & plotly")


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
            with vuetify.VCol(classes="pa-0", style="border-right: 1px solid #ccc; position: relative;"):
                html_view = vtk.VtkRemoteView(render_window, **VTK_VIEW_SETTINGS)
                ctrl.update_view = html_view.update
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
                with observer.SizeObserver("figure_size"):
                    html_plot = plotly.Plotly(
                        "figure",
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
    layout.start()
