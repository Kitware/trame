#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "trame",
# ]
# ///
import time

from trame.app import TrameApp
from trame.ui.html import DivLayout
from trame.widgets import html


class ReservedState(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._count = 1
        self._build_ui()

    def make_server_busy(self):
        time.sleep(1)

    def update_title(self):
        self.state.trame__title = f"T({self._count})"
        self._count += 1

    def update_favicon(self):
        self.state.trame__favicon = f"https://picsum.photos/id/{self._count}/32/32"
        self._count += 10

    def _build_ui(self):
        with DivLayout(self.server) as self.ui:
            html.Div("trame__busy: {{ trame__busy }}")
            html.Button("Make server busy", click=self.make_server_busy)
            html.Button("Update title", click=self.update_title)
            html.Button("Update favicon", click=self.update_favicon)


def main():
    app = ReservedState()
    app.server.start()


if __name__ == "__main__":
    main()
