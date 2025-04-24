from trame.app import get_server
from trame.assets.local import LocalFileManager
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import html, vuetify

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

favicons = LocalFileManager(__file__)
favicons.url("open", "./data/fileopen.png")
favicons.url("filter", "./data/filter.png")
favicons.url("kitware", "./data/kw.png")
favicons.url("paraview_mac", "./data/pv_icon.png")
favicons.url("paraview", "./data/pv.png")

_idx = 0
OPTIONS = [*favicons.assets]


def random_update():
    global _idx
    _idx = (_idx + 1) % len(OPTIONS)
    name = OPTIONS[_idx]
    state.favicon = name
    state.trame__title = name


@state.change("favicon")
def update_favicon(favicon, **kwargs):
    state.trame__favicon = favicons[favicon]


# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

layout = SinglePageLayout(server)

with layout:
    layout.title.set_text("Title favicon")

    # Toolbar
    with layout.toolbar as toolbar:
        vuetify.VSpacer()
        vuetify.VSelect(
            label="favicon",
            v_model=("favicon", None),
            items=(
                "favicon_items",
                [{"text": value, "value": value} for value in favicons.assets.keys()],
            ),
            style="max-width: 200px;",
            dense=True,
            hide_details=True,
            classes="mx-4",
        )
        with html.Div(style="width: 200px;", classes="mx-4"):
            vuetify.VTextField(
                label="Title",
                v_model="trame__title",
                dense=True,
                hide_details=True,
            )
        with vuetify.VBtn(icon=True, click=random_update):
            vuetify.VIcon("mdi-refresh")


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
