# Deck.gl

deck.gl is a WebGL-powered framework for visual exploratory data analysis of large datasets which has a Python layer available under [pydeck](https://pydeck.gl/).

Trame leverages pydeck (see documentation and examples [here](https://deckgl.readthedocs.io/en/latest/)) to build data layers which deck.gl then renders. Developers can make interactive data layers on top of base map providers like [Mapbox](https://github.com/Kitware/trame/blob/3cec4490d9a550d61e44dc1a4c1b059c66a2ce54/examples/PlainPython/GeoMaps/MappingDemo/app.py#L10).

[![deck gl](/trame/images/module-deckgl-pydeck.jpg)](https://deckgl.readthedocs.io/en/latest/)

## How to use it?

```python
from trame.html import deckgl
import pydeck as pdk

# Make data layer with pydeck
deck = pdk.Deck(**pydeck_parameters)
deck2 = pdk.Deck(**pydeck_parameters_2) # make a change

# Deck.gl component properties
deckgl_options = {
  "mapboxApiKey": ...,    # api token for mapbox layer
  "tooltip": False,       # whether to show tooltip
  "customLibraries": ..., # deckgl add ons
}

# Method 1 ----------------------------------------------------------------------

deck_component = deckgl.Deck(
  deck=deck, # Deck of layers to render
  **deckgl_options,
)
deck_component.update(deck2) # Make changes

# Method 2 ----------------------------------------------------------------------

deck_component2 = deckgl.Deck(
  name="myDeck", # Shared state name for deck
  **deckgl_options,
)
deck_component2.update(deck) # Set deck
deck_component2.update(deck2) # Make changes
```

## Examples

- [API](https://trame.readthedocs.io/en/latest/trame.html.deckgl.html)
- [GeoMaps/UberPickupsNYC](https://github.com/Kitware/trame/blob/master/examples/PlainPython/GeoMaps/UberPickupsNYC)
- [GeoMaps/MappingDemo](https://github.com/Kitware/trame/blob/master/examples/PlainPython/GeoMaps/MappingDemo)
