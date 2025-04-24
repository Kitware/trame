import time

from trame.app import get_server
from trame.ui.html import DivLayout
from trame.widgets import html

server = get_server()
state, ctrl = server.state, server.controller

state.other_txt_content = "Some content to download..."


@ctrl.trigger("download_content")
def generate_content():
    return f"Hello on the server is {time.time()}"


with DivLayout(server):
    html.Button(
        "Download from method",
        click="utils.download('method.txt', trigger('download_content'), 'text/plain')",
    )
    html.Button(
        "Download from state",
        click="utils.download('state.txt', other_txt_content, 'text/plain')",
    )

if __name__ == "__main__":
    server.start()
