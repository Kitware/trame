from pathlib import Path

from trame.app import get_server
from trame.ui.html import DivLayout
from trame.widgets import html

DIRECTORY = Path(__file__).parent.parent.parent / "docs/vitepress/assets/images/apps"

server = get_server()
server.enable_module({"serve": {"data": str(DIRECTORY.absolute())}})

with DivLayout(server):
    for file in DIRECTORY.iterdir():
        html.Img(src=f"/data/{file.name}", style="width: 200px;")


if __name__ == "__main__":
    server.start()
