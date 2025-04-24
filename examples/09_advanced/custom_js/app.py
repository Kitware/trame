from pathlib import Path

from trame.app import get_server
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import client, vuetify3


def load_my_js(server):
    # must run before server start
    js_file = Path(__file__).with_name("my_utils.js").resolve()
    server.enable_module(
        dict(
            # Path to serve under /my_code
            serve={"my_code": str(js_file.parent)},
            # JS file(s) to load
            scripts=[f"my_code/{js_file.name}"],
        )
    )


class CustomAddOnJS:
    def __init__(self, server=None, table_size=10):
        self.server = get_server(server, client_type="vue3")
        self.ui = self._build_ui()

        # Make sure my js code get loaded on the client side
        load_my_js(self.server)

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    def trigger_alert(self):
        self.ctrl.js_eval(f"server({self.state.name})")

    def _build_ui(self):
        with SinglePageLayout(self.server, full_height=True) as layout:
            self.ctrl.js_eval = client.JSEval(
                exec="utils.my_code.actions.hello($event)"
            ).exec
            with layout.toolbar:
                vuetify3.VTextField(
                    v_model=("name", "world"),
                    density="compact",
                    hide_details=True,
                )
                vuetify3.VBtn("Local JS", click="utils.my_code.actions.hello(name)")
                vuetify3.VBtn("JS from Py", click=self.trigger_alert)
            with layout.content:
                vuetify3.VTextField(
                    v_model=("text_1", "1.2"),
                    # Use our extended trame.utils in template definition
                    rules=("[utils.my_code.rules.number]",),
                )
                vuetify3.VTextField(
                    v_model=("text_2", "2"),
                    # Use our extended trame.utils in template definition
                    rules=("[utils.my_code.rules.int]",),
                )


def main():
    app = CustomAddOnJS()
    app.server.start()


if __name__ == "__main__":
    main()
