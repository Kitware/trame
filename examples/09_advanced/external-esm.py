#

from trame.app import get_server
from trame.widgets import html
from trame.ui.html import DivLayout


class ExternalJS:
    def __init__(self, server=None):
        self.server = get_server(server)

        self.server.enable_module(
            {
                "module_scripts": [
                    "https://esm.sh/canvas-confetti@1.9.3",
                ],
            }
        )
        self.ui = self._build_ui()

    def _build_ui(self):
        with DivLayout(self.server):
            html.Button("Click Me")


def main():
    app = ExternalJS()
    app.server.start()


if __name__ == "__main__":
    main()
