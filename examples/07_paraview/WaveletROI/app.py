from paraview import servermanager, simple

from trame.app import get_server
from trame.decorators import TrameApp, change
from trame.ui.vuetify3 import SinglePageWithDrawerLayout
from trame.widgets import paraview as pv_widgets
from trame.widgets import vuetify3 as v3


@TrameApp()
class App:
    def __init__(self, server=None):
        self.server = get_server(server, client_type="vue3")
        self.state.volume = 0

        # Data source
        self.source = simple.Wavelet()
        self.source.UpdatePipeline()

        # Extract info
        ds = servermanager.Fetch(self.source)
        self.origin = ds.GetOrigin()
        self.spacing = ds.GetSpacing()
        self.extent = ds.GetExtent()

        # Pipeline
        self.extract = simple.ExtractSubset(
            Input=self.source,
            VOI=list(self.extent),
        )
        self.representation = simple.Show(self.extract)
        self.representation.SetRepresentationType("Volume")
        self.view = simple.Render()

        # bbox
        self.box = simple.Box()
        self.box_rep = simple.Show(self.box)
        self.box_rep.SetRepresentationType("Wireframe")

        self._build_ui()

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    @change("i_range", "j_range", "k_range")
    def update_roi(self, i_range, j_range, k_range, **_):
        # Update Volume
        self.extract.VOI = [*i_range, *j_range, *k_range]

        # Update box
        self.box.XLength = self.spacing[0] * (i_range[1] - i_range[0])
        self.box.YLength = self.spacing[1] * (j_range[1] - j_range[0])
        self.box.ZLength = self.spacing[2] * (k_range[1] - k_range[0])
        self.box.Center = [
            self.origin[0] + 0.5 * self.spacing[0] * (i_range[1] + i_range[0]),
            self.origin[1] + 0.5 * self.spacing[0] * (j_range[1] + j_range[0]),
            self.origin[2] + 0.5 * self.spacing[0] * (k_range[1] + k_range[0]),
        ]

        # Compute volume
        self.extract.UpdatePipeline()
        bounds = self.extract.GetDataInformation().GetBounds()
        self.state.volume = (
            (bounds[1] - bounds[0]) * (bounds[3] - bounds[2]) * (bounds[5] - bounds[4])
        )

        self.ctrl.view_update()

    def _build_ui(self):
        with SinglePageWithDrawerLayout(self.server, full_height=True) as layout:
            with layout.toolbar:
                v3.VLabel(
                    "Extent [{{i_range.join(', ')}}, {{j_range.join(', ')}}, {{k_range.join(', ')}}]"
                    " - Volume: {{ volume }}",
                    classes="mx-2",
                )
                v3.VBtn(icon="mdi-crop-free", click=self.ctrl.view_reset_camera)
            with layout.drawer as drawer:
                drawer.width = 300
                with v3.VCol():
                    v3.VRangeSlider(
                        v_model=("i_range", self.extent[0:2]),
                        min=-10,
                        max=10,
                        step=1,
                        density="compact",
                        hide_details=True,
                    )
                    v3.VRangeSlider(
                        v_model=("j_range", self.extent[2:4]),
                        min=-10,
                        max=10,
                        step=1,
                        density="compact",
                        hide_details=True,
                    )
                    v3.VRangeSlider(
                        v_model=("k_range", self.extent[4:]),
                        min=-10,
                        max=10,
                        step=1,
                        density="compact",
                        hide_details=True,
                    )

            with layout.content:
                with v3.VContainer(fluid=True, classes="fill-height pa-0"):
                    with pv_widgets.VtkRemoteView(
                        self.view,
                        interactive_ratio=1,
                    ) as view:
                        self.ctrl.view_update = view.update
                        self.ctrl.view_reset_camera = view.reset_camera


def main():
    app = App()
    app.server.start()


if __name__ == "__main__":
    main()
