from trame import html, start, update_state, change
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
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch

# Grab implementation
import vtkmodules.vtkRenderingOpenGL2

# -----------------------------------------------------------------------------
# VTK code
# -----------------------------------------------------------------------------

DEFAULT_RESOLUTION = 6

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


@change("resolution")
def update_cone(resolution=DEFAULT_RESOLUTION, **kwargs):
    cone_source.SetResolution(resolution)
    html_view.update()


def update_reset_resolution():
    update_state("resolution", DEFAULT_RESOLUTION)


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

html_view = vtk.VtkRemoteView(renderWindow, ref="view")

layout = SinglePage("VTK Remote rendering")
layout.logo.click = "$refs.view.resetCamera()"
layout.title.content = "Cone Application"
layout.toolbar.children += [
    vuetify.VSpacer(),
    vuetify.VSlider(
        v_model=("resolution", DEFAULT_RESOLUTION),
        min=3,
        max=60,
        step=1,
        hide_details=True,
        dense=True,
        style="max-width: 300px",
    ),
    vuetify.VDivider(vertical=True, classes="mx-2"),
    vuetify.VBtn(
        icon=True,
        click=update_reset_resolution,
        children=[vuetify.VIcon("mdi-undo-variant")],
    ),
]

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
    # print(layout.html)
    start(layout, on_ready=update_cone)
