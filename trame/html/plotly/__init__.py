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

    def __init__(self, _name, figure=None, **kwargs):
        super().__init__(
            "Plotly",
            data=(f"{_name}_figure.data",),
            layout=(f"{_name}_figure.layout",),
            **kwargs,
        )
        self.__figure_key = f"{_name}_figure"
        self.__figure_data = figure
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
        self._event_names += [
            ("after_export", "afterexport"),
            ("after_plot", "afterplot"),
            ("animated", "animated"),
            ("animating_frame", "animatingframe"),
            ("animation_interrupted", "animationinterrupted"),
            ("auto_size", "autosize"),
            ("before_export", "beforeexport"),
            ("button_clicked", "buttonclicked"),
            ("click", "click"),
            ("click_annotation", "clickannotation"),
            ("deselect", "deselect"),
            ("double_click", "doubleclick"),
            ("framework", "framework"),
            ("hover", "hover"),
            ("legend_click", "legendclick"),
            ("legend_double_click", "legenddoubleclick"),
            ("relayout", "relayout"),
            ("restyle", "restyle"),
            ("redraw", "redraw"),
            ("selected", "selected"),
            ("selecting", "selecting"),
            ("slider_change", "sliderchange"),
            ("slider_end", "sliderend"),
            ("slider_start", "sliderstart"),
            ("transitioning", "transitioning"),
            ("transition_interrupted", "transitioninterrupted"),
            ("unhover", "unhover"),
        ]
        self.update()

    def update(self, plotly_fig=None):
        if plotly_fig:
            self.__figure_data = plotly_fig

        if self.__figure_data:
            state[self.__figure_key] = safe_figure(self.__figure_data.to_plotly_json())

class Figure(Plotly):
    pass