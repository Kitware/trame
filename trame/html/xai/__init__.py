from trame import get_app_instance
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
            "colorMode",
            "colorRange",
            "colorPreset",
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
            "maxHeight",
            "maxWidth",
            "width",
            "colors",
            "areas",
            "areaKey",
            "areaStyle",
            "areaSelected",
            "areaSelectedOpacity",
            "areaOpacity",
            "heatmaps",
            "heatmapOpacity",
            "heatmapColorPreset",
            "heatmapColorRange",
            "heatmapActive",
            "heatmapColorMode",
        ]
        self._event_names += [
            ("area_selection_change", "areaSelectionChange"),
        ]
