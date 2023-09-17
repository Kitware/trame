from tkinter import filedialog, Tk

from trame.app import get_server
from trame.ui.html import DivLayout
from trame.widgets import html

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller

# Keep track of the currently selected directory
state.selected_dir = None

root = Tk()

# Ensure the tkinter main window is hidden
root.withdraw()

# Ensure that the file browser will appear in front on Windows
root.wm_attributes("-topmost", 1)


@ctrl.set("open_directory")
def open_directory():
    kwargs = {
        "title": "Select Directory",
    }
    state.selected_dir = filedialog.askdirectory(**kwargs)


# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

with DivLayout(server):
    html.Button("Select Directory", click=ctrl.open_directory)
    html.Div("{{ selected_dir }}")

# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
