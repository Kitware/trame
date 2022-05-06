# From v1 to v2

Trame v2 is a coming and has several breaking changes. Some features of trame v1 have been removed but in general the migration should be mostly manageable at the top of your files by tweaking imports and variables definitions.

## Common code migration

Before

```python
from trame import state, controller

[...]

if __name__ == "__main__":
    layout.start()
```

After

```python
from trame.app import activate

app = activate()
state, controller = app.state, app.controller

[...]

if __name__ == "__main__":
    app.start()
```

## Advanced ones

...todo