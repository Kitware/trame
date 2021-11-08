from trame import get_app_instance
from trame.html import AbstractElement
from pywebvue.modules import Widgets

# Make sure used module is available
_app = get_app_instance()
_app.enable_module(Widgets)


class FloatCard(AbstractElement):
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
        ]
        self._event_names += [
            ("actives_change", "activesChange"),
            ("visibility_change", "visibilityChange"),
        ]
