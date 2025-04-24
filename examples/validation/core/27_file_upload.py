from trame.app import get_server
from trame.app.file_upload import ClientFile
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify

server = get_server(client_type="vue2")

with SinglePageWithDrawerLayout(server) as layout:
    with layout.toolbar:
        vuetify.VFileInput(
            v_model=("file_exchange", None),
        )


@server.state.change("file_exchange")
def handle(file_exchange, **kwargs):
    file = ClientFile(file_exchange)
    print(file.info)


if __name__ == "__main__":
    server.start()
