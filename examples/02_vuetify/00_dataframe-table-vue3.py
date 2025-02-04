r"""
Installation requirements:
    pip install trame trame-vuetify pandas
"""

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify

import pandas as pd

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

state.setdefault("active_ui", None)

# --------------------------------------------------------------------------------
# Loading dataframe
# --------------------------------------------------------------------------------
data = [
    {
        "name": "Frozen Yogurt",
        "calories": 200,
        "fat": 6,
        "carbs": 24,
        "protein": 4,
        "iron": "1%",
        "glutenfree": True,
    },
    {
        "name": "Ice cream sandwich",
        "calories": 200,
        "fat": 9,
        "carbs": 37,
        "protein": 4.3,
        "iron": "1%",
        "glutenfree": False,
    },
    {
        "name": "Eclair",
        "calories": 300,
        "fat": 16,
        "carbs": 23,
        "protein": 6,
        "iron": "7%",
        "glutenfree": False,
    },
    {
        "name": "Cupcake",
        "calories": 300,
        "fat": 3.7,
        "carbs": 67,
        "protein": 4.3,
        "iron": "8%",
        "glutenfree": True,
    },
    {
        "name": "Gingerbread",
        "calories": 400,
        "fat": 16,
        "carbs": 49,
        "protein": 3.9,
        "iron": "16%",
        "glutenfree": True,
    },
    {
        "name": "Jelly bean",
        "calories": 400,
        "fat": 0,
        "carbs": 94,
        "protein": 0,
        "iron": "0%",
        "glutenfree": False,
    },
    {
        "name": "Lollipop",
        "calories": 400,
        "fat": 0.2,
        "carbs": 98,
        "protein": 0,
        "iron": "2%",
        "glutenfree": True,
    },
    {
        "name": "Honeycomb",
        "calories": 400,
        "fat": 3.2,
        "carbs": 87,
        "protein": 6.5,
        "iron": "45%",
        "glutenfree": True,
    },
    {
        "name": "Donut",
        "calories": 500,
        "fat": 25,
        "carbs": 51,
        "protein": 4.9,
        "iron": "22%",
        "glutenfree": True,
    },
    {
        "name": "KitKat",
        "calories": 500,
        "fat": 26,
        "carbs": 65,
        "protein": 7,
        "iron": "6%",
        "glutenfree": True,
    },
]


frame = pd.DataFrame.from_dict(data)

# --------------------------------------------------------------------------------
# Configure table columns and options
# --------------------------------------------------------------------------------

# fmt: off
header_options = {
    "name":         {"text": "Dessert", "align": "start", "sortable": False},
    "calories":     {"text": "Calories"},
    "fat":          {"text": "Fat (g)"},
    "carbs":        {"text": "Carbs (g)"},
    "protein":      {"text": "Protein (g)"},
    "iron":         {"text": "Iron (%)"},
    "glutenfree":   {"text": "Gluten-Free"}
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


@state.change("rows")
def update_values(rows, **kwargs):
    print("rows changed")
    # print(rows)


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
        state.rows = rows
        with vuetify.VDataTable(**table):
            with vuetify.Template(
                calories="{ item }",
                __properties=[
                    ("calories", "v-slot:item.calories"),
                ],
            ):
                vuetify.VChip(
                    "{{ item.calories }}",
                    color=("item.color",),
                    dark=True,
                )
            with vuetify.Template(
                glutenfree="{ item }",
                __properties=[
                    ("glutenfree", "v-slot:item.glutenfree"),
                ],
            ):
                vuetify.VSimpleCheckbox(
                    "{{ item.glutenfree }}",
                    v_model=("item.glutenfree",),
                    disabled=False,
                    input="flushState('rows')",
                )


if __name__ == "__main__":
    server.start()
