from trame.internal.app import get_app_instance


def change(*_args, **_kwargs):
    """
    The @change decorator allows us to register a function so that it will be
    automatically called when any of the given list of state names gets modified.

    The decorated function is passed the full state as ``**kwargs`` when possible.
    This means you should have a method profile similar to ``fn(..., **kwargs)``

    :param _args: List of names that your function should listen to
    :type _args: `list[str]`

    >>> @change('settings')
    ... def show_settings(settings, user, **kwargs):
    ...     print(settings, "for", user)

    """
    _app = get_app_instance()
    return _app.change(*_args, **_kwargs)
