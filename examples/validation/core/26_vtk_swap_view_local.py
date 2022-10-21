import asyncio
from trame.app import get_server
from trame.ui.vuetify import VAppLayout
from trame.widgets import vtk, vuetify, html

from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

from vtkmodules.vtkFiltersSources import vtkConeSource, vtkSphereSource
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera


# Required for interactor initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa

# Required for rendering initialization, not necessary for
# local rendering, but doesn't hurt to include it
import vtkmodules.vtkRenderingOpenGL2  # noqa


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

server = get_server()
state, ctrl = server.state, server.controller

state.visible_view = 0


# -----------------------------------------------------------------------------
# Background thread
# -----------------------------------------------------------------------------


async def refresh_function(**kwargs):
    while True:
        with state:
            state.visible_view += 1
            ctrl.view_update()

        await asyncio.sleep(5)


ctrl.on_server_ready.add_task(refresh_function)

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------


with VAppLayout(server) as layout:
    with layout.root:
        with vuetify.VContainer(
            fluid=True, classes="pa-0 fill-height", style="position: relative;"
        ):
            with html.Div(
                style="z-index: 1; width; 100%; height: 100%;",
                v_if="!(visible_view % 2)",
            ):
                view = vtk.VtkLocalView(
                    cone_window,
                    context_name="cone",
                    namespace="cone",
                    ref="cone",
                    style="position: absolute; width: 100%; height: 100%;",
                )
                ctrl.view_update.add(view.update)
            with html.Div(
                style="z-index: 1; width; 100%; height: 100%;", v_if="visible_view % 2"
            ):
                view = vtk.VtkLocalView(
                    sphere_window,
                    context_name="sphere",
                    namespace="sphere",
                    ref="sphere",
                    style="position: absolute; width: 100%; height: 100%;",
                )
                ctrl.view_update.add(view.update)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
