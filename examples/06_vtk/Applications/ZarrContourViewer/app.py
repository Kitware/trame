r"""
Version for trame 1.x - https://github.com/Kitware/trame/tree/release-v1/examples/VTK/Applications/ZarrContourViewer
Delta v1..v2          - https://github.com/Kitware/trame/commit/7b3cda7c45b8a60132892f762e16ed28cb709481
"""

from trame.app import get_server
from trame.widgets import html, vuetify, vtk as vtk_widgets
from trame.ui.vuetify import SinglePageLayout

from vtkContourGeneratorFromZarr import vtkContourGeneratorFromZarr

from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa
import vtkmodules.vtkRenderingOpenGL2  # noqa

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# set up class to process zarr
# -----------------------------------------------------------------------------

DEFAULT_LEVEL = 3

server.cli.add_argument("--data", help="directory to zarr files", dest="data")
args = server.cli.parse_args()
skin_generator = vtkContourGeneratorFromZarr(args.data)
skin_generator.contourForLevel(DEFAULT_LEVEL)

MAX_LEVEL = skin_generator.getMaxLevel()

# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(skin_generator.getContour().GetOutputPort())
actor = vtkActor()
actor.SetMapper(mapper)

renderer.AddActor(actor)
renderer.ResetCamera()
renderWindow.Render()

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------

state.points = 0
state.cells = 0
state.level = DEFAULT_LEVEL


@state.change("level")
def update_skin(level=DEFAULT_LEVEL, **kwargs):
    nb_points, nb_cells = skin_generator.contourForLevel(level)
    state.points = nb_points
    state.cells = nb_cells
    ctrl.view_update()


def update_reset_level():
    state.level = DEFAULT_LEVEL


def increase_level():
    if state.level < MAX_LEVEL:
        state.level += 1


def decrease_level():
    if 1 < state.level:
        state.level -= 1


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

state.trame__title = "Zarr Skin Generator Demo"


with SinglePageLayout(server) as layout:
    layout.icon.click = "$refs.view.resetCamera()"
    layout.title.set_text("Skin Generator")
    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VBtn(
            vuetify.VIcon("mdi-minus"),
            x_small=True,
            icon=True,
            outlined=True,
            click=decrease_level,
            classes="mx-2",
        )
        vuetify.VBtn(
            vuetify.VIcon("mdi-plus"),
            x_small=True,
            icon=True,
            outlined=True,
            click=increase_level,
            classes="mx-2",
        )
        html.Div(
            "Level({{ level }}) - Points({{parseInt( points ).toLocaleString()}}) - Cells({{parseInt( cells ).toLocaleString()}})",
            style="min-width: 350px; text-align: right;",
        )
        vuetify.VDivider(vertical=True, classes="mx-2"),
        vuetify.VBtn(
            icon=True,
            click=update_reset_level,
            children=[vuetify.VIcon("mdi-undo-variant")],
        )

    with layout.content:
        with vuetify.VContainer(
            fluid=True,
            classes="pa-0 fill-height",
        ):
            html_view = vtk_widgets.VtkRemoteView(renderWindow, ref="view")
            ctrl.view_update = html_view.update
            ctrl.view_reset_camera = html_view.reset_camera

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
