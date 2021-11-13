import os

import trame as tr
from trame.layouts import SinglePage
from trame.html import vtk, vuetify, Element

from vtkmodules.web.utils import mesh as vtk_mesh
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkFiltersGeneral import vtkExtractSelectedFrustum
from vtkmodules.vtkFiltersCore import vtkThreshold

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


data_directory = os.path.join(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ),
    "data",
)
f1_vtp = os.path.join(data_directory, "f1.vtp")

reader = vtkXMLPolyDataReader()
reader.SetFileName(f1_vtp)
reader.Update()
f1_mesh = reader.GetOutput()
tr.update_state(
    "f1",
)

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

layout = SinglePage("F1 Probing")
layout.title.set_text("F1 Probing")
layout.state = {
    # Fields available
    "field": "solid",
    "fields": [
        {"value": "solid", "text": "Solid color"},
        {"value": "p", "text": "Pressure"},
        {"value": "U", "text": "Velocity"},
    ],
    "fieldParameters": fieldParameters,
    "colorMap": "erdc_rainbow_bright",
    # picking controls
    "pickingMode": "hover",
    "modes": [
        {"value": "hover", "icon": "mdi-magnify"},
        {"value": "click", "icon": "mdi-cursor-default-click-outline"},
        {"value": "select", "icon": "mdi-select-drag"},
    ],
    # Picking feedback
    "pickData": None,
    "selectData": None,
    "tooltip": "",
    "tooltipStyle": {"display": "none"},
    "cone": {},
    "coneVisibility": False,
    # Meshed
    "f1": vtk_mesh(f1_mesh, point_arrays=["p", "U"]),
    "f1Visible": True,
    "selection": None,
    "frustrum": None,
    # View interactions
    "interactorSettings": VIEW_INTERACT,
}


# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


@tr.change("pickingMode")
def update_picking_mode(pickingMode, **kwargs):
    mode = pickingMode
    if mode is None:
        tr.update_state("tooltip", "")
        tr.update_state("tooltipStyle", {"display": "none"})
        tr.update_state("coneVisibility", False)
        tr.update_state("interactorSettings", VIEW_INTERACT)
    else:
        tr.update_state(
            "interactorSettings", VIEW_SELECT if mode == "select" else VIEW_INTERACT
        )
        tr.update_state("frustrum", None)
        tr.update_state("selection", None)
        tr.update_state("selectData", None)


@tr.change("selectData")
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
    tr.update_state("frustrum", vtk_mesh(extract.GetOutput()))
    extract.ShowBoundsOff()
    extract.PreserveTopologyOn()
    threshold.Update()
    tr.update_state("selection", vtk_mesh(threshold.GetOutput()))

    tr.update_state("selectData", None)
    tr.update_state("pickingMode", None)


@tr.change("pickData")
def update_tooltip(pickData, **kwargs):
    tr.update_state("tooltip", "")
    tr.update_state("tooltipStyle", {"display": "none"})
    tr.update_state("coneVisibility", False)
    data = pickData

    if tr.is_dirty("pickData") and data and data["representationId"] == "f1":
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
                tr.update_state("coneVisibility", True)
                tr.update_state("tooltip", "\n".join(messages))
                tr.update_state("cone", cone_state)
                tr.update_state(
                    "tooltipStyle",
                    {
                        "position": "absolute",
                        "left": f"{x + 10}px",
                        "bottom": f"{y + 10}px",
                        "zIndex": 10,
                        "pointerEvents": "none",
                    },
                )


with layout.toolbar:
    vuetify.VSpacer()
    with vuetify.VBtnToggle(v_model=("pickingMode", []), dense=True):
        with vuetify.VBtn(value=("item.value",), v_for="item, idx in modes"):
            vuetify.VIcon("{{item.icon}}")
    vuetify.VSelect(
        v_model=("field",),
        items=("fields",),
        classes="ml-8",
        dense=True,
        hide_details=True,
        style="max-width: 140px",
    )
    vuetify.VSelect(
        v_model=("colorMap"),
        items=("''|vtkColorPresetItems",),
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
        indeterminate=True, absolute=True, bottom=True, active=("busy",)
    )

visualization = [
    vtk.VtkGeometryRepresentation(
        vtk.VtkMesh("f1", state=("f1",)),
        id="f1",
        v_if="f1",
        color_map_preset=("colorMap",),
        color_data_range=("fieldParameters[field].range",),
        actor=("{ visibility: f1Visible }",),
        mapper=(
            "{ colorByArrayName: field, scalarMode: 3, interpolateScalarsBeforeMapping: true, scalarVisibility: field !== 'solid' }",
        ),
    ),
    vtk.VtkGeometryRepresentation(
        vtk.VtkMesh("selection", state=("selection",)),
        id="selection",
        actor=("{ visibility: !!selection }",),
        property=("{ color: [0.99,0.13,0.37], representation: 0, pointSize: 5 }",),
    ),
    vtk.VtkGeometryRepresentation(
        vtk.VtkMesh("frustrum", state=("frustrum",)),
        id="frustrum",
        actor=("{ visibility: !!frustrum }",),
    ),
    vtk.VtkGeometryRepresentation(
        vtk.VtkAlgorithm(
            vtk_class="vtkConeSource",
            state=("cone",),
        ),
        id="pointer",
        property=("{ color: [1, 0, 0]}",),
        actor=("{ visibility: coneVisibility }",),
    ),
]


with layout.content:
    with vuetify.VContainer(
        fluid=True, classes="pa-0 fill-height", style="position: relative;"
    ):
        with vuetify.VCard(
            style=("tooltipStyle", {"display": "none"}), elevation=2, outlined=True
        ):
            with vuetify.VCardText():
                Element("pre", "{{ tooltip }}")
        vtk.VtkView(
            visualization,
            ref="view",
            picking_modes=("[pickingMode]",),
            interactor_settings=("interactorSettings", VIEW_INTERACT),
            click="set('pickData', $event)",
            hover="set('pickData', $event)",
            select="set('selectData', $event)",
        )
# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
