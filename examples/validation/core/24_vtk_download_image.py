import vtkmodules.vtkRenderingOpenGL2  # noqa

# -----------------------------------------------------------------------------
# VTK
# -----------------------------------------------------------------------------
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa
from vtkmodules.vtkIOImage import vtkPNGWriter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkWindowToImageFilter,
)

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vtk, vuetify

DEFAULT_RESOLUTION = 6

renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)

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

# -----------------------------------------------------------------------------
# Web App setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller


@state.change("resolution")
def update_resolution(resolution, **kwargs):
    cone_source.SetResolution(int(resolution))
    ctrl.view_update()


@ctrl.trigger("download_screenshot")
def download_screenshot():
    w2if = vtkWindowToImageFilter()
    w2if.SetInput(renderWindow)
    w2if.SetInputBufferTypeToRGB()
    w2if.ReadFrontBufferOff()
    #
    writer1 = vtkPNGWriter()
    writer1.SetInputConnection(w2if.GetOutputPort())
    writer1.SetWriteToMemory(True)
    writer1.Write()
    #
    return server.protocol.addAttachment(memoryview(writer1.GetResult()))


with SinglePageLayout(server) as layout:
    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VSlider(
            v_model=("resolution", DEFAULT_RESOLUTION),
            min=3,
            max=60,
            style="max-width: 300px",
            dense=True,
            hide_details=True,
        )
        with vuetify.VBtn(
            icon=True,
            click="utils.download('vtk.png', trigger('download_screenshot'), 'image/png')",
        ):
            vuetify.VIcon("mdi-camera")

    with layout.content:
        with vuetify.VContainer(classes="pa-0 fill-height", fluid=True):
            view = vtk.VtkRemoteView(renderWindow)
            ctrl.view_update = view.update


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
