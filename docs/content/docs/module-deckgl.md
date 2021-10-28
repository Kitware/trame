# deck.gl 
Trame leverages pydeck [(see docs and examples)](https://deckgl.readthedocs.io/en/latest/) to build data layers which deck.gl then renders. Developers can make interactive data layers on top of base map providers like [Mapbox](https://github.com/Kitware/trame/blob/3cec4490d9a550d61e44dc1a4c1b059c66a2ce54/examples/PlainPython/GeoMaps/MappingDemo/app.py#L10).

```python
from trame.html import deckgl
import pydeck as pdk

# Make data chart with pydeck
pydeck_parameters = # ... (skipped, see pydeck docs)

deck = pdk.Deck(**pydeck_parameters)

# UI Component
deckgl.Deck(deck)
```
[![deck gl](./module-deckgl-pydeck.jpg)](https://deckgl.readthedocs.io/en/latest/)

# Interactivity
Trame's deck.gl component can make maps interactive by responding to updates in the data. When clicked, this Vuetify button will adjust the map by 10 degress latitude. More examples of interactive maps in Trame are [here](https://github.com/Kitware/trame/blob/master/examples/PlainPython/GeoMaps/UberPickupsNYC) and [here](https://github.com/Kitware/trame/blob/master/examples/PlainPython/GeoMaps/MappingDemo).
```python
# Continued from example above...

def increase_latitude():
    initial_state_view["latitude"] += 1
    updatedDeck = pdk.Deck(**initial_state_view, **layers)

    myMap.update(updatedDeck) # Update UI component

VBtn("Increase latitude", click=increase_latitude)
```
