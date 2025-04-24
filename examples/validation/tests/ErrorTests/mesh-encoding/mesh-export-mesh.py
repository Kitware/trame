from pathlib import Path

from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader

from trame.html import vtk, vuetify
from trame.layouts import SinglePage

DATA_DIR = Path(Path(__file__).parent.parent.parent.parent, "data")
MESH_PATH = str(Path(DATA_DIR, "mesh.vtu"))

# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(MESH_PATH)

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

layout = SinglePage("VTK.js rendering")
layout.title.set_text("Test mesh exchange")

with layout.content:
    with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
        with vtk.VtkView() as view:
            layout.logo.click = view.reset_camera
            with vtk.VtkGeometryRepresentation(property=("{ edgeVisibility: true }",)):
                vtk.VtkPolyData("cone", dataset=reader)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
