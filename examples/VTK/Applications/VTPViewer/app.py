import trame as tr
from trame.layouts import SinglePage
from trame.html import vtk, vuetify, StateChange

from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.web.utils import mesh as vtk_mesh

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


@tr.change("files")
def load_client_files(files, **kwargs):
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
            print(f'Load {file.get("name")}')
            bytes = file.get("content")
            filesOutput.append({"name": file.get("name"), "size": file.get("size")})
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

    tr.update_state("field", field)
    tr.update_state("fields", fields)
    tr.update_state("meshes", meshes)
    tr.update_state("files", filesOutput)
    print(f"show {len(meshes)} meshes")


# -----------------------------------------------------------------------------
# Web App setup
# -----------------------------------------------------------------------------

tr.update_state("fields", [])
tr.update_state("meshes", [])

layout = SinglePage("File loading")
layout.title.set_text("File Loader")
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
        indeterminate=True, absolute=True, bottom=True, active=("busy",)
    )
    StateChange(name="meshes", change="$refs.view.resetCamera()")


with layout.content:
    with vuetify.VContainer(
        fluid=True, classes="pa-0 fill-height", style="position: relative;"
    ):
        with vtk.VtkView(ref="view"):
            with vtk.VtkGeometryRepresentation(
                v_for="mesh, idx in meshes",
                key=("idx",),
                color_data_range=("fields[field] && fields[field].range || [0, 1]",),
                mapper=(
                    "{ colorByArrayName: field, scalarMode: fields[field] && fields[field].scalarMode || 3, interpolateScalarsBeforeMapping: true, scalarVisibility: field !== 'solid' }",
                ),
            ):
                vtk.VtkMesh("myMesh", state=("mesh",))


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
