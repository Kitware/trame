import os
from trame import state
from trame.layouts import SinglePage
from trame.html import markdown, vuetify

# -----------------------------------------------------------------------------
# Read markdown file
# -----------------------------------------------------------------------------


@state.change("file_name")
def update_md(file_name, **kwargs):
    md_file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(md_file_path) as md:
        state.md = md.read()


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

layout = SinglePage("MD Viewer", on_ready=update_md)
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
    markdown.Markdown(
        classes="pa-4 mx-2",
        v_model=("md",),
    )


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
