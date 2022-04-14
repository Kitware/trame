from IPython import display


def display_iframe(src, **kwargs):
    """Convenience method to display an iframe for the given url source"""

    # Set some defaults. The kwargs can override these.
    # width and height are both required.
    iframe_kwargs = {
        "width": "100%",
        "height": 600,
        **kwargs,
    }
    iframe = display.IFrame(src=src, **iframe_kwargs)
    return display.display(iframe)
