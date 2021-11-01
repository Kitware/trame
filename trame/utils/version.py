# When we require python 3.8, we can use importlib.metadata instead...
from pkg_resources import get_distribution, DistributionNotFound


def get_version():
    try:
        return get_distribution("trame").version
    except DistributionNotFound:
        # package is not installed
        pass
