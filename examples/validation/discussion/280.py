from trame.app import get_server
from trame.ui.vuetify import VAppLayout
from trame.widgets import vuetify

server = get_server(client_type="vue2")


@server.state.change("value")
def update_number(value, **kwargs):
    print(f"{type(value)}({value})")


with VAppLayout(server):
    vuetify.VTextField(v_model_number=("value", 1), type="number")

server.start()
