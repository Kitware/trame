#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "trame",
#     "trame-vuetify",
# ]
# ///
from pathlib import Path

from trame.app import TrameApp
from trame.decorators import trigger
from trame.ui.html import DivLayout
from trame.widgets import html

BINARY_FILE = Path(__file__).parent.parent / "data/can.ex2"


class DownloadBinary(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._build_ui()

    def _build_ui(self):
        with DivLayout(self.server):
            html.Button(
                "Download ",
                click="utils.download('can.ex2', trigger('download_binary'), 'application/octet-stream')",
            )

    @trigger("download_binary")
    def download(self):
        return BINARY_FILE.read_bytes()


def main():
    app = DownloadBinary()
    app.server.start()


if __name__ == "__main__":
    main()
