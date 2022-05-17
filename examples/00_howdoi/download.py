r"""
Version for trame 1.x - https://github.com/Kitware/trame/blob/release-v1/examples/howdoi/download.py
Delta v1..v2          - https://github.com/Kitware/trame/commit/ae5066e942db36d0e1d5b957dd5c2c364996719d
"""

from trame.app import get_server
from trame.ui.vuetify import VAppLayout
from trame.widgets import vuetify

server = get_server()

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
