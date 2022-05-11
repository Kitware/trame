"""An example of showing geographic data."""

import os
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import html, vuetify, deckgl, vega

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller

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
    },
    {
        "id": "lga",
        "title": "La Guardia Airport",
        "lat": 40.7900,
        "lon": -73.8700,
        "zoom": 12,
    },
    {
        "id": "jfk",
        "title": "JFK Airport",
        "lat": 40.6650,
        "lon": -73.7821,
        "zoom": 11,
    },
    {
        "id": "nwk",
        "title": "Newark Airport",
        "lat": 40.7090,
        "lon": -74.1805,
        "zoom": 11,
    },
]


def updateMap(data, id, lat, lon, zoom, **kwarg):
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
    ctrl[f"{id}_update"](deck)
    state[f"{id}Title"] = kwarg["title"]


@state.change("pickupHour")
def updateData(pickupHour, **kwargs):
    state.chartTitle = f"All New York City from {pickupHour}:00 and {pickupHour + 1}:00"

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
    ctrl.hour_breakdown_update(
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
# GUI Layout
# -----------------------------------------------------------------------------

dynamicTitle = "{{nycTitle}} from {{pickupHour}}:00 and {{pickupHour + 1}}:00"

mapProps = {
    "classes": "elevation-5",
    "mapboxApiKey": os.environ["MAPBOX_API_KEY"],
    "style": "height: 50vh;",
}

with SinglePageLayout(server) as layout:
    layout.title.set_text("NYC Uber Ridesharing Data")

    with layout.content:
        with vuetify.VContainer(fluid="true") as container:
            html.Div(
                """Examining how Uber pickups vary over time in New York City's
                    and at its major regional airports.
                    By sliding the slider on the left you can view different slices
                    of time and explore different transportation trends.""",
                classes="text-body-1",
            )
            vuetify.VSlider(
                v_model=("pickupHour", 0),
                classes="mt-4",
                label="Select hour of pickup",
                min=0,
                max=23,
                thumb_label=True,
            )

            with vuetify.VRow():
                with vuetify.VCol(cols=4):
                    html.Div(dynamicTitle, classes="text-h5")
                    ctrl.nyc_update = deckgl.Deck(**mapProps).update
                with vuetify.VCol(cols=8) as col:
                    with vuetify.VRow():
                        for title, name in [
                            ("{{jfkTitle}}", "jfk"),
                            ("{{lgaTitle}}", "lga"),
                            ("{{nwkTitle}}", "nwk"),
                        ]:
                            with vuetify.VCol(cols=4):
                                html.Div(title, classes="text-h5")
                                ctrl[f"{name}_update"] = deckgl.Deck(**mapProps).update

            with html.Div(classes="text-center mt-6"):
                ctrl.hour_breakdown_update = vega.Figure(style="width: 100%").update


# -----------------------------------------------------------------------------
# Start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
