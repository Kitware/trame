from trame.app import get_server
from trame.ui.html import DivLayout
from trame.widgets import client, html


class DeepReactiveArray:
    def __init__(self, server=None):
        self.server = get_server(server)

        self.state.data = {}

        with DivLayout(self.server) as self.ui:
            html.Button("Add", click=self.add)
            html.Button("Remove", click=self.remove)
            with client.DeepReactive("data"):
                with html.Ul():
                    with html.Li(
                        key="k",
                        v_for="v, k in data",
                    ):
                        html.Span("{{ v.name }}")
                        html.Input(
                            type="range",
                            min=0,
                            max=100,
                            step=1,
                            v_model="data[k].slider",
                        )

            html.Pre("{{ JSON.stringify(data, null, 2) }}")

    @property
    def state(self):
        return self.server.state

    def add(self):
        name = f"Item {len(self.state.data)}"
        self.state.data[name] = {"name": name, "slider": 50}
        self.state.dirty("data")

    def remove(self):
        last_key = f"Item {len(self.state.data) - 1}"
        self.state.data.pop(last_key)
        self.state.dirty("data")
        # self.state.data = { k:v for k,v in self.state.data.items() if k != last_key }


def main():
    app = DeepReactiveArray()
    app.server.start()


if __name__ == "__main__":
    main()
