import plotly.express as px

from trame.app import get_server
from trame.ui.router import RouterViewLayout
from trame.ui.vuetify3 import SinglePageWithDrawerLayout
from trame.widgets import plotly, router
from trame.widgets import vuetify3 as vuetify

# -----------------------------------------------------------------------------
# Charts
# -----------------------------------------------------------------------------


def scatter():
    df = px.data.iris()

    template = "plotly"
    if state.theme_mode == "dark":
        template = "plotly_dark"

    fig = px.scatter(
        df,
        x="sepal_width",
        y="sepal_length",
        color="species",
        template=template,
        title="A Plotly Express Figure",
    )

    return fig


# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
server.client_type = "vue3"
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


@state.change("theme_mode")
def update_cube_axes_visibility(**kwargs):
    ctrl.graph_update(scatter())


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

# Home route
with RouterViewLayout(server, "/"):
    with vuetify.VCard():
        vuetify.VCardTitle("This is home")
        with vuetify.VContainer(fluid=True, style="height: 600px;"):
            with vuetify.VRow(dense=True):
                vuetify.VSpacer()
                figure = plotly.Figure(
                    display_logo=False,
                    display_mode_bar="true",
                    # selected=(on_event, "['selected', utils.safe($event)]"),
                    # hover=(on_event, "['hover', utils.safe($event)]"),
                    # selecting=(on_event, "['selecting', $event]"),
                    # unhover=(on_event, "['unhover', $event]"),
                )
                ctrl.graph_update = figure.update
                vuetify.VSpacer()

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
with SinglePageWithDrawerLayout(server, theme=("theme_mode", "light")) as layout:
    layout.title.set_text("Multi-Page demo")

    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VCheckbox(
            v_model=("theme_mode", "light"),
            true_icon="mdi-lightbulb-off-outline",
            false_icon="mdi-lightbulb-outline",
            true_value="dark",
            false_value="light",
            classes="mx-1",
            hide_details=True,
            dense=True,
        )
        # vuetify.VCheckbox(
        #     v_model="$vuetify.theme.dark",
        #     color="white",
        #     change=("graph_theme", "[$event]"),
        #     on_icon="mdi-lightbulb-off-outline",
        #     off_icon="mdi-lightbulb-outline",
        #     classes="mx-1",
        #     hide_details=True,
        #     dense=True,
        # )

    with layout.content:
        with vuetify.VContainer():
            router.RouterView()

    # add router buttons to the drawer
    with layout.drawer:
        with vuetify.VList(shaped=True, v_model=("selectedRoute", 0)):
            # vuetify.VSubheader("Routes")

            with vuetify.VListItem(to="/"):
                vuetify.VIcon("mdi-home")
                vuetify.VListItemTitle("Home")

            with vuetify.VListItem(to="/foo"):
                vuetify.VIcon("mdi-food")
                vuetify.VListItemTitle("Foo")

            with vuetify.VListGroup(value=("true",), sub_group=True):
                with vuetify.Template(v_slot_activator=True):
                    vuetify.VListItemTitle("Bars")
                # with vuetify.VListItemContent():
                #     with vuetify.VListItem(v_for="id in [1]", to=("'/bar/' + id",)):
                #         # with vuetify.VListItemIcon():
                #         #     vuetify.VIcon("mdi-peanut-outline")
                #         with vuetify.VListItemContent():
                #             vuetify.VListItemTitle("Bar")
                #             vuetify.VListItemSubtitle("ID '{{id}}'")

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main():
    server.start()


if __name__ == "__main__":
    main()
