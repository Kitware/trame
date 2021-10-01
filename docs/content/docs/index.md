# Trame

Trame aims to streamline creation of graphical interface for interactive data manipulation and visualization.

## Core API

The Trame package provide a set of core fonctionality for designing your Python application with a Web UI.
Trame is mostly a `shared state` that let you bind UI elements to Python methods by allowing your code to react when the underlying data is changing.
On top of that `shared state` concept, you can simply bind `Python methods` to UI events such a click. The binding of function is done by defining triggers which tends to be done for you when using the `trame.html.*`

The core trame API is described below:

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

## HTML Elements

HTML elements in trame are just helper for generating HTML content. But because they exist as Python objects, users can interact with them simply by setting attributes on them.

## How to use it

Trame really aim to be simple and enable anyone to create GUI to a Python based application.
The fact that the UI is web based should not matter for the user, I guess this could be seen as a add-on bonus in case you want to use your application remotely across the internet. But trame can definitely be levarged for local use cases too.

The anatomy of a trame application should be as follow:

1. Business logic on what you application is doing
2. Connect any method that should react to state change (i.e. slider changing a sampling parameter)
3. Define functions that should be called when someone click or do something in the UI
4. Pick a layout and fill it with some widgets
   1. When defining widgets, you could bind states to their model with which initial value they should have.
   2. When clicking on something, provide the function that should be called
5. Start your server/application
