r"""
Version for trame 1.x - https://github.com/Kitware/trame/blob/release-v1/examples/PlainPython/Tables/app.py
Delta v1..v2          - https://github.com/Kitware/trame/commit/9a64369ebb1d016be3c1393fd06475694370b238

Installation requirements:
    pip install trame trame-vuetify trame-vega altair pandas numpy
"""

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, vega

from itertools import cycle

import altair as alt
import pandas as pd
import numpy as np

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller

# --------------------------------------------------------------------------------
# Making dataframe
# --------------------------------------------------------------------------------
np.random.seed(4)
DATA_FRAME = None


def fetch_data(samples=15):
    global DATA_FRAME
    deltas = cycle(
        [
            pd.Timedelta(weeks=-2),
            pd.Timedelta(days=-1),
            pd.Timedelta(hours=-1),
            pd.Timedelta(0),
            pd.Timedelta(minutes=5),
            pd.Timedelta(seconds=10),
            pd.Timedelta(microseconds=50),
            pd.Timedelta(microseconds=10),
        ]
    )
    dummy_data = {
        "id": range(samples),
        "date_time_naive": pd.date_range("2021-01-01", periods=samples),
        "apple": np.random.randint(0, 100, samples) / 3.0,
        "banana": np.random.randint(0, 100, samples) / 5.0,
        "chocolate": np.random.randint(0, 100, samples),
        "group": np.random.choice(["A", "B"], size=samples),
        "season": np.random.choice(
            ["Spring", "Summer", "Fall", "Winter"], size=samples
        ),
        "date_only": pd.date_range("2020-01-01", periods=samples).date,
        "timedelta": [next(deltas) for i in range(samples)],
        "date_tz_aware": pd.date_range(
            "2022-01-01", periods=samples, tz="Asia/Katmandu"
        ),
    }
    DATA_FRAME = pd.DataFrame(dummy_data)
    return DATA_FRAME


fetch_data()

# --------------------------------------------------------------------------------
# Preparing table
# --------------------------------------------------------------------------------
header_options = {"apple": {"sortable": False}}
headers, rows = vuetify.dataframe_to_grid(DATA_FRAME, header_options)

table = {
    "headers": ("headers", headers),
    "items": ("rows", rows),
    "v_model": ("selection", []),
    "search": ("query", ""),
    "classes": "elevation-1 ma-4",
    "multi_sort": True,
    "dense": True,
    "show_select": True,
    "single_select": False,
    "item_key": "id",
}

# --------------------------------------------------------------------------------
# Describing chart
# --------------------------------------------------------------------------------


@state.change("selection")
def selection_change(selection=[], **kwargs):
    global DATA_FRAME
    selected_df = pd.DataFrame(selection)

    # Chart
    chart_data = DATA_FRAME.loc[
        :, ["date_time_naive", "apple", "banana", "chocolate"]
    ].assign(source="total")

    if not selected_df.empty:
        selected_data = selected_df.loc[
            :, ["date_time_naive", "apple", "banana", "chocolate"]
        ].assign(source="selection")
        chart_data = pd.concat([chart_data, selected_data])

    chart_data = pd.melt(
        chart_data,
        id_vars=["date_time_naive", "source"],
        var_name="item",
        value_name="quantity",
    )
    chart = (
        alt.Chart(chart_data)
        .mark_bar()
        .encode(
            x=alt.X("item:O"),
            y=alt.Y("sum(quantity):Q", stack=False),
            color=alt.Color("source:N", scale=alt.Scale(domain=["total", "selection"])),
        )
    ).properties(width="container", height=100)

    ctrl.fig_update(chart)


# --------------------------------------------------------------------------------
# GUI
# --------------------------------------------------------------------------------

with SinglePageLayout(server) as layout:
    layout.title.set_text("Vuetify table example")
    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VTextField(
            v_model=("query",),
            placeholder="Search",
            dense=True,
            hide_details=True,
            prepend_icon="mdi-magnify",
        )

    with layout.content:
        with vuetify.VRow(classes="justify-center ma-6"):
            fig = vega.Figure(classes="ma-2", style="width: 100%;")
            ctrl.fig_update = fig.update
        vuetify.VDataTable(**table)

# -----------------------------------------------------------------------------
# Start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
