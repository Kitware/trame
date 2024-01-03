from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, vtk as vtk_widgets

from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
)

import vtkmodules.vtkRenderingOpenGL2  # noqa

USING_WITH = True
server = get_server(client_type="vue2")
ctrl = server.controller


class App:
    def __init__(self, server):
        self.server = server
        self.layout = None
        self.container = None

        self.rw = vtkRenderWindow()
        self.renderer = vtkRenderer()
        self.rw.AddRenderer(self.renderer)
        self.cone_source = None

        # Just because we are deferring UI initialization
        vtk_widgets.initialize(server)
        vuetify.initialize(server)

        self.ctrl.add("on_server_ready")(self.ui)
        self.state.change("resolution")(self.update_resolution)

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    def update_resolution(self, resolution, **kwargs):
        if self.cone_source:
            self.cone_source.SetResolution(resolution)
            self.ctrl.view_update()

    def add_cone(self):
        self.state.cone_disabled = True
        self.cone_source = vtkConeSource()
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(self.cone_source.GetOutputPort())
        actor = vtkActor()
        actor.SetMapper(mapper)
        self.renderer.AddActor(actor)
        self.renderer.ResetCamera()

        if USING_WITH:
            with self.layout:  # Will call self.layout.flush_content() on_exit
                with self.container:
                    with vtk_widgets.VtkLocalView(self.rw) as view:
                        self.ctrl.view_update = view.update
                        self.ctrl.view_reset_camera = view.reset_camera
        else:
            # Could also be
            view = vtk_widgets.VtkLocalView(self.rw)
            self.ctrl.view_update = view.update
            self.ctrl.view_reset_camera = view.reset_camera
            self.container.add_child(view)
            self.layout.flush_content()

    def ui(self, **kwargs):
        with SinglePageLayout(self.server) as layout:
            self.layout = layout
            layout.title.set_text("Hello trame")
            layout.icon.click = self.ctrl.view_reset_camera

            with layout.toolbar:
                vuetify.VSpacer()
                vuetify.VSlider(
                    v_show=("cone_disabled",),
                    v_model=("resolution", 6),
                    max=60,
                    dense=True,
                    hide_details=True,
                )
                vuetify.VBtn(
                    "Cone Pipeline",
                    disabled=("cone_disabled", False),
                    click=self.add_cone,
                )

            with layout.content:
                self.container = vuetify.VContainer(
                    fluid=True,
                    classes="pa-0 fill-height",
                )


if __name__ == "__main__":
    app = App(server)
    server.start()
