r"""
Installation requirements:
    pip install trame trame-vuetify trame-vtk trame-components
"""

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, trame, vtk as vtk_widgets
from trame.app.file_upload import ClientFile

from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.web.utils import mesh as vtk_mesh

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


@state.change("files")
def load_client_files(files, **kwargs):
    if files is None or len(files) == 0:
        return

    field = "solid"
    fields = {
        "solid": {"value": "solid", "text": "Solid color", "range": [0, 1]},
    }
    meshes = []
    filesOutput = []

    if files and len(files):
        if not files[0].get("content"):
            return

        for file in files:
            file = ClientFile(file)
            print(f"Load {file.name}")
            bytes = file.content
            filesOutput.append({"name": file.name, "size": file.size})
            reader = vtkXMLPolyDataReader()
            reader.ReadFromInputStringOn()
            reader.SetInputString(bytes)
            reader.Update()
            ds = reader.GetOutputAsDataSet(0)
            point_arrays = []
            pd = ds.GetPointData()
            nb_arrays = pd.GetNumberOfArrays()
            for i in range(nb_arrays):
                array = pd.GetArray(i)
                name = array.GetName()
                min, max = array.GetRange(-1)
                fields[name] = {
                    "name": name,
                    "range": [min, max],
                    "value": name,
                    "text": name,
                    "scalarMode": 3,
                }
                point_arrays.append(name)

            cell_arrays = []
            cd = ds.GetCellData()
            nb_arrays = cd.GetNumberOfArrays()
            for i in range(nb_arrays):
                array = cd.GetArray(i)
                name = array.GetName()
                min, max = array.GetRange(-1)
                fields[name] = {
                    "name": name,
                    "range": [min, max],
                    "value": name,
                    "text": name,
                    "scalarMode": 4,
                }
                cell_arrays.append(name)

            meshes.append(
                vtk_mesh(ds, point_arrays=point_arrays, cell_arrays=cell_arrays)
            )

    state.field = field
    state.fields = fields
    state.meshes = meshes
    state.files = filesOutput
    print(f"show {len(meshes)} meshes")


# -----------------------------------------------------------------------------
# Web App setup
# -----------------------------------------------------------------------------

state.trame__title = "File loading"
state.fields = []
state.meshes = []

with SinglePageLayout(server) as layout:
    layout.title.set_text("File Loader")
    layout.icon.click = ctrl.view_reset_camera
    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VSelect(
            v_model=("field", "solid"),
            items=("Object.values(fields)",),
            hide_details=True,
            dense=True,
            style="max-width: 200px;",
            classes="mr-4",
        )
        vuetify.VFileInput(
            multiple=True,
            show_size=True,
            small_chips=True,
            truncate_length=25,
            v_model=("files", None),
            dense=True,
            hide_details=True,
            style="max-width: 300px;",
            accept=".vtp",
            __properties=["accept"],
        )
        vuetify.VProgressLinear(
            indeterminate=True, absolute=True, bottom=True, active=("trame__busy",)
        )
        trame.ClientStateChange(name="meshes", change=ctrl.view_reset_camera)

    with layout.content:
        with vuetify.VContainer(
            fluid=True, classes="pa-0 fill-height", style="position: relative;"
        ):
            with vtk_widgets.VtkView(ref="view") as view:
                ctrl.view_reset_camera = view.reset_camera
                with vtk_widgets.VtkGeometryRepresentation(
                    v_for="mesh, idx in meshes",
                    key=("idx",),
                    color_data_range=(
                        "fields[field] && fields[field].range || [0, 1]",
                    ),
                    mapper=(
                        """{
                            colorByArrayName: field,
                            scalarMode: fields[field] && fields[field].scalarMode || 3,
                            interpolateScalarsBeforeMapping: true,
                            scalarVisibility: field !== 'solid',
                        }""",
                    ),
                ):
                    vtk_widgets.VtkMesh("myMesh", state=("mesh",))


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
