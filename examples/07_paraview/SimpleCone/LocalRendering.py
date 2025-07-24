r"""
Installation requirements:
    pip install trame trame-vuetify trame-vtk
"""

# import paraview.web.venv  # Available in PV 5.11
from paraview import simple

from trame.app import get_server
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import paraview, vuetify3

# -----------------------------------------------------------------------------

server = get_server(client_type="vue3")
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
        vuetify3.VSpacer()
        vuetify3.VSlider(
            v_model=("resolution", DEFAULT_RESOLUTION),
            min=3,
            max=60,
            step=1,
            hide_details=True,
            density="compact",
            style="max-width: 300px",
        )
        vuetify3.VDivider(vertical=True, classes="mx-2")
        vuetify3.VBtn(icon="mdi-undo-variant", click=update_reset_resolution)

    with layout.content:
        with vuetify3.VContainer(fluid=True, classes="pa-0 fill-height"):
            html_view = paraview.VtkLocalView(view)
            ctrl.view_reset_camera = html_view.reset_camera
            ctrl.view_update = html_view.update

if __name__ == "__main__":
    server.start()
