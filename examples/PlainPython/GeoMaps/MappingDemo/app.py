import pydeck as pdk
import pandas as pd
import os

from trame import start, change, update_state
from trame.layouts import SinglePage
from trame.html import vuetify, deckgl


# -----------------------------------------------------------------------------
# Getting a Mapbox API key
# -----------------------------------------------------------------------------
# By default, pydeck 0.6 provides basemap tiles through Carto.
#
# You can optionally use a Mapbox API key, by registering for Mapbox via
# this link [1]. You should then create a new public API token [2].
# You can learn more about Mapbox tokens via their documentation [3].
#
# [1] https://account.mapbox.com/auth/signup/
# [2] https://account.mapbox.com/access-tokens/
# [3] https://docs.mapbox.com/help/how-mapbox-works/access-tokens/#how-access-tokens-work
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# GUI Components
# -----------------------------------------------------------------------------
# Expect MAPBOX_API_KEY environment variable
deckMap = deckgl.Deck(
    mapboxApiKey=os.environ["MAPBOX_API_KEY"],
    style="width: 100vw;",
    classes="fill-height",
)

# -----------------------------------------------------------------------------
# GUI Layout
# -----------------------------------------------------------------------------

layout = SinglePage("Deck + Mapbox Demo")
layout.title.content = "Deck + Mapbox Demo"
layout.content.children += [
    deckMap,
    vuetify.VSelect(
        style="position: absolute; top: 10px; left: 25px; width: 600px;",
        items=(
            "layerNames",
            [
                "Bike Rentals",
                "Bart Stop Exits",
                "Bart Stop Names",
                "Outbound Flow",
            ],
        ),
        v_model=(
            "activeLayers",
            [
                "Bike Rentals",
                "Bart Stop Exits",
                "Bart Stop Names",
                "Outbound Flow",
            ],
        ),
        dense=True,
        hide_details=True,
        multiple=True,
        chips=True,
    ),
]
# -----------------------------------------------------------------------------


def from_data_file(filename):
    url = (
        "https://raw.githubusercontent.com/streamlit/"
        "example-data/master/hello/v1/%s" % filename
    )
    return pd.read_json(url)


ALL_LAYERS = {
    "Bike Rentals": pdk.Layer(
        "HexagonLayer",
        data=from_data_file("bike_rental_stats.json"),
        get_position=["lon", "lat"],
        radius=200,
        elevation_scale=4,
        elevation_range=[0, 1000],
        extruded=True,
    ),
    "Bart Stop Exits": pdk.Layer(
        "ScatterplotLayer",
        data=from_data_file("bart_stop_stats.json"),
        get_position=["lon", "lat"],
        get_color=[200, 30, 0, 160],
        get_radius="[exits]",
        radius_scale=0.05,
    ),
    "Bart Stop Names": pdk.Layer(
        "TextLayer",
        data=from_data_file("bart_stop_stats.json"),
        get_position=["lon", "lat"],
        get_text="name",
        get_color=[0, 0, 0, 200],
        get_size=15,
        get_alignment_baseline="'bottom'",
    ),
    "Outbound Flow": pdk.Layer(
        "ArcLayer",
        data=from_data_file("bart_path_stats.json"),
        get_source_position=["lon", "lat"],
        get_target_position=["lon2", "lat2"],
        get_source_color=[200, 30, 0, 160],
        get_target_color=[200, 30, 0, 160],
        auto_highlight=True,
        width_scale=0.0001,
        get_width="outbound",
        width_min_pixels=3,
        width_max_pixels=30,
    ),
}

defaultLayers = [
    "Bike Rentals",
    "Bart Stop Exits",
    "Bart Stop Names",
    "Outbound Flow",
]


@change("activeLayers")
def update_map(activeLayers=defaultLayers, **kwargs):
    selected_layers = [
        layer for layer_name, layer in ALL_LAYERS.items() if layer_name in activeLayers
    ]

    if selected_layers:
        deck = pdk.Deck(
            map_provider="mapbox",
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": 37.76,
                "longitude": -122.4,
                "zoom": 11,
                "pitch": 50,
            },
            layers=selected_layers,
        )
        deckMap.update(deck)
    else:
        update_state("error", "Please choose at least one layer above.")


# -----------------------------------------------------------------------------
# Start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    start(layout, on_ready=update_map)
