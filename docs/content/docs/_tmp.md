
### Server Management

```python
def start(layout=None, name=None, favicon=None, on_ready=None, port=None):
    """
    Start web server for serving your application

    Parameters
    ----------
    layout  : None or str or trame.layouts.*
        UI content that should be used for your application
    name    : None or str
        "Title" that you can see in your tab browser.
        This will be filled automatically if a trame.layouts.* layout was provided.
    favicon : None or str
        Relative path to a png image that should be used as favicon
    port    : None or Number
        Port on which the server should run on
    on_ready: None or function
        Function called once the server is ready
```

### State Management

```python
def update_state(key, value=None):
    """
    Method updating current application state that is shared with the Web UI
    """
```

```python
def get_state(*names):
    """
    Return a list of the values of the given state keys

    Paramters
    ---------
    *names : *str
        List of name of state values to retreive

    Returns
    -------
    [any, ...]
        List of value matching the requested state property names
    """
```

```python
def update_layout(layout):
    """
    Dynamically update current application layout

    Parameters
    ----------
    layout  : str or trame.layouts.*
        UI content that should be used for your application
    """
```

### Method annotations

```python
def change(*_args, **_kwargs):
    """
    @change decorator allow to register a function in a way that it will be
    automatically called when the given list of state names get modified.

    The decorated function is passed the full state as *kwarg when possible.
    This means you should have a method profile similar to `fn(..., *kwargs)`

    Parameters
    ----------
    *_args : *str
        List of name that your function should listen to
    """
```

```python
def trigger(name):
    """
    @trigger decorator allow to register a function as a trigger with a given name

    Parameters
    ----------
    name : str
        Name of the trigger
    """
    _app = get_app_instance()
    return _app.trigger(name)
```

## Layouts

Layout in trame are Python classes that have already made the decision on how the main part of a given application should looks like. Think, header, content, footer with maybe left drawer.

From a given layout that the user would pick, it will be the responsability of the user to fill it up with content that match his expectation by using trame.html.* elements.
