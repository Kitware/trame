from trame.app import get_server
from trame.decorators import TrameApp, change, controller, life_cycle, trigger
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify


@TrameApp()
class App:
    def __init__(self, server=None):
        self.server = get_server(server, client_type="vue2")
        self.ui()

    @property
    def ctrl(self):
        return self.server.controller

    @trigger("exec")
    def method_call(self, *args):
        print("method_called", args)

    @controller.set("hello")
    def method_on_ctrl(self, *args):
        print("method_on_ctrl", args)

    @change("slider_value1", "slider_value2")
    def both_sliders(self, slider_value1, slider_value2, **kwargs):
        print("Slider value (1 or 2)", slider_value1, slider_value2)

    @change("slider_value1")
    def one_slider(self, slider_value1, **kwargs):
        print("Slider value 1", slider_value1)

    @life_cycle.server_ready
    def on_ready(self, *args, **kwargs):
        print("on_ready")

    @life_cycle.on_error
    def on_error(self, message):
        print(f"A JS error occured: {message}")

    def ui(self):
        with SinglePageLayout(self.server) as layout:
            with layout.toolbar:
                vuetify.VSpacer()
                vuetify.VSlider(
                    v_model=("slider_value1", 0), dense=True, hide_details=True
                )
                vuetify.VSlider(
                    v_model=("slider_value2", 0), dense=True, hide_details=True
                )
                vuetify.VBtn("trigger", click="trigger('exec')")
                vuetify.VBtn("method", click=self.method_call)
                vuetify.VBtn("ctrl", click=self.ctrl.hello)
                vuetify.VBtn("JS error", click="undefined_func()")


app = App()
app.server.start()
