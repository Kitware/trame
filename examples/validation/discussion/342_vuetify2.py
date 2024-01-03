r"""
https://v2.vuetifyjs.com/en/components/tooltips/

    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn v-bind="attrs" v-on="on">Hover over me</v-btn>
      </template>
      <span>Tooltip</span>
    </v-tooltip>
"""

from trame.app import get_server
from trame.ui.vuetify2 import VAppLayout
from trame.widgets import vuetify2, html

server = get_server(client_type="vue2")

with VAppLayout(server):
    with vuetify2.VTooltip(bottom=True):
        with vuetify2.Template(v_slot_activator="{ on, attrs }"):
            vuetify2.VBtn(
                "Hover over me",
                v_bind="attrs",
                v_on="on",
            )
        html.Span("Tooltip")

server.start(port=10002)
