from pathlib import Path

from trame.app import get_server
from trame.ui.html import DivLayout
from trame.widgets import helper
from trame.widgets import vuetify3 as vuetify

server = get_server(client_type="vue3")
state = server.state
controller = server.controller


SCRIPT_PATH = Path(__file__).with_name("707.js")
draggable_module = dict(
    serve={"__trame_vuedraggable": str(SCRIPT_PATH.parent.absolute())},
    scripts=[
        "https://cdn.jsdelivr.net/npm/sortablejs@1.10.2/Sortable.min.js",
        "https://cdn.jsdelivr.net/npm/vuedraggable@next/dist/vuedraggable.umd.min.js",
        "__trame_vuedraggable/707.js",
    ],
    vue_use=["trame_vuedraggable"],
)


# helper class
Draggable = helper.create_class(
    "Draggable", "draggable", module=draggable_module, properties=["item_key"]
)

state.tags = [
    {"id": "0", "name": "Shopping"},
    {"id": "1", "name": "Art"},
    {"id": "2", "name": "Tech"},
    {"id": "3", "name": "Creative Writing"},
]

# layout
with DivLayout(server) as layout:
    with vuetify.VApp():
        with vuetify.VContainer(classes="pa-4"):
            with vuetify.VCard(max_width=400, classes="mx-auto"):
                with Draggable(v_model=("tags",), item_key="id") as drag:
                    with vuetify.Template(
                        v_slot_item="{element}",
                        __properties=[("v_slot_items", "v-slot:items")],
                    ):
                        with vuetify.VCard(key="element.id"):
                            vuetify.VCardText("{{ element.name }}")

server.start()
