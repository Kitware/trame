from tkinter import filedialog, Tk

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# Keep track of the currently selected directory
state.selected_dir = "None"

root = Tk()

# Ensure the tkinter main window is hidden
root.withdraw()

# Ensure that the file browser will appear in front on Windows
root.wm_attributes("-topmost", 1)


def open_directory():
    kwargs = {
        "title": "Select Directory",
    }
    dirpath = filedialog.askdirectory(**kwargs)
    if not dirpath:
        # User canceled.
        print("Canceled")
        return

    print("Selected directory:", dirpath)
    state.selected_dir = dirpath


# The controller would let us set up callback logic in a separate file
ctrl.open_directory = open_directory

# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

layout = SinglePageLayout(server)

with layout:
    # Toolbar
    with layout.toolbar as toolbar:
        toolbar.clear()

        vuetify.VSpacer()

        vuetify.VBtn("Select Directory", click=ctrl.open_directory)

        vuetify.VSpacer()

        with layout.content:
            with vuetify.VContainer() as container:
                container.add_child("Selected Directory: {{ selected_dir }}")

# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
