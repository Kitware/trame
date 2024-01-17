from pathlib import Path

from trame.app import get_server
from trame.widgets import vuetify3
from trame.ui.vuetify3 import SinglePageLayout


def load_my_js(server):
    # must run before server start
    js_file = Path(__file__).with_name("my_utils.js").resolve()
    server.enable_module(
        dict(
            serve={"my_code": str(js_file.parent)}, scripts=[f"my_code/{js_file.name}"]
        )
    )


class CustomAddOnJS:
    def __init__(self, server=None, table_size=10):
        self.server = get_server(server, client_type="vue3")
        load_my_js(self.server)
        self.ui = self._build_ui()

    def _build_ui(self):
        with SinglePageLayout(self.server, full_height=True) as layout:
            with layout.content:
                vuetify3.VTextField(
                    v_model=("text_1", "1.2"),
                    rules=("[utils.my_code.rules.number]",),
                )
                vuetify3.VTextField(
                    v_model=("text_2", "2"),
                    rules=("[utils.my_code.rules.int]",),
                )


def main():
    app = CustomAddOnJS()
    app.server.start()


if __name__ == "__main__":
    main()
