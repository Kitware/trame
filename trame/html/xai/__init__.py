from trame.internal.app import get_app_instance
from trame.html import AbstractElement
from pywebvue.modules import XAI

# Make sure used module is available
_app = get_app_instance()
_app.enable_module(XAI)


class XaiHeatMap(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("xai-heat-map", children, **kwargs)
        self._attr_names += [
            "heatmap",
            "shape",
            "color_mode",
            "color_range",
            "color_preset",
        ]
        self._event_names += [
            "hover",
            "enter",
        ]


class XaiImage(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("xai-image", children, **kwargs)
        self._attr_names += [
            "src",
            "max_height",
            "max_width",
            "width",
            "colors",
            "areas",
            "area_key",
            "area_style",
            "area_selected",
            "area_selected_opacity",
            "area_opacity",
            "heatmaps",
            "heatmap_opacity",
            "heatmap_color_preset",
            "heatmap_color_range",
            "heatmap_active",
            "heatmap_color_mode",
        ]
        self._event_names += [
            ("area_selection_change", "areaSelectionChange"),
            ("color_range", "colorRange"),
            "hover",
            "enter",
        ]
