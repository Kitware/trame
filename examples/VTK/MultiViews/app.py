from trame import state, controller as ctrl
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

cone_source = vtkConeSource()
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cone_source.GetOutputPort())

# -----------------------------------------------------------------------------
# View 1
# -----------------------------------------------------------------------------

actor_1 = vtkActor()
actor_1.SetMapper(mapper)

renderer_1 = vtkRenderer()
renderer_1.SetBackground(0.5, 0, 0)
render_window_1 = vtkRenderWindow()
render_window_1.AddRenderer(renderer_1)

render_window_interactor_1 = vtkRenderWindowInteractor()
render_window_interactor_1.SetRenderWindow(render_window_1)
render_window_interactor_1.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

renderer_1.AddActor(actor_1)
renderer_1.ResetCamera()
render_window_1.Render()


# -----------------------------------------------------------------------------
# View 2
# -----------------------------------------------------------------------------

actor_2 = vtkActor()
actor_2.SetMapper(mapper)

renderer_2 = vtkRenderer()
renderer_2.SetBackground(0, 0.5, 0)
render_window_2 = vtkRenderWindow()
render_window_2.AddRenderer(renderer_2)

render_window_interactor_2 = vtkRenderWindowInteractor()
render_window_interactor_2.SetRenderWindow(render_window_2)
render_window_interactor_2.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

renderer_2.AddActor(actor_2)
renderer_2.ResetCamera()
render_window_2.Render()

# -----------------------------------------------------------------------------

@state.change("resolution")
def update_cone(resolution=DEFAULT_RESOLUTION, **kwargs):
    cone_source.SetResolution(resolution)
    ctrl.update_views()

def update_reset_resolution():
    state.resolution = DEFAULT_RESOLUTION


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

layout = SinglePage("VTK Remote rendering", on_ready=update_cone)
layout.logo.click = ctrl.reset_camera
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
    with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
        with vuetify.VRow(classes="pa-0 ma-0 fill-height"):
            with vuetify.VCol(cols=6, classes="pa-0 ma-0"):
                view_1 = vtk.VtkRemoteView(render_window_1, ref="view1")
                ctrl.update_views.add(view_1.update)
                ctrl.reset_camera.add(view_1.reset_camera)

            with vuetify.VCol(cols=6, classes="pa-0 ma-0"):
                view_2 = vtk.VtkRemoteView(render_window_2, ref="view2")
                ctrl.update_views.add(view_2.update)
                ctrl.reset_camera.add(view_2.reset_camera)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
