# Deck.gl
Trame leverages pydeck (see documentation and examples [here](https://deckgl.readthedocs.io/en/latest/)) to build data layers which deck.gl then renders. Developers can make interactive data layers on top of base map providers like [Mapbox](https://github.com/Kitware/trame/blob/3cec4490d9a550d61e44dc1a4c1b059c66a2ce54/examples/PlainPython/GeoMaps/MappingDemo/app.py#L10).

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
[![deck gl](./module-deckgl-pydeck.jpg)](https://deckgl.readthedocs.io/en/latest/)

More examples of interactive maps in Trame are [here](https://github.com/Kitware/trame/blob/master/examples/PlainPython/GeoMaps/UberPickupsNYC) and [here](https://github.com/Kitware/trame/blob/master/examples/PlainPython/GeoMaps/MappingDemo).
