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
        "stepper": {
            "next": "Next",
            "prev": "Previous",
        },
    },
    "fr": {
        "stepper": {
            "next": "Suivant(me)",
            "prev": "Precedent(me)",
        },
    },
}

CONFIG = {
    "locale": {
        "locale": "en",
        "fallback": "en",
        "messages": LANG,
    }
}


# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

with SinglePageLayout(server, vuetify_config=CONFIG) as layout:
    # Toolbar
    with layout.toolbar as toolbar:
        vuetify3.VSpacer()
        vuetify3.VSelect(
            v_model=("$vuetify.locale.current",),
            items=("langs", ["en", "fr"]),
            density="compact",
        )

    with layout.content:
        with vuetify3.VStepper(
            items=("steps", ["Step 1", "Step 2", "Step 3"]),
        ):
            for i in range(3):
                with vuetify3.Template(raw_attrs=[f"v-slot:item.{i + 1}"]):
                    vuetify3.VCardTitle(title=f"Step {i + 1}")


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
