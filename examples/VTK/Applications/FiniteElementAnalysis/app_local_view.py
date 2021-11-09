import os
import io
import numpy as np
import pandas as pd

from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCellArray
from vtkmodules.vtkFiltersCore import vtkThreshold

from vtkmodules.numpy_interface.dataset_adapter import numpyTovtkDataArray as np2da
from vtkmodules.util import vtkConstants

# Add import for the rendering
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa
import vtkmodules.vtkRenderingOpenGL2  # noqa
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

from trame import change, update_state, get_state, get_cli_parser
from trame.layouts import SinglePage
from trame.html import vuetify, vtk

# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

vtk_idlist = vtkIdList()
vtk_grid = vtkUnstructuredGrid()
vtk_filter = vtkThreshold()
vtk_filter.SetInputData(vtk_grid)
field_to_keep = "my_array"

renderer = vtkRenderer()
renderer.SetBackground(0.8, 0.8, 0.8)
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

filter_mapper = vtkDataSetMapper()
filter_mapper.SetInputConnection(vtk_filter.GetOutputPort())
filter_actor = vtkActor()
filter_actor.SetMapper(filter_mapper)
renderer.AddActor(filter_actor)

lut = vtkLookupTable()
lut.SetHueRange(0.667, 0)
lut.Build()
filter_mapper.SetLookupTable(lut)

mesh_mapper = vtkDataSetMapper()
mesh_mapper.SetInputData(vtk_grid)
mesh_mapper.SetScalarVisibility(0)
mesh_actor = vtkActor()
mesh_actor.SetMapper(mesh_mapper)
renderer.AddActor(mesh_actor)


html_view = vtk.VtkLocalView(renderWindow)


@change("nodes_file", "elems_file", "field_file")
def update_grid(nodes_file, elems_file, field_file, **kwargs):
    if not nodes_file:
        return

    if not elems_file:
        return

    nodes_bytes = nodes_file.get("content")
    elems_bytes = elems_file.get("content")

    df_nodes = pd.read_csv(
        io.StringIO(nodes_bytes.decode("utf-8")),
        delim_whitespace=True,
        header=None,
        skiprows=1,
        names=["id", "x", "y", "z"],
    )

    df_nodes["id"] = df_nodes["id"].astype(int)
    df_nodes = df_nodes.set_index("id", drop=True)
    # fill missing ids in range as VTK uses position (index) to map cells to points
    df_nodes = df_nodes.reindex(
        np.arange(df_nodes.index.min(), df_nodes.index.max() + 1), fill_value=0
    )

    df_elems = pd.read_csv(
        io.StringIO(elems_bytes.decode("utf-8")),
        skiprows=1,
        header=None,
        delim_whitespace=True,
        engine="python",
        index_col=None,
    ).sort_values(0)
    # order: 0: eid, 1: eshape, 2+: nodes, iloc[:,0] is index
    df_elems.iloc[:, 0] = df_elems.iloc[:, 0].astype(int)

    n_nodes = df_elems.iloc[:, 1].map(
        lambda x: int("".join(i for i in x if i.isdigit()))
    )
    df_elems.insert(2, "n_nodes", n_nodes)
    # fill missing ids in range as VTK uses position (index) to map data to cells
    new_range = np.arange(df_elems.iloc[:, 0].min(), df_elems.iloc[:, 0].max() + 1)
    df_elems = df_elems.set_index(0, drop=False).reindex(new_range, fill_value=0)

    # mapping specific to Ansys Mechanical data
    vtk_shape_id_map = {
        "Tet4": vtkConstants.VTK_TETRA,
        "Tet10": vtkConstants.VTK_QUADRATIC_TETRA,
        "Hex8": vtkConstants.VTK_HEXAHEDRON,
        "Hex20": vtkConstants.VTK_QUADRATIC_HEXAHEDRON,
        "Tri6": vtkConstants.VTK_QUADRATIC_TRIANGLE,
        "Quad8": vtkConstants.VTK_QUADRATIC_QUAD,
        "Tri3": vtkConstants.VTK_TRIANGLE,
        "Quad4": vtkConstants.VTK_QUAD,
        "Wed15": vtkConstants.VTK_QUADRATIC_WEDGE,
    }
    df_elems["cell_types"] = np.nan
    df_elems.loc[df_elems.loc[:, 0] > 0, "cell_types"] = df_elems.loc[
        df_elems.loc[:, 0] > 0, 1
    ].map(
        lambda x: vtk_shape_id_map[x.strip()]
        if x.strip() in vtk_shape_id_map.keys()
        else np.nan
    )
    df_elems = df_elems.dropna(subset=["cell_types"], axis=0)

    # convert dataframes to vtk-desired format
    points = df_nodes[["x", "y", "z"]].to_numpy()
    cell_types = df_elems["cell_types"].to_numpy()
    n_nodes = df_elems.loc[:, "n_nodes"].to_numpy()
    # subtract starting node id from all grid references in cells to avoid filling from 0 to first used node (in case mesh doesnt start at 1)
    p = df_elems.iloc[:, 3:-1].to_numpy() - df_nodes.index.min()
    # if you need to, re-order nodes here-ish
    a = np.hstack((n_nodes.reshape((len(n_nodes), 1)), p))
    # convert to flat numpy array
    cells = a.ravel()
    # remove nans (due to elements with different no. of nodes)
    cells = cells[np.logical_not(np.isnan(cells))]
    cells = cells.astype(int)

    # update grid
    vtk_pts = vtkPoints()
    vtk_pts.SetData(np2da(points))
    vtk_grid.SetPoints(vtk_pts)

    vtk_cells = vtkCellArray()
    vtk_cells.SetCells(
        cell_types.shape[0], np2da(cells, array_type=vtkConstants.VTK_ID_TYPE)
    )
    vtk_grid.SetCells(
        np2da(cell_types, array_type=vtkConstants.VTK_UNSIGNED_CHAR), vtk_cells
    )
    update_state("mesh_status", 1)

    # Add field if any
    if field_file:
        field_bytes = field_file.get("content")
        df_elem_data = pd.read_csv(
            io.StringIO(field_bytes.decode("utf-8")),
            delim_whitespace=True,
            header=None,
            skiprows=1,
            names=["id", "val"],
        )
        df_elem_data = df_elem_data.sort_values("id").set_index("id", drop=True)
        # fill missing ids in range as VTK uses position (index) to map data to cells
        df_elem_data = df_elem_data.reindex(
            np.arange(df_elems.index.min(), df_elems.index.max() + 1), fill_value=0.0
        )
        np_val = df_elem_data["val"].to_numpy()
        # assign data to grid with the name 'my_array'
        vtk_array = np2da(np_val, name=field_to_keep)
        vtk_grid.GetCellData().SetScalars(vtk_array)
        full_min, full_max = vtk_array.GetRange()
        update_state("full_min", full_min)
        update_state("full_max", full_max)
        update_state("threshold_range", list(vtk_array.GetRange()))
        update_state("mesh_status", 2)

        # Color handling in plain VTK
        filter_mapper.SetScalarRange(full_min, full_max)

    renderer.ResetCamera()
    html_view.update()


