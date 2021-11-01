from trame import start, change
from trame.layouts import FullScreenPage
from trame.html import vuetify

layout = FullScreenPage("File upload")
layout.children += [
    vuetify.VFileInput(
        v_model=("file_exchange", None),
    )
]

@change("file_exchange")
def file_uploaded(file_exchange, **kwargs):
    file_name = file_exchange.get("name")
    file_size = file_exchange.get("size")
    file_time = file_exchange.get("lastModified")
    file_mime_type = file_exchange.get("type")
    file_binary_content = file_exchange.get("content")
    print(f"Go file {file_name} of size {file_size}")

if __name__ == "__main__":
    start(layout)