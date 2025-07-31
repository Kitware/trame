import vtk

from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3, vtk as vtk_widgets


class PushCamera(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._setup_vtk()
        self._build_ui()

    def _setup_vtk(self):
        render_window = vtk.vtkRenderWindow()
        render_window.SetOffScreenRendering(True)

        renderer = vtk.vtkRenderer()
        render_window.AddRenderer(renderer)

        cone = vtk.vtkConeSource()
        mapper = vtk.vtkPolyDataMapper()
        actor = vtk.vtkActor()

        mapper.SetInputConnection(cone.GetOutputPort())
        actor.SetMapper(mapper)
        renderer.AddActor(actor)
        renderer.ResetCamera()

        self.render_window = render_window
        self.camera = renderer.GetActiveCamera()

    def _build_ui(self):
        with SinglePageLayout(self.server) as self.ui:
            self.ui.title.set_text("Client-side Camera Control")

            with self.ui.content:
                with vuetify3.VContainer(
                    fluid=True,
                    classes="pa-0 fill-height",
                ):
                    vtk_widgets.VtkLocalView(self.render_window, ctx_name="view")

            with self.ui.toolbar:
                vuetify3.VSpacer()
                vuetify3.VBtn("Set Top View", click=self.set_top_view)

    def set_top_view(self):
        self.camera.SetPosition(0, 5, 0)
        self.camera.SetFocalPoint(0, 0, 0)
        self.camera.SetViewUp(0, 0, -1)

        self.ctx.view.push_camera()
        # self.ctx.view.update()


if __name__ == "__main__":
    app = PushCamera()
    app.server.start()
