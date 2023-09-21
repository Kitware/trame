r"""
https://vuetifyjs.com/en/components/tooltips/

    <v-tooltip text="Tooltip">
      <template v-slot:activator="{ props }">
        <v-btn v-bind="props">Hover over me</v-btn>
      </template>
    </v-tooltip>
"""

from trame.app import get_server
from trame.ui.vuetify3 import VAppLayout
from trame.widgets import vuetify3

server = get_server()
server.client_type = "vue3"

with VAppLayout(server):
    with vuetify3.VTooltip(text="Tooltip"):
        with vuetify3.Template(v_slot_activator="{ props }"):
            vuetify3.VBtn("Hover over me", v_bind="props")

server.start(port=10003)
