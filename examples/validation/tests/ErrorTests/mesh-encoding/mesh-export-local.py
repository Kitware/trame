from pathlib import Path

from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

from trame import controller as ctrl
from trame.html import vtk, vuetify
from trame.layouts import SinglePage

DATA_DIR = Path(Path(__file__).parent.parent.parent.parent, "data")
MESH_PATH = str(Path(DATA_DIR, "mesh.vtu"))

# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(MESH_PATH)

renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

mapper = vtkDataSetMapper()
actor = vtkActor()
actor.GetProperty().SetEdgeVisibility(1)
mapper.SetInputConnection(reader.GetOutputPort())
actor.SetMapper(mapper)
renderer.AddActor(actor)
renderer.ResetCamera()
renderWindow.Render()

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

layout = SinglePage("VTK.js rendering", on_ready=ctrl.on_ready)
layout.title.set_text("Test mesh exchange")

with layout.content:
    with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
        with vtk.VtkLocalView(renderWindow) as view:
            layout.logo.click = view.reset_camera
            ctrl.on_ready = view.update

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
