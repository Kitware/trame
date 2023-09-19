# Exposing a trame application into Jupyter

## Disable warning

```python
import os
os.environ["TRAME_DISABLE_V3_WARNING"] = "1"
```

## Define application

<<< @/../../examples/core_features/jupyter.py

## Use application within Jupyter

```python
cone = Cone()
await cone.ui.ready
cone.ui
```

![Trame in Jupyer](/assets/images/deployment/jupyter.png)

## Edit state in another cell

```python
cone.resolution = 4
```

