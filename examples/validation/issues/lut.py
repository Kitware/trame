import vtk
import vtk.util.numpy_support
import numpy as np

# trame imports
import trame.app
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, vtk as vtk_widgets


def get_scalar_bar(colorTransferFunction):
    scalar_bar = vtk.vtkScalarBarActor()
    scalar_bar.SetLookupTable(colorTransferFunction)
    scalar_bar.SetTitle("Color Temp")
    scalar_bar.UnconstrainedFontSizeOn()
    scalar_bar.SetNumberOfLabels(5)
    scalar_bar.SetMaximumWidthInPixels(800 // 8)
    scalar_bar.SetMaximumHeightInPixels(800 // 3)
    scalar_bar.SetObjectName("ScalarBar")
    return scalar_bar


ren1 = vtk.vtkRenderer()
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.0, 0.69, 0.69, 0.69)
colorTransferFunction.AddRGBPoint(1.0, 1.0, 0.3, 0.3)
scalar_bar = get_scalar_bar(colorTransferFunction)
ren1.AddActor2D(scalar_bar)
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(ren1)
renderWindow.Render()


server = trame.app.get_server(name="1234")
state, ctrl = server.state, server.controller

with SinglePageLayout(server) as layout:
    layout.title.set_text("2D View")
    with layout.content:
        with vuetify.VContainer(
            fluid=True,
            classes="pa-0 fill-height",
        ):
            view = vtk_widgets.VtkLocalView(renderWindow, ref="view")
            ctrl.view_update = view.update

server.start()
