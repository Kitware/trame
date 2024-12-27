from __future__ import annotations

import logging
from typing import Literal

from trame_client.widgets.core import VirtualNode
from trame_server import Client, Server
from trame_server.core import set_default_client_type

# Ensure this is imported so that mimetypes.init() is decorated
import trame.app.mimetypes  # noqa: F401

DEFAULT_NAME = "trame"
AVAILABLE_SERVERS: dict[str, Server] = {}
AVAILABLE_CLIENTS: dict[str, Client] = {}

logger = logging.getLogger(__name__)

set_default_client_type("vue3")


def apply_client_type(server: Server, client_type: str | None = None) -> Server:
    if client_type is not None:
        server.client_type = client_type
    return server


def get_server(
    name: str | Server | None = None,
    create_if_missing: bool = True,
    client_type: Literal["vue2", "vue3"] | None = None,
    **kwargs,
) -> Server | None:
    """Return a server for serving trame applications.

    If a name is given and such server is not available yet,
    it will be created otherwise the previously created instance will be returned.

    :param name: A server name identifier which can be useful when several servers
                are expected to be created. Most of the time, passing no arguments
                is what you are looking for. Also an actual Server instance can be
                provided so you can use it as a decorator function.
    :type name: None | str | Server instance

    :param create_if_missing: By default if a server for a given name does not exist
        that method will create it.
    :type create_if_missing: bool

    :param client_type: If provided, it will set it on the server.
    :type client_type: None | "vue2" | "vue3"

    :param **kwargs: any extra keyword args are passed as option to the server instance.

    :return: Return a unique Server instance per given name.
    :rtype: trame_server.core.Server
    """
    # Convenient method for decorator like usage
    if isinstance(name, Server):
        return apply_client_type(name, client_type)

    if name is None:
        name = DEFAULT_NAME

    if name in AVAILABLE_SERVERS:
        return apply_client_type(AVAILABLE_SERVERS[name], client_type)

    if create_if_missing:
        server = Server(name, VirtualNode, **kwargs)
        AVAILABLE_SERVERS[name] = server

        return apply_client_type(server, client_type)

    # No server available for given name
    return None


def get_client(
    url: str | None = None,
    hot_reload: bool = False,
    **kwargs,
) -> Client:
    """Return a client to a remote trame applications.

    If a url is given and such client is not available yet,
    it will be created otherwise the previously created instance will be returned.

    :param url: Websocket URL which to connect to.
    :type url: str


    :param hot_reload: Enable when state change function should be hot reloaded.
    :type hot_reload: bool

    :param **kwargs: any extra keyword args use for authentication configuration.

    :return: Return a unique Client instance per given url. Each instance needs to call
             connect().
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
