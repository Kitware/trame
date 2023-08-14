r"""
Version for trame 1.x - https://github.com/Kitware/trame/blob/release-v1/examples/PlainPython/Plotly/basic/app.py
Delta v1..v2          - https://github.com/Kitware/trame/commit/cbc614f8a2e408a28574cddbe8f4b43b1b91e2dc

Installation requirements:
    pip install trame trame-vuetify trame-plotly
"""

import plotly.graph_objects as go
import plotly.express as px

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, plotly

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Charts
# -----------------------------------------------------------------------------


def contour_plot():
    """https://plotly.com/python/contour-plots/"""
    return go.Figure(
        data=go.Contour(
            z=[
                [10, 10.625, 12.5, 15.625, 20],
                [5.625, 6.25, 8.125, 11.25, 15.625],
                [2.5, 3.125, 5.0, 8.125, 12.5],
                [0.625, 1.25, 3.125, 6.25, 10.625],
                [0, 0.625, 2.5, 5.625, 10],
            ]
        )
    )


def bar_plot(color="Gold"):
    return go.Figure(data=go.Bar(y=[2, 3, 1], marker_color=color))


def scatter():
    df = px.data.iris()

    fig = px.scatter(
        df,
        x="sepal_width",
        y="sepal_length",
        color="species",
        title="Using The add_trace() method With A Plotly Express Figure",
    )

    fig.add_trace(
        go.Scatter(
            x=[2, 4],
            y=[4, 8],
            mode="lines",
            line=go.scatter.Line(color="gray"),
            showlegend=False,
        )
    )

    return fig


PLOTS = {
    "Contour": contour_plot,
    "Bar": bar_plot,
    "Scatter": scatter,
}


def on_event(type, e):
    print(type, e)


# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


@state.change("active_plot")
def update_plot(active_plot, **kwargs):
    ctrl.figure_update(PLOTS[active_plot]())


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

state.trame__title = "Plotly"

with SinglePageLayout(server) as layout:
    layout.title.set_text("trame ❤️ plotly")

    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VSelect(
            v_model=("active_plot", "Contour"),
            items=("plots", list(PLOTS.keys())),
            hide_details=True,
            dense=True,
        )

    with layout.content:
        with vuetify.VContainer(fluid=True):
            with vuetify.VRow(dense=True):
                vuetify.VSpacer()
                figure = plotly.Figure(
                    display_logo=False,
                    display_mode_bar="true",
                    # selected=(on_event, "['selected', utils.safe($event)]"),
                    # hover=(on_event, "['hover', utils.safe($event)]"),
                    # selecting=(on_event, "['selecting', $event]"),
                    # unhover=(on_event, "['unhover', $event]"),
                )
                ctrl.figure_update = figure.update
                vuetify.VSpacer()

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
