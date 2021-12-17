import trame.internal as tri

NEXT_TRIGGER_ID = 0
TRIGGER_MAP = {}


def trigger_key(_fn):
    """
    Providing a function, a generated trigger name will be returned.
    The function will return the same string for the same function.

    Parameters
    ----------
    :param _fn: Function that we would like to be able to call from the client
                side.
    :type _fn: function
    :returns: Unique name that can be used for a trigger to call that function
    :rtype: str
    """
    # Return precomputed key
    global TRIGGER_MAP, NEXT_TRIGGER_ID
    if _fn in TRIGGER_MAP:
        return TRIGGER_MAP[_fn]

    # Compute unique trigger key
    NEXT_TRIGGER_ID += 1
    key = f"trigger_{NEXT_TRIGGER_ID}"
    TRIGGER_MAP[_fn] = key

    # Register function trigger
    _app = tri.get_app_instance()
    _app.trigger(key)(_fn)

    return key
