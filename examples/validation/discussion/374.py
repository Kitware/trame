# export PYTHONPATH=/Applications/ParaView-5.12.0-RC1.app/Contents/Python/
# export DYLD_LIBRARY_PATH=/Applications/ParaView-5.12.0-RC1.app/Contents/Libraries/

from paraview import simple

from trame.app import get_server
from trame.ui.html import DivLayout
from trame.widgets import html, paraview

# create a new 'IOSS Reader'
disk_out_refex2 = simple.IOSSReader(
    registrationName="disk_out_ref.ex2",
    FileName=[
        "/Applications/ParaView-5.12.0-RC1.app/Contents/examples/disk_out_ref.ex2"
    ],
)

# get active view
renderView1 = simple.GetActiveViewOrCreate("RenderView")

# show data in view
disk_out_refex2Display = simple.Show(
    disk_out_refex2, renderView1, "UnstructuredGridRepresentation"
)

# trace defaults for the display properties.
disk_out_refex2Display.Representation = "Surface"


# update the view to ensure updated data information
renderView1.Update()

# change representation type
disk_out_refex2Display.SetRepresentationType("Surface LIC")


server = get_server(client_type="vue3")
with DivLayout(server) as layout:
    layout.root.style = "width: 100vw; height: 100vh; margin: 0; padding: 0;"
    reset_camera = paraview.VtkRemoteView(renderView1).reset_camera
    html.Button(
        "Reset", style="position: absolute; top: 10px; left: 10px;", click=reset_camera
    )

server.start()
