# Getting Started with trame + Vue3

__client_type="vue3"__ is trame's default, production client — everything in
this guide works today with nothing extra to install or opt into. If you
create a `TrameApp` without specifying `client_type`, you're already using
it.

## All imports used in this guide

```python
from trame.app import TrameApp
from trame.decorators import change, controller
from trame.ui.html import DivLayout
from trame.widgets import html, client
```

Every example below uses some subset of these. Nothing else is needed for the
use cases covered here.

## 1. Minimal app

```python
from trame.app import TrameApp
from trame.ui.html import DivLayout
from trame.widgets import html


class MyApp(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._build_ui()

    def _build_ui(self):
        with DivLayout(self.server) as self.ui:
            html.Div("Hello, trame + Vue3")


if __name__ == "__main__":
    app = MyApp()
    app.server.start()
```

A `TrameApp` subclass and a layout is all it takes — `vue3` is the default
`client_type`, so it doesn't need to be named explicitly. `self.state`,
`self.ctrl`, `DivLayout`, and `html.*` all work exactly the way you'd expect.

## 2. Static content and static props

Plain strings and plain attribute values need nothing special — they're static data:

```python
html.Div("This text never changes")
html.Input(type="range", min=0, max=10, step=1)
html.Button("Click me", classes="my-button")
```

## 3. Showing a value that changes over time

To display a value that updates as state changes, use Vue's double-mustache
interpolation directly inside the string child:

```python
html.Div("count = {{ count }}")
```

Multiple bindings and literal text can be mixed freely in the same string:

```python
html.Div("Reset count to {{ default_value }} then double it to {{ double_default }}")
```

<span v-pre>`{{ ... }}`</span> evaluated against the current
state — a plain state key name (`count`) is itself a trivially valid
expression, so no special-casing is needed for the common case.


## 4. Binding a dynamic value to a prop

Any prop can be bound to state with a `(name, default)` tuple:

```python
html.Input(
    type="range", min=0, max=10, step=1,
    v_model=("count", 2),
)
```

- **The first element of the tuple is the state key** (or a JS expression, for
  props that accept one) evaluated client-side.
- **The second element sets a default** on trame's shared state — equivalent
  to `state.setdefault("count", 2)` — so the app has a sane value on first
  render even before any Python code sets it.

This same `(name, default)` convention is used everywhere in trame — not just
for `v_model`, but for `style`, `classes`, and any other prop you want to
drive from state.

## 5. Handling events and calling Python

Events bind to a plain Python method for the no-argument case, or a tuple of
`(method, "[js_args]")` when you need to pass arguments evaluated
client-side:

```python
# No-argument call
html.Button("Reset", click=self.reset)

# Call with arguments (JS expression strings, evaluated client-side)
html.Button("Reset to 4", click=(self.reset, "[4]"))

# Raw JS expression instead of a Python call
html.Input(change="count = Number($event.target.value)")

# Event modifiers - chained with underscores, mirroring Vue's dot syntax
# (@click.left.stop="...")
html.Div(v_on_click_left_stop="handleClick")
```

```python
def reset(self, value=2):
    self.state.count = value
```

## 6. Building a controlled input (two-way binding)

Unlike a one-way <span v-pre>`{{ }}`</span> binding, `v_model` is already two-way: it both
reflects state into the element and writes the element's changes back to
state, so no separate change handler is needed:

```python
html.Input(
    type="range", min=0, max=10, step=1,
    v_model=("count", 2),
)
```

## 7. Rendering content conditionally

To render content only when a condition holds, use `v_if` with a JS
expression string:

```python
html.Div("Count is high", v_if="count > 5")
```

`v_show` works the same way, but toggles CSS visibility instead of adding or
removing the element from the DOM:

```python
html.Div("Always mounted, sometimes hidden", v_show="count > 5")
```

## 8. Rendering a list of items

`v_for` takes Vue's `"item, index in list"` syntax directly, and `key` is
bound like any other string expression:

```python
with html.Ul():
    html.Li(
        "{{ item }}",
        v_for="item, i in items",
        key="i",
    )
```

```python
self.state.items = ["Apple", "Banana", "Cherry"]
```

**Don't forget `key=`.** Each list item needs a stable, unique key so Vue can
track which piece of content corresponds to which piece of data across
updates.

## 9. Letting a widget hand data back into content you provide

Some widgets need to hand data back into the content you give them — for
example, a data table that lets you control exactly how each row's cells
look, while it decides which row is currently being rendered. This maps to
Vue's scoped slots, expressed in Python with the `Template` widget from
`trame.widgets.html`:

```python
from trame.widgets import html

with SomeDataTable(items=("items",)):
    with html.Template(v_slot_item_name="{ item }"):
        html.Strong("{{ item.name }}")
```

The widget calls into this slot once per row, providing `item` as a local
scoped variable that <span v-pre>`{{ item.name }}`</span> and any other bindings inside the
`Template` block can reference. The slot name (here, `item.name`, written as
the `v_slot_item_name` kwarg) must be one the widget you're using actually
exposes — check that widget's documentation for its available named slots.


## 10. Referencing an element or component to call its methods

`ref=` lets you attach a name to an element or component so you can call
methods on it later:

```python
html.Input(ref="my_input")
html.Canvas(ref="my_chart")
```

Calling a method on a ref uses `server.js_call(ref, method, *args)`:

```python
def focus_input(self):
    self.server.js_call("my_input", "focus")

def reset_zoom(self):
    self.server.js_call("my_chart", "resetZoom")
```

For a plain DOM element (`html.Input`), the method called is whatever the
native DOM API provides (`focus()`, `scrollIntoView()`, ...). For a custom
widget, it's whatever that widget's author chose to expose — trame doesn't
standardize or restrict this.

## 11. Full worked example

Putting it together — a counter with a derived value, a reset button, and a
todo list:

```python
from trame.app import TrameApp
from trame.decorators import change
from trame.ui.html import DivLayout
from trame.widgets import html


class TodoApp(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self.state.todos = ["Write docs", "Review PR", "Ship it"]
        self._build_ui()

    @change("count")
    def update_count(self, count, **_):
        self.state.double = 2 * int(count)

    def reset(self, value=2):
        self.state.count = value

    def _build_ui(self):
        with DivLayout(self.server) as self.ui:
            html.Div("count = {{ count }}")
            html.Div("2 x count = {{ double }}")
            html.Input(
                type="range", min=0, max=10, step=1,
                v_model=("count", 2),
            )
            html.Button("Reset", click=self.reset)

            with html.Ul(v_if="todos.length > 0"):
                html.Li("{{ todo }}", v_for="todo in todos", key="todo")

            html.Div("Nothing left to do!", v_if="todos.length === 0")


if __name__ == "__main__":
    app = TodoApp()
    app.server.start()
```
