from trame.app import get_server
from trame.ui.html import DivLayout
from trame.widgets import html, trame, vtk

server = get_server()

# -----------------------------------------------------------------------------
# Web App setup
# -----------------------------------------------------------------------------

with DivLayout(server) as layout:
    container = layout.root
    trame.LifeCycleMonitor(events=("['created']",))
    container.style = "width: 100vw; height: 100vh;"
    with vtk.VtkView(ref="view"):
        with vtk.VtkGeometryRepresentation():
            vtk.VtkAlgorithm(vtk_class="vtkConeSource", state=("{ resolution }",))
    html.Input(
        type="range",
        min=3,
        max=60,
        step=1,
        v_model=("resolution", 6),
        style="position: absolute; top: 20px; left: 20px; z-index: 1; width: 25%; min-width: 300px;",
    )

# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
