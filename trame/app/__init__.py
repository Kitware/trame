import os
import logging
from trame_server import Server, Client
from trame_server.core import set_default_client_type, DEFAULT_CLIENT_TYPE
from trame_client.widgets.core import VirtualNode

# Ensure this is imported so that mimetypes.init() is decorated
import trame.app.mimetypes  # noqa: F401

DEFAULT_NAME = "trame"
AVAILABLE_SERVERS = {}
AVAILABLE_CLIENTS = {}

logger = logging.getLogger(__name__)


def trame_3_warning(*args, **kwargs):
    if os.environ.get("TRAME_DISABLE_V3_WARNING", 0):
        return

    logger.warning("")
    logger.warning("-" * 80)
    logger.warning(
        "   !!! You are currently using trame@3 which may break your application !!!"
    )
    logger.warning("-" * 80)
    logger.warning(
        "\n 1. trame@3 only provides by default trame.widgets.[html,client] and remove"
        "\n    everything else as implicit dependency. Those other widgets will still"
        "\n    exist and will be supported, but they will need to be defined as a"
        "\n    dependency of your application."
        "\n"
        "\n       $ pip install trame-vtk trame-vuetify trame-plotly"
        "\n"
        "\n    Import paths are remaining the same."
        "\n"
        "\n    For libraries like vuetify since they offer different API between"
        "\n    their vue2 and vue3 implementation, the widget name will reflect"
        "\n    which vue version they are referencing. But original naming will remain."
        "\n"
        "\n       from trame.widgets import vuetify2, vuetify3"
        "\n\n"
        "\n 2. trame@3 aims to use vue3 as a new default. But to smooth the transition"
        "\n    we will maintain the server.client_type = 'vue2' default until"
        "\n    December 2023 which is the vue2 EOL."
        "\n"
        "\n    After that time, the new default will be switched to 'vue3'."
        "\n    Vue2 will still work 'forever' and many of the new widgets will be"
        "\n    written to support both versions."
        "\n"
        "\n    If you have a 'vue2' application and don't need or want to update your code,"
        "\n    you can still use trame@3 with vue2 by setting `server.client_type='vue2'."
        "\n"
        "\n Actions items"
        "\n ~~~~~~~~~~~~~"
        "\n   a. Make sure you set `server.client_type` to either 'vue2' or 'vue3'."
        "\n   b. List the expected dependencies or have a 'trame<3' dependency"
        "\n"
    )
    logger.warning("-" * 80)
    logger.warning(f" => Current client_type default: {DEFAULT_CLIENT_TYPE}")
    logger.warning("-" * 80)
    logger.warning("")


# ---------------------------------------------------------
# After December 2023 we will switch to vue3
# ---------------------------------------------------------
set_default_client_type("vue2")
# ---------------------------------------------------------


def apply_client_type(server, client_type=None):
    if client_type is not None:
        server.client_type = client_type
    return server


def get_server(name=None, create_if_missing=True, client_type=None, **kwargs):
    """
    Return a server for serving trame applications.
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
    if client_type is None:
        trame_3_warning()

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
