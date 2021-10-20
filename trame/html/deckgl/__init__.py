from trame import get_app_instance
from trame.html import AbstractElement
from pywebvue.modules import Deck
import json

# Make sure used module is available
_app = get_app_instance()
_app.enable_module(Deck)


class Deck(AbstractElement):
    @staticmethod
    def to_jsonInput(deck):
        return json.loads(deck.to_json())

    def __init__(self, name=None, deck=None, **kwargs):
        super().__init__("Deck", **kwargs)
        self._deck = deck
        self._attr_names += ["mapboxApiKey", "tooltip", "customLibraries"]
        self._name = name or f"deck_{self._id}"
        self._attributes["jsonInput"] = f':jsonInput="{self._name}"'
        self.update(deck)

    def update(self, deck=None):
        if deck:
            self._deck = deck
        if self._deck:
            _app = get_app_instance()
            _app.set(self._name, Deck.to_jsonInput(self._deck))
