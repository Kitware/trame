import plotly.graph_objects as go
import plotly.express as px

from trame import state
from trame.layouts import SinglePage
from trame.html import vuetify, plotly


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


html_plot = None
layout = SinglePage("Plotly")
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
            html_plot = plotly.Plotly(
                "demo",
                display_mode_bar=("true",),
                selected=(on_event, "['selected', VuePlotly.safe($event)]"),
                # hover=(on_event, "['hover', VuePlotly.safe($event)]"),
                # selecting=(on_event, "['selecting', $event]"),
                # unhover=(on_event, "['unhover', $event]"),
            )
            vuetify.VSpacer()


@state.change("active_plot")
def update_plot(active_plot, **kwargs):
    html_plot.update(PLOTS[active_plot]())


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    update_plot("Contour")
    layout.start()
