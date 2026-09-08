# Getting Started with trame + React 

## All imports used in this guide

```python
from trame.app import TrameApp
from trame.decorators import change, trigger, controller, life_cycle
from trame.ui.html import DivLayout
from trame.widgets import html, react
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
        super().__init__(server, client_type="react")
        self._build_ui()

    def _build_ui(self):
        with DivLayout(self.server) as self.ui:
            html.Div("Hello, trame + React")


if __name__ == "__main__":
    app = MyApp()
    app.server.start()
```

A `TrameApp` subclass with `client_type="react"` and a layout is all it takes.
`self.state`, `self.ctrl`, `DivLayout`, and `html.*` all work exactly the way
you'd expect from any other trame app.

## 2. Static content and static props

Plain strings and plain attribute values need nothing special — they're
static data:

```python
html.Div("This text never changes")
html.Input(type="range", min=0, max=10, step=1)
html.Button("Click me", classes="my-button")
```

## 3. Showing a value that changes over time

To display a value that updates as state changes, add a `react.Bind(...)`
entry directly in the children list, right next to whatever literal text
surrounds it:

```python
html.Div(["count = ", react.Bind("count", count=2)])
```

Multiple children (literal text and bindings both) always go in a single
list/tuple argument — `html.Div` takes one `children` argument, not variadic
`*args`:

```python
html.Div([
    "Reset count to ", react.Bind("default_value", default_value=1),
    " then double it to ", react.Bind("double_default", double_default=2),
])
```

`react.Bind`'s first argument is a JavaScript expression string, evaluated
against the current state. A plain state key name (`"count"`) is itself a
trivially valid expression, so no special-casing is needed for the common
case.

## 4. Binding a dynamic value to a prop

The same `react.Bind` also works as a prop value. Its signature is:

```python
react.Bind(js_expression, **state_defaults)
```

- **The first, positional argument is a JavaScript expression string**,
  evaluated client-side against the current scope (trame state, plus any
  `react.For`/`react.Slot` local scope in effect). A plain state key name
  (`"count"`) is the trivial case of a valid expression; it doesn't have to
  be just a bare key.
- **Every keyword argument sets a default on trame's shared state**, one
  `state.setdefault(key, value)` call per kwarg — not a single "default value
  for the bound key" slot.

The common case binds and defaults the same single key:

```python
html.Input(
    type="range", min=0, max=10, step=1,
    value=react.Bind("count", count=2),  # expression: "count", default: state.count = 2
)
```

But because the kwargs are independent of the expression, an expression that
combines several state keys can default all of them in one call:

```python
# expression: "count + offset" — defaults both count and offset,
# neither of which needs to already exist in state
html.Div(["total = ", react.Bind("count + offset", count=2, offset=1)])
```

Kwarg names don't have to match anything in the expression either — you could
default a key elsewhere in state that this particular binding doesn't
reference, though in practice keeping kwarg names aligned with the keys the
expression actually reads is the common, readable pattern.

## 5. Handling events and calling Python

`react.Callback` wraps either a raw JS expression or a Python callable:

```python
# Raw JS expression, evaluated client-side
html.Input(onChange=react.Callback("count = Number($event.target.value)"))

# Python callable, invoked server-side
html.Button("Reset", onClick=react.Callback(self.reset))

# Python callable with extra positional/keyword arguments
# (JS expression strings, evaluated client-side and sent along with the call)
html.Button("Reset to 4", onClick=react.Callback(self.reset, "[4]", "{}"))

# Event modifiers - run $event.preventDefault(), $event.stopPropagation(), etc.
# before the callback fires
html.Input(
    onDoubleClick=react.Callback(
        "count = 2 * count",
        modifiers=["prevent"],
    )
)
```

```python
def reset(self, value=2):
    self.state.count = value
```

## 6. Building a controlled input (two-way binding)

To create an input whose value both reflects and updates state, pair
`react.Bind` (for `value=`) with `react.Callback` (for `onChange=`):

```python
html.Input(
    type="range", min=0, max=10, step=1,
    value=react.Bind("count", count=2),
    onChange=react.Callback("count = Number($event.target.value)"),
)
```

## 7. Rendering content conditionally

To render content only when a condition holds, wrap it in `react.If`:

```python
with react.If(value="count > 5"):
    html.Div("Count is high")
```

## 8. Rendering a list of items

`name=` introduces the loop variable, referenced in children the same way any
other bound value is — via `react.Bind`:

```python
with html.Ul():
    with react.For(
        items=react.Bind("items", items=["Apple", "Banana", "Cherry"]),
        name="item",
    ):
        html.Li(
            react.Bind("item.name"),
            key=react.Bind("item.id"),
        )
```

**Don't forget `key=`.** Each list item needs a stable, unique key so the
renderer can track which piece of content corresponds to which piece of data
across updates. `key` is a plain shared attribute, bound the same way as any
other prop.

## 9. Letting a widget hand data back into content you provide

Some widgets need to hand data back into the content you give them — for
example, a data table that lets you control exactly how each row's cells look,
while it decides which row is currently being rendered. Define that content
with `react.Slot` and pass the resulting handle as an ordinary prop — not
nested inside the widget's own `with` block:

```python
with react.Slot(params=["item"]) as render_item_name:
    html.Strong([react.Bind("item.name")])

VDataTable(
    items=react.Bind("items"),
    renderItemName=render_item_name,
)
```

The widget calls `renderItemName(item)` once per row; you never need to know
or care how that invocation happens from the Python side.

## 10. Referencing an element or component to call its methods

`ref=` lets you attach a name to an element or component so you can call
methods on it later:

```python
html.Input(ref="my_input")
html.Canvas(ref="my_chart")
```

Calling a method on a ref uses `server.js_call(ref, method, *args)` — an
existing, already-implemented API (`trame_server.core.Server.js_call`), used
today by widgets like `JSEval` and `ClientTriggers`:

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
from trame.widgets import html, react


class TodoApp(TrameApp):
    def __init__(self, server=None):
        super().__init__(server, client_type="react")
        self.state.todos = ["Write docs", "Review PR", "Ship it"]
        self._build_ui()

    @change("count")
    def update_count(self, count, **_):
        self.state.double = 2 * int(count)

    def reset(self, value=2):
        self.state.count = value

    def _build_ui(self):
        with DivLayout(self.server) as self.ui:
            html.Div(["count = ", react.Bind("count", count=2)])
            html.Div(["2 x count = ", react.Bind("double", double=4)])
            html.Input(
                type="range", min=0, max=10, step=1,
                value=react.Bind("count", count=2),
                onChange=react.Callback("count = Number($event.target.value)"),
            )
            html.Button("Reset", onClick=react.Callback(self.reset))

            with react.If(value="todos.length > 0"):
                with html.Ul():
                    with react.For(items="todos", name="todo"):
                        html.Li([react.Bind("todo")], key=react.Bind("todo"))

            with react.If(value="todos.length === 0"):
                html.Div("Nothing left to do!")


if __name__ == "__main__":
    app = TodoApp()
    app.server.start()
```
