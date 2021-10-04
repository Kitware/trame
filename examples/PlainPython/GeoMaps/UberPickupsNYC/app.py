"""An example of showing geographic data."""

import os
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

from trame.vegaEmbed import VegaEmbed
from trame.deckgl import Deck
from trame import start, change, update_state
from trame.layouts import SinglePage
from trame.html import Div
from trame.html.vuetify import VSlider, VRow, VCol, VContainer

# -----------------------------------------------------------------------------
# GUI Components
# -----------------------------------------------------------------------------
dynamicTitle = "{{nycTitle}} from {{pickupHour}}:00 and {{pickupHour + 1}}:00"

hourBreakdownChart = VegaEmbed(style="width: 100%")

mapProps = {
    "classes": "elevation-5",
    "mapboxApiKey": os.environ["MAPBOX_API_KEY"],
    "style": "height: 50vh;",
}

nycMap = Deck(**mapProps)
jfkMap = Deck(**mapProps)
lgaMap = Deck(**mapProps)
nwkMap = Deck(**mapProps)

# -----------------------------------------------------------------------------
# GUI Layout
# -----------------------------------------------------------------------------
layout = SinglePage("NYC Uber Ridesharing Data")
layout.title.content = "NYC Uber Ridesharing Data"
layout.logo.content = "mdi-chart-donut-variant"

mapRow = VRow(
    [
        VCol([Div("{{jfkTitle}}", classes="text-h5"), jfkMap], cols=4),
        VCol([Div("{{lgaTitle}}", classes="text-h5"), lgaMap], cols=4),
        VCol([Div("{{nwkTitle}}", classes="text-h5"), nwkMap], cols=4),
    ]
)

mapLayout = VRow(
    children=[
        VCol(
            cols=4,
            children=[Div(dynamicTitle, classes="text-h5"), nycMap],
        ),
        VCol(
            cols=8,
            children=[mapRow],
        ),
    ]
)

layout.content.children += [
    VContainer(
        fluid="true",
        children=[
            Div(
                """Examining how Uber pickups vary over time in New York City's 
                and at its major regional airports.
                By sliding the slider on the left you can view different slices 
                of time and explore different transportation trends.""",
                classes="text-body-1",
            ),
            VSlider(
                v_model=("pickupHour", 0),
                classes="mt-4",
                label="Select hour of pickup",
                min=0,
                max=23,
                thumb_label=True,
            ),
            mapLayout,
            Div(
                classes="text-center mt-6",
                children=[hourBreakdownChart],
            ),
        ],
    )
]


# -----------------------------------------------------------------------------
# LOADING DATA
# -----------------------------------------------------------------------------
DATE_TIME = "date/time"
DATA_URL = (
    "http://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)


def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data


data = load_data(100000)

# CREATING FUNCTION FOR MAPS

map_list = [
    {
        "id": "nyc",
        "title": "All New York City",
        "lat": np.average(data["lat"]),
        "lon": np.average(data["lon"]),
        "zoom": 11,
        "mapRef": nycMap,
    },
    {
        "id": "lga",
        "title": "La Guardia Airport",
        "lat": 40.7900,
        "lon": -73.8700,
        "zoom": 12,
        "mapRef": lgaMap,
    },
    {
        "id": "jfk",
        "title": "JFK Airport",
        "lat": 40.6650,
        "lon": -73.7821,
        "zoom": 11,
        "mapRef": jfkMap,
    },
    {
        "id": "nwk",
        "title": "Newark Airport",
        "lat": 40.7090,
        "lon": -74.1805,
        "zoom": 11,
        "mapRef": nwkMap,
    },
]


def updateMap(data, lat, lon, zoom, mapRef, **kwarg):
    deck = pdk.Deck(
        map_provider="mapbox",
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["lon", "lat"],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ],
    )
    mapRef.update(deck)
    update_state(f'{kwarg["id"]}Title', kwarg["title"])


@change("pickupHour")
def updateData(pickupHour=0, **kwargs):
    update_state(
        "chartTitle",
        f"All New York City from {pickupHour}:00 and {pickupHour + 1}:00",
    )

    # FILTERING DATA BY HOUR SELECTED
    filtered_data = data[data[DATE_TIME].dt.hour == pickupHour]

    for item in map_list:
        updateMap(filtered_data, **item)

    # FILTERING DATA FOR THE HISTOGRAM
    filtered = filtered_data[
        (data[DATE_TIME].dt.hour >= pickupHour)
        & (data[DATE_TIME].dt.hour < (pickupHour + 1))
    ]

    hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]

    chart_data = pd.DataFrame({"minute": range(60), "pickups": hist})

    # LAYING OUT THE HISTOGRAM SECTION
    hourBreakdownChart.update(
        alt.Chart(chart_data)
        .mark_area(
            interpolate="step-after",
        )
        .properties(width="container", height=150)
        .encode(
            x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
            y=alt.Y("pickups:Q"),
            tooltip=["minute", "pickups"],
        )
        .configure_mark(opacity=0.5, color="red")
    )


# -----------------------------------------------------------------------------
# Start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    start(layout, on_ready=updateData)
