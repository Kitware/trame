from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import html, vuetify, vtk as vtk_widgets

from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
)

import vtkmodules.vtkRenderingOpenGL2  # noqa

USING_WITH = True
server = get_server()
ctrl = server.controller


class Cone:
    def __init__(self, server, name):
        self.server = server
        self.name = name

        self.rw = vtkRenderWindow()
        renderer = vtkRenderer()
        self.rw.AddRenderer(renderer)
        cone_source = vtkConeSource()
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(cone_source.GetOutputPort())
        actor = vtkActor()
        actor.SetMapper(mapper)
        renderer.AddActor(actor)
        renderer.ResetCamera()

        self.ui()

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    def ui(self, **kwargs):
        with vtk_widgets.VtkLocalView(self.rw, ref=f"view_{self.name}") as view:
            html.Div(
                self.name,
                style="position: absolute; left: 10px; top: 10px; z-index: 100; color: white;",
            )
            self.ctrl.view_update = view.update
            self.ctrl.view_reset_camera = view.reset_camera


# ---------------------------------------------------------
# Main UI
# ---------------------------------------------------------

with SinglePageLayout(server) as layout:
    with layout.toolbar:
        layout.title.set_text("Active Tab: {{ active_tab }}")
        layout.title.style = "min-width: 200px;"
        vuetify.VSpacer()
        with vuetify.VTabs(v_model=("active_tab", 0), right=True):
            for i in range(5):
                vuetify.VTab(f"Cone {i + 1}")

    with layout.content:
        with vuetify.VContainer(classes="fill-height", fluid=True):
            with vuetify.VTabsItems(
                value=("active_tab",), style="width: 100%; height: 100%;"
            ):
                for i in range(5):
                    with vuetify.VTabItem(
                        value=(i,), style="width: 100%; height: 100%;"
                    ):
                        # html.Div(f"Instance {i + 1}", style="background: red; width: 100%; height: 100%;")
                        Cone(server, f"cone_{i + 1}")


if __name__ == "__main__":
    server.start()
