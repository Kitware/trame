import mpld3
from trame import state

from trame.html import AbstractElement
from trame.internal.app import get_app_instance
from trame.internal.utils.numpy import safe_serialization

# Only available 2.7.0+
from pywebvue.modules import Matplotlib as module

# Make sure used module is available
_app = get_app_instance()
_app.enable_module(module)


class Figure(AbstractElement):
    """
    Create a matplotlib figure viewer element

    :param name: Variable name in state
    :param figure: Matplotlib figure to show (default: None)

    >>> component1 = Figure("figure_1", figure=fig1)

    >>> component2 = Figure("figure_2")
    >>> component2.update(fig2)
    """

    def __init__(self, _name, figure=None, **kwargs):
        super().__init__("matplotlib", **kwargs)
        self._key = _name
        self._attributes["name"] = f'name="{_name}"'
        self._attributes["spec"] = f':spec="{_name}"'
        self._figure = figure
        if figure is not None:
            self.update(figure)
        else:
            # Make sure we create a state entry
            state[self._key] = None

    def update(self, figure=None):
        if figure:
            self._figure = figure

        if self._figure:
            state[self._key] = safe_serialization(mpld3.fig_to_dict(self._figure))
