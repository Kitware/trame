#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "trame",
# ]
# ///
from trame.app import TrameApp
from trame.ui.html import DivLayout
from trame.widgets import html


class MultiLayout(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._build_ui()

    def _build_ui(self):
        with DivLayout(self.server) as self.ui:
            html.A("Open UI(a)", href="/?ui=a", target="_blank")
            html.Br()
            html.A("Open UI(b)", href="/?ui=b", target="_blank")

        with DivLayout(self.server, "a"):
            html.Div("UI for A")

        with DivLayout(self.server, "b"):
            html.Div("UI for B")


def main():
    app = MultiLayout()
    app.server.start()


if __name__ == "__main__":
    main()
