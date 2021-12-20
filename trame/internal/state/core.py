from trame.internal.app import get_app_instance
from trame.internal.utils import is_dunder

from .decorators import change


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


def flush_state(*args):
    """
    Force push selected keys of the server state to the client

    :param args: Which keys to flush
    :type args: list[str]

    >>> flush_state('myNestedDict')
    """
    _app = get_app_instance()
    return _app.flush_state(*args)


def is_dirty(*args):
    """
    Check if a set of keys in an @change have been modified

    :param args: Which keys to check for modification
    :type args: list[str]
    :return: True if any of the keys in `args` are modified

    >>> @change('sound_settings', 'picture_settings')
    ... def show_changed_settings(sound_settings, picture_settings, **kwargs):
    ...     if is_dirty('sound_settings'):
    ...         print(sound_settings)
    ...     if is_dirty('picture_settings'):
    ...         print(picture_settings)

    """
    _app = get_app_instance()
    return _app.is_dirty(*args)


def is_dirty_all(*args):
    """
    See whether all keys in an @change have been modified

    :param args: Which keys to check for modification
    :type args: list[str]
    :return: True if all of the keys in `args` are modified

    >>> @change('sound_settings', 'picture_settings')
    ... def save_changed_settings(sound_settings, picture_settings, **kwargs):
    ...     if is_dirty_all('sound_settings', 'picture_settings'):
    ...         print("Cannot save both sound and picture settings at once")
    ...         raise

    """
    _app = get_app_instance()
    return _app.is_dirty_all(*args)


class State:
    """This static class provides pythonic access to the state

    For instance, these getters are the same:

    >>> field, = get_state("field")
    >>> field = state.field

    As are these setters:

    >>> update_state("field", value)
    >>> state.field = value

    ``get_state()`` should be used instead if more than one argument is to be
    passed, and ``update_state()`` should be used instead to specify additional
    arguments (e.g. ``force=True``).

    The state may also be accessed and updated similar to dictionaries:

    >>> value = state["field"]
    >>> state["field"] = value
    >>> state.update({"field": value})

    When state update happen outside the main loop, or if a variable get modified
    internally without a reference change, you can force a flush of a set of variables
    to the client.

    >>> state.flush("field", "field1")

    An instance of this static class can be imported via

    >>> from trame import state
    """
    @staticmethod
    def __getattr__(name):
        if is_dunder(name):
            # Forward dunder calls to object
            return getattr(object, name)

        return State.__getitem__(name)

    @staticmethod
    def __setattr__(name, value):
        # Do not allow pre-existing attributes, such as update(), to be
        # re-defined.
        if name in State.__dict__:
            msg = (
                f"'{name}' is a special attribute on State that cannot be "
                "re-assigned"
            )
            raise Exception(msg)

        State.__setitem__(name, value)

    @staticmethod
    def __getitem__(name):
        value, = get_state(name)
        return value

    @staticmethod
    def __setitem__(name, value):
        update_state(name, value)

    @staticmethod
    def update(d):
        return update_state(d)

    @staticmethod
    def flush(*args):
        return flush_state(*args)

    @staticmethod
    def is_dirty(*args):
        return is_dirty(*args)

    @staticmethod
    def is_dirty_all(*args):
        return is_dirty_all(*args)

    # Allow the change decorator to be accessed via @state.change
    change = staticmethod(change)
