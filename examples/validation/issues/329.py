import os
from pathlib import Path
from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vtk as vtk2, vuetify
import vtk

from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

# Required for interactor initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa

# Required for rendering initialization, not necessary for
# local rendering, but doesn't hurt to include it
import vtkmodules.vtkRenderingOpenGL2  # noqa

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.OffScreenRenderingOn()

renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()


# Read the data

# reader = vtkStructuredPointsReader()
reader = vtkUnstructuredGridReader()

reader.SetFileName(str(Path(__file__).with_name("lv_fiber.vtk").absolute()))
reader.Update()
# 2. 创建箭头源
arrow_source = vtk.vtkArrowSource()
arrow_source.Update()
# 3. 创建箭头映射器
arrow_mapper = vtk.vtkGlyph3DMapper()
arrow_mapper.SetInputConnection(reader.GetOutputPort())
arrow_mapper.SetSourceConnection(arrow_source.GetOutputPort())
arrow_mapper.SetScaleFactor(1.0)  # 调整箭头大小
arrow_mapper.ScalingOn()
arrow_mapper.Update()
# 4. 创建箭头演员
arrow_actor = vtk.vtkActor()
arrow_actor.SetMapper(arrow_mapper)
# 7. 添加箭头演员到渲染器
renderer.AddActor(arrow_actor)
# 8. 设置渲染器背景颜色和相机位置
renderer.SetBackground(1.0, 1.0, 1.0)
# 9. 设置箭头及轴的尺寸
arrow_source.SetTipLength(0.1)  # 箭头尖部的长度
arrow_source.SetTipRadius(0.05)  # 箭头尖部的半径
arrow_source.SetShaftRadius(0.02)  # 箭头杆的半径

renderer.ResetCamera()
renderWindow.Render()

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
ctrl = server.controller

with SinglePageLayout(server) as layout:
    layout.title.set_text("Hello1 trame")

    with layout.content:
        with vuetify.VContainer(
            fluid=True,
            classes="pa-0 fill-height",
        ):
            view = vtk2.VtkRemoteView(renderWindow, interactive_ratio=1)
            # view = vtk2.VtkLocalView(renderWindow)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
