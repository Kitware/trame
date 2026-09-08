# Enabling your React widgets inside trame

Bringing an existing React component library into trame is a two-sided job:

- **On the JavaScript side** — generate a UMD/ESM bundle and expose a function
  that registers each of your components under a tag name (e.g.
  `mui-button`) that trame's React client can look up at render time. That
  bundling/registration step is outside the scope of this guide.
- **On the Python side** — describe the same set of components as plain
  Python classes, so an application author can write `mui.Button(...)`
  instead of hand-rolling a JSON tree. This is what the rest of this guide
  covers, using [trame-mui](https://github.com/Kitware/trame-mui) (a
  from-scratch binding of [MUI](https://mui.com/) to trame) as a concrete,
  real-world example throughout.

## The `trame` namespace

Every trame widget library — whether it ships with trame itself or is
installed separately (`trame-vuetify`, `trame-vtk`, `trame-mui`, ...) — is
actually two Python distributions layered on top of each other:

1. **Your real implementation package**, named `trame_<name>` (an underscore,
   since it's a regular, importable package). This is where all of your
   actual code lives — widget classes, module/asset declarations, and any
   layout helpers. For trame-mui this is `trame_mui`.
2. **A thin facade** that plugs into the shared `trame` namespace, named
   `trame-<name>` on PyPI but contributing files under `trame/widgets/`,
   `trame/modules/`, and optionally `trame/ui/`.

The reason this works without every widget library stepping on every other
one is that `trame`, `trame.widgets`, `trame.modules`, and `trame.ui` are all
[namespace packages](https://packaging.python.org/en/latest/guides/packaging-namespace-packages/):
their `__init__.py` is nothing but

```python
__path__ = __import__("pkgutil").extend_path(__path__, __name__)
```

Because every trame-related distribution ships this exact same one-liner at
every level, Python merges all of their `trame/`, `trame/widgets/`,
`trame/modules/`, and `trame/ui/` directories into one logical namespace at
import time. That's why `from trame.widgets import html, vuetify3, mui` all
resolve correctly even though `html`/`vuetify3` and `mui` come from entirely
unrelated pip packages that know nothing about each other.

Concretely, trame-mui's `src/` layout looks like this:

```
src/
├── trame/                    # namespace facade — thin, re-exporting only
│   ├── __init__.py           #   pkgutil.extend_path
│   ├── modules/mui.py        #   from trame_mui.module import *
│   ├── widgets/mui.py        #   from trame_mui.widgets.mui import *
│   └── ui/mui.py             #   from trame_mui.ui.mui import * (optional)
└── trame_mui/                # your actual implementation package
    ├── __init__.py
    ├── module/__init__.py    # JS/CSS assets this library needs to serve
    ├── widgets/mui.py        # one Python class per component
    └── ui/mui.py             # optional convenience layouts
```

The facade files are intentionally tiny — each one just re-exports from the
real package next to it:

```python
# trame/widgets/mui.py
from trame_mui.widgets.mui import *  # noqa: F403


def initialize(server):
    from trame_mui import module

    server.enable_module(module)
```

```python
# trame/modules/mui.py
from trame_mui.module import *  # noqa: F403
```

Picking `<name>` (`mui` here) is the one naming decision you make: it becomes
your PyPI package suffix (`trame-mui`), your import package (`trame_mui`),
and the module name application authors will type after `from trame.widgets
import ...` / `from trame.modules import ...`.

## Declaring your module: serving JS/CSS assets

Before any widget can render, its JS bundle and CSS need to be served to the
page. This is what a *trame module* (a plain object/namespace with a known
set of attributes, unrelated to a Python `import module`) declares —
`trame_mui/module/__init__.py`:

```python
from pathlib import Path

from trame_mui import __version__

# Lookup at runtime the directory to serve
serve_path = str(Path(__file__).with_name("serve").resolve())

# Serving static content
serve = {
    f"__trame_mui_{__version__}": serve_path,
}

# Module scripts (mjs)
module_scripts = [
    # ...
]

# UMD like scripts
scripts = [
    f"__trame_mui_{__version__}/trame-mui.umd.js",
]

# Css files to load
styles = [
    f"__trame_mui_{__version__}/roboto/300.css",
    f"__trame_mui_{__version__}/roboto/400.css",
]

# Method to use to install components
react_use = ["TrameMui"]

# Optional when custom code execution is needed
def setup(server, **_):
    if server.client_type != "react":
        msg = f"Server using client_type='{server.client_type}' while we expect 'react'"
        raise TypeError(msg)
```

- **`serve`** maps a URL prefix to a local directory to serve statically.
  Namespacing it with your package's `__version__` avoids asset collisions
  when two apps in the same process pin different versions of your library.
- **`module_scripts`** / **`scripts`** / **`styles`** list the actual files (resolved against `serve`) to inject into the page.
- **`react_use`** is the React counterpart of Vue's `vue_use`: it names the
  global registration function your JS bundle exposes (the piece mentioned
  in the introduction above) so the client-side runtime calls it to register
  your components' tags into its own renderer.
- **`setup(server, **_)`** runs once, the first time the module is enabled —
  a good place to assert preconditions like the expected `client_type`.

A module is activated with `server.enable_module(module)`; trame tracks
already-loaded modules, so calling it repeatedly (e.g. once per widget
instance, as below) is harmless.

## Defining a widget: props and events

Every widget class ultimately inherits from
`trame_client.widgets.core.AbstractElement`. Libraries typically define one
small intermediate base class per library that takes care of enabling the
module automatically, so individual widgets don't have to repeat that:

```python
from trame_client.widgets.core import AbstractElement
from trame_mui import module


class MuiHtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)
```

Every concrete component then subclasses `MuiHtmlElement` instead of
`AbstractElement` directly:

```python
class Accordion(MuiHtmlElement):
    """MUI Accordion - https://mui.com/material-ui/api/accordion/

    :param default_expanded: If true, expands the accordion by default. (default: false) (``bool``)
    :param disabled: If true, the component is disabled. (default: false) (``bool``)
    :param expanded: If true, expands the accordion, otherwise collapses it. (``bool``)
    :param on_change: Callback fired when the expand/collapse state is changed. (``func``)
    """

    def __init__(self, children=None, **kwargs):
        super().__init__("mui-accordion", children, **kwargs)
        self.props += [
            ("default_expanded", "defaultExpanded"),
            "disabled",
            "expanded",
            ("on_change", "onChange"),
        ]
```

A few things to note in that constructor:

- **The first argument to `super().__init__(...)` is the tag name** —
  `"mui-accordion"` — the exact string the JS-side registration function
  (mentioned above) used to register this component. The name just needs to be unique without risking overriding another library widget. Vue.js use the `kebab-case` convention, but `camel-case` can be fine too as long it match whatever the JS side registered.
- **`self.props` is where you declare every prop your widget accepts.**
  `self.props` start out populated with the shared
  DOM/React props/events every element understands (`id`, `style`,
  `on_click`, `on_change`, ...); `self.props += [...]` extends that list   with whatever is specific to this component.
  Technically, you can also add to `self.events += [...]` for the `on_*` callback. But at the end with react, both are merged without any distinction. 
- **Each entry is either a bare string or a `(python_name, react_name)`
  tuple.** A bare string (`"disabled"`) means the Python kwarg and the React
  prop share the exact same name. A tuple is for everything else — most
  commonly translating Python's `snake_case` convention into React's
  `camelCase` (`("default_expanded", "defaultExpanded")`).

### Events are just props

Unlike trame's Vue bindings, where properties (`props`) and events
(`events`) are two separate lists rendered with different HTML syntax
(`prop="..."` vs `@event="..."`), React has no such distinction at the
wire level — an event handler is simply a prop whose value happens to be a
function. trame's React implementation mirrors that: **there is no separate
`self.events` list to populate** — `on_change`, `on_click`, and any other
callback prop are declared in `self.props` exactly like any other prop,
using the same `("python_name", "reactPropName")` tuple form:

```python
self.props += [
    ("on_change", "onChange"),   # a value, when set, is expected to be a
                                  # react.Callback(...) — see the Getting
                                  # Started guide for react.Bind / react.Callback
]
```

The application author is the one who eventually passes a
`react.Callback(...)` (or `react.Bind(...)` for a two-way-bound value) as the
value for that prop — the widget definition only needs to declare that the
prop exists and what its React name is.

### Docstrings

The `:param name: description (default: ...) (\`\`type\`\`)` convention shown
above isn't required by trame, but keeping it consistent across your
library's classes means any docstring-based doc generator (Sphinx autodoc,
IDE tooltips, ...) renders a useful per-prop reference automatically, the
same way it does for the rest of the codebase.

### Widgets that need eager children (`literal_children`)

A small number of components (MUI's `Select`, `Tabs`, `Stepper`, ...) don't
render their children in the usual React way — they inspect
`child.props.*` directly (via `React.Children`) *before* rendering, to
figure out things like which item is selected, then clone that child with
extra props injected. trame's default children handling wraps each child
lazily, which defeats that inspection since the props such a component reads
would live on the wrapper instead of on the real element. Opt out of the
wrapper for those specific widgets by setting `self.literal_children = True`
after calling `super().__init__(...)` or directly in the constructor:

```python
class Select(MuiHtmlElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("mui-select", children, literal_children= True, **kwargs)
        self.props += [...]
```

This is the exception, not the rule — most widgets never need it.

## Putting it together

With `MuiHtmlElement` and one class per component defined in
`trame_mui/widgets/mui.py`, the facade at `trame/widgets/mui.py` re-exports
all of them with `from trame_mui.widgets.mui import *`. From an application's
point of view, none of the namespace plumbing is visible — it's just:

```python
from trame.widgets import mui, react

mui.Accordion(
    expanded=react.Bind("panel_open", panel_open=False),
    on_change=react.Callback("panel_open = $event.target.checked"),
)
```
