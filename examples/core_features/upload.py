from trame.app import get_server
from trame.ui.html import DivLayout
from trame.widgets import html
from trame.app.file_upload import ClientFile

server = get_server()


def upload(files):
    for file in files:
        file_helper = ClientFile(file)
        print(file_helper.info)


with DivLayout(server) as a:
    html.Input(
        type="file",
        multiple=True,
        change=(upload, "[$event.target.files]"),
        __events=["change"],
    )


if __name__ == "__main__":
    server.start()
