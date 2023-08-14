r"""
Version for trame 1.x - https://github.com/Kitware/trame/blob/release-v1/examples/PlainPython/Router/app.py
Delta v1..v2          - https://github.com/Kitware/trame/commit/f2ad3e65c17539315d23f5e3e981048f68b4d31e

Installation requirements:
    pip install trame trame-vuetify trame-router
"""

from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.ui.router import RouterViewLayout
from trame.widgets import vuetify, router

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

# Home route
with RouterViewLayout(server, "/"):
    with vuetify.VCard():
        vuetify.VCardTitle("This is home")

# Foo route
with RouterViewLayout(server, "/foo"):
    with vuetify.VCard():
        vuetify.VCardTitle("This is foo")
        with vuetify.VCardText():
            vuetify.VBtn("Take me back", click="$router.back()")

# Bar/id
with RouterViewLayout(server, "/bar/:id"):
    with vuetify.VCard():
        vuetify.VCardTitle("This is bar with ID '{{ $route.params.id }}'")

# Main page content
with SinglePageWithDrawerLayout(server) as layout:
    layout.title.set_text("Multi-Page demo")

    with layout.content:
        with vuetify.VContainer():
            router.RouterView()

    # add router buttons to the drawer
    with layout.drawer:
        with vuetify.VList(shaped=True, v_model=("selectedRoute", 0)):
            vuetify.VSubheader("Routes")

            with vuetify.VListItem(to="/"):
                with vuetify.VListItemIcon():
                    vuetify.VIcon("mdi-home")
                with vuetify.VListItemContent():
                    vuetify.VListItemTitle("Home")

            with vuetify.VListItem(to="/foo"):
                with vuetify.VListItemIcon():
                    vuetify.VIcon("mdi-food")
                with vuetify.VListItemContent():
                    vuetify.VListItemTitle("Foo")

            with vuetify.VListGroup(value=("true",), sub_group=True):
                with vuetify.Template(v_slot_activator=True):
                    vuetify.VListItemTitle("Bars")
                with vuetify.VListItemContent():
                    with vuetify.VListItem(v_for="id in [1,2,3]", to=("'/bar/' + id",)):
                        with vuetify.VListItemIcon():
                            vuetify.VIcon("mdi-peanut-outline")
                        with vuetify.VListItemContent():
                            vuetify.VListItemTitle("Bar")
                            vuetify.VListItemSubtitle("ID '{{id}}'")

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
