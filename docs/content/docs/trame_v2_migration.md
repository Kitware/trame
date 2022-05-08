# From v1 to v2

Trame v2 is a coming and has several breaking changes. Some features of trame v1 have been removed but in general the migration should be mostly manageable at the top of your files by tweaking imports and variables definitions.

## Main code change

Before

```python
from trame import state, controller
from trame.layouts import SinglePage
from trame.html import vuetify

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

## 