@change("threshold_range")
def update_filter(threshold_range, **kwargs):
    filter_mapper.SetScalarRange(
        threshold_range
    )  # Comment if you want to have a fix color range
    vtk_filter.SetLowerThreshold(threshold_range[0])
    vtk_filter.SetUpperThreshold(threshold_range[1])
    html_view.update()


@change("mesh_status")
def update_mesh_representations():
    # defaults
    color = [1, 1, 1]
    representation = 2
    opacity = 1

    if get_state("mesh_status")[0] == 2:
        color = [0.3, 0.3, 0.3]
        representation = 1
        opacity = 0.2

    property = mesh_actor.GetProperty()
    property.SetRepresentation(representation)
    property.SetColor(color)
    property.SetOpacity(opacity)
    html_view.update()


def reset():
    update_state("nodes_file", None)
    update_state("elems_file", None)
    update_state("field_file", None)
    update_state("mesh_status", 0)


# -----------------------------------------------------------------------------
# Web App setup
# -----------------------------------------------------------------------------

layout = SinglePage("FEA - Mesh viewer")
layout.logo.click = reset
layout.title.set_text("Mesh Viewer")

file_style = {
    "dense": True,
    "hide_details": True,
    "style": "max-width: 200px",
    "class": "mx-2",
    "small_chips": True,
    "clearable": ("false",),
    "accept": ".txt",
}

# Toolbar ----------------------------------------
with layout.toolbar:
    vuetify.VSpacer()
    vuetify.VRangeSlider(
        thumb_size=16,
        thumb_label=True,
        label="Threshold",
        v_if=("mesh_status > 1",),
        v_model=("threshold_range", [0, 1]),
        min=("full_min", 0),
        max=("full_max", 1),
        dense=True,
        hide_details=True,
        style="max-width: 400px",
    )
    vuetify.VFileInput(
        v_show=("mesh_status < 1",),
        prepend_icon="mdi-vector-triangle",
        v_model=("nodes_file", None),
        placeholder="Nodes",
        **file_style,
    )
    vuetify.VFileInput(
        v_show=("mesh_status < 1",),
        prepend_icon="mdi-dots-triangle",
        v_model=("elems_file", None),
        placeholder="Elements",
        **file_style,
    )
    vuetify.VFileInput(
        v_show=("mesh_status < 2",),
        prepend_icon="mdi-gradient",
        v_model=("field_file", None),
        placeholder="Field",
        **file_style,
    )
    with vuetify.VBtn(
        v_if=("mesh_status",), icon=True, click="$refs.view.resetCamera()"
    ):
        vuetify.VIcon("mdi-crop-free")

    vuetify.VProgressLinear(
        indeterminate=True, absolute=True, bottom=True, active=("busy",)
    )

# Content ----------------------------------------
layout.content.children += [
    vuetify.VContainer(
        fluid=True,
        classes="pa-0 fill-height",
        style="position: relative",
        children=[html_view],
    )
]

# Variables not defined within HTML but used
layout.state = {
    # 0: empty / 1: mesh / 2: mesh+filter
    "mesh_status": 0,
}

# -----------------------------------------------------------------------------
# Use --data to skip file upload
# -----------------------------------------------------------------------------

parser = get_cli_parser()
parser.add_argument("--data", help="Unstructured file path", dest="data")
args = parser.parse_args()
if args.data:
    from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader

    reader = vtkXMLUnstructuredGridReader()
    reader.SetFileName(os.path.abspath(args.data))
    reader.Update()
    vtu = reader.GetOutput()
    vtk_grid.ShallowCopy(vtu)

    vtk_array = vtu.GetCellData().GetScalars()
    full_min, full_max = vtk_array.GetRange()
    update_state("full_min", full_min)
    update_state("full_max", full_max)
    update_state("threshold_range", [full_min, full_max])
    update_state("mesh_status", 2)
    update_mesh_representations()

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
