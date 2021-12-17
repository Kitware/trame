from trame.internal.app import get_app_instance
from trame.html import AbstractElement
from pywebvue.modules import Deck
import json

# Make sure used module is available
_app = get_app_instance()
_app.enable_module(Deck)


class Deck(AbstractElement):
    """
    Deck.gl component. See vue-deck docs |deck_link| for more info.

    .. |deck_link| raw:: html

        <a href="https://github.com/localeai/vue-deck.gl" target="_blank">here</a>

    :param name: Identifier for this element in shared state. Generated if not given
    :type name:  str | None
    :param deck: pydeck instance to display
    :param mapboxApiKey: See vue-deck docs |deck_link| for more info
    :param tooltip: See vue-deck docs |deck_link| for more info
    :param customLibraries: See vue-deck docs |deck_link| for more info
    """

    @staticmethod
    def to_jsonInput(deck):
        """
        Serialize pydeck instance
        """
        return json.loads(deck.to_json())

    def __init__(self, name=None, deck=None, **kwargs):
        super().__init__("Deck", **kwargs)
        self._deck = deck
        self._attr_names += ["mapboxApiKey", "tooltip", "customLibraries"]
        self._name = name or f"deck_{self._id}"
        self._attributes["jsonInput"] = f':jsonInput="{self._name}"'
        self.update(deck)

    def update(self, deck=None):
        """
        Change the deck this component displays

        :param deck: pydeck instance to display
        """
        if deck:
            self._deck = deck
        if self._deck:
            _app = get_app_instance()
            _app.set(self._name, Deck.to_jsonInput(self._deck))
