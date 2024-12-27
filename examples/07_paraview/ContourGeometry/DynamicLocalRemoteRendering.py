r"""
Installation requirements:
    pip install trame trame-vuetify trame-vtk
"""

import paraview.web.venv

from pathlib import Path

from trame.app import get_server
from trame.widgets import vuetify, paraview
from trame.ui.vuetify import SinglePageLayout

from paraview import simple

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Data file
# -----------------------------------------------------------------------------

data_directory = Path(__file__).parent.parent.parent.with_name("data")
head_vti = data_directory / "head.vti"

# -----------------------------------------------------------------------------
# ParaView pipeline
# -----------------------------------------------------------------------------
simple.LoadDistributedPlugin("AcceleratedAlgorithms", remote=False, ns=globals())
reader = simple.XMLImageDataReader(FileName=[str(head_vti)])
# contour = simple.Contour(Input=reader) # Default filter    => no plugin but slow
contour = simple.FlyingEdges3D(Input=reader)  # Faster processing => make it interactive

# Extract data range => Update store/state
array = reader.GetPointDataInformation().GetArray(0)
data_name = array.GetName()
data_range = array.GetRange()
contour_value = 0.5 * (data_range[0] + data_range[1])
state.data_range = data_range
state.contour_value = contour_value

contour.ContourBy = ["POINTS", data_name]
contour.Isosurfaces = [contour_value]
contour.ComputeNormals = 1
contour.ComputeScalars = 0

# Rendering setup
view = simple.GetRenderView()
view.OrientationAxesVisibility = 0
representation = simple.Show(contour, view)
view = simple.Render()
simple.ResetCamera()
view.CenterOfRotation = view.CameraFocalPoint

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


@state.change("contour_value")
def update_contour(contour_value, **kwargs):
    contour.Isosurfaces = [contour_value]
    html_view.update_image()


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

modes = (
    ("auto", "mdi-autorenew"),
    ("local", "mdi-rotate-3d"),
    ("remote", "mdi-image"),
)

state.trame__title = "ParaView contour - Remote/Local rendering"
ctrl.on_server_ready.add(ctrl.view_update)

with SinglePageLayout(server) as layout:
    layout.title.set_text("Contour Application - Remote rendering")
    layout.icon.click = ctrl.view_reset_camera

    with layout.toolbar:
        vuetify.VSpacer()

        with vuetify.VBtnToggle(
            v_model=("override", "auto"),
            dense=True,
            mandatory=True,
        ):
            for entry in modes:
                with vuetify.VBtn(value=entry[0]):
                    vuetify.VIcon(entry[1])

        vuetify.VSpacer()
        vuetify.VSlider(
            v_model="contour_value",
            min=("data_range[0]",),
            max=("data_range[1]",),
            hide_details=True,
            dense=True,
            style="max-width: 300px",
            start="trigger('demoAnimateStart')",
            end="trigger('demoAnimateStop')",
        )
        vuetify.VSwitch(
            v_model="$vuetify.theme.dark",
            hide_details=True,
        )

        with vuetify.VBtn(icon=True, click=ctrl.view_reset_camera):
            vuetify.VIcon("mdi-crop-free")

        vuetify.VProgressLinear(
            indeterminate=True,
            absolute=True,
            bottom=True,
            active=("trame__busy",),
        )

    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            html_view = paraview.VtkRemoteLocalView(
                view,
                namespace="demo",
                # second arg is to force the view to start in "local" mode
                mode=("override === 'auto' ? demoMode : override", "local"),
            )
            ctrl.view_update = html_view.update
            ctrl.view_reset_camera = html_view.reset_camera

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
