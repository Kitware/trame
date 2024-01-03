from trame.app import get_server
from trame.widgets import vtk, trame, vuetify
from trame.ui.vuetify import SinglePageLayout

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller


def reset_resolution():
    state.resolution = 6


# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

layout = SinglePageLayout(server)

with layout:
    # Validate client life cycle
    trame.LifeCycleMonitor(events=("['created']",))

    layout.icon.click = ctrl.reset_camera
    layout.title.set_text("Cone")
    layout.toolbar.dense = True

    # Toolbar
    with layout.toolbar as toolbar:
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
        with vuetify.VBtn(icon=True, click=reset_resolution):
            vuetify.VIcon("mdi-undo")

    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            with vtk.VtkView() as view:
                ctrl.reset_camera = view.reset_camera
                with vtk.VtkGeometryRepresentation():
                    vtk.VtkAlgorithm(
                        vtk_class="vtkConeSource", state=("{ resolution }",)
                    )


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
