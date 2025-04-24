import vtk
import vtkmodules.vtkRenderingOpenGL2  # noqa (needed for vtkHardwareSelector)
from vtkmodules.vtkFiltersCore import vtkTubeFilter
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
# Generate dataset
# -----------------------------------------------------------------------------

points = vtk.vtkPoints()
points.SetNumberOfPoints(4)
line = vtk.vtkLine()
lines = vtk.vtkCellArray()

# create first line segment
points.SetPoint(0, 0, 0, 0)
line.GetPointIds().SetId(0, 0)

points.SetPoint(1, 1, 1, 1)
line.GetPointIds().SetId(1, 1)

lines.InsertNextCell(line)

# create second line segment
points.SetPoint(2, 1, 1, 1)
line.GetPointIds().SetId(0, 2)

points.SetPoint(3, 2, 2, 2)
line.GetPointIds().SetId(1, 3)

lines.InsertNextCell(line)

linesPolyData = vtk.vtkPolyData()
linesPolyData.SetPoints(points)
linesPolyData.SetLines(lines)

# -----------------------------------------------------------------------------
# Trame initialization
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Interactions
# -----------------------------------------------------------------------------


def foo(pickData):
    print("hello")


# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

tubes_filter = vtkTubeFilter()
tubes_filter.SetInputData(linesPolyData)
tubes_filter.SetRadius(2)
tubes_filter.SetNumberOfSides(3)
tubes_filter.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(tubes_filter.GetOutputPort())
actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.SetBackground(1, 1, 1)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)

rw_interactor = vtkRenderWindowInteractor()
rw_interactor.SetRenderWindow(render_window)
rw_interactor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

renderer.ResetCamera()

# -----------------------------------------------------------------------------
# GUI layout
# -----------------------------------------------------------------------------

with SinglePageLayout(server) as layout:
    with layout.content:
        with vuetify.VContainer(fluid=True, classes="fill-height pa-0 ma-0"):
            view = vtk_widgets.VtkRemoteView(
                render_window,
                interactor_events=("events", ["LeftButtonPress"]),
                LeftButtonPress=(foo, "[utils.vtk.event($event)]"),
            )
            view.update
            view.reset_camera

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
