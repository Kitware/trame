#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "trame",
#     "trame-vuetify",
# ]
# ///
import time

from trame.app import TrameApp
from trame.decorators import trigger
from trame.ui.html import DivLayout
from trame.widgets import html


class DownloadText(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._build_ui()
        self.state.other_txt_content = "Some content to download..."

    @trigger("download_content")
    def generate_content(self):
        return f"Hello on the server is {time.time()}"

    def _build_ui(self):
        with DivLayout(self.server) as self.ui:
            html.Button(
                "Download from method",
                click="utils.download('method.txt', trigger('download_content'), 'text/plain')",
            )
            html.Button(
                "Download from state",
                click="utils.download('state.txt', other_txt_content, 'text/plain')",
            )


def main():
    app = DownloadText()
    app.server.start()


if __name__ == "__main__":
    main()
