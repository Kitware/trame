from trame import update_state, change
from trame.html import vuetify, vtk
from trame.layouts import SinglePage

from vtkmodules.vtkFiltersSources import vtkConeSource

# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

DEFAULT_RESOLUTION = 6

cone_generator = vtkConeSource()

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


@change("resolution")
def update_cone(resolution=DEFAULT_RESOLUTION, **kwargs):
    cone_generator.SetResolution(resolution)
    html_polydata.update()


def update_reset_resolution():
    update_state("resolution", DEFAULT_RESOLUTION)


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

html_polydata = vtk.VtkPolyData("cone", dataset=cone_generator)

layout = SinglePage("VTK Local rendering", on_ready=update_cone)
layout.logo.click = "$refs.view.resetCamera()"
layout.title.set_text("Cone Application")
layout.toolbar.children += [
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
    vuetify.VBtn(
        icon=True,
        click=update_reset_resolution,
        children=[vuetify.VIcon("mdi-undo-variant")],
    ),
]

layout.content.children += [
    vuetify.VContainer(
        fluid=True,
        classes="pa-0 fill-height",
        children=[
            vtk.VtkView([vtk.VtkGeometryRepresentation([html_polydata])]),
        ],
    )
]

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # print(layout.html)
    layout.start()
