import trame as tr
from trame.layouts import SinglePage
from trame.html import vuetify, vtk

# -----------------------------------------------------------------------------
# Web App setup
# -----------------------------------------------------------------------------

layout = SinglePage("VTK Rendering")

view = vtk.VtkView(
    ref="view",
    children=[
        vtk.VtkGeometryRepresentation(
            vtk.VtkAlgorithm(vtkClass="vtkConeSource", state=("{ resolution }",))
        )
    ],
)
with layout.content:
    vuetify.VContainer(view, fluid=True, classes="pa-0 fill-height")

with layout.toolbar:
    vuetify.VSpacer()
    vuetify.VSlider(
        hide_details=True,
        v_model=("resolution", 6),
        max=60,
        min=3,
        step=1,
        style="max-width: 300px;",
    )
    vuetify.VSwitch(hide_details=True, v_model=("$vuetify.theme.dark",))
    with vuetify.VBtn(icon=True, click="$refs.view.resetCamera()"):
        vuetify.VIcon("mdi-crop-free")

if __name__ == "__main__":
    layout.start()
