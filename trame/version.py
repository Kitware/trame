# When we require python 3.8, we can use importlib.metadata instead...
from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution("trame").version
except DistributionNotFound:
    # package is not installed
    __version__ = None
