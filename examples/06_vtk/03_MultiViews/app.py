r"""
Version for trame 1.x - https://github.com/Kitware/trame/blob/release-v1/examples/VTK/MultiViews/app.py
Delta v1..v2          - https://github.com/Kitware/trame/commit/ba381b3ad286b6269e181d76d1e13ef0cc2d5bc7

Installation requirements:
    pip install trame trame-vuetify trame-vtk
"""

import vtkmodules.vtkRenderingOpenGL2  # noqa
from vtkmodules.vtkFiltersSources import vtkConeSource

# VTK factory initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vtk as vtk_widgets
from trame.widgets import vuetify

# -----------------------------------------------------------------------------
# Trame initialization
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

state.trame__title = "VTK Remote rendering"

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
    with state:
        state.resolution = DEFAULT_RESOLUTION

    ctrl.update_views()


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

with SinglePageLayout(server) as layout:
    layout.icon.click = ctrl.reset_camera
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
            end=ctrl.update_views,
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
                        view = vtk_widgets.VtkRemoteView(
                            render_window, ref=f"view{idx}"
                        )
                        html_views.append(view)
                        ctrl.update_views.add(view.update)
                        ctrl.reset_camera.add(view.reset_camera)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
