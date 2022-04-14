from .display import display_iframe


def run(name, **kwargs):
    """Run and display a Jupyter server proxy process with the given name

    Note that the proxy process must be registered with Jupyter by setting
    the `jupyter_serverproxy_servers` entrypoint in its setup.py or setup.cfg
    file.
    """
    src = f"/{name}"
    return display_iframe(src, **kwargs)
