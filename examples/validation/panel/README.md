https://panel.holoviz.org/gallery/vtk_interactive.html


pip install trame trame-quasar trame-vtk

python ./app_trame.py

## In jupyter

from app_trame import StHelens

app = StHelens()
await app.ui.ready
app.ui