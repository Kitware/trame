# -----------------------------------------------------------------------------
# trame
# -----------------------------------------------------------------------------
from trame.app import get_server
from trame.widgets import html

CLIENT_TYPE = "vue3"

if CLIENT_TYPE == "vue2":
    from trame.widgets import vuetify2 as vuetify
    from trame.ui.vuetify2 import SinglePageLayout
else:
    from trame.widgets import vuetify3 as vuetify
    from trame.ui.vuetify3 import SinglePageLayout

server = get_server()
server.client_type = CLIENT_TYPE

state, ui = server.state, server.ui  # ui is an instance of VirtualNodeManager


def my_component(name):
    """Emulate a component that is discovered at runtime"""
    vname = f"my_comp_val_{name}"
    with state:  # Force to update state before template
        state.setdefault(vname, 0)
    html.Div(name)
    vuetify.VBtn("{{" + vname + "}}", click=f"{vname}++")


def udpate_content():
    with ui.customizable_slot.clear():
        my_component(state.demanded_name)


# -----------------------------------------------------------------------------
# GUI (Layout)
# -----------------------------------------------------------------------------

# virtualnodes added to layout
with SinglePageLayout(server) as layout:
    with layout.content as content:
        content.clear()
        vuetify.VTextField(v_model=("demanded_name", "init"))
        vuetify.VBtn("update content", click=udpate_content)
        with html.Div():
            ui.customizable_slot(layout)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start(open_browser=False)
