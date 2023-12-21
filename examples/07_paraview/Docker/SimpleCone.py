import paraview.web.venv  # Available in PV 5.10

from trame.app import get_server
from trame.widgets import vuetify, paraview
from trame.ui.vuetify import SinglePageLayout

from paraview import simple

# -----------------------------------------------------------------------------
# trame setup
# -----------------------------------------------------------------------------

server = get_server()
server.client_type = "vue2"
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# ParaView code
# -----------------------------------------------------------------------------

DEFAULT_RESOLUTION = 6

cone = simple.Cone()
representation = simple.Show(cone)
view = simple.Render()


@state.change("resolution")
def update_cone(resolution, **kwargs):
    cone.Resolution = resolution
    ctrl.view_update()


def update_reset_resolution():
    state.resolution = DEFAULT_RESOLUTION


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

state.trame__title = "ParaView cone"

with SinglePageLayout(server) as layout:
    layout.icon.click = ctrl.view_reset_camera
    layout.title.set_text("Cone Application")

    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VSlider(
            v_model=("resolution", DEFAULT_RESOLUTION),
            min=3,
            max=60,
            step=1,
            hide_details=True,
            dense=True,
            style="max-width: 300px",
        )
        vuetify.VDivider(vertical=True, classes="mx-2")
        with vuetify.VBtn(icon=True, click=update_reset_resolution):
            vuetify.VIcon("mdi-undo-variant")

    with layout.content:
        with vuetify.VContainer(
            fluid=True,
            classes="pa-0 fill-height",
        ):
            html_view = paraview.VtkRemoteView(view)
            # html_view = paraview.VtkLocalView(view)
            ctrl.view_update = html_view.update
            ctrl.view_reset_camera = html_view.reset_camera

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
