r"""
Installation requirements:
    pip install trame trame-vuetify trame-vtk
"""

import paraview.web.venv  # Available in PV 5.11
from paraview import simple

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import paraview, vuetify

# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller
state.trame__title = "ParaView cone"

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
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            html_view = paraview.VtkRemoteView(view, ref="view")
            ctrl.view_reset_camera = html_view.reset_camera
            ctrl.view_update = html_view.update

if __name__ == "__main__":
    server.start()
