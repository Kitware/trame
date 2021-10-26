from trame import start
from trame.html import vuetify, vtk
from trame.layouts import SinglePage

from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkPolyDataMapper,
    vtkActor,
)

# Required for interacter faactory
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch

# Required for remote rendering factory initialization, not necessary for 
# local rendering, but doesn't hurt to include it
import vtkmodules.vtkRenderingOpenGL2


# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()
renderWindowInteractor.EnableRenderOff()

cone_source = vtkConeSource()
mapper = vtkPolyDataMapper()
actor = vtkActor()
mapper.SetInputConnection(cone_source.GetOutputPort())
actor.SetMapper(mapper)
renderer.AddActor(actor)
renderer.ResetCamera()
renderWindow.Render()

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

def update_cone(**kwargs):
    html_view.update()

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

layout = SinglePage("Hello Trame")
layout.title.content = "Hello Trame"

html_view = vtk.VtkLocalView(renderWindow, ref="view")

layout.content.children += [
    vuetify.VContainer(
        fluid=True,
        classes="pa-0 fill-height",
        children=[html_view],
    )
]

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    start(layout, on_ready=update_cone)
