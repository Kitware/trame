import multiprocessing

from trame import state
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

renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.OffScreenRenderingOn()

renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

cone_source = vtkConeSource()
mapper = vtkPolyDataMapper()
actor = vtkActor()
mapper.SetInputConnection(cone_source.GetOutputPort())
actor.SetMapper(mapper)
renderer.AddActor(actor)
renderer.ResetCamera()
renderWindow.Render()


@state.change("resolution")
def update_cone(resolution=DEFAULT_RESOLUTION, **kwargs):
    cone_source.SetResolution(resolution)
    html_view.update()


def update_reset_resolution():
    state.resolution = DEFAULT_RESOLUTION


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------


def event(*args, **kwargs):
    print("event", args, kwargs)


html_view = vtk.VtkRemoteView(
    renderWindow,
    ref="view",
    interactor_events=(
        "event_types",
        [
            "StartAnimation",
            "Animation",
            "EndAnimation",
            "MouseEnter",
            "MouseLeave",
            "StartMouseMove",
            "MouseMove",
            "EndMouseMove",
            "LeftButtonPress",
            "LeftButtonRelease",
            "MiddleButtonPress",
            "MiddleButtonRelease",
            "RightButtonPress",
            "RightButtonRelease",
            "KeyPress",
            "KeyDown",
            "KeyUp",
            "StartMouseWheel",
            "MouseWheel",
            "EndMouseWheel",
            "StartPinch",
            "Pinch",
            "EndPinch",
            "StartPan",
            "Pan",
            "EndPan",
            "StartRotate",
            "Rotate",
            "EndRotate",
            "Button3D",
            "Move3D",
            "StartPointerLock",
            "EndPointerLock",
            "StartInteraction",
            "Interaction",
            "EndInteraction",
        ],
    ),
    StartAnimation=(event, "[vtkEvent($event)]"),
    Animation=(event, "[vtkEvent($event)]"),
    EndAnimation=(event, "[vtkEvent($event)]"),
    MouseEnter=(event, "[vtkEvent($event)]"),
    MouseLeave=(event, "[vtkEvent($event)]"),
    StartMouseMove=(event, "[vtkEvent($event)]"),
    MouseMove=(event, "[vtkEvent($event)]"),
    EndMouseMove=(event, "[vtkEvent($event)]"),
    LeftButtonPress=(event, "[vtkEvent($event)]"),
    LeftButtonRelease=(event, "[vtkEvent($event)]"),
    MiddleButtonPress=(event, "[vtkEvent($event)]"),
    MiddleButtonRelease=(event, "[vtkEvent($event)]"),
    RightButtonPress=(event, "[vtkEvent($event)]"),
    RightButtonRelease=(event, "[vtkEvent($event)]"),
    KeyPress=(event, "[vtkEvent($event)]"),
    KeyDown=(event, "[vtkEvent($event)]"),
    KeyUp=(event, "[vtkEvent($event)]"),
    StartMouseWheel=(event, "[vtkEvent($event)]"),
    MouseWheel=(event, "[vtkEvent($event)]"),
    EndMouseWheel=(event, "[vtkEvent($event)]"),
    StartPinch=(event, "[vtkEvent($event)]"),
    Pinch=(event, "[vtkEvent($event)]"),
    EndPinch=(event, "[vtkEvent($event)]"),
    StartPan=(event, "[vtkEvent($event)]"),
    Pan=(event, "[vtkEvent($event)]"),
    EndPan=(event, "[vtkEvent($event)]"),
    StartRotate=(event, "[vtkEvent($event)]"),
    Rotate=(event, "[vtkEvent($event)]"),
    EndRotate=(event, "[vtkEvent($event)]"),
    Button3D=(event, "[vtkEvent($event)]"),
    Move3D=(event, "[vtkEvent($event)]"),
    StartPointerLock=(event, "[vtkEvent($event)]"),
    EndPointerLock=(event, "[vtkEvent($event)]"),
    StartInteraction=(event, "[tkEvent($event)']"),
    Interaction=(event, "[vtkEvent($event)]"),
    EndInteraction=(event, "[vtkEvent($event)]"),
)

layout = SinglePage("VTK Remote rendering", on_ready=update_cone)
layout.logo.click = html_view.reset_camera
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
    vuetify.VContainer(
        fluid=True,
        classes="pa-0 fill-height",
        children=[html_view],
    )

# Uncomment following line to hide footer
# layout.footer.hide()

# Uncomment following line to change logo to use mdi icon
# layout.logo.children = [vuetify.VIcon('mdi-menu')]

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # Freeze support is needed particularly for Windows, to prevent infinite
    # recursion when multiprocessing is used.
    multiprocessing.freeze_support()
    layout.start()
    # The layout can alternatively be started as a desktop window instead
    # layout.start_desktop_window()
