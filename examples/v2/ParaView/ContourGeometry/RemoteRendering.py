from paraview.web import venv  # Available in PV 5.10-RC2+

from pathlib import Path

from trame import state
from trame.html import vuetify, paraview
from trame.layouts import SinglePage

from paraview import simple

# -----------------------------------------------------------------------------
# ParaView pipeline
# -----------------------------------------------------------------------------

simple.LoadDistributedPlugin("AcceleratedAlgorithms", remote=False, ns=globals())

data_directory = Path(__file__).parent.parent.parent.with_name("data")
head_vti = data_directory / "head.vti"

reader = simple.XMLImageDataReader(FileName=[head_vti])
# contour = simple.Contour(Input=reader) # Default filter    => no plugin but slow
contour = FlyingEdges3D(Input=reader)  # Faster processing => make it interactive

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


@state.change("contour_value", "interactive")
def update_contour(contour_value, interactive, force=False, **kwargs):
    if interactive or force:
        contour.Isosurfaces = [contour_value]
        html_view.update()


def commit_changes():
    update_contour(
        contour_value=state.contour_value,
        interactive=state.contour_value,
        force=True,
    )


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------
html_view = paraview.VtkRemoteView(view)

layout = SinglePage(
    "ParaView contour - Remote/Local rendering", on_ready=html_view.update
)
layout.title.set_text("Contour Application - Remote rendering")
layout.logo.click = html_view.reset_camera

with layout.toolbar:
    vuetify.VSpacer()

    vuetify.VSwitch(
        v_model=("interactive", False),
        hide_details=True,
        label="Update while dragging",
    )
    vuetify.VSlider(
        v_model=("contour_value", contour_value),
        change=commit_changes,
        min=("data_range[0]",),
        max=("data_range[1]",),
        hide_details=True,
        dense=True,
        style="max-width: 300px",
    )
    vuetify.VSwitch(
        v_model="$vuetify.theme.dark",
        hide_details=True,
    )

    with vuetify.VBtn(icon=True, click="$refs.view.resetCamera()"):
        vuetify.VIcon("mdi-crop-free")

    vuetify.VProgressLinear(
        indeterminate=True,
        absolute=True,
        bottom=True,
        active=("busy",),
    )

with layout.content:
    vuetify.VContainer(
        fluid=True,
        classes="pa-0 fill-height",
        children=[html_view],
    )

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
