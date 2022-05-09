from trame.app import get_server
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

    file_name = file_exchange.get("name")
    file_size = file_exchange.get("size")
    file_time = file_exchange.get("lastModified")
    file_mime_type = file_exchange.get("type")
    file_binary_content = file_exchange.get("content")
    print(f"Got file {file_name} of size {file_size}")
    print(file_binary_content)


if __name__ == "__main__":
    server.start()
