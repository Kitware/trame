#!/usr/bin/env -S uv run --script
# -----------------------------------------------------------------------------
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pandas",
#     "plotly",
#     "trame-plotly",
#     "trame-vuetify",
#     "trame[app]",
# ]
# ///
# -----------------------------------------------------------------------------
"""
Trame Plotly Chart Selector with drag and drop

Running with uv
   uv run ./drag-and-drop.py
   or ./drag-and-drop.py

Required Packages:
   pip install "trame[app]" trame-vuetify trame-plotly plotly pandas jupyterlab

Run as a Desktop Application:
   python drag-and-drop.py --app

Run as a Web Application (default):
   python drag-and-drop.py --server
   # Access via the URLs provided in the console (e.g., http://localhost:8080)
"""

from trame.app import TrameApp
from trame.ui.vuetify3 import VAppLayout
from trame.widgets import vuetify3 as v3, plotly, html

import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# Plotly figures
# -----------------------------------------------------------------------------

SCATTER_MATRIX = px.scatter_matrix(
    px.data.iris(),
    dimensions=["sepal_width", "sepal_length", "petal_width", "petal_length"],
    color="species",
)
SCATTER_3D = px.scatter_3d(
    px.data.iris(),
    x="sepal_length",
    y="sepal_width",
    z="petal_width",
    color="petal_length",
    symbol="species",
)
BAR_CHART = go.Figure(
    data=[go.Bar(x=[1, 2, 3], y=[1, 3, 2])], layout_title_text="A Bar Chart"
)
CONTOUR_PLOT = go.Figure(
    data=[
        go.Contour(
            z=[
                [10, 10.625, 12.5, 15.625, 20],
                [5.625, 6.25, 8.125, 11.25, 15.625],
                [2.5, 3.125, 5.0, 8.125, 12.5],
                [0.625, 1.25, 3.125, 6.25, 10.625],
                [0, 0.625, 2.5, 5.625, 10],
            ]
        )
    ]
)
CONTOUR_PLOT.update_layout(title_text="Contour Plot")

PLOTS = {
    "Contour": CONTOUR_PLOT,
    "Scatter3D": SCATTER_3D,
    "ScatterMatrix": SCATTER_MATRIX,
    "BarChart": BAR_CHART,
}

PLOTS_NAME_ICON = {
    "Contour": "mdi-fingerprint",
    "Scatter3D": "mdi-cube-outline",
    "ScatterMatrix": "mdi-matrix",
    "BarChart": "mdi-chart-bar",
}

# -----------------------------------------------------------------------------
# Trame app
# -----------------------------------------------------------------------------


class PlotlyViewer(TrameApp):
    def __init__(self, server=None):
        super().__init__(server, client_type="vue3")
        self.active_plot_name = None
        self._build_ui()

    def select_plot(self, plot_name):
        self.active_plot_name = plot_name

    def apply_placement(self, slot_name):
        if slot_name is not None and self.active_plot_name is not None:
            self.update_plot_figure(self.active_plot_name, slot_name)
        self.active_plot_name = None

    def update_plot_figure(self, plot_name, slot_name):
        figure_data = PLOTS.get(plot_name)
        if figure_data:
            self.ctx[slot_name].update(figure_data)
            self.state[slot_name] = True  # show the plot

    def _build_ui(self):
        with VAppLayout(self.server, full_height=True) as self.ui:
            with v3.VNavigationDrawer(width=150):
                with v3.VList(density="comfortable"):
                    v3.VListItem(title="Drag & drop")
                    v3.VDivider()
                    for name, icon in PLOTS_NAME_ICON.items():
                        with v3.VListItem():
                            v3.VChip(
                                text=name,
                                classes="w-100",
                                draggable=True,
                                prepend_icon=icon,
                                mousedown=(self.select_plot, f"['{name}']"),
                                variant="text",
                            )

            with v3.VMain():
                with v3.VRow(classes="h-100 pa-1 ma-0", dense=True):
                    for i in range(4):
                        name = f"slot_{i}"
                        with v3.VCol(cols="6", classes="h-50"):
                            with v3.VCard(
                                classes="h-100 d-flex align-center justify-center",
                                variant="tonal",
                                v_on_mouseover=(self.apply_placement, f"['{name}']"),
                            ):
                                plotly.Figure(
                                    v_if=(name, False),
                                    ctx_name=name,
                                    display_logo=True,
                                    display_mode_bar=True,
                                    v_on_mouseover=(
                                        self.apply_placement,
                                        f"['{name}']",
                                    ),
                                )
                                html.Div(
                                    "Drop chart here",
                                    classes="text-subtitle-1",
                                    v_else=True,
                                )


def main(**kwargs):
    app = PlotlyViewer()
    app.server.start(**kwargs)


if __name__ == "__main__":
    main()
