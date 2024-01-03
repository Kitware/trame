# -----------------------------------------------------------------------------
# Dependencies (pip install): trame reloading
# Run: python ./30_reloading.py
# Test: Click on the burger icon next to "Dynamic reload" title
# -----------------------------------------------------------------------------

# DEPRECATED
# Since trame-server>=2.7.2 the hot_reload capability is now built-in
# which make that example less relevant than the 17_hot_reload.py one


from trame.app import get_server
from trame.widgets import vuetify, html
from trame.ui.vuetify import SinglePageLayout

from reloading import reloading

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

state.message = "Hello world"
state.side_effect = ""

# -----------------------------------------------------------------------------
# Dynamic reloading
# -----------------------------------------------------------------------------

IDX = 1


@ctrl.set("update_message")
def update_message():
    _update_message()


@state.change("message")
def message_change(message, **kwargs):
    _message_change(message)


@reloading
def _update_message():
    global IDX
    IDX += 1
    state.message = f"New message {IDX}"  # Edit that line


@reloading
def _message_change(message, **kwargs):
    state.side_effect = f">>> {message} <<<"  # Edit that line


# -----------------------------------------------------------------------------
# Ideally want to be able to write it like that
# -----------------------------------------------------------------------------
#
# @ctrl.set("update_message")
# @reloading
# def update_message():
#     pass
#
# @state.change("message")
# @reloading
# def message_change(message, **kwargs):
#     pass
#
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

with SinglePageLayout(server) as layout:
    layout.icon.click = ctrl.update_message
    layout.title.set_text("Dynamic reload")

    with layout.content:
        with vuetify.VContainer(fluid=True):
            with vuetify.VCol():
                with vuetify.VRow():
                    html.Div("Message", classes="pa-6 text-h6")
                    html.Div("{{ message }}", classes="pa-6")
                with vuetify.VRow():
                    html.Div("Side effect", classes="pa-6 text-h6")
                    html.Div("{{ side_effect }}", classes="pa-6")


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
