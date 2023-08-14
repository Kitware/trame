r"""
Version for trame 1.x - https://github.com/Kitware/trame/blob/release-v1/examples/howdoi/static.py
Delta v1..v2          - https://github.com/Kitware/trame/commit/25ce0c5b46f1f5ae1f0838fe2a539e0b8b0d7f5e

Installation requirements:
    pip install trame trame-vuetify
"""

from trame.app import get_server
from trame.ui.vuetify import VAppLayout

server = get_server()

html = """
<h3>Welcome to trame...</h3>

<div>
    <i>Hello</i> <b>World</b>
</div>
"""

with VAppLayout(server) as layout:
    layout.root.add_child(html)

if __name__ == "__main__":
    server.start()
