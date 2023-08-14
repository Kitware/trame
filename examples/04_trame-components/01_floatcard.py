r"""
Version for trame 1.x - https://github.com/Kitware/trame/blob/release-v1/examples/modules/Widgets/FloatCard.py
Delta v1..v2          - https://github.com/Kitware/trame/commit/6f7e14180296b04d4bcd6fd6d8c7b6c9a1df730a

Installation requirements:
    pip install trame trame-vuetify trame-components
"""

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import trame

server = get_server()

with SinglePageLayout(server) as layout:
    layout.title.set_text("FloatCard Demo")

    with layout.content:
        trame.FloatCard(
            "Drag the handle to move me anywhere",
            classes="pa-8",
        )

if __name__ == "__main__":
    server.start()
