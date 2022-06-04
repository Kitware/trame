from trame.app import get_server
from trame.widgets import vtk, vuetify
from trame.ui.vuetify import SinglePageLayout

# -----------------------------------------------------------------------------
# trame
# -----------------------------------------------------------------------------

server = get_server(
    # log_network="/Users/sebastien.jourdain/Documents/code/open-source/Web/trame-next/test-examples/logs",
)
state, ui = server.state, server.ui

state.toolbar_version = 0

# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------


@state.change("toolbar_version")
def udpate_toolbar(toolbar_version=0, **kwargs):
    if toolbar_version == 1:
        toolbar_2()
    elif toolbar_version == 2:
        toolbar_3()
    else:
        toolbar_1()


# -----------------------------------------------------------------------------
# GUI (VirtualNodes)
# -----------------------------------------------------------------------------


def toolbar_1():
    with ui.toolbar as tb:
        tb.clear()
        tb.add_child("Toolbar 1")
        vuetify.VSpacer()
        ui.toolbar_selector()


def toolbar_2():
    with ui.toolbar as tb:
        tb.clear()
        tb.add_child("Toolbar 2")
        vuetify.VSpacer()
        ui.toolbar_selector()


def toolbar_3():
    with ui.toolbar as tb:
        tb.clear()
        tb.add_child("Toolbar 3")
        vuetify.VSpacer()
        ui.toolbar_selector()


with ui.toolbar_selector:
    with vuetify.VBtnToggle(v_model="toolbar_version"):
        with vuetify.VBtn():
            vuetify.VIcon("mdi-numeric-1-circle")
        with vuetify.VBtn():
            vuetify.VIcon("mdi-numeric-2-circle")
        with vuetify.VBtn():
            vuetify.VIcon("mdi-numeric-3-circle")


# -----------------------------------------------------------------------------
# GUI (Layout)
# -----------------------------------------------------------------------------

with SinglePageLayout(server) as layout:
    with layout.toolbar as tb:
        tb.clear()
        ui.toolbar(layout)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
