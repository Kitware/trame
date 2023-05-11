from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, vtk as vtk_widgets


class Cone:
    def __init__(self, server=None):
        if server is None:
            server = get_server()

        if isinstance(server, str):
            server = get_server(server)

        self._server = server
        self.ui()

    @property
    def server(self):
        return self._server

    @property
    def ctrl(self):
        return self.server.controller

    @property
    def state(self):
        return self.server.state

    def ui(self):
        with SinglePageLayout(self.server) as layout:
            with layout.content:
                with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                    with vtk_widgets.VtkView() as view:
                        self.ctrl.view_reset_camera = view.reset_camera
                        with vtk_widgets.VtkGeometryRepresentation():
                            vtk_widgets.VtkAlgorithm(
                                vtk_class="vtkConeSource",
                                state=("{ resolution }",),
                            )

            with layout.toolbar:
                vuetify.VSpacer()
                vuetify.VSlider(
                    v_model=("resolution", 6),
                    min=3,
                    max=60,
                    step=1,
                    hide_details=True,
                    style="max-width: 300px;",
                )
                with vuetify.VBtn(icon=True, click=self.ctrl.view_reset_camera):
                    vuetify.VIcon("mdi-crop-free")


def show_in_jupyter(server=None, **kwargs):
    from trame.app.jupyter import show

    cone = Cone(server)
    show(cone.server, **kwargs)


def main(**kwargs):
    cone = Cone()
    cone.server.start(**kwargs)


if __name__ == "__main__":
    main()
