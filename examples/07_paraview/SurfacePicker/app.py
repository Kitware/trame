# pip install trame trame-vtk trame-vuetify

import paraview.web.venv

from paraview import simple
from typing import Any
from trame.app import get_server
from trame.decorators import TrameApp, change
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3 as vuetify, paraview, client
from trame_server import Server
from trame_server.controller import Controller


@TrameApp()
class Viewer:
    def __init__(self, server: Server = None) -> None:
        self.server = get_server(server, client_type="vue3")

        self.pixel_ratio = 1

        self.load_cone_source()
        self.setup_ui()

    @property
    def ctrl(self) -> Controller:
        return self.server.controller

    @property
    def active_view(self) -> Any:
        return simple.GetActiveViewOrCreate("RenderView")

    @property
    def active_camera(self) -> Any:
        return simple.GetActiveCamera()

    def load_cone_source(self) -> None:
        cone = simple.Cone()
        simple.Show(cone)
        simple.Render()

    def add_sphere(self, sphere_center: list, color: list) -> None:
        sphere = simple.Sphere()
        sphere.Center = sphere_center
        sphere.Radius = 0.01
        sphere_display = simple.Show(sphere)
        sphere_display.AmbientColor = color
        sphere_display.DiffuseColor = color

        self.ctrl.view_update()

    def on_right_button_release(self, pickData: dict) -> None:
        mouse_position = pickData["position"]
        world_position = [0, 0, 0]
        normal = [0, 0, 0]
        on_mesh = self.active_view.ConvertDisplayToPointOnSurface(
            [
                int(mouse_position["x"] / self.pixel_ratio),
                int(mouse_position["y"] / self.pixel_ratio),
            ],
            world_position,
            normal,
        )

        sphere_color = [0.0, 1.0, 0.0] if on_mesh else [1.0, 0.0, 0.0]
        self.add_sphere(world_position, sphere_color)

    def on_end_animation(self, camera_info: dict) -> None:
        # Synchronize cameras
        self.active_camera.SetPosition(camera_info.get("position"))
        self.active_camera.SetFocalPoint(camera_info.get("focalPoint"))
        self.active_camera.SetViewUp(camera_info.get("viewUp"))
        self.active_camera.SetViewAngle(camera_info.get("viewAngle"))

    @change("view_size")
    def on_view_size_change(self, view_size: dict, **kwargs):
        # Synchronize views' size
        if view_size:
            self.pixel_ratio = view_size["pixelRatio"]
            self.active_view.ViewSize = [
                int(view_size["size"]["width"]),
                int(view_size["size"]["height"]),
            ]

    def setup_ui(self) -> None:
        with SinglePageLayout(self.server) as layout:
            with (
                layout.content,
                vuetify.VContainer(fluid=True, classes="ma-0 pa-0 grey fill-height"),
                client.SizeObserver("view_size"),
            ):
                view = paraview.VtkLocalView(
                    self.active_view,
                    ref="view",
                    interactor_events=(
                        "events",
                        ["RightButtonRelease", "EndAnimation"],
                    ),
                    RightButtonRelease=(
                        self.on_right_button_release,
                        "[utils.vtk.event($event)]",
                    ),
                    EndAnimation=(
                        self.on_end_animation,
                        "[$event.pokedRenderer.getActiveCamera().get()]",
                    ),
                )
                self.ctrl.view_update = view.update


if __name__ == "__main__":
    app = Viewer()
    app.server.start()
