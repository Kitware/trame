r"""
Installation requirements:
    pip install trame trame-vuetify trame-vtk
"""

import paraview.web.venv
from paraview import simple

from pathlib import Path
from trame.app import get_server
from trame.widgets import vuetify, paraview, client
from trame.ui.vuetify import SinglePageLayout

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller
state.trame__title = "State Viewer"

# Preload paraview modules onto server
paraview.initialize(server)

# -----------------------------------------------------------------------------
# ParaView code
# -----------------------------------------------------------------------------


@ctrl.add("on_server_ready")
def load_data(**kwargs):
    # CLI
    args, _ = server.cli.parse_known_args()

    full_path = str(Path(args.data).resolve().absolute())
    working_directory = str(Path(args.data).parent.resolve().absolute())

    # ParaView
    simple.LoadState(
        full_path,
        data_directory=working_directory,
        restrict_to_data_directory=True,
    )
    view = simple.GetActiveView()
    view.MakeRenderWindowInteractor(True)
    simple.Render(view)

    # HTML
    with SinglePageLayout(server) as layout:
        layout.icon.click = ctrl.view_reset_camera
        layout.title.set_text("ParaView State Viewer")

        with layout.content:
            with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                html_view = paraview.VtkRemoteView(view)
                ctrl.view_reset_camera = html_view.reset_camera
                ctrl.view_update = html_view.update


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

with SinglePageLayout(server) as layout:
    layout.icon.click = ctrl.view_reset_camera
    layout.title.set_text("ParaView State Viewer")

    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            client.Loading("Loading state")


if __name__ == "__main__":
    server.cli.add_argument("--data", help="Path to state file", dest="data")
    server.start()
