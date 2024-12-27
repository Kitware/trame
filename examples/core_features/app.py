from trame.app import get_server
from trame.decorators import TrameApp, change, controller, trigger, life_cycle
from trame.ui.html import DivLayout
from trame.widgets import html


@TrameApp()
class App:
    def __init__(self, name=None):
        self.server = get_server(name)
        self.ui()

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    @trigger("exec")
    def method_call(self, msg):
        print("method_called", msg)

    @controller.set("hello")
    def method_on_ctrl(self, *args):
        print("method_on_ctrl", args)

    @change("resolution")
    def one_slider(self, resolution, **kwargs):
        print("Slider value 1", resolution)

    @life_cycle.server_ready
    def on_ready(self, *args, **kwargs):
        print("on_ready")

    def ui(self):
        with DivLayout(self.server):
            html.Input(
                type="range",
                min=3,
                max=60,
                step=1,
                v_model_number=("resolution", 6),
            )
            html.Button("trigger", click="trigger('exec', ['trigger'])")
            html.Button("method", click=(self.method_call, "['method']"))
            html.Button("ctrl", click=self.ctrl.hello)


if __name__ == "__main__":
    app = App()
    app.server.start()
