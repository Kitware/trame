from trame.app import get_server
from trame.ui.html import DivLayout
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import client, html, trame, vuetify

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

LAYOUTS = {}
state.last_line_count = 1

# -----------------------------------------------------------------------------
# Actions
# -----------------------------------------------------------------------------


def add_line(layout_name):
    layout = LAYOUTS[layout_name]
    with layout:
        with layout.content:
            html.Div(f"Line - {state.last_line_count}")
            state.last_line_count += 1


# -----------------------------------------------------------------------------
# Layouts
# -----------------------------------------------------------------------------

for name in "abcdef":
    layout = DivLayout(server, name)
    LAYOUTS[name] = layout
    with layout:
        trame.LifeCycleMonitor(name=f"{name} Layout", events=("['created']",))
        with vuetify.VCard():
            with vuetify.VCardTitle(f"Layout {name}") as title:
                vuetify.VSpacer()
                title.add_child("{{ slider_value }}")
                vuetify.VSpacer()
                with vuetify.VBtn(icon=True, click=(add_line, f"['{name}']")):
                    vuetify.VIcon("mdi-plus")
            vuetify.VDivider()
            with vuetify.VCardText():
                layout.content = vuetify.VCol()

# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

main_layout = SinglePageLayout(server)

with main_layout:
    # Validate client life cycle
    trame.LifeCycleMonitor(name="Main Layout", events=("['created']",))

    main_layout.title.set_text("Many Layouts")
    main_layout.toolbar.dense = True

    # Toolbar
    with main_layout.toolbar as toolbar:
        vuetify.VSpacer()
        vuetify.VSlider(
            v_model=("slider_value", 5),
            min=1,
            max=10,
            dense=True,
            hide_details=True,
            style="max-width: 300px;",
        )
        toolbar.add_child("{{ last_line_count }}")

    # Multi-layout
    with main_layout.content:
        with vuetify.VContainer(fluid=True):
            with vuetify.VRow():
                for key in LAYOUTS:
                    with vuetify.VCol(cols=2):
                        client.ServerTemplate(name=key, classes="pa-4")

# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
