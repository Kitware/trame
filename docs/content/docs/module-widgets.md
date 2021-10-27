# Kitware Widgets
These widgets are commonly used across Kitware's web tools.

# FloatCard
A container which floats above the application and can be moved freely from a handle.

## Parameters
#### `handle_color`
Sets the color for the handle on the FloatCard.
#### `handle_position`
Sets the position of the handle to either "top", "left", "right", or "bottom"
#### `handle_size`
Sets the size of the handle for the FloatCard.
#### `location`
Sets coordinates of the FloatCard's location on the page with a list of coordinates `[x, y]`.

## Inherited Parameters
FloatCard inherits these parameters from Vuetify's v-card. See [v-card documentation](https://vuetifyjs.com/en/api/v-card/#props) for more on these properties.
#### `color`
#### `dark`
#### `flat`
#### `height`
#### `elevation`
#### `hover`
#### `img`
#### `light`
#### `loader_height`
#### `loading`
#### `max_height`
#### `max_width`
#### `min_height`
#### `min_width`
#### `outlined`
#### `raised`
#### `rounded`
#### `shaped`
#### `tile`
#### `width`

## Example Usage
```python
from trame.html import widgets

widgets.FloatCard("Move this card wherever you like")
```

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
