from trame.internal.app import get_app_instance
from trame.html import AbstractElement

from pywebvue.modules import Markdown

# Make sure used module is available
_app = get_app_instance()
_app.enable_module(Markdown)


class Markdown(AbstractElement):
    """
    Create a markdown viewer element

    :param v_model: Variable name in state

    >>> component = Markdown(v_model=("document", "**Bold**"))

    >>> content = \"\"\"
    ...
    ... # My document
    ... 1. First
    ... 2. Second
    ... 3. Third
    ...
    ... Hello "trame"
    ... \"\"\"
    >>> component = Markdown(v_model=("document2", content))
    """

    def __init__(self, **kwargs):
        super().__init__("markdown-it-vue", **kwargs)
        self._attr_names += [("v_model", ":content")]
