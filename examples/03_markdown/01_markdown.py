r"""
Installation requirements:
    pip install trame trame-vuetify trame-markdown
"""

import os

from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import markdown
from trame.widgets import vuetify3 as v3
from trame.decorators import change

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------


class MarkdownApp(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._build_ui()

    # -----------------------------------------------------------------------------
    # Read markdown file
    # -----------------------------------------------------------------------------

    @change("file_name")
    def update_md(self, file_name, **kwargs):
        md_file_path = os.path.join(os.path.dirname(__file__), file_name)
        with open(md_file_path, encoding="utf-8") as md:
            self.ctrl.md_update(md.read())

    # -----------------------------------------------------------------------------
    # GUI
    # -----------------------------------------------------------------------------

    def _build_ui(self):
        self.state.trame__title = "MD Viewer"

        with SinglePageLayout(self.server) as self.ui:
            self.ui.title.set_text("Markdown Viewer")

            with self.ui.toolbar:
                v3.VSpacer()
                v3.VSelect(
                    v_model=("file_name", "demo.md"),
                    items=("options", ["demo.md", "sample.md", "module.md"]),
                    hide_details=True,
                    dense=True,
                )

            with self.ui.content:
                md = markdown.Markdown(classes="pa-4 mx-2")
                self.ctrl.md_update = md.update


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main():
    mdApp = MarkdownApp()
    mdApp.server.start()


if __name__ == "__main__":
    main()
