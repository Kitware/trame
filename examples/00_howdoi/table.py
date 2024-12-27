r"""
Installation requirements:
    pip install trame trame-vuetify pandas
"""

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify
import json

import pandas as pd

server = get_server(client_type="vue2")

# --------------------------------------------------------------------------------
# Loading dataframe
# --------------------------------------------------------------------------------
data = json.loads(
    """
[
    {"name":"Frozen Yogurt","calories":200,"fat":6,"carbs":24,"protein":4,"iron":"1%"},
    {"name":"Ice cream sandwich","calories":200,"fat":9,"carbs":37,"protein":4.3,"iron":"1%"},
    {"name":"Eclair","calories":300,"fat":16,"carbs":23,"protein":6,"iron":"7%"},
    {"name":"Cupcake","calories":300,"fat":3.7,"carbs":67,"protein":4.3,"iron":"8%"},
    {"name":"Gingerbread","calories":400,"fat":16,"carbs":49,"protein":3.9,"iron":"16%"},
    {"name":"Jelly bean","calories":400,"fat":0,"carbs":94,"protein":0,"iron":"0%"},
    {"name":"Lollipop","calories":400,"fat":0.2,"carbs":98,"protein":0,"iron":"2%"},
    {"name":"Honeycomb","calories":400,"fat":3.2,"carbs":87,"protein":6.5,"iron":"45%"},
    {"name":"Donut","calories":500,"fat":25,"carbs":51,"protein":4.9,"iron":"22%"},
    {"name":"KitKat","calories":500,"fat":26,"carbs":65,"protein":7,"iron":"6%"}
]
    """
)

frame = pd.DataFrame.from_dict(data)

# --------------------------------------------------------------------------------
# Configure table columns and options
# --------------------------------------------------------------------------------

# fmt: off
header_options = {
    "name":     {"text": "Dessert", "align": "start", "sortable": False},
    "calories": {"text": "Calories"},
    "fat":      {"text": "Fat (g)"},
    "carbs":    {"text": "Carbs (g)"},
    "protein":  {"text": "Protein (g)"},
    "iron":     {"text": "Iron (%)"},
}

# fmt: on
headers, rows = vuetify.dataframe_to_grid(frame, header_options)
table = {
    "headers": ("headers", headers),
    "items": ("rows", rows),
    "search": ("query", ""),
    "classes": "elevation-1 ma-4",
    "multi_sort": True,
    "dense": True,
    "items_per_page": 5,
}


# --------------------------------------------------------------------------------
# GUI
# --------------------------------------------------------------------------------

with SinglePageLayout(server) as layout:
    layout.title.set_text("Vuetify table example")
    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VTextField(
            v_model=("query", ""),
            placeholder="Search",
            dense=True,
            hide_details=True,
        )

    with layout.content:
        vuetify.VDataTable(**table)

if __name__ == "__main__":
    server.start()
