# Ensure we are in the base conda environment first, or it won't work.
. $CONDA_DIR/bin/activate

conda create -y conda python=$TRAME_PYTHON --prefix $TRAME_VENV
conda activate $TRAME_VENV
conda clean -afy
