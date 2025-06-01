from trame.app import TrameApp
from trame.decorators import change, controller, life_cycle, trigger
from trame.ui.html import DivLayout
from trame.widgets import html


class App(TrameApp):
    def __init__(self, name=None):
        super().__init__(server=name)
        self._build_ui()

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

    def _build_ui(self):
        with DivLayout(self.server) as self.ui:
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
