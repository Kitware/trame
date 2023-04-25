from trame_server import Server, Client
from trame_client.widgets.core import VirtualNode

# Ensure this is imported so that mimetypes.init() is decorated
import trame.app.mimetypes  # noqa: F401

DEFAULT_NAME = "trame"
AVAILABLE_SERVERS = {}
AVAILABLE_CLIENTS = {}


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
        AVAILABLE_SERVERS[name] = server
        return server

    # No server available for given name
    return None


def get_client(url=None, hot_reload=False, **kwargs):
    """
    Return a client to a remote trame applications.
    If a url is given and such client is not available yet,
    it will be created otherwise the previously created instance will be returned.

    :param url: Websocket URL which to connect to.
    :type url: str


    :param hot_reload: Enable when state change function should be hot reloaded.
    :type hot_reload: bool

    :param **kwargs: any extra keyword args use for authentication configuration.

    :return: Return a unique Client instance per given url. Each instance need to a connect() call.
    :rtype: trame_server.client.Client
    """
    if url in AVAILABLE_CLIENTS:
        return AVAILABLE_CLIENTS[url]

    client = Client(url=url, config=kwargs, hot_reload=hot_reload)
    if url is not None:
        AVAILABLE_CLIENTS[url] = client

    return client


__all__ = [
    "get_server",
    "get_client",
]
