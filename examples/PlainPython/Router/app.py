from trame.layouts import SinglePageWithDrawer
from trame.html import Template, vuetify, router

layout = SinglePageWithDrawer("Multi-Page demo")
layout.title.set_text("Multi-Page demo")

# There are two ways to register a route
home_template = vuetify.VCard()
with home_template:
    vuetify.VCardTitle("This is home")

foo_template = vuetify.VCard()
with foo_template:
    vuetify.VCardTitle("This is foo")
    with vuetify.VCardText():
        vuetify.VBtn("Take me back", click="$router.back()")

# You can add a route with add_route
layout.add_route("home", "/", home_template)
layout.add_route("foo", "/foo", foo_template)

# or use the contextmanager 'with_route'
with layout.with_route("bar", "/bar/:id", vuetify.VCard()):
    vuetify.VCardTitle("This is bar with ID '{{ $route.params.id }}'")

# add <router-view />
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
            with Template(v_slot_activator=True):
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
    layout.start()
