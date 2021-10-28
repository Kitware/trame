from trame import start, update_state, get_state, change, get_cli_parser
from trame.html import Div
from trame.html import vuetify, vtk
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
renderWindowInteractor.EnableRenderOff()

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

update_state("points", 0)
update_state("cells", 0)
update_state("level", DEFAULT_LEVEL)


@change("level")
def update_skin(level=DEFAULT_LEVEL, **kwargs):
    nb_points, nb_cells = skin_generator.contourForLevel(level)
    update_state("points", nb_points)
    update_state("cells", nb_cells)
    html_view.update()


def update_reset_level():
    update_state("level", DEFAULT_LEVEL)


def increase_level():
    (current_level,) = get_state("level")
    if current_level < MAX_LEVEL:
        update_state("level", current_level + 1)


def decrease_level():
    (current_level,) = get_state("level")
    if 1 < current_level:
        update_state("level", current_level - 1)


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

html_view = vtk.VtkRemoteView(renderWindow, ref="view")

layout = SinglePage("Zarr Skin Generator Demo")
layout.logo.click = "$refs.view.resetCamera()"
layout.title.content = "Skin Generator"
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
    start(layout, on_ready=update_skin)
