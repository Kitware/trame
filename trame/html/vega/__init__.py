from trame import get_app_instance
from trame.html import AbstractElement

from pywebvue.modules import VegaEmbed

# Make sure used module is available
_app = get_app_instance()
_app.enable_module(VegaEmbed)


class VegaEmbed(AbstractElement):
    @staticmethod
    def altair_to_spec(chart):
        return chart.to_dict()

    def __init__(self, chart=None, name=None, **kwargs):
        super().__init__("VegaEmbed", **kwargs)
        self._chart = chart
        self._name = name or f"chart_{self._id}"
        self._attributes["spec"] = f':spec="{self._name}"'

    def update(self, chart=None):
        if chart:
            self._chart = chart
        if self._chart:
            _app = get_app_instance()
            _app.set(self._name, VegaEmbed.altair_to_spec(self._chart))
