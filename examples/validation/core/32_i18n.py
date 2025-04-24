from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller


# -----------------------------------------------------------------------------
# i18n
# -----------------------------------------------------------------------------

LANG = {
    "en": {
        "$vuetify": {
            "title": "Hello world",
            "selector": "Language selection",
        },
    },
    "fr": {
        "$vuetify": {
            "title": "Bonjour tout le monde",
            "selector": "Langue selection",
        },
    },
}

server.enable_module(
    dict(
        vue_use=[
            (
                "trame_vuetify",
                {
                    "current": "en",
                    "locales": LANG,
                },
            )
        ]
    )
)


# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

with SinglePageLayout(server) as layout:
    # Toolbar
    with layout.toolbar as toolbar:
        vuetify.VSpacer()
        # toolbar.add_child("{{ $vuetify.lang.translator('title') }}")
        vuetify.VSpacer()
        toolbar.add_child("{{ $vuetify.lang.current }}")
        vuetify.VSpacer()
        vuetify.VSelect(
            label=("$vuetify.lang.t('selector')",),
            v_model=("$vuetify.lang.current",),
            items=("langs", ["en", "fr"]),
        )

    layout.content.add_child("i18n test {{ Object.keys($vuetify.lang.locales) }}")


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
