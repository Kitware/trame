from trame import get_app_instance
from trame.html import AbstractElement

from pywebvue.modules import Markdown

# Make sure used module is available
_app = get_app_instance()
_app.enableModule(Markdown)


class Markdown(AbstractElement):
    def __init__(self, **kwargs):
        super().__init__("markdown-it-vue", **kwargs)
        self._attr_names += [("v_model", ":content")]
