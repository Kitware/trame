r"""
Installation requirements:
    pip install trame trame-vuetify trame-vtk trame-components
"""

from pathlib import Path

from vtkmodules.vtkFiltersCore import vtkThreshold
from vtkmodules.vtkFiltersGeneral import vtkExtractSelectedFrustum
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.web.utils import mesh as vtk_mesh

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import html, trame, vuetify
from trame.widgets import vtk as vtk_widgets

# -----------------------------------------------------------------------------
# Trame
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

SCALE_P = 0.0001
SCALE_U = 0.01

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
# VTK pipeline
# -----------------------------------------------------------------------------

data_directory = Path(__file__).parent.parent.parent.with_name("data")
f1_vtp = data_directory / "f1.vtp"
# print(f1_vtp)

reader = vtkXMLPolyDataReader()
reader.SetFileName(f1_vtp)
reader.Update()
f1_mesh = reader.GetOutput()
state.f1 = None

# Extract fieldParameters
fieldParameters = {"solid": {"range": [0, 1]}}
pd = f1_mesh.GetPointData()
nb_arrays = pd.GetNumberOfArrays()
for i in range(nb_arrays):
    array = pd.GetArray(i)
    name = array.GetName()
    min, max = array.GetRange(-1)
    fieldParameters[name] = {"name": name, "range": [min, max]}

# Frustrum extraction
extract = vtkExtractSelectedFrustum()
extract.SetInputConnection(reader.GetOutputPort())

threshold = vtkThreshold()
threshold.SetInputConnection(extract.GetOutputPort())
threshold.SetLowerThreshold(0)
threshold.SetInputArrayToProcess(0, 0, 0, 1, "vtkInsidedness")  # 1 => cell


# -----------------------------------------------------------------------------
# Web App setup
# -----------------------------------------------------------------------------

state.trame__title = "F1 Probing"
state.update(
    {
        # Fields available
        "fieldParameters": fieldParameters,
        # picking controls
        "modes": [
            {"value": "hover", "icon": "mdi-magnify"},
            {"value": "click", "icon": "mdi-cursor-default-click-outline"},
            {"value": "select", "icon": "mdi-select-drag"},
        ],
        # Picking feedback
        "pickData": None,
        "selectData": None,
        "tooltip": "",
        "coneVisibility": False,
        "pixel_ratio": 2,
        # Meshes
        "f1Visible": True,
    }
)

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


@state.change("pickingMode")
def update_picking_mode(pickingMode, **kwargs):
    mode = pickingMode
    if mode is None:
        state.update(
            {
                "tooltip": "",
                "tooltipStyle": {"display": "none"},
                "coneVisibility": False,
                "interactorSettings": VIEW_INTERACT,
            }
        )
    else:
        state.interactorSettings = VIEW_SELECT if mode == "select" else VIEW_INTERACT
        state.update(
            {
                "frustrum": None,
                "selection": None,
                "selectData": None,
            }
        )


@state.change("selectData")
def update_selection(selectData, **kwargs):
    if selectData is None:
        return

    frustrum = selectData.get("frustrum")
    vtk_frustrum = []
    for xyz in frustrum:
        vtk_frustrum += xyz
        vtk_frustrum += [1]

    extract.CreateFrustum(vtk_frustrum)
    extract.ShowBoundsOn()
    extract.PreserveTopologyOff()
    extract.Update()
    state.frustrum = vtk_mesh(extract.GetOutput())
    extract.ShowBoundsOff()
    extract.PreserveTopologyOn()
    threshold.Update()
    state.selection = vtk_mesh(threshold.GetOutput())
    state.selectData = None
    state.pickingMode = None


@state.change("pickData")
def update_tooltip(pickData, pixel_ratio, **kwargs):
    state.tooltip = ""
    state.tooltipStyle = {"display": "none"}
    state.coneVisibility = False
    data = pickData

    if data and data["representationId"] == "f1":
        xyx = data["worldPosition"]
        idx = f1_mesh.FindPoint(xyx)
        if idx > -1:
            messages = []
            cone_state = {
                "resolution": 12,
                "radius": pd.GetArray("p").GetValue(idx) * SCALE_P,
                "center": f1_mesh.GetPoints().GetPoint(idx),
            }

            for i in range(nb_arrays):
                array = pd.GetArray(i)
                name = array.GetName()
                nb_comp = array.GetNumberOfComponents()
                value = array.GetValue(idx)
                value_str = f"{array.GetValue(idx):.2f}"
                norm_str = ""
                if nb_comp == 3:
                    value = array.GetTuple3(idx)
                    norm = (value[0] ** 2 + value[1] ** 2 + value[2] ** 2) ** 0.5
                    norm_str = f" norm({norm:.2f})"
                    value_str = ", ".join([f"{v:.2f}" for v in value])
                    cone_state["height"] = SCALE_U * norm
                    cone_state["direction"] = [v / norm for v in value]

                messages.append(f"{name}: {value_str} {norm_str}")

            if "height" in cone_state:
                new_center = [v for v in cone_state["center"]]
                for i in range(3):
                    new_center[i] -= (
                        0.5 * cone_state["height"] * cone_state["direction"][i]
                    )
                cone_state["center"] = new_center

            if len(messages):
                x, y, z = data["displayPosition"]
                state.coneVisibility = True
                state.tooltip = "\n".join(messages)
                state.cone = cone_state
                state.tooltipStyle = {
                    "position": "absolute",
                    "left": f"{(x / pixel_ratio) + 10}px",
                    "bottom": f"{(y / pixel_ratio) + 10}px",
                    "zIndex": 10,
                    "pointerEvents": "none",
                }


