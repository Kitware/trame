#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "trame",
# ]
# ///
from trame.app import TrameApp
from trame.decorators import controller
from trame.ui.html import DivLayout
from trame.widgets import html


class Events(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)

        # setup state
        self.state.a = 1

        # build ui
        self._build_ui()

        # Can be defined after usage
        self.ctrl.alias_3 = self.method_4

    def _build_ui(self):
        with DivLayout(self.server) as self.ui:
            html.Div(
                "State a={{ a }}",
                style="padding: 20px; margin: 20px; border: solid 1px #333;",
            )
            html.Button("Method 1", click=self.method_1)
            html.Button("Method 2", click=(self.method_2, "['hello', 'world']"))
            html.Button("Method 3", click=(self.method_3, "[1, 2]", "{ x: 3, y: 4 }"))
            html.Button("alias_1", click=(self.ctrl.alias_1, "[2]", "{ z: 4 }"))
            html.Button("alias_2", click=(self.ctrl.alias_2, "[3]", "{ z: 5 }"))
            html.Button("alias_3", click=(self.ctrl.alias_3, "[4]", "{ z: 6 }"))
            html.Button("a+", click="a+=1")

    @controller.set("alias_1")
    def method_1(self, *args, **kwargs):
        print(f"Server: method_1 {args=} {kwargs=}")
        self.state.a += 1

    @controller.add("alias_2")
    def method_2(self, *args, **kwargs):
        print(f"Server: method_2 {args=} {kwargs=}")
        self.state.a += 2

    @controller.add("alias_2")
    def method_3(self, *args, **kwargs):
        print(f"Server: method_3 {args=} {kwargs=}")
        self.state.a += 3

    def method_4(self, *args, **kwargs):
        print(f"Server: method_4 {args=} {kwargs=}")
        self.state.a += 10


def main():
    app = Events()
    app.server.start()


if __name__ == "__main__":
    main()
