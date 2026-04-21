# Ensure this is imported so that mimetypes.init() is decorated
import trame.assets.mimetypes  # noqa: F401
from trame.app.core import get_client, get_server
from trame.app.klass import TrameApp, TrameComponent

__all__ = [
    "get_server",
    "get_client",
    "TrameApp",
    "TrameComponent",
]
