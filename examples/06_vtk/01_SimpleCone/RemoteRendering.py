r"""
Version for trame 1.x - https://github.com/Kitware/trame/blob/release-v1/examples/VTK/SimpleCone/RemoteRendering.py
Delta v1..v2          - https://github.com/Kitware/trame/commit/674f72774228bbcab5689417c1c5642230b1eab8

Installation requirements:
    pip install trame trame-vuetify trame-vtk vtk
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
# Custom / Advanced event handling
# -----------------------------------------------------------------------------

VTK_VIEW_EVENTS = [
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
]
DEFAULT_RESOLUTION = 6


def on_event(*args, **kwargs):
    print("event", args, kwargs)


def event_listeners(events):
    result = {}
    for event in events:
        result[event] = (on_event, "[utils.vtk.event($event)]")
    return result


# -----------------------------------------------------------------------------
# VTK code
# -----------------------------------------------------------------------------

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
    ctrl.view_update()


def update_reset_resolution():
    state.resolution = DEFAULT_RESOLUTION


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

with SinglePageLayout(server) as layout:
    layout.icon.click = ctrl.view_reset_camera
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
        with vuetify.VContainer(
            fluid=True,
            classes="pa-0 fill-height",
        ):
            view = vtk_widgets.VtkRemoteView(
                renderWindow,
                ref="view",
                # For Custom / Advanced event handling
                # interactor_events=("event_types", VTK_VIEW_EVENTS),
                # **event_listeners(VTK_VIEW_EVENTS),
            )
            ctrl.view_update = view.update
            ctrl.view_reset_camera = view.reset_camera

    # Uncomment following line to hide footer
    # layout.footer.hide()


# -----------------------------------------------------------------------------
# Jupyter
# -----------------------------------------------------------------------------


def show(**kwargs):
    from trame.app import jupyter

    jupyter.show(server, **kwargs)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
