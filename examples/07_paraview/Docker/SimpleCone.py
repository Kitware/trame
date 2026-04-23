from paraview import simple

from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3 as v3, paraview
from trame.decorators import change

# -----------------------------------------------------------------------------
# ParaView code
# -----------------------------------------------------------------------------

DEFAULT_RESOLUTION = 6

cone = simple.Cone()
representation = simple.Show(cone)
view = simple.Render()

# -----------------------------------------------------------------------------
# trame setup
# -----------------------------------------------------------------------------


class SimpleCone(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._build_ui()

    @change("resolution")
    def update_cone(self, resolution, **kwargs):
        cone.Resolution = resolution
        self.ctrl.view_update()

    def update_reset_resolution(self):
        self.state.resolution = DEFAULT_RESOLUTION

    # -----------------------------------------------------------------------------
    # GUI
    # -----------------------------------------------------------------------------

    def _build_ui(self):
        self.state.trame__title = "ParaView cone"

        with SinglePageLayout(self.server) as self.ui:
            self.ui.icon.click = self.ctrl.view_reset_camera
            self.ui.title.set_text("Cone Application")

            with self.ui.toolbar:
                v3.VSpacer()
                v3.VSlider(
                    v_model=("resolution", DEFAULT_RESOLUTION),
                    min=3,
                    max=60,
                    step=1,
                    hide_details=True,
                    dense=True,
                    style="max-width: 300px",
                )
                v3.VDivider(vertical=True, classes="mx-2")
                with v3.VBtn(icon=True, click=self.update_reset_resolution):
                    v3.VIcon("mdi-undo-variant")

            with self.ui.content:
                with v3.VContainer(
                    fluid=True,
                    classes="pa-0 fill-height",
                ):
                    html_view = paraview.VtkRemoteView(view)
                    # html_view = paraview.VtkLocalView(view)
                    self.ctrl.view_update = html_view.update
                    self.ctrl.view_reset_camera = html_view.reset_camera


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main():
    app = SimpleCone()
    app.server.start()


if __name__ == "__main__":
    main()
