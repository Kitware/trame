from pathlib import Path

from trame.app import get_server
from trame.ui.html import DivLayout

module = {
    "serve": {
        "tailwind": str(Path(__file__).parent.resolve()),
    },
    "scripts": [
        "tailwind/tailwind.js",
    ],
}

HTML_CONTENT = Path(__file__).with_name("content.html").read_text()
CLASSES = "bg-white dark:bg-gray-900 dark:before:fixed dark:before:-z-50 dark:before:inset-0 dark:before:bg-gray-950/50"


class App:
    def __init__(self, server=None, table_size=10):
        self.server = get_server(server, client_type="vue3")
        self.server.enable_module(module)
        self._build_ui()

    def _build_ui(self):
        with DivLayout(self.server) as layout:
            layout.root.classes = CLASSES
            layout.root.add_child(HTML_CONTENT)


def main():
    app = App()
    app.server.start()


if __name__ == "__main__":
    main()
