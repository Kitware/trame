from trame.app import get_server
from trame.widgets import vuetify3
from trame.ui.vuetify3 import SinglePageLayout

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue3")
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
                    "locale": {
                        "locale": "en",
                        "fallback": "en",
                        "messages": LANG,
                    }
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
        vuetify3.VSpacer()
        toolbar.add_child("{{ $vuetify.locale.t('title') }}")
        vuetify3.VSpacer()
        toolbar.add_child("{{ $vuetify.lang.current }}")
        vuetify3.VSpacer()
        vuetify3.VSelect(
            label=("$vuetify.locale.t('selector')",),
            v_model=("$vuetify3.locale.current",),
            items=("langs", ["en", "fr"]),
        )

    layout.content.add_child("i18n test {{ Object.keys($vuetify.locale) }}")


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
