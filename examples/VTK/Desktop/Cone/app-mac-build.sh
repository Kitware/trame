## Need to have python with dylib
# env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install -v 3.9.9

## Setup venv app dependencies
rm -rf build dist
python3.9 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r ./requirements.txt

## Bundle app
python app-mac-setup.py py2app

## Clean behind us
mv dist/Cone.app Cone.app
deactivate
rm -rf build dist .eggs .venv