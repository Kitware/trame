# Try handle virtual env if provided
import os
import sys

if "--virtual-env" in sys.argv:
    virtualEnvPath = sys.argv[sys.argv.index("--virtual-env") + 1]
    virtualEnv = virtualEnvPath + "/bin/activate_this.py"
    exec(open(virtualEnv).read(), {"__file__": virtualEnv})

import trame as tr
from trame.html import vuetify, paraview
from trame.layouts import SinglePage

from paraview import simple

# -----------------------------------------------------------------------------
# ParaView code
# -----------------------------------------------------------------------------

layout = None


def load_data():
    # CLI
    parser = tr.get_cli_parser()
    parser.add_argument("--data", help="Path to state file", dest="data")
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

    # HTML
    html_view = paraview.VtkRemoteView(view)
    layout.content.children[0].add_child(html_view)
    layout.flush_content()


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

layout = SinglePage("State Viewer", on_ready=load_data)
layout.logo.click = "$refs.view.resetCamera()"
layout.title.set_text("ParaView State Viewer")
layout.content.add_child(vuetify.VContainer(fluid=True, classes="pa-0 fill-height"))

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
