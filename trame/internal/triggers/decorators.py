import trame.internal as tri


def trigger(name):
    """
    The @trigger decorator allows you to register a function as a trigger with a
    given name.

    Parameters
    ----------
    :param name: Name which this trigger function should listen to.
    :type name: str

    <v-btn @click="blue_button_clicked">Blue Button</v-btn>

    >>> @trigger('blue_button_clicked')
    ... def log_clicks():
    ...     print("The blue button was clicked")

    """
    _app = tri.get_app_instance()
    return _app.trigger(name)
