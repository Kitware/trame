## Running example require ParaView 5.10+

Setup a local venv with `trame` installed

```python
python3.9 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install trame

export PV_VENV=$PWD/.venv
```

Assuming you are in the directory that contains the `pv_selection.py` file you should be able to execute the following command to start the example application:

```bash
# My local ParaView setup
export PVPYTHON=/Applications/ParaView-5.11.0.app/Contents/bin/pvpython

$PVPYTHON -m paraview.apps.trame --trame-app pv_selection
```

## Runtime error

You may have to patch the method listed on the Python exception by replacing the method content by just a `pass`. That method is supposed to extract all the build settings and fail to import a file that get deleted at install phase. For ParaView it is safe to skip that method content.