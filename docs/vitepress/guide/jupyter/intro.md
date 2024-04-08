# Trame and Jupyter Lab

A trame application, while working in standlone fashion, can also be imported inside Jupyter and displayed within a notebook.
To make that possible, the user will need to be able to import and instantiate such application in a Jupyter context. Then, the user will need to have access to the layout (ui) of that application so it can be displayed in the notebook flow. 

## Simple example

If you want to give it a try, you can setup a virtual environment like below:

```bash
# Create virtual-environment
python3 -m venv .venv

# Activate environment
source .venv/bin/activate  # => Linux / Mac
# .\.venv\Scripts\activate # => Window

# Install dependencies
pip install trame trame-vtk trame-vuetify # adding vuetify + vtk.js for demo app
pip install setuptools # used in trame-vuetify but not always available nowaday
pip install jupyterlab
```

Then you can start Jupyter Lab and run the follow cells

```bash
# start Jupyter
jupyter lab
```

Then within a new notebook, you can import our trame cone demo example (We'll look into the code later).

```python
from trame.app.demo import Cone

# Create new application instance
app = Cone()

# Let's start the server by waiting for its UI to be ready
await app.ui.ready

# Put the UI into the resulting cell
app.ui
```

This should look like 

![Cone in Jupyter](/assets/images/jupyter/jupyter-cone.png)

If you want [more examples using the same code, you can look at that binder example repository](https://github.com/Kitware/trame-binder).