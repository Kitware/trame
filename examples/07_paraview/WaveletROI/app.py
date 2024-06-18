from trame.app import get_server
from trame.ui.vuetify3 import SinglePageWithDrawerLayout
from trame.widgets import vuetify3 as v3, paraview as pv_widgets
from trame.decorators import TrameApp, change

from paraview import simple


@TrameApp()
class App:
    def __init__(self, server=None):
        self.server = get_server(server, client_type="vue3")

        # PV pipeline
        self.source = simple.Wavelet()
        self.extract = simple.ExtractSubset(
            Input=self.source,
            VOI=[-10, 10, -10, 10, -10, 10],
        )
        self.representation = simple.Show(self.extract)
        self.representation.SetRepresentationType("Volume")
        self.view = simple.Render()

        self._build_ui()

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    @change("i_range", "j_range", "k_range")
    def update_roi(self, i_range, j_range, k_range, **_):
        self.extract.VOI = [*i_range, *j_range, *k_range]
        self.ctrl.view_update()

    def _build_ui(self):
        with SinglePageWithDrawerLayout(self.server, full_height=True) as layout:
            with layout.drawer as drawer:
                drawer.width = 300
                with v3.VCol():
                    v3.VRangeSlider(
                        v_model=("i_range", [-10, 10]),
                        min=-10,
                        max=10,
                        step=1,
                        density="compact",
                        hide_details=True,
                    )
                    v3.VRangeSlider(
                        v_model=("j_range", [-10, 10]),
                        min=-10,
                        max=10,
                        step=1,
                        density="compact",
                        hide_details=True,
                    )
                    v3.VRangeSlider(
                        v_model=("k_range", [-10, 10]),
                        min=-10,
                        max=10,
                        step=1,
                        density="compact",
                        hide_details=True,
                    )

            with layout.content:
                with v3.VContainer(fluid=True, classes="fill-height"):
                    with pv_widgets.VtkRemoteView(
                        self.view, interactive_ratio=1
                    ) as view:
                        self.ctrl.view_update = view.update
                        self.ctrl.view_reset_camera = view.reset_camera


def main():
    app = App()
    app.server.start()


if __name__ == "__main__":
    main()
