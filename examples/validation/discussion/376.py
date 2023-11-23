from trame.app import get_server
from trame.widgets import vtk as vtk_widgets

import pyvista as pv
from pyvista.trame.ui import plotter_ui

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkRenderer,
    vtkRenderWindow,
    vtkPolyDataMapper,
    vtkActor,
)

CLIENT_TYPE = "vue3"
USE_PV = False
RADIUS = 0.1

if CLIENT_TYPE == "vue2":
    from trame.widgets import vuetify2 as vuetify
    from trame.ui.vuetify2 import SinglePageLayout
else:
    from trame.widgets import vuetify3 as vuetify
    from trame.ui.vuetify3 import SinglePageLayout


class App:
    def __init__(self, server=None):
        self.server = get_server(server, client_type=CLIENT_TYPE)

        if USE_PV:
            self.plotter = pv.Plotter()
        else:
            self.renderWindow = vtkRenderWindow()
            self.renderer = vtkRenderer()
            self.renderWindow.AddRenderer(self.renderer)
        self.sources_counter = 0
        self.ui()

    @property
    def ctrl(self):
        return self.server.controller

    @property
    def state(self):
        return self.server.state

    def add_actor(self):
        center = (self.sources_counter * RADIUS * 2.1, 0, 0)
        self.sources_counter += 1
        if USE_PV:
            mapper = pv.DataSetMapper(pv.Sphere(radius=RADIUS, center=center))
            actor = pv.Actor(mapper=mapper)
            self.plotter.add_actor(actor)
        else:
            _source = vtkSphereSource()
            _source.SetRadius(RADIUS)
            _source.SetCenter(*center)
            mapper = vtkPolyDataMapper()
            actor = vtkActor()
            mapper.SetInputConnection(_source.GetOutputPort())
            actor.SetMapper(mapper)
            self.renderer.AddActor(actor)

        self.ctrl.view_update()
        self.ctrl.view_reset_camera()

    def ui(self):
        with SinglePageLayout(self.server) as layout:
            self.layout = layout
            layout.icon.click = self.ctrl.view_reset_camera

            with layout.content:
                with vuetify.VCol():
                    vuetify.VBtn("AddActor", click=self.add_actor)
                with vuetify.VContainer(
                    fluid=True,
                    classes="pa-0 fill-height",
                ):
                    view = (
                        plotter_ui(self.plotter, mode="client")
                        if USE_PV
                        else vtk_widgets.VtkLocalView(self.renderWindow)
                    )
                    self.ctrl.view_update = view.update
                    self.ctrl.view_reset_camera = view.reset_camera


if __name__ == "__main__":
    app = App()
    app.add_actor()
    app.add_actor()
    app.server.start()
