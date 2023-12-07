from trame.app import get_server
from trame.ui.html import DivLayout
from trame.widgets import vuetify

with DivLayout(get_server(client_type="vue2")) as layout:
    vuetify.VTextField(
        label="defectName",
        v_model=("defectForm",),
        required=True,
        __properties=["required"],
    )
    print(layout)
