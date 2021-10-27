# Widgets

## FloatCard
A container which floats above the application and can be moved freely from a handle.

<center>
  <img src="./module-widgets-floatcard.gif" width="400px"/>
</center>

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

FloatCard also inherits style properties from Vuetify's v-card. See [v-card documentation](https://vuetifyjs.com/en/api/v-card/#props) for more about these: `color` `dark` `flat` `height` `elevation` `hover` `img` `light` `loader_height` `loading` `max_height` `max_width` `min_height` `min_width` `outlined` `raised` `rounded` `shaped` `tile` `width` 

<!--
# GitTree
A component to visualize a git repository.

## Parameters
#### `sources`
#### `actives`
#### `active_background`
#### `delta_x`
#### `delta_y`
#### `font_size`
#### `margin`
#### `multiselect`
#### `offset`
#### `palette`
#### `radius`
#### `root_id`
#### `stroke`
#### `width`
#### `active_circle_stroke_color`
#### `not_visible_circle_fill_color`
#### `text_color`
#### `text_weight`

[ ...example ]

# ListBrowser
A component to browse a list.
## Parameters
    m_widgets: widgets
#### `path_icon`
#### `path_selected_icon`
#### `filter_icon`
#### `filter`
#### `path`
#### `list`

[ ...example ]
-->
