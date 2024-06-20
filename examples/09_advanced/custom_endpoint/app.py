from trame.app import get_server
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3 as v3, html
from trame.decorators import TrameApp, controller

import time
from pathlib import Path
from aiohttp import web


@TrameApp()
class App:
    def __init__(self, server=None):
        self.server = get_server(server, client_type="vue3")
        self.server.cli.add_argument("--session")
        self._build_ui()

        # Use CLI to know when used inside docker
        args, _ = self.server.cli.parse_known_args()
        session = args.session

        # simple default state
        self.state.response = {}
        self.state.session = session
        self.state.url = "/trame-endpoint"

        # Need to adjust URL when within docker
        if session:
            self.state.url = f"/api/{session}/trame-endpoint"

    @property
    def state(self):
        return self.server.state

    @controller.add("on_server_bind")
    def _bind_routes(self, wslink_server):
        wslink_server.app.add_routes(
            [web.get("/trame-endpoint", self.on_trame_endpoint)]
        )

    def on_trame_endpoint(self, request):
        return web.json_response({"url": self.state.url, "time": time.time()})

    def _build_ui(self):
        with SinglePageLayout(self.server) as layout:
            with layout.toolbar:
                v3.VSpacer()
                v3.VBtn(
                    "Make request",
                    click="utils.get('fetch')(url).then(v => v.json()).then(v => (response = v))",
                )
            with layout.content:
                html.Div("URL: {{ url }}")
                html.Div("Session: {{ session }}")
                html.Div("Response")
                html.Pre("{{ JSON.stringify(response, null, 2) }}")


def main():
    app = App()
    app.server.start()


if __name__ == "__main__":
    main()
