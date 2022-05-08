from trame.layouts import FullScreenPage

# Bring all web dependencies
from trame.html import (
    deckgl,  # noqa
    markdown,  # noqa
    matplotlib,  # noqa
    observer,  # noqa
    paraview,  # noqa
    plotly,  # noqa
    router,  # noqa
    # simput, # noqa - (pip install simput)
    vega,  # noqa
    vtk,  # noqa
    vuetify,  # noqa
    widgets,  # noqa
    xai,  # noqa
)

layout = FullScreenPage("Empty")

if __name__ == "__main__":
    layout.start()
