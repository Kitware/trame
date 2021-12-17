from trame.internal.app import get_app_instance
from trame.html import AbstractElement

from simput.pywebvue.modules import SimPut

# Make sure used module is available
_app = get_app_instance()
_app.enable_module(SimPut)


class Simput(AbstractElement):
    """
    Simput data management component. This must be set as the root of a layout to provide children with Simput data. See simput docs |simput_link| for more info.

    .. |simput_link| raw:: html

        <a href="https://github.com/Kitware/py-simput" target="_blank">here</a>

    :param ui_manager: See simput docs |simput_link| for more info
    :param domains_manager: See simput docs |simput_link| for more info
    :param prefix: Constructing a Simput component will set several variables, optionally prefixed by a namespace
    :type prefix:  str | None
    :param children: The children nested within this element
    :type children:  str | list[trame.html.*] | trame.html.* | None

    >>> layout.root = simput.Simput(ui_manager, prefix="myForm")
    """

    def __init__(
        self, ui_manager, domains_manager=None, prefix=None, children=None, **kwargs
    ):
        super().__init__("Simput", children, **kwargs)
        ns = f"simput_{self._id}"
        if prefix:
            ns = prefix
        self._simput_helper = SimPut.create_helper(
            ui_manager, domains_manager, namespace=ns
        )
        self._attributes["wsClient"] = ':wsClient="wsClient"'
        self._attributes["namespace"] = f'namespace="{ns}"'

    @property
    def controller(self):
        """
        Simput helper object
        """
        return self._simput_helper

    def apply(self):
        """
        Flush modified properties so they can be pushed to their concrete objects
        """
        self._simput_helper.apply()

    def reset(self):
        """
        Unapply properties
        """

        self._simput_helper.reset()

    def push(self, id=None, type=None):
        """
        Ask server to push data, ui, or constraints
        """
        self._simput_helper.push(id, type)

    def update(self, change_set):
        """
        List of properties and value to update

        >>> change_set = [
        ... {"id":"12", "name":"Radius", "value": 0.75},
        ... {"id": "12", "name":"Resolution", "value": 24}
        ... ]

        """
        self._simput_helper.update(change_set)

    def refresh(self, id=0, property=""):
        self._simput_helper.refresh(id, property)

    @property
    def changeset(self):
        """
        All unapplied changesets
        """
        return self._simput_helper.changeset()

    @property
    def has_changes(self):
        """
        Does the changeset have content?
        """
        return self._simput_helper.has_changes

    @property
    def auto_update(self):
        """
        Whether to automatically apply changes
        """
        return self._simput_helper.auto_update

    @auto_update.setter
    def auto_update(self, value):
        self._simput_helper.auto_update = value


class SimputItem(AbstractElement):
    """
    Simput data display component. This must be child of a Simput component to have access to Simput data. See simput docs |simput_link| for more info.

    :param itemId: The simput id of the data to display
    :type itemId: str
    :param extract: Columns to make available from this component to its children
    :type extract: list[str]
    :param no_ui: Whether to show simput template UI
    :type no_ui: bool
    :param children: The children nested within this element
    :type children:  str | list[trame.html.*] | trame.html.* | None

    Events

    :param dirty: Function to call when itemId is changed
    :type dirty: function
    """

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
