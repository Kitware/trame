# PyPI / Conda / CLI

Trame applications are regular Python code which means they can be deployed to PyPI or conda and be used as command line tools.

The [trame-cookiecutter](https://github.com/Kitware/trame-cookiecutter) provide an initial structure for streamlining such use case.

But technically nothing would separate a trame app than any other Python package.

[![PyPI](/assets/logos/pypi.svg)](https://pypi.org/project/trame/)

```bash
pip install \
    trame \          # Main package (client+server)
    trame-vuetify \  # Widget library used by the demo for its buttons
    trame-vtk        # Widget library used by the demo for rendering vtk

# Run simple example app
python -m trame.app.demo
```

[![Conda](/assets/logos/conda.svg){ width=15% }](https://anaconda.org/conda-forge/trame)

```bash
conda install \
    -c conda-forge \ # conda channel to use
    trame        \   # Main package (client+server)
    trame-vuetify \  # Widget library used by the demo for its buttons
    trame-vtk        # Widget library used by the demo for rendering vtk

# Run simple example app
python -m trame.app.demo
```


![Simple trame app](/assets/images/deployment/cone-browser.png)