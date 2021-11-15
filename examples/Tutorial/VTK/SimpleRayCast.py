#!/usr/bin/env python

# Web imports
import os
from trame import start, get_cli_parser
from trame.layouts import SinglePage
from trame.html import vtk, vuetify

# -----------------------------------------------------------------------------
# Example:    SimpleRayCast
# taken from: https://kitware.github.io/vtk-examples/site/Python/
# -----------------------------------------------------------------------------

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolume import vtkFixedPointVolumeRayCastMapper

# noinspection PyUnresolvedReferences
from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkOpenGLRayCastImageDisplayHelper

# -----------------------------------------------------------------------------
# Getting file to load (from CLI --data /path/to/ironProt.vtk)
# => https://github.com/naucoin/VTKData/raw/master/Data/ironProt.vtk
# -----------------------------------------------------------------------------

parser = get_cli_parser()
parser.add_argument("--data", help="File to load", dest="data")
args = parser.parse_args()
fileName = os.path.abspath(args.data)

# -----------------------------------------------------------------------------

colors = vtkNamedColors()

# This is a simple volume rendering example that
# uses a vtkFixedPointVolumeRayCastMapper

# Create the standard renderer, render window
# and interactor.
ren1 = vtkRenderer()

renWin = vtkRenderWindow()
renWin.AddRenderer(ren1)

iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.GetInteractorStyle().SetCurrentStyleToTrackballCamera()  # +++

# Create the reader for the data.
reader = vtkStructuredPointsReader()
reader.SetFileName(fileName)

# Create transfer mapping scalar value to opacity.
opacityTransferFunction = vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(20, 0.0)
opacityTransferFunction.AddPoint(255, 0.2)

# Create transfer mapping scalar value to color.
colorTransferFunction = vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(64.0, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(128.0, 0.0, 0.0, 1.0)
colorTransferFunction.AddRGBPoint(192.0, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(255.0, 0.0, 0.2, 0.0)

# The property describes how the data will look.
volumeProperty = vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.ShadeOn()
volumeProperty.SetInterpolationTypeToLinear()

# The mapper / ray cast function know how to render the data.
volumeMapper = vtkFixedPointVolumeRayCastMapper()
volumeMapper.SetInputConnection(reader.GetOutputPort())

# The volume holds the mapper and the property and
# can be used to position/orient the volume.
volume = vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

ren1.AddVolume(volume)
ren1.SetBackground(colors.GetColor3d("Wheat"))
ren1.GetActiveCamera().Azimuth(45)
ren1.GetActiveCamera().Elevation(30)
ren1.ResetCameraClippingRange()
ren1.ResetCamera()

# -----------------------------------------------------------------------------
# Web Application setup
# -----------------------------------------------------------------------------

layout = SinglePage("Hello Trame")
layout.title.set_text("Hello Trame")

# html_view = vtk.VtkRemoteView(renWin)
html_view = vtk.VtkLocalView(renWin)

layout.content.children += [
    vuetify.VContainer(
        fluid=True,
        classes="pa-0 fill-height",
        children=[html_view],
    )
]

layout.on_ready = html_view.update

if __name__ == "__main__":
    layout.start()
