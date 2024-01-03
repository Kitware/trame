r"""
Installation requirements:
    pip install trame trame-vuetify trame-markdown
"""

import os
from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import markdown, vuetify

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Read markdown file
# -----------------------------------------------------------------------------


@state.change("file_name")
def update_md(file_name, **kwargs):
    md_file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(md_file_path, encoding="utf-8") as md:
        ctrl.md_update(md.read())


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

state.trame__title = "MD Viewer"

with SinglePageLayout(server) as layout:
    layout.title.set_text("Markdown Viewer")

    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VSelect(
            v_model=("file_name", "demo.md"),
            items=("options", ["demo.md", "sample.md", "module.md"]),
            hide_details=True,
            dense=True,
        )

    with layout.content:
        md = markdown.Markdown(classes="pa-4 mx-2")
        ctrl.md_update = md.update


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
