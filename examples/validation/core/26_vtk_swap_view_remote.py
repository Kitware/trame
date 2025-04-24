import asyncio

# Required for rendering initialization, not necessary for
# local rendering, but doesn't hurt to include it
import vtkmodules.vtkRenderingOpenGL2  # noqa
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkConeSource, vtkSphereSource

# Required for interactor initialization
from vtkmodules.vtkInteractionStyle import (
    vtkInteractorStyleSwitch,  # noqa
    vtkInteractorStyleTrackballCamera,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

from trame.app import asynchronous, get_server
from trame.ui.vuetify import VAppLayout
from trame.widgets import vtk, vuetify

# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------


colors = vtkNamedColors()


def cone():
    cone = vtkConeSource()
    cone.SetResolution(60)

    # Create a mapper and actor
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(cone.GetOutputPort())

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetDiffuseColor(colors.GetColor3d("bisque"))

    # Visualize
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtkRenderWindowInteractor()
    interactor_style = vtkInteractorStyleTrackballCamera()
    renderWindowInteractor.SetInteractorStyle(interactor_style)
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d("bisque"))
    renderer.ResetCamera()

    renderWindow.SetSize(640, 480)
    renderWindow.SetWindowName("Cone")

    return renderWindow


def sphere():
    sphere = vtkSphereSource()

    # Create a mapper and actor
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(sphere.GetOutputPort())

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetDiffuseColor(colors.GetColor3d("bisque"))

    # Visualize
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtkRenderWindowInteractor()
    interactor_style = vtkInteractorStyleTrackballCamera()
    renderWindowInteractor.SetInteractorStyle(interactor_style)
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d("Salmon"))
    renderer.ResetCamera()

    renderWindow.SetSize(640, 480)
    renderWindow.SetWindowName("Sphere")

    return renderWindow


cone_window = cone()
sphere_window = sphere()

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# Initial VTK window width and height values
state.vtk_window_width = 300
state.vtk_window_height = 300


# -----------------------------------------------------------------------------
# Background thread
# -----------------------------------------------------------------------------


@asynchronous.task
async def refresh_function(**kwargs):
    counter = 1
    while True:
        with state:
            if counter % 2 == 0:
                ren_win = sphere_window
            else:
                ren_win = cone_window

            ctrl.view_replace(ren_win)
            ctrl.view_update()

            counter += 1

        await asyncio.sleep(5)


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------


with VAppLayout(server) as layout:
    with layout.root:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            view = vtk.VtkRemoteView(cone_window)
            # view = vtk.VtkLocalView(cone_window)
            ctrl.view_update = view.update
            ctrl.view_replace = view.replace_view
            ctrl.on_server_ready.add(refresh_function)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
