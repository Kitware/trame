r"""
Installation requirements:
    pip install trame trame-vuetify
"""

from trame.app import get_server
from trame.ui.vuetify import VAppLayout
from trame.widgets import vuetify

server = get_server(client_type="vue2")

with VAppLayout(server):
    vuetify.VBtn(
        "Download",
        click="utils.download('my_file_name.csv', file_content, 'text/csv')",
    )

server.state.file_content = """a,b,c
1,2,3
4,5,6
7,8,9
"""


if __name__ == "__main__":
    server.start()
