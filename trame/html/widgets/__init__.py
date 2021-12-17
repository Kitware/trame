from trame.internal.app import get_app_instance
from trame.html import AbstractElement
from pywebvue.modules import Widgets

# Make sure used module is available
_app = get_app_instance()
_app.enable_module(Widgets)


class FloatCard(AbstractElement):
    """
    A |floatcard_vuetify_link| which floats above the application and can be moved freely from a handle

    .. |floatcard_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-card" target="_blank">vuetify VCard container</a>


    :param handle_color:
    :param handle_position:
    :param handle_size:
    :param location:

    Vuetify VCard attributes

    :param color:
    :param dark:
    :param flat:
    :param height:
    :param elevation:
    :param hover:
    :param img:
    :param light:
    :param loader_height:
    :param loading:
    :param max_height:
    :param max_width:
    :param min_height:
    :param min_width:
    :param outlined:
    :param raised:
    :param rounded:
    :param shaped:
    :param tile:
    :param width:
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("kw-float-card", children, **kwargs)
        self._attr_names += [
            "handle_color",
            "handle_position",
            "handle_size",
            "location",
            "color",
            "dark",
            "flat",
            "height",
            "elevation",
            "hover",
            "img",
            "light",
            "loader_height",
            "loading",
            "max_height",
            "max_width",
            "min_height",
            "min_width",
            "outlined",
            "raised",
            "rounded",
            "shaped",
            "tile",
            "width",
        ]


class ListBrowser(AbstractElement):
    """
    A component that list items that be used for browsing directories or simple item picking

    :param list: List stored in state
    :param filter: Function to filter list
    :param path_icon:
    :param path_selected_icon:
    :param filter_icon:
    :param path:
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("kw-list-browser", children, **kwargs)
        self._attr_names += [
            "path_icon",
            "path_selected_icon",
            "filter_icon",
            "filter",
            "path",
            "list",
        ]


class GitTree(AbstractElement):
    """
    A component to present a Tree the same way Git does it (Like a subway map)

    :param sources: All of the elements of the tree
    :param actives: Any active elements of the tree

    Vuetify styling attributes

    :param active_background:
    :param delta_x:
    :param delta_y:
    :param font_size:
    :param margin:
    :param multiselect:
    :param offset:
    :param palette:
    :param radius:
    :param root_id:
    :param stroke:
    :param width:
    :param active_circle_stroke_color:
    :param not_visible_circle_fill_color:
    :param text_color:
    :param text_weight:
    :param action_map:
    :param action_size:

    Events

    :param actives_change:
    :param visibility_change:
    :param action:

    """

    def __init__(self, children=None, **kwargs):
        super().__init__("kw-git-tree", children, **kwargs)
        self._attr_names += [
            "sources",
            "actives",
            "active_background",
            "delta_x",
            "delta_y",
            "font_size",
            "margin",
            "multiselect",
            "offset",
            "palette",
            "radius",
            "root_id",
            "stroke",
            "width",
            "active_circle_stroke_color",
            "not_visible_circle_fill_color",
            "text_color",
            "text_weight",
            "action_map",
            "action_size",
        ]
        self._event_names += [
            ("actives_change", "activesChange"),
            ("visibility_change", "visibilityChange"),
            "action",
        ]
