import asyncio
import enum
from trame import state, controller as ctrl
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

# VTK factory initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa
import vtkmodules.vtkRenderingOpenGL2  # noqa

# -----------------------------------------------------------------------------
# VTK code
# -----------------------------------------------------------------------------

DEFAULT_RESOLUTION = 6

cone_source = vtkConeSource()
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cone_source.GetOutputPort())

# -----------------------------------------------------------------------------
# Views
# -----------------------------------------------------------------------------

NB_COLS = 4

render_windows = []
html_views = []

PALETTE = [
    (0.5, 0, 0),
    (0, 0.5, 0),
    (0, 0, 0.5),
    (0.5, 0, 0.5),
    (0.5, 0.5, 0),
    (0, 0.5, 0.5),
]
colors = PALETTE + PALETTE

# Build render windows
for color in colors:
    actor = vtkActor()
    actor.SetMapper(mapper)

    renderer = vtkRenderer()
    renderer.SetBackground(*color)
    render_window = vtkRenderWindow()
    render_window.AddRenderer(renderer)

    render_window_interactor = vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    render_window_interactor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

    renderer.AddActor(actor)
    renderer.ResetCamera()
    render_window.Render()

    render_windows.append(render_window)

# -----------------------------------------------------------------------------


@state.change("resolution")
def update_cone(resolution=DEFAULT_RESOLUTION, **kwargs):
    cone_source.SetResolution(resolution)
    ctrl.update_views()


def update_reset_resolution():
    state.resolution = DEFAULT_RESOLUTION


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

layout = SinglePage("VTK Remote rendering", on_ready=update_cone)
layout.logo.click = ctrl.reset_camera
layout.title.set_text("Cone Application")

with layout.toolbar:
    vuetify.VSpacer()
    vuetify.VSlider(
        v_model=("resolution", DEFAULT_RESOLUTION),
        min=3,
        max=60,
        step=1,
        hide_details=True,
        dense=True,
        style="max-width: 300px",
    )
    vuetify.VDivider(vertical=True, classes="mx-2")
    with vuetify.VBtn(icon=True, click=update_reset_resolution):
        vuetify.VIcon("mdi-undo-variant")


with layout.content:
    with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
        container = None
        for idx, render_window in enumerate(render_windows):
            if idx % NB_COLS == 0:
                container = vuetify.VRow(
                    classes="pa-0 ma-0",
                    style=f"height: {NB_COLS * 100 / len(render_windows)}%;",
                )
            with container:
                with vuetify.VCol(classes="pa-0 ma-0"):
                    view = vtk.VtkRemoteView(render_window, ref=f"view{idx}")
                    html_views.append(view)
                    ctrl.update_views.add(view.update)
                    ctrl.reset_camera.add(view.reset_camera)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
