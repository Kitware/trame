from trame.layouts import FullScreenPage
from trame.html import widgets

selection = ["2"]
tree = [
    {"id": "1", "parent": "0", "visible": 0, "name": "Wavelet"},
    {"id": "2", "parent": "1", "visible": 0, "name": "Clip"},
    {"id": "3", "parent": "1", "visible": 1, "name": "Slice"},
    {"id": "4", "parent": "2", "visible": 1, "name": "Slice 2"},
]

layout = FullScreenPage("Git Tree")
with layout:
    widgets.GitTree(
        sources=("tree", tree),
        actives=("selection", selection),
    )

if __name__ == "__main__":
    layout.start()
