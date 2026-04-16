r"""
Installation requirements:
    pip install trame trame-vuetify trame-vega altair pandas numpy
"""

from itertools import cycle

import altair as alt
import numpy as np
import pandas as pd

from trame.app import TrameApp
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vega
from trame.widgets import vuetify as v2
from trame.decorators import change

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------


class DataframeTable(TrameApp):
    def __init__(self, server=None):
        super().__init__(server, client_type="vue2")

        np.random.seed(4)
        self.fetch_data()
        self.prepare_table()

        self._build_ui()

    # --------------------------------------------------------------------------------
    # Making dataframe
    # --------------------------------------------------------------------------------

    def fetch_data(self, samples=15):
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
        self.DATA_FRAME = pd.DataFrame(dummy_data)

    # --------------------------------------------------------------------------------
    # Preparing table
    # --------------------------------------------------------------------------------

    def prepare_table(self):
        header_options = {"apple": {"sortable": False}}
        headers, rows = v2.dataframe_to_grid(self.DATA_FRAME, header_options)

        self.table = {
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

    @change("selection")
    def selection_change(self, selection=[], **_):
        selected_df = pd.DataFrame(selection)

        # Chart
        chart_data = self.DATA_FRAME.loc[
            :, ["date_time_naive", "apple", "banana", "chocolate"]
        ].assign(source="total")
        chart_data["date_time_naive"] = chart_data["date_time_naive"].astype(str)

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
        self.chart = (
            alt.Chart(chart_data)
            .mark_bar()
            .encode(
                x=alt.X("item:O"),
                y=alt.Y("sum(quantity):Q", stack=False),
                color=alt.Color(
                    "source:N", scale=alt.Scale(domain=["total", "selection"])
                ),
            )
        ).properties(width="container", height=100)

        self.ctrl.fig_update(self.chart)

    # --------------------------------------------------------------------------------
    # GUI
    # --------------------------------------------------------------------------------

    def _build_ui(self):
        with SinglePageLayout(self.server) as self.ui:
            self.ui.title.set_text("Vuetify table example")
            with self.ui.toolbar:
                v2.VSpacer()
                v2.VTextField(
                    v_model=("query",),
                    placeholder="Search",
                    dense=True,
                    hide_details=True,
                    prepend_icon="mdi-magnify",
                )

            with self.ui.content:
                with v2.VRow(classes="justify-center ma-6"):
                    fig = vega.Figure(classes="ma-2", style="width: 100%;")
                    self.ctrl.fig_update = fig.update
                v2.VDataTable(**self.table)


# -----------------------------------------------------------------------------
# Start server
# -----------------------------------------------------------------------------


def main():
    dfTable = DataframeTable()
    dfTable.server.start()


if __name__ == "__main__":
    main()
