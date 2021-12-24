from trame.internal.app import get_app_instance
from trame import state
from trame.html import AbstractElement

from pywebvue.modules import Plotly

# Make sure used module is available
_app = get_app_instance()
_app.enable_module(Plotly)

try:
    import numpy as np
except:
    pass


def safe_data(data):
    """Replace numpy array to list()"""
    result = []
    for item in data:
        for name in ["x", "y", "z"]:
            if name in item and isinstance(item[name], (np.ndarray, np.generic)):
                item[name] = item[name].tolist()

        result.append(item)

    return result


def safe_figure(fig):
    return {
        "data": safe_data(fig["data"]),
        "layout": fig["layout"],
    }


class Plotly(AbstractElement):
    """
    Create a Plotly figure element
    """

    def __init__(self, _name, **kwargs):
        super().__init__(
            "Plotly",
            data=(f"{_name}_figure.data",),
            layout=(f"{_name}_figure.layout",),
            **kwargs,
        )
        self.__figure_key = f"{_name}_figure"
        state[self.__figure_key] = {"data": [], "layout": {}}
        self._attr_names += [
            "data",
            "layout",
            ("display_mode_bar", "displayModeBar"),
            ("scroll_zoom", "scrollZoom"),
            "editable",
            ("static_plot", "staticPlot"),
            "format",
            "filename",
            "height",
            "width",
            "scale",
            ("mode_bar_buttons_to_remove", "modeBarButtonsToRemove"),
            ("mode_bar_buttons_to_add", "modeBarButtonsToAdd"),
            "locale",
            "displaylogo",
            "responsive",
            ("double_click_delay", "doubleClickDelay"),
        ]

    def update(self, plotly_fig):
        state[self.__figure_key] = safe_figure(plotly_fig.to_plotly_json())
