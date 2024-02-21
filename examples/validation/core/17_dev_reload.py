import sys
from trame.app import get_server, dev
from trame.widgets import vtk, vuetify
from trame.ui.vuetify import SinglePageLayout
from trame_server import Server

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller


def reset_resolution():
    state.resolution = 6


# Mode A ----------------------------------------------------------------------
def full_reload(server: Server):
    print("=> Reload mode A")
    dev.remove_change_listeners(server, "resolution")
    dev.reload(sys.modules.get("__main__"))


# Mode B ----------------------------------------------------------------------
def reload_app(server: Server):
    print("=> Reload mode B")
    # dev.clear_triggers(app) # Not needed here
    dev.clear_change_listeners(server)
    dev.reload(sys.modules.get("__main__"))


# Reload mode selector --------------------------------------------------------
ctrl.on_server_reload = ctrl.on_server_reload.clear  # Will happen first

if True:
    ctrl.on_server_reload.add(reload_app)
else:
    ctrl.on_server_reload.add(full_reload)


@state.change("resolution")
def update_resolution(resolution, **kwargs):
    print("Update resolution", resolution)


# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

layout = SinglePageLayout(server)

with layout:
    layout.title.set_text("Dynamic reload")
    layout.toolbar.dense = True

    # Toolbar
    with layout.toolbar as toolbar:
        vuetify.VSpacer()
        vuetify.VSlider(
            # label="hello", # comment/uncomment between reload
            hide_details=True,
            v_model=("resolution", 6),
            max=60,
            min=3,
            step=1,
            style="max-width: 300px;",
        )
        vuetify.VSwitch(
            hide_details=True,
            v_model=("$vuetify.theme.dark",),
        )
        with vuetify.VBtn(icon=True, click=reset_resolution):
            vuetify.VIcon("mdi-undo")

    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            with vtk.VtkView() as view:
                ctrl.reset_camera = view.reset_camera
                with vtk.VtkGeometryRepresentation():
                    vtk.VtkAlgorithm(
                        vtk_class="vtkConeSource", state=("{ resolution }",)
                    )


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__" and not server.running:
    server.start()
