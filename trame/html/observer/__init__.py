from trame.html import AbstractElement
from trame.internal.app import get_app_instance
from trame import state

# Only available 2.8.0+
from pywebvue.modules import SizeObserver as module

# Make sure used module is available
_app = get_app_instance()
_app.enable_module(module)

class SizeObserver(AbstractElement):
    """
    Component following parent size and reporting its size at mount time and when size change.

    :param name: Variable name to update with size information
    """
    def __init__(self, _name, **kwargs):
        super().__init__("size-observer", name=_name, **kwargs)
        self._attr_names += ["name"]
        # Placeholder for state
        state[_name] = None
