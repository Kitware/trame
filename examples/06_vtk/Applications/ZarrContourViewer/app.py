# TODO: Need to migrate to trame v2
from trame import state, get_cli_parser
from trame.html import Div, vuetify, vtk
from trame.layouts import SinglePage

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
# set up class to process zarr
# -----------------------------------------------------------------------------

DEFAULT_LEVEL = 3

parser = get_cli_parser()
parser.add_argument("--data", help="directory to zarr files", dest="data")
args = parser.parse_args()
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
    html_view.update()


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

html_view = vtk.VtkRemoteView(renderWindow, ref="view")

layout = SinglePage("Zarr Skin Generator Demo", on_ready=update_skin)
layout.logo.click = "$refs.view.resetCamera()"
layout.title.set_text("Skin Generator")
layout.toolbar.children += [
    vuetify.VSpacer(),
    vuetify.VBtn(
        vuetify.VIcon("mdi-minus"),
        x_small=True,
        icon=True,
        outlined=True,
        click=decrease_level,
        classes="mx-2",
    ),
    vuetify.VBtn(
        vuetify.VIcon("mdi-plus"),
        x_small=True,
        icon=True,
        outlined=True,
        click=increase_level,
        classes="mx-2",
    ),
    Div(
        "Level({{ level }}) - Points({{parseInt( points ).toLocaleString()}}) - Cells({{parseInt( cells ).toLocaleString()}})",
        style="min-width: 350px; text-align: right;",
    ),
    vuetify.VDivider(vertical=True, classes="mx-2"),
    vuetify.VBtn(
        icon=True,
        click=update_reset_level,
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
    layout.start()
