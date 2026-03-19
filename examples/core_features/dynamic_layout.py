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


class DynamicLayout(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self.line_count = 1
        self._build_ui()

    def add_line(self):
        with self.ui:
            html.Div(f"Line: {self.line_count}")
        self.line_count += 1

    def update_first_line(self):
        with self.server.ui.first_line:
            self.server.ui.first_line.clear()
            html.Div(f"First line: {self.line_count}")
            self.line_count += 1

    def _build_ui(self):
        with DivLayout(self.server) as self.ui:
            self.server.ui.first_line(self.ui)  # Insert place holder

            html.Button("Add line", click=self.add_line)
            html.Button("Update first line", click=self.update_first_line)


def main():
    app = DynamicLayout()
    app.server.start()


if __name__ == "__main__":
    main()
