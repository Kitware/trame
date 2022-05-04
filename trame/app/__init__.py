from trame_server import Server
from trame_client import module

DEFAULT_NAME = "trame"
AVAILABLE_SERVERS = {}


def get_server(name=None, create_if_missing=True, **kwargs):
    """
    Return a server for serving trame applications.
    If a name is given and such server is not available yet,
    it will be created otherwise the previsouly created instance will be returned.
    """
    if name is None:
        name = DEFAULT_NAME

    if name in AVAILABLE_SERVERS:
        return AVAILABLE_SERVERS[name]

    if create_if_missing:
        server = Server(name, **kwargs)
        server.enable_module(module)  # Always load html module first
        AVAILABLE_SERVERS[name] = server
        return server

    # No server available for given name
    return None
