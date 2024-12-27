r"""
Installation requirements:
    pip install trame trame-vuetify trame-vtk
"""

from trame.app import get_server
from trame.decorators import TrameApp, change
from trame.widgets import (
    vuetify3 as v3,
    paraview as pv_widgets,
)
from trame.ui.vuetify3 import SinglePageLayout

from paraview import simple

# -----------------------------------------------------------------------------


@TrameApp()
class ConeApp:
    def __init__(self, server=None):
        # ParaView
        self.cone = simple.Cone()
        self.representation = simple.Show(self.cone)
        self.view = simple.Render()

        # Trame setup
        self.server = get_server(server, client_type="vue3")
        self.state.trame__title = "ParaView - Cone"
        self.ui = self._build_ui()

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    @change("resolution")
    def on_resolution_change(self, resolution, **_):
        self.cone.Resolution = resolution
        self.ctrl.view_update()

    def reset_resolution(self):
        self.state.resolution = 6

    def _build_ui(self):
        with SinglePageLayout(self.server, full_height=True) as layout:
            layout.icon.click = self.ctrl.view_reset_camera
            layout.title.set_text("ParaView - Cone")

            with layout.toolbar:
                v3.VSpacer()
                v3.VSlider(
                    v_model=("resolution", 6),
                    min=3,
                    max=60,
                    step=1,
                    hide_details=True,
                    dense=True,
                    style="max-width: 300px",
                )
                v3.VDivider(vertical=True, classes="mx-2")
                with v3.VBtn(icon=True, click=self.reset_resolution):
                    v3.VIcon("mdi-undo-variant")

            with layout.content:
                with v3.VContainer(fluid=True, classes="pa-0 fill-height"):
                    html_view = pv_widgets.VtkRemoteView(self.view, interactive_ratio=1)
                    self.ctrl.view_reset_camera = html_view.reset_camera
                    self.ctrl.view_update = html_view.update

            return layout


# -----------------------------------------------------------------------------


def main(**kwargs):
    app = ConeApp()
    app.server.start(**kwargs)


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
