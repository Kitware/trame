#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "trame>=3.12",
#     "trame-vtklocal",
#     "trame-rca",
#     "trame-vuetify",
#     "vtk>=9.6",
#  ]
#
# [tool.uv]
# prerelease = "allow"
#
# [[tool.uv.index]]
# url = "https://wheels.vtk.org"
# ///
import vtk

from trame.app import TrameApp
from trame.decorators import change
from trame.ui.vuetify3 import VAppLayout
from trame.ui.html import DivLayout
from trame.widgets import rca, vtklocal, client
from trame.widgets import vuetify3 as v3

OVERLAY = "position:absolute;top:1rem;left:1rem;z-index:10;"


class ClientRemoteRendering(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._setup_vtk()
        self._build_ui()

    def _setup_vtk(self):
        renderer = vtk.vtkRenderer()
        render_window = vtk.vtkRenderWindow()
        render_window.AddRenderer(renderer)
        render_window.OffScreenRenderingOn()

        render_window_interactor = vtk.vtkRenderWindowInteractor()
        render_window_interactor.SetRenderWindow(render_window)
        render_window_interactor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

        cone_source = vtk.vtkConeSource()
        mapper = vtk.vtkPolyDataMapper()
        actor = vtk.vtkActor()
        mapper.SetInputConnection(cone_source.GetOutputPort())
        actor.SetMapper(mapper)
        renderer.AddActor(actor)
        renderer.ResetCamera()
        render_window.Render()

        self.render_window = render_window
        self.cone = cone_source

    def _build_ui(self):
        # WASM Rendering
        self.state.setdefault("local_camera", {})
        with DivLayout(self.server, template_name="local", classes="h-100"):
            vtklocal.LocalView(
                self.render_window,
                ctx_name="local",
                throttle_rate=20,
                camera="local_camera = $event",
                ref="wasm",  # to allow JS method call
            )
            # -----------------------------------------------------------------
            # vtk 9.6 seems to have a sizing issue with WASM which I tried to
            # fix by calling a resize() locally but that didn't help.
            # -----------------------------------------------------------------
            # client.ClientTriggers(mounted="utils.get('Vue').nextTick(trame.refs.wasm.resize)")
            # -----------------------------------------------------------------

        # Remote Rendering
        with DivLayout(self.server, template_name="remote", classes="h-100"):
            view = rca.RemoteControlledArea(display="image")
            self.ctx.remote = view.create_view_handler(
                self.render_window, encoder="turbo-jpeg"
            )

        # Main UI
        with VAppLayout(self.server) as self.ui:
            # Switch between rendering UI
            client.ServerTemplate(name=("rendering_mode", "local"))

            # Controller UI
            with v3.VCard(style=OVERLAY, classes="pa-2"):
                with v3.VBtnToggle(
                    v_model="rendering_mode",
                    group=True,
                    mandatory=True,
                    density="compact",
                ):
                    for name in ["Local", "Remote"]:
                        v3.VBtn(
                            text=name,
                            value=name.lower(),
                            density="compact",
                            classes="text-none",
                        )

                v3.VSlider(
                    v_model=("resolution", 6),
                    min=3,
                    max=30,
                    step=1,
                    hide_details=True,
                    density="comfortable",
                )

    @change("resolution", "rendering_mode")
    def _on_resolution(self, resolution, rendering_mode, **_):
        self.cone.resolution = resolution
        self.ctx[rendering_mode].update()

    @change("local_camera")
    def _on_camera_sync(self, local_camera, **_):
        if local_camera:
            self.ctx.local.vtk_update_from_state(local_camera)


def main():
    app = ClientRemoteRendering()
    app.server.start()


if __name__ == "__main__":
    main()
