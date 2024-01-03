r"""
Installation requirements:
    pip install trame trame-vuetify trame-components
"""

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import trame

server = get_server(client_type="vue2")

with SinglePageLayout(server) as layout:
    layout.title.set_text("FloatCard Demo")

    with layout.content:
        trame.FloatCard(
            "Drag the handle to move me anywhere",
            classes="pa-8",
        )

if __name__ == "__main__":
    server.start()
