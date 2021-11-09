import os
from trame import change, update_state
from trame.layouts import SinglePage
from trame.html.markdown import Markdown
from trame.html.vuetify import VSelect, VSpacer

# -----------------------------------------------------------------------------
# Read markdown file
# -----------------------------------------------------------------------------


@change("file_name")
def update_md(file_name, **kwargs):
    md_file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(md_file_path) as md:
        update_state("md", md.read())


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

layout = SinglePage("MD Viewer", on_ready=update_md)
layout.title.content = "Markdown Viewer"
layout.toolbar.children += [
    VSpacer(),
    VSelect(
        v_model=("file_name", "demo.md"),
        items=("options", ["demo.md", "sample.md", "module.md"]),
        hide_details=True,
        dense=True,
    ),
]
layout.content.children += [
    Markdown(
        classes="pa-4 mx-2",
        v_model=("md",),
    ),
]

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
