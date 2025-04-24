# To run with Paraview
# pvpython ./examples/validation/core/23_pv_interactive_render_exit.py --venv .venv
import paraview.web.venv

# -----------------------------------------------------------------------------
# VTK
# -----------------------------------------------------------------------------
from paraview import simple

from trame.app import get_server
from trame.ui.html import DivLayout
from trame.widgets import html, paraview

DEFAULT_RESOLUTION = 8

cone = simple.Cone()
sphere = simple.Sphere()

simple.Show(cone)
simple.Show(sphere)

view = simple.Render()

# -----------------------------------------------------------------------------
# Web App setup
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller

with DivLayout(server) as layout:
    container = layout.root
    container.style = "width: 100vw; height: 100vh;"
    html_view = paraview.VtkRemoteView(view, interactive_ratio=1, interactive_quality=0)
    ctrl.view_update = html_view.update
    html.Input(
        type="range",
        min=8,
        max=1000,
        step=1,
        v_model=("resolution", 8),
        style="position: absolute; top: 20px; left: 20px; z-index: 1; width: 25%; min-width: 300px;",
    )


@state.change("resolution")
def update_resolution(resolution, **kwargs):
    cone.Resolution = int(resolution)
    sphere.PhiResolution = int(resolution)
    sphere.ThetaResolution = int(resolution)
    ctrl.view_update()


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
