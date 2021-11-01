from trame import start
from trame.layouts import SinglePage
import trame.html.vuetify as vuetify

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

layout = SinglePage("Vuetify Storybook")
layout.title.content = "List of Vuetify components"

excluded = ["AbstractElement", "VApp", "VNavigationDrawer", "VDialog", "VOverlay"]
all_vuetify_exports = vuetify.__dict__.items()
for (name, component) in all_vuetify_exports:
    if isinstance(component, type) and name not in excluded:
        layout.content.children += [
            vuetify.VCard(
                [vuetify.VCardTitle(name), vuetify.VCardText(component())],
                classes="mx-2",
            )
        ]

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    start(layout)
