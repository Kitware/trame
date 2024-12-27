from trame_client.widgets.core import AbstractElement

__all__ = [
    "create_class",
]


def create_class(
    class_name,
    component_name,
    properties=[],
    events=[],
    module=None,
):
    """Helper for creating Widget class

    Args:
        class_name (string): name of the Python generated class
        component_name (string): name of the vue component
        properties (list, optional): List of properties mapping. Defaults to [].
        events (list, optional): List of events mapping. Defaults to [].
        module (dict, optional): Module to enable when using the class. Defaults to None.
    """

    def constructor(self, **kwargs):
        AbstractElement.__init__(self, component_name, **kwargs)
        if module is not None:
            self.server.enable_module(module)
        self._attr_names += properties
        self._event_names += events

    return type(
        class_name,
        (AbstractElement,),
        dict(__init__=constructor),
    )
