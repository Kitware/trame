import trame.widgets.html as h
import trame.widgets.vuetify3 as v3
from trame.app import get_server
from trame.ui.vuetify3 import SinglePageLayout, VAppLayout


class Example2:
    def __init__(self, server=None):
        self.server = get_server(server, client_type="vue3")
        self.layout = self._build_ui()
        self.count = 0

    def _build_ui(self):
        with VAppLayout(self.server, template_name="example2") as layout:
            with layout:
                v3.VBtn(
                    "test (spoiler, I work)",
                    style="background-color:gray;",
                    click=self.test,
                )
                with v3.VContainer() as self.div:
                    h.Div("YES")
        return layout

    def test(self):
        self.count += 1

        self.div.clear()
        with self.div:
            h.Div(f"test {self.count}")
        self.layout.flush_content()


class Example3:
    def __init__(self, server=None):
        self.server = get_server(server, client_type="vue3")
        self.layout = self._build_ui()
        self.count = 0

    def _build_ui(self):
        with VAppLayout(self.server, template_name="example_3") as layout:
            with layout:
                v3.VBtn(
                    "test (spoiler, I don't work)",
                    style="background-color:gray;",
                    click=self.test,
                )
                with v3.VContainer() as self.div:
                    h.Div("YES")
        return layout

    def test(self):
        self.count += 1

        self.div.clear()
        with self.div:
            h.Div(f"test {self.count}")
        self.layout.flush_content()


class Example:
    def __init__(self, server=None):
        self.server = get_server(server, client_type="vue3")
        self.layout = self._build_ui()
        self.example2 = Example2()
        self.example3 = Example3()

    def _build_ui(self):
        with SinglePageLayout(self.server) as layout:
            with layout.toolbar:
                v3.VBtn(
                    "Not Working",
                    click="window.open('/?ui=example_3', target='_blank')",
                )
                v3.VBtn(
                    "Working", click="window.open('/?ui=example2', target='_blank')"
                )


if __name__ == "__main__":
    app = Example()
    app.server.start()
