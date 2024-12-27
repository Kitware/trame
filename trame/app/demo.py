from trame.app import get_server
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3 as v3, vtk as vtk_widgets


class Cone:
    def __init__(self, server_or_name=None):
        self.server = get_server(server_or_name)
        self.ui = self._generate_ui()

    @property
    def ctrl(self):
        return self.server.controller

    @property
    def state(self):
        return self.server.state

    @property
    def resolution(self):
        return self.state.resolution

    @resolution.setter
    def resolution(self, v):
        with self.state:
            self.state.resolution = v

    def reset_resolution(self):
        self.resolution = 6

    def _generate_ui(self):
        with SinglePageLayout(self.server) as layout:
            layout.title.set_text("Trame demo")
            with layout.toolbar as toolbar:
                toolbar.dense = True
                v3.VSpacer()
                v3.VSlider(
                    v_model=("resolution", 6),
                    min=3,
                    max=60,
                    step=1,
                    hide_details=True,
                    style="max-width: 300px;",
                )
                with v3.VBtn(icon=True, click=self.reset_resolution):
                    v3.VIcon("mdi-lock-reset")
                with v3.VBtn(
                    icon=True,
                    click=self.ctrl.view_reset_camera,
                ):
                    v3.VIcon("mdi-crop-free")

            with layout.content:
                with v3.VContainer(fluid=True, classes="pa-0 fill-height"):
                    with vtk_widgets.VtkView() as view:
                        self.ctrl.view_reset_camera = view.reset_camera
                        with vtk_widgets.VtkGeometryRepresentation():
                            vtk_widgets.VtkAlgorithm(
                                vtk_class="vtkConeSource",
                                state=("{ resolution }",),
                            )

            return layout


def main(**kwargs):
    cone = Cone()
    cone.server.start(**kwargs)


if __name__ == "__main__":
    main()
