from trame import get_app_instance


def update_state(key, value=None, force=False):
    """
    Updating the current application state that is shared with the Web UI

    :param key: The key for the value we wish to update
    :type key: str
    :param value: The new value
    :type value: Any
    :param force: Set to True when you want to force push a new or same value to the client.
    :type force: bool

    >>> update_state("workload_finished",  True)

    update_state() may not detect a change if the same reference is passed
    even if its content has change. You have the option to let the system
    know that you want to force the update.

    >>> a = { "x": 1 }
    >>> update_state("a", a)
    >>> a["x"] = 2
    >>> update_state("a", a, force=True)

    Sometime you may want to update a set of variables at once without
    triggering any @change callback. To do so, just provide a dictionary.
    Even if no @change is called, the client will receive the updated
    modified change.

    >>> change_set = { "a": 1, "b": 2 }
    >>> update_state(change_set)

    """
    _app = get_app_instance()
    if isinstance(key, dict):
        _app.state.update(key)
        _app.flush_state(*list(key.keys()))
        return key
    else:
        _app.set(key, value, force)
    return value


# -----------------------------------------------------------------------------


def get_state(*names):
    """
    Return the list of values of the given state keys or the full state
    dictionary if no key names were provided.

    :param names: List of names of state values to retreive
    :type names: list[str]
    :rtype: List[Any] | dict[str, Any]
    :returns: Either a list of values matching the given state property names or the full state dict

    >>> greeting, name  = get_state("greeting", "name")
    >>> f'{greeting}, {name}!'
    "Hello, Trame!"

    >>> greeting, = get_state("greeting")
    >>> greeting
    "Hello"

    >>> full_state = get_state()
    >>> full_state.get("greeting")
    "Hello"

    """
    _app = get_app_instance()

    if len(names):
        results = []
        for name in names:
            results.append(_app.get(name))
        return results

    return _app.state
