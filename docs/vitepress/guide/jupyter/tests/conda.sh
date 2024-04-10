# Install MiniConda (Linux/Mac)
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh

# Create env
mamba create --name trame-jupyter python=3.10 trame trame-vtk trame-vuetify jupyterlab trame-jupyter-extension
mamba activate trame-jupyter
