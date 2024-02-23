import os
from trame.app import get_server
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import trame, vuetify3

server = get_server()
server.client_type = os.environ.get("VUE_VERSION", "vue3")

FILE_LISTING = [
    {
        "text": "Hello.txt",
        "value": "hello.txt",
        "type": "File",
        "prependIcon": "mdi-file-document-outline",
    }
]

PATH_HIERARCHY = []

server.state["menu_items"] = ["one", "two", "three"]


def on_click(e):
    print(e)


def load_data(entry, item):
    print(entry, item)


with SinglePageLayout(server) as layout:
    layout.title.set_text("List Browser")
    with layout.content:
        trame.ListBrowser(
            style="position: relative",
            classes="pa-8",
            location=("[100, 100]",),
            handle_position="bottom",
            filter=True,
            list=("listing", FILE_LISTING),
            path=("path", PATH_HIERARCHY),
            click=(on_click, "[$event]"),
            contextmenu="""
                    $event.preventDefault();
                    menuX = $event.clientX;
                    menuY = $event.clientY;
                    menuShow = $event.srcElement.textContent;
                 """,
        )
        with vuetify3.VMenu(
            v_model=("menuShow", False),
            style=("{ position: 'absolute', left: `${menuX}px`, top: `${menuY}px`}",),
        ) as menu:
            with vuetify3.VList():
                with vuetify3.VListItem(
                    v_for="(item, i) in menu_items",
                    key="i",
                    value=["item"],
                ):
                    vuetify3.VBtn(
                        "{{ item }}",
                        click=(load_data, "[menuShow, item]"),
                    )


if __name__ == "__main__":
    server.start()
