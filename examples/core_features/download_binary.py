from pathlib import Path
from trame.app import get_server
from trame.ui.html import DivLayout
from trame.widgets import html

BINARY_FILE = Path(__file__).parent.parent / "data/can.ex2"

server = get_server()
state, ctrl = server.state, server.controller


@ctrl.trigger("download_binary")
def download():
    return server.protocol.addAttachment(BINARY_FILE.read_bytes())


with DivLayout(server):
    html.Button(
        "Download ",
        click="utils.download('can.ex2', trigger('download_binary'), 'application/octet-stream')",
    )

if __name__ == "__main__":
    server.start()
