## Origin

https://panel.holoviz.org/gallery/vtk_interactive.html

## Trame

### Standalone

```bash
pip install trame trame-quasar trame-vtk
python ./app_trame.py
```

### jupyter

```python
from app_trame import StHelens

app = StHelens()
await app.ui.ready
app.ui
```

## Panel

### Standalone

```bash
pip install panel
panel serve ./app_panel.py
```

### Jupyter

```python
from app_panel import ui
ui
```