from trame import get_app_instance
from trame.html import AbstractElement

from simput.pywebvue.modules import SimPut

# Make sure used module is available
_app = get_app_instance()
_app.enable_module(SimPut)


class Simput(AbstractElement):
    def __init__(self, ui_manager, prefix=None, children=None, **kwargs):
        super().__init__("Simput", children, **kwargs)
        ns = f"simput_{self._id}"
        if prefix:
            ns = prefix
        self._simput_helper = SimPut.create_helper(ui_manager, namespace=ns)
        self._attributes["wsClient"] = ':wsClient="wsClient"'
        self._attributes["namespace"] = f'namespace="{ns}"'

    @property
    def controller(self):
        return self._simput_helper

    def apply(self):
        self._simput_helper.apply()

    def reset(self):
        self._simput_helper.reset()

    def push(self, id=None, type=None):
        self._simput_helper.push(id, type)

    def update(self, change_set):
        self._simput_helper.update(change_set)

    def refresh(self, id=0, property=""):
        self._simput_helper.refresh(id, property)

    @property
    def changeset(self):
        return self._simput_helper.changeset()

    @property
    def has_changes(self):
        return self._simput_helper.has_changes

    @property
    def auto_update(self):
        return self._simput_helper.auto_update

    @auto_update.setter
    def auto_update(self, value):
        self._simput_helper.auto_update = value


class SimputItem(AbstractElement):
    def __init__(self, children=None, extract=[], **kwargs):
        super().__init__("SimputItem", children, **kwargs)
        self._attr_names += [
            ("itemId", ":itemId"),
            "no_ui",
        ]
        self._event_names += [
            "dirty",
        ]

        if extract:
            self._attributes["prop_extract"] = f'#properties="{{{", ".join(extract)}}}"'
