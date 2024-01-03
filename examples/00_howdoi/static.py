r"""
Installation requirements:
    pip install trame
"""

from trame.app import get_server
from trame.ui.html import DivLayout

server = get_server()

html = """
<h3>Welcome to trame...</h3>

<div>
    <i>Hello</i> <b>World</b>
</div>
"""

with DivLayout(server) as layout:
    layout.root.add_child(html)

if __name__ == "__main__":
    server.start()
