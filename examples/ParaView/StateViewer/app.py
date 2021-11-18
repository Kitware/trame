from paraview.web import venv # Available in PV 5.10-RC2+

import os
import trame as tr
from trame.html import vuetify, paraview, VTKLoading
from trame.layouts import SinglePage

from paraview import simple

# -----------------------------------------------------------------------------
# ParaView code
# -----------------------------------------------------------------------------

parser = tr.get_cli_parser()
layout = None

def load_data(**kwargs):
    # CLI
    args, _ = parser.parse_known_args()

    full_path = os.path.abspath(args.data)
    working_directory = os.path.dirname(full_path)

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
    html_view = paraview.VtkRemoteView(view)
    layout.content.children[0].children[0] = html_view
    layout.flush_content()

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

layout = SinglePage("State Viewer", on_ready=load_data)
layout.logo.click = "$refs.view.resetCamera()"
layout.title.set_text("ParaView State Viewer")
layout.content.add_child(vuetify.VContainer(VTKLoading("Loading state"), fluid=True, classes="pa-0 fill-height"))

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    parser.add_argument("--data", help="Path to state file", dest="data")
    layout.start()
