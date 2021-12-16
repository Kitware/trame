r"""
###########################################################
###                 Not working yet                     ###
###########################################################

=> multiprocessing inside pvpython seems to be broken
   but should work inside plain Python if well configured
"""
from paraview.web import venv  # Available in PV 5.10-RC2+

import os
import webview
import trame as tr
from trame.html import vuetify, paraview, VTKLoading
from trame.layouts import SinglePage

from paraview import simple

# -----------------------------------------------------------------------------
# ParaView code
# -----------------------------------------------------------------------------

layout = None


def load_data(full_path):
    full_path = os.path.abspath(full_path)
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

layout = SinglePage("State Viewer")
layout.logo.click = "$refs.view.resetCamera()"
layout.title.set_text("ParaView State Viewer")
layout.content.add_child(
    vuetify.VContainer(
        VTKLoading("Loading state"), fluid=True, classes="pa-0 fill-height"
    )
)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def process_msg(msg):
    if msg[0] == "file_dialog":
        load_data(msg[1][0])


if __name__ == "__main__":
    layout.start_desktop_window(
        on_msg=process_msg,
        on_top=True,
        confirm_close=False,
        file_dialog={
            "dialog_type": webview.OPEN_DIALOG,
            "allow_multiple": False,
            "file_types": ("ParaView State File (*.pvsm)", "All files (*.*)"),
        },
    )
