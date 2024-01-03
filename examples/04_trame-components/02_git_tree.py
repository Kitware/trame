r"""
Installation requirements:
    pip install trame trame-vuetify trame-components
"""

from trame.app import get_server
from trame.ui.vuetify import VAppLayout
from trame.widgets import trame

selection = ["2"]
tree = [
    {"id": "1", "parent": "0", "visible": 0, "name": "Wavelet"},
    {"id": "2", "parent": "1", "visible": 0, "name": "Clip"},
    {"id": "3", "parent": "1", "visible": 1, "name": "Slice"},
    {"id": "4", "parent": "2", "visible": 1, "name": "Slice 2"},
]
server = get_server(client_type="vue2")

with VAppLayout(server):
    trame.GitTree(
        sources=("tree", tree),
        actives=("selection", selection),
    )

if __name__ == "__main__":
    server.start()
