# Jupyter

Trame applications can be imported and shown within a Jupyter cell without missing any of your application capabilities.

The [trame-cookiecutter](https://github.com/Kitware/trame-cookiecutter) provide an initial helper that live under `{package_name}/app/jupyter.py` which provide a `show()` method.

But such `show()` method can be implemented for a single file application like below when no additional parameter are required for your application:

```python
def show(**kwargs):
    from trame.app import jupyter
    jupyter.show(server, **kwargs)
```

The way such integration works is by running the trame server as an asynchronous task within Tornedo (Jupyter kernel) and opening a new port so that iframe can connect to it.
This means that everything defined within your Jupyter environment is accessible within trame and vice-versa.
