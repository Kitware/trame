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
