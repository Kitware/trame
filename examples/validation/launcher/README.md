## Generate client side to serve
python -m trame.tools.www --output ./www vuetify vtk trame

## Start launcher
mkdir -p viz-logs
python -m wslink.launcher ./config.json