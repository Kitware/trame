r"""
Version for trame 1.x - https://github.com/Kitware/trame/blob/release-v1/examples/howdoi/upload.py
Delta v1..v2          - https://github.com/Kitware/trame/commit/faf00108b8d4cb3f4c4babc256ee995e181bfa34
"""

from trame.app import get_server
from trame.app.file_upload import ClientFile
from trame.ui.vuetify import VAppLayout
from trame.widgets import vuetify

server = get_server(log_network="./upload-exchange.txt")
state = server.state

with VAppLayout(server):
    vuetify.VFileInput(
        v_model=("file_exchange", None),
    )


@state.change("file_exchange")
def file_uploaded(file_exchange, **kwargs):
    if file_exchange is None:
        return

    file = ClientFile(file_exchange)
    file_name = file_exchange.get("name")
    file_size = file_exchange.get("size")
    file_time = file_exchange.get("lastModified")
    file_mime_type = file_exchange.get("type")
    file_binary_content = file_exchange.get(
        "content"
    )  # can be either list(bytes, ...), or bytes
    print(file.info)
    print(type(file.content))  # will always be bytes
    # print(file_binary_content)


if __name__ == "__main__":
    server.start()
