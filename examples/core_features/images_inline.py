from pathlib import Path

from trame.app import get_server
from trame.assets.local import LocalFileManager
from trame.widgets import html
from trame.ui.html import DivLayout


KEYS = []
DIRECTORY = Path(__file__).parent.parent.parent / "docs/vitepress/assets/images/apps"
ASSETS = LocalFileManager(DIRECTORY)

for image in DIRECTORY.iterdir():
    key = image.stem.replace("-", "_")
    ASSETS.url(key, image.name)
    KEYS.append(key)


server = get_server()
with DivLayout(server):
    for key in KEYS:
        html.Img(src=ASSETS[key], style="width: 200px;")


if __name__ == "__main__":
    server.start()
