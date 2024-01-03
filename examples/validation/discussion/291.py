from pathlib import Path
from trame.app import get_server
from trame.ui.vuetify import VAppLayout

server = get_server(client_type="vue2")

SCRIPT_PATH = Path(__file__).with_name("291.js")
split_pane_module = {
    "serve": {
        "__trame_splitpanes": str(SCRIPT_PATH.parent.absolute()),
    },
    "scripts": ["https://unpkg.com/splitpanes@legacy", "__trame_splitpanes/291.js"],
    "styles": ["https://unpkg.com/splitpanes@legacy/dist/splitpanes.css"],
    "vue_use": ["trame_splitpanes"],
}
server.enable_module(split_pane_module)

with VAppLayout(server) as layout:
    layout.root.add_child(
        """
    <splitpanes class="default-theme">
        <pane min-size="20">
            1
            <br>
            <em class="specs"> I have a min width of 20%<em>
        </pane>
        <pane>
            <splitpanes class="default-theme" horizontal>
                <pane min-size="15">
                    2
                    <br>
                    <em class="specs"> I have a min height of 15%</em>
                </pane>
                <pane>3</pane>
                <pane>4</pane>
            </splitpanes>
        </pane>
        <pane>
            5
        </pane>
    </splitpanes>
    """
    )

server.start()
