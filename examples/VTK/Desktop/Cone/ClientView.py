from trame import update_state, change
from trame.html import vuetify, vtk
from trame.layouts import SinglePage

# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

DEFAULT_RESOLUTION = 6

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


@change("resolution")
def update_cone(resolution=DEFAULT_RESOLUTION, **kwargs):
    update_state("coneProps", {"resolution": resolution})


def update_reset_resolution():
    update_state("resolution", DEFAULT_RESOLUTION)


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

layout = SinglePage("VTK Local rendering", on_ready=update_cone)
layout.logo.click = "$refs.view.resetCamera()"
layout.title.set_text("Cone Application")

with layout.toolbar:
    vuetify.VSpacer(),
    vuetify.VSlider(
        v_model=("resolution", DEFAULT_RESOLUTION),
        min=3,
        max=60,
        step=1,
        hide_details=True,
        dense=True,
        style="max-width: 300px",
    ),
    vuetify.VDivider(vertical=True, classes="mx-2"),
    with vuetify.VBtn(
        icon=True,
        click=update_reset_resolution,
    ):
        vuetify.VIcon("mdi-undo-variant")

with layout.content:
    with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
        with vtk.VtkView():
            with vtk.VtkGeometryRepresentation():
                vtk.VtkAlgorithm(
                    vtk_class="vtkConeSource",
                    state=("coneProps", {"resolution": DEFAULT_RESOLUTION}),
                )

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
