# Try handle virtual env if provided
import sys

if "--virtual-env" in sys.argv:
    virtualEnvPath = sys.argv[sys.argv.index("--virtual-env") + 1]
    virtualEnv = virtualEnvPath + "/bin/activate_this.py"
    exec(open(virtualEnv).read(), {"__file__": virtualEnv})

from trame import update_state, change
from trame.html import vuetify, paraview
from trame.layouts import SinglePage

from paraview import simple

# -----------------------------------------------------------------------------
# ParaView code
# -----------------------------------------------------------------------------

DEFAULT_RESOLUTION = 6

cone = simple.Cone()
representation = simple.Show(cone)
view = simple.Render()


@change("resolution")
def update_cone(resolution, **kwargs):
    cone.Resolution = resolution
    html_view.update()


def update_reset_resolution():
    update_state("resolution", DEFAULT_RESOLUTION)


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

html_view = paraview.VtkRemoteView(view, ref="view")

layout = SinglePage("ParaView cone", on_ready=update_cone)
layout.logo.click = "$refs.view.resetCamera()"
layout.title.set_text("Cone Application")

with layout.toolbar:
    vuetify.VSpacer()
    vuetify.VSlider(
        v_model=("resolution", DEFAULT_RESOLUTION),
        min=3,
        max=60,
        step=1,
        hide_details=True,
        dense=True,
        style="max-width: 300px",
    )
    vuetify.VDivider(vertical=True, classes="mx-2")
    with vuetify.VBtn(icon=True, click=update_reset_resolution):
        vuetify.VIcon("mdi-undo-variant")

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
