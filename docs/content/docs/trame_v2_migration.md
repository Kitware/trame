# From v1 to v2

Trame v2 is a coming and has several breaking changes. Some features of trame v1 have been removed but in general the migration should be mostly manageable at the top of your files by tweaking imports and variables definitions.

## Main code change

Before

```python
from trame import state, controller
from trame.layouts import SinglePage
from trame.html import vuetify

[...]

tab_title = "Hello world"
layout = SinglePage(tab_title, on_ready=_fn)

[...]

if __name__ == "__main__":
    layout.start()
```

After

```python
from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify

server = get_server()
state, controller = server.state, server.controller

[...]

tab_title = "Hello world"
state.trame__title = tab_title
ctrl.on_server_ready.add(_fn)

with SinglePageLayout(server) as layout:
    pass

[...]

if __name__ == "__main__":
    server.start()
```
## Command Line Interface parser

Before

```python
from trame import get_cli_parser

parser = get_cli_parser()
```

After

```python
from trame.app import get_server

server = get_server()
parser = server.cli
```

## Client side download util

Before

```python
vuetify.VBtn(
    "Download",
    click="download('my_file_name.csv', file_content, 'text/csv')",
)
```

After

```python
vuetify.VBtn(
    "Download",
    click="utils.download('my_file_name.csv', file_content, 'text/csv')",
)
```

All the client helper functions are now nested under a `utils.*` namespace object to allow better extensibility and prevent possible state variables conflict.

## Busy

The state variable `busy` has been renamed to `trame__busy`.


## StateChange => ClientStateChange

Before

```
from trame.html import StateChange

StateChange("var_name", change=fn_)
```

After

```
from trame.widgets.trame import ClientStateChange


ClientStateChange(value="var_name", change=fn_)
```

## Triggers

Before

```
layout.triggers.add("mounted", "pixel_ratio = window.devicePixelRatio")
```

After

```
with layout:
    trame.ClientTriggers(
        mounted="pixel_ratio = window.devicePixelRatio",
        created=_fn,
        ...
    )
```

## Size Observer

Before

```
from trame.html import observer

observer.SizeObserver(...)
```

After

```
from trame.widgets import trame

trame.SizeObserver(...)
```

## Remote files

Before

```
from trame import RemoteFile

dataset_file = RemoteFile(
    "./data/disk_out_ref.vtu",
    "https://github.com/Kitware/trame/raw/master/examples/data/disk_out_ref.vtu",
    __file__,
)
```

After

```
from trame.assets.remote import HttpFile

dataset_file = HttpFile(
    "./data/disk_out_ref.vtu",
    "https://github.com/Kitware/trame/raw/master/examples/data/disk_out_ref.vtu",
    __file__,
)
```