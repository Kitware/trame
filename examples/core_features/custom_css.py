from pathlib import Path

from trame.app import get_server
from trame.ui.html import DivLayout
from trame.widgets import client

CSS_FILE = Path(__file__).with_name("custom.css")

server = get_server()
with DivLayout(server):
    client.Style(CSS_FILE.read_text())


if __name__ == "__main__":
    server.start()
