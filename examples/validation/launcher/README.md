## Python environment

#### Define a virtual environment

python -m venv ./env
. ./env/bin/activate

#### Install requirements

pip install trame trame-vtk trame-vuetify trame-components vtk

## Generate client side to serve

python -m trame.tools.www --output ./www --client-type vue2

## Start launcher

mkdir -p viz-logs
python -m wslink.launcher ./config.json

Open http://localhost:8080/
