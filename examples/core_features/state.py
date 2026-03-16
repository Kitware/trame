#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "trame",
# ]
# ///
from trame.app import TrameApp
from trame.decorators import change
from trame.ui.html import DivLayout
from trame.widgets import html


# UI helper to extent layout
def create_ui_for_state_var(name):
    with html.Div(style="margin: 20px; padding: 20px; border: solid 1px #333;"):
        html.Div(
            f"Variable \"{name}\" {{{{ {name} }}}} == get({{{{ get('{name}') }}}})",
            style="padding: 10px;",
        )
        with html.Div(style="padding: 10px;"):
            html.Button(f"{name}+", click=f"{name} += 1")
            html.Button(f"{name}-", click=f"{name} -= 1")
            html.Button(f"{name}=5", click=f"{name} = 5")
            html.Button(f"set({name}+)", click=f"set('{name}', {name} + 1)")
            html.Button(f"set({name}-)", click=f"set('{name}', {name} - 1)")
            html.Button(f"set({name}=5)", click=f"set('{name}', 5)")


class StateUsage(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self.state_setup()
        self._build_ui()

    def state_setup(self):
        # Creating new entries to the shared state
        self.state.a = 1
        self.state["b"] = 2

        # Force state.d to be client side only
        self.state.client_only("b")
        # self.state.trame__client_only += ["b"]

    def _build_ui(self):
        with DivLayout(self.server) as self.ui:
            create_ui_for_state_var("a")
            create_ui_for_state_var("b")

    @change("a", "b")
    def state_change(self, a, b, **_):
        """State listener"""
        print(f"State updated a={a} b={b}")


def main():
    app = StateUsage()
    app.server.start()


if __name__ == "__main__":
    main()
