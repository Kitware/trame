# ParaView and Trame

ParaView comes with its Python which might be missing some dependencies for your usage.
You can add more Python package into your ParaView by create a virtual environment (not the venv one but [the original](https://virtualenv.pypa.io/en/latest/)) and activate it inside your application.

## Virtual Environment for ParaView

```bash
virtualenv -p python3.9 pv-lib
source ./pv-lib/bin/activate
pip install trame
deactivate
```

## Running an application with ParaView Python

```bash
/Application/ParaView-5.10.app/Content/bin/pvpython ./app.py --virtual-env ./pv-lib
```