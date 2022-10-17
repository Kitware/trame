This sample application aims to map the features of our Async SC22 ParaView demo
and highlight the shortcoming of standard ParaView in term of interactivity/responsiveness.

This trame application mimic [the code available with async]() but adapted to run on regular ParaView.

```bash
python3.9 -m venv .pv_venv
source ./.pv_venv/bin/activate
pip install -U pip
pip install trame trame-rca

export PV_VENV=$PWD/.pv_venv
$PV_PYTHON ./app.py
```