with SinglePageLayout(server) as layout:
    layout.title.set_text("F1 Probing")
    # Let the server know the browser pixel ratio
    trame.ClientTriggers(mounted="pixel_ratio = window.devicePixelRatio")

    with layout.toolbar:
        vuetify.VSpacer()
        with vuetify.VBtnToggle(v_model=("pickingMode", "hover"), dense=True):
            with vuetify.VBtn(value=("item.value",), v_for="item, idx in modes"):
                vuetify.VIcon("{{item.icon}}")
        vuetify.VSelect(
            v_model=("field", "solid"),
            items=(
                "fields",
                [
                    {"value": "solid", "text": "Solid color"},
                    {"value": "p", "text": "Pressure"},
                    {"value": "U", "text": "Velocity"},
                ],
            ),
            classes="ml-8",
            dense=True,
            hide_details=True,
            style="max-width: 140px",
        )
        vuetify.VSelect(
            v_model=("colorMap", "erdc_rainbow_bright"),
            # items=("''|vtkColorPresetItems",),                 # <= For trame-vtk<2.1
            items=("trame.utils.vtk.vtkColorPresetItems('')",),  # <= for trame-vtk>=2.1
            classes="ml-8",
            dense=True,
            hide_details=True,
            style="max-width: 200px",
        )
        vuetify.VSpacer()
        with vuetify.VBtn(icon=True, click="f1Visible = !f1Visible"):
            vuetify.VIcon("mdi-eye-outline", v_if="f1Visible")
            vuetify.VIcon("mdi-eye-off-outline", v_if="!f1Visible")
        with vuetify.VBtn(icon=True, click="$refs.view.resetCamera()"):
            vuetify.VIcon("mdi-crop-free")
        vuetify.VProgressLinear(
            indeterminate=True, absolute=True, bottom=True, active=("trame__busy",)
        )

    with layout.content:
        with vuetify.VContainer(
            fluid=True, classes="pa-0 fill-height", style="position: relative;"
        ):
            with vuetify.VCard(
                style=("tooltipStyle", {"display": "none"}), elevation=2, outlined=True
            ):
                with vuetify.VCardText():
                    html.Pre("{{ tooltip }}")
            with vtk_widgets.VtkView(
                ref="view",
                picking_modes=("[pickingMode]",),
                interactor_settings=("interactorSettings", VIEW_INTERACT),
                click="pickData = $event",
                hover="pickData = $event",
                select="selectData = $event",
            ):
                with vtk_widgets.VtkGeometryRepresentation(
                    id="f1",
                    v_if="f1",
                    color_map_preset=("colorMap",),
                    color_data_range=("fieldParameters[field].range",),
                    actor=("{ visibility: f1Visible }",),
                    mapper=(
                        """{
                            colorByArrayName: field,
                            scalarMode: 3,
                            interpolateScalarsBeforeMapping: true,
                            scalarVisibility: field !== 'solid',
                        }""",
                    ),
                ):
                    vtk_widgets.VtkMesh("f1", dataset=f1_mesh, point_arrays=["p", "U"])
                with vtk_widgets.VtkGeometryRepresentation(
                    id="selection",
                    actor=("{ visibility: !!selection }",),
                    property=(
                        "{ color: [0.99,0.13,0.37], representation: 0, pointSize: Math.round(5 * pixel_ratio)}",
                    ),
                ):
                    vtk_widgets.VtkMesh("selection", state=("selection", None))
                with vtk_widgets.VtkGeometryRepresentation(
                    id="frustrum",
                    actor=("{ visibility: !!frustrum }",),
                ):
                    vtk_widgets.VtkMesh("frustrum", state=("frustrum", None))
                with vtk_widgets.VtkGeometryRepresentation(
                    id="pointer",
                    property=("{ color: [1, 0, 0]}",),
                    actor=("{ visibility: coneVisibility }",),
                ):
                    vtk_widgets.VtkAlgorithm(
                        vtk_class="vtkConeSource",
                        state=("cone", {}),
                    )
# -----------------------------------------------------------------------------
# Jupyter
# -----------------------------------------------------------------------------


def show(**kwargs):
    from trame.app import jupyter

    jupyter.show(server, **kwargs)


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
