r"""
Installation requirements:
    pip install trame trame-vuetify pandas
"""

from trame.app import get_server
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import html, vuetify3 as vuetify

import pandas as pd

server = get_server(client_type="vue3")
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
headers = [
    {"key": "name", "title": "Dessert", "align": "start", "sortable": False},
    {"key": "calories", "title": "Calories"},
    {"key": "fat", "title": "Fat (g)"},
    {"key": "carbs", "title": "Carbs (g)"},
    {"key": "protein", "title": "Protein (g)"},
    {"key": "iron", "title": "Iron (%)"},
    {"key": "glutenfree", "title": "Gluten-Free"},
]

state.setdefault("group_by", [{"key": "glutenfree", "order": "asc"}])

# fmt: on
_, rows = vuetify.dataframe_to_grid(frame)


table = {
    "group_by": ("group_by",),
    "headers": ("headers", headers),
    "items": ("rows", rows),
    "search": ("query", ""),
    "classes": "elevation-1 ma-4",
    "multi_sort": True,
    "dense": True,
    "items_per_page": 10,
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
                group_header="{ item, columns, toggleGroup, isGroupOpen }",
                __properties=[
                    ("group_header", "v-slot:group-header"),
                ],
            ):
                with html.Tr():
                    with html.Td(colspan=("columns.length",)):
                        vuetify.VBtn(
                            icon=("isGroupOpen(item) ? '$expand' : '$next'",),
                            size="small",
                            variant="text",
                            click="toggleGroup(item)",
                        )
                        html.Span("{{ item.value ?'Gluten free' : 'Contains gluten' }}")

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
                vuetify.VCheckbox(
                    "{{ item.glutenfree }}",
                    v_model=("item.glutenfree",),
                    disabled=False,
                    input="flushState('rows')",
                )


if __name__ == "__main__":
    server.start()
