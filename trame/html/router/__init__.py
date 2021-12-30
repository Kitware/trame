from trame.internal.app import get_app_instance
from trame.html import AbstractElement
from pywebvue.modules import Router

# Make sure used module is available
_app = get_app_instance()
_app.enable_module(Router)


class RouterView(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("router-view", children=children, **kwargs)


class RouterLink(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("router-link", children=children, **kwargs)
        self._attr_names += ["to"]
