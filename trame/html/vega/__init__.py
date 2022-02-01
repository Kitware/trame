from trame import state
from trame.internal.app import get_app_instance
from trame.html import AbstractElement

from pywebvue.modules import VegaEmbed

# Make sure used module is available
_app = get_app_instance()
_app.enable_module(VegaEmbed)


class VegaEmbed(AbstractElement):
    """
    Vega component. See vega docs |vega_link| for more info.

    .. |vega_link| raw:: html

        <a href="https://github.com/vega/vega-embed" target="_blank">here</a>

    :param chart: The chart to display. Defaults to None.
    :param name: The identifier of this components data in shared state. Generated if not given.
    """

    @staticmethod
    def altair_to_spec(chart):
        """
        Serialize altair chart
        """
        return chart.to_dict()

    def __init__(self, name=None, chart=None, **kwargs):
        super().__init__("VegaEmbed", **kwargs)
        self._chart = chart
        self._name = name or f"chart_{self._id}"
        self._attributes["spec"] = f':spec="{self._name}"'
        state[self._name] = None
        self.update()

    def update(self, chart=None):
        """
        Change which chart is displayed

        :param chart: The chart to display. Defaults to None.
        """
        if chart:
            self._chart = chart
        if self._chart:
            _app = get_app_instance()
            _app.set(self._name, VegaEmbed.altair_to_spec(self._chart))
