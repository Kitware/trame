from trame import get_app_instance
from trame.html import AbstractElement

from simput.pywebvue.modules import SimPut

# Make sure used module is available
_app = get_app_instance()
_app.enableModule(SimPut)


class Simput(AbstractElement):
    def __init__(self, ui_manager, __content=None, **kwargs):
        super().__init__("Simput", __content, **kwargs)
        ns = f"simput_{self._id}"
        self._simput_helper = SimPut.create_helper(ui_manager, namespace=ns)
        self._attributes["wsClient"] = ':wsClient="wsClient"'
        self._attributes["namespace"] = f'namespace="{ns}"'

    @property
    def controller(self):
        return self._simput_helper


class SimputItem(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("SimputItem", __content, **kwargs)
        self._attr_names += [
            "itemId",
            "noUi",
        ]
        self._event_names += [
            "dirty",
        ]
