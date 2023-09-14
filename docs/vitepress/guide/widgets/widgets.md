# Widgets

Widgets is a small set of add-on components that tends to be useful when building applications. They mostly come from needs that were driven by applications but became part of the library as they could provide cross application benefits.

## FloatCard

A [VCard](https://vuetifyjs.com/en/components/cards/) container which floats above the application and can be moved freely from a handle.

![FloatCard example](/assets/images/widgets/module-widgets-floatcard.gif)

### How to use it?

```python
from trame.html import widgets

widgets.FloatCard(
  handle_color="#aaaaaa", # color of the handle
  handle_position="top",  # position of the handle: top, left, right, or bottom
  handle_size=12,         # size of the handle
  location=[0,0],         # coordinates of the FloatCard's location on the page
  **vuetify_vcard_props,  # Vuetify VCard properties
  children=[...]          # VCardTitle, VCardSubTitle, VCardText, VCardActions...
)
```

FloatCard also inherits style properties from Vuetify's v-card. See [v-card documentation](https://vuetifyjs.com/en/api/v-card/#props) for more about these: `color`, `dark`, `flat`, `height`, `elevation`, `hover`, `img`, `light`, `loader_height`, `loading`, `max_height`, `max_width`, `min_height`, `min_width`, `outlined`, `raised`, `rounded`, `shaped`, `tile`, `width`.

## GitTree

A component to present a Tree the same way Git does it (Like a subway map).


![GitTree example](/assets/images/widgets/module-widgets-gittree.jpg)

### How to use it?

```python
from trame.html import widgets

tree = [
  { "id": "1", "parent": "0", "visible": 1, "name": "Wavelet" },
  { "id": "2", "parent": "1", "visible": 0, "name": "Clip" },
  { "id": "3", "parent": "1", "visible": 1, "name": "Slice" },
]

selection = ["2"]

widgets.GitTree(
  sources=("tree", tree)           # bind variable with default
  actives=("selection", selection) # bind variable with default
  **styling_properties,
)
```

GitTree can by also be styled with any of these properties: `active_background`, `delta_x`, `delta_y`, `font_size`, `margin`, `multiselect`, `offset`, `palette`, `radius`, `root_id`, `stroke`, `width`, `active_circle_stroke_color`, `not_visible_circle_fill_color`, `text_color`, `text_weight`.


## ListBrowser

A component that list items that be used for browsing directories or simple item picking.

### How to use it?

```python
from trame.html import widgets

widgets.ListBrowser(
  list=("myList", [...]), # Shared state reference to the list
  filter=...,             # JS function to filter list
  **styling_properties,
)
```
ListBrowser can also be styled with any of these properties: `path_icon`, `path_selected_icon`, `filter_icon`.

## Examples

- [API](https://trame.readthedocs.io/en/latest/trame.html.widgets.html)
