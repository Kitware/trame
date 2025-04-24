import asyncio

from trame.app import get_server
from trame.decorators import TrameApp, controller
from trame.ui.html import DivLayout
from trame.widgets import trame


def toggle_node(node, node_id):
    if node.get("id") == node_id:
        new_visible = (node.get("visible") + 1) % 2
        return {**node, "visible": new_visible}
    return node


@TrameApp()
class App:
    def __init__(self, server=None):
        self.server = get_server(server, client_type="vue3")
        self.ui = self._build_ui()

    @property
    def state(self):
        return self.server.state

    def toggle_visibility(self, node_id):
        with self.state:
            self.state.pipeline = [toggle_node(n, node_id) for n in self.state.pipeline]

    @controller.add_task("on_server_ready")
    async def auto_toggle(self, **kwargs):
        while True:
            for node_id in ["1", "2"]:
                await asyncio.sleep(0.1)
                self.toggle_visibility(node_id)

    def _build_ui(self):
        with DivLayout(self.server):
            trame.GitTree(
                sources=(
                    "pipeline",
                    [
                        {"id": "1", "parent": "0", "visible": 1, "name": "Mesh"},
                        {"id": "2", "parent": "1", "visible": 1, "name": "Contour"},
                    ],
                ),
            )


if __name__ == "__main__":
    app = App()
    app.server.start()
