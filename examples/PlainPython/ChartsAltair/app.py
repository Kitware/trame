# -----------------------------------------------------------------------------
# More examples available at https://altair-viz.github.io/gallery/
# -----------------------------------------------------------------------------

import trame as tr
import altair as alt
from vega_datasets import data

from trame.layouts import SinglePage
from trame.html import vuetify, Div, vega


# -----------------------------------------------------------------------------
# Chart examples
# -----------------------------------------------------------------------------


def ScatterMatrix():
    """https://altair-viz.github.io/gallery/scatter_matrix.html"""
    source = data.cars()

    chart = (
        alt.Chart(source)
        .mark_circle()
        .encode(
            alt.X(alt.repeat("column"), type="quantitative"),
            alt.Y(alt.repeat("row"), type="quantitative"),
            color="Origin:N",
        )
        .properties(width=200, height=200)
        .repeat(
            row=["Horsepower", "Acceleration", "Miles_per_Gallon"],
            column=["Miles_per_Gallon", "Acceleration", "Horsepower"],
        )
        .interactive()
    )

    # Push chart to client
    vega_component.update(chart)


# -----------------------------------------------------------------------------


def USIncomeByState():
    """https://altair-viz.github.io/gallery/us_incomebrackets_by_state_facet.html"""
    states = alt.topo_feature(data.us_10m.url, "states")
    source = data.income.url

    chart = (
        alt.Chart(source)
        .mark_geoshape()
        .encode(
            shape="geo:G",
            color="pct:Q",
            tooltip=["name:N", "pct:Q"],
            facet=alt.Facet("group:N", columns=3),
        )
        .transform_lookup(
            lookup="id", from_=alt.LookupData(data=states, key="id"), as_="geo"
        )
        .properties(
            width=300,
            height=175,
        )
        .project(type="albersUsa")
    )

    # Push chart to client
    vega_component.update(chart)


# -----------------------------------------------------------------------------


def StackedDensityEstimates():
    """https://altair-viz.github.io/gallery/density_stack.html"""
    source = data.iris()

    chart = (
        alt.Chart(source)
        .transform_fold(
            ["petalWidth", "petalLength", "sepalWidth", "sepalLength"],
            as_=["Measurement_type", "value"],
        )
        .transform_density(
            density="value",
            bandwidth=0.3,
            groupby=["Measurement_type"],
            extent=[0, 8],
            counts=True,
            steps=200,
        )
        .mark_area()
        .encode(
            alt.X("value:Q"),
            alt.Y("density:Q", stack="zero"),
            alt.Color("Measurement_type:N"),
        )
        .properties(width=400, height=100)
    )

    vega_component.update(chart)


def StreamGraph():
    """https://altair-viz.github.io/gallery/streamgraph.html"""
    source = data.unemployment_across_industries.url

    chart = (
        alt.Chart(source)
        .mark_area()
        .encode(
            alt.X(
                "yearmonth(date):T",
                axis=alt.Axis(format="%Y", domain=False, tickSize=0),
            ),
            alt.Y("sum(count):Q", stack="center", axis=None),
            alt.Color("series:N", scale=alt.Scale(scheme="category20b")),
        )
        .properties(width="container")
        .interactive()
    )

    vega_component.update(chart)


# -----------------------------------------------------------------------------
# Interface
# -----------------------------------------------------------------------------


@tr.change("active")
def update_chart(active="ScatterMatrix", **kwargs):
    globals()[active]()


example_charts = [
    {"text": "Scatter Matrix", "value": "ScatterMatrix"},
    {"text": "US Income By State", "value": "USIncomeByState"},
    # {"text": "Stacked Density Estimates", "value": "StackedDensityEstimates"},
    {"text": "StreamGraph", "value": "StreamGraph"},
]

layout = SinglePage("Altair Plotting Demo", on_ready=update_chart)
layout.title.set_text("Altair Chart examples")

# Overwrite icon
layout.toolbar.children[0] = vuetify.VIcon("mdi-chart-donut-variant", classes="mr-2")

with layout.toolbar:
    vuetify.VSpacer()
    vuetify.VSelect(
        v_model=("active", "ScatterMatrix"),
        items=("examples", example_charts),
        dense=True,
        hide_details=True,
        style="max-width: 240px;",
    )


# Why does this work
vega_component = vega.VegaEmbed(name="myChart", style="width: 100%;")
with layout.content:
    vuetify.VContainer(vega_component, classes="text-center")

# -----------------------------------------------------------------------------
# Start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
