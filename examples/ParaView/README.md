# ParaView and trame

ParaView comes with its own Python, which may be missing some dependencies for the desired usage.
We can add more Python packages into ParaView by create a virtual environment and activate it inside your application by importing our helper module [venv.py](https://github.com/Kitware/trame/blob/master/examples/ParaView/venv.py).


## venv for ParaView

```bash
python3.9 -m venv .pvenv
source .pvenv/bin/activate
pip install trame
deactivate
```

## Running an application with ParaView Python

```bash
/Application/ParaView-5.10.app/Content/bin/pvpython ./app.py --venv .pvenv
```

**Note**:
 - venv.py must be either next to your app.py or available inside your Python runtime.