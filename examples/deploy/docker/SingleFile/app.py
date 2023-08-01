from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, vtk as vtk_widgets

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
server.client_type = "vue2"
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Web App setup
# -----------------------------------------------------------------------------

state.trame__title = "VTK Rendering"

with SinglePageLayout(server) as layout:
    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            with vtk_widgets.VtkView(ref="view"):
                with vtk_widgets.VtkGeometryRepresentation():
                    vtk_widgets.VtkAlgorithm(
                        vtk_class="vtkConeSource", state=("{ resolution }",)
                    )

    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VSlider(
            hide_details=True,
            v_model=("resolution", 6),
            max=60,
            min=3,
            step=1,
            style="max-width: 300px;",
        )
        vuetify.VSwitch(
            hide_details=True,
            v_model=("$vuetify.theme.dark",),
        )
        with vuetify.VBtn(icon=True, click="$refs.view.resetCamera()"):
            vuetify.VIcon("mdi-crop-free")

if __name__ == "__main__":
    server.start()
