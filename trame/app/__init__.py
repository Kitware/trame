from trame_server import Server
from trame_client import module
from trame_client.widgets.core import VirtualNode

# Ensure this is imported so that mimetypes.init() is decorated
import trame.app.mimetypes  # noqa: F401

DEFAULT_NAME = "trame"
AVAILABLE_SERVERS = {}


def get_server(name=None, create_if_missing=True, **kwargs):
    """
    Return a server for serving trame applications.
    If a name is given and such server is not available yet,
    it will be created otherwise the previously created instance will be returned.

    :param name: A server name identifier which can be useful when several servers
                are expected to be created. Most of the time, passing no arguments
                is what you are looking for.
    :type name: str


    :param create_if_missing: By default if a server for a given name does not exist
        that method will create it.
    :type create_if_missing: bool

    :param **kwargs: any extra keyword args are passed as option to the server instance.

    :return: Return a unique Server instance per given name.
    :rtype: trame_server.core.Server
    """
    if name is None:
        name = DEFAULT_NAME

    if name in AVAILABLE_SERVERS:
        return AVAILABLE_SERVERS[name]

    if create_if_missing:
        server = Server(name, VirtualNode, **kwargs)
        server.enable_module(module)  # Always load html module first
        AVAILABLE_SERVERS[name] = server
        return server

    # No server available for given name
    return None


__all__ = [
    "get_server",
]
