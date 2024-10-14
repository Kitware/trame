r"""
Installation requirements:
    pip install trame trame-vuetify trame-vtk vtk
"""

import tempfile
from urllib.error import HTTPError
from urllib.request import urlretrieve

import vtkmodules.vtkRenderingOpenGL2  # noqa
from trame.ui.vuetify3 import SinglePageLayout
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter

# VTK imports
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderer,
    vtkRenderWindow,
)

# Trame imports
from trame.app import get_server
from trame.widgets import vtk as vtk_widgets
from trame.widgets import vuetify3 as vuetify

server = get_server(client_type="vue3")
server.cli.add_argument(
    "--remote-url",
    dest="remote_url",
    help="Remote URL pointing to a VTU file.",
    default="https://github.com/Kitware/trame/raw/master/examples/data/disk_out_ref.vtu",
)
(args, _unknown) = server.cli.parse_known_args()

state, ctrl = server.state, server.controller

with tempfile.NamedTemporaryFile() as fp:
    try:
        print(f"using local file {fp.name}")
        urlretrieve(args.remote_url, fp.name)
        reader = vtkXMLUnstructuredGridReader()
        reader.SetFileName(fp.name)
        reader.Update()
    except HTTPError as e:
        print(RuntimeError(f"Failed to download {args.remote_url}. {e.reason}"))
        raise e


dataset = reader.GetOutput()

renderer = vtkRenderer()
renderer.SetBackground(1, 1, 1)
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)

surface_filter = vtkGeometryFilter()
surface_filter.SetInputConnection(reader.GetOutputPort())
surface_filter.SetPassThroughPointIds(True)

mapper = vtkDataSetMapper()
mapper.SetInputConnection(surface_filter.GetOutputPort())
actor = vtkActor()
actor.GetProperty().SetOpacity(0.5)
actor.SetMapper(mapper)

renderer.AddActor(actor)
renderer.ResetCamera()


state.trame__title = "Fetch Remote URL example"
ctrl.on_server_ready.add(ctrl.view_update)

with SinglePageLayout(server) as layout:
    layout.title.set_text("Unstructured grid from remote URL")

    with layout.content:
        with vuetify.VContainer(fluid=True, classes="fill-height pa-0 ma-0"):
            with vuetify.VRow(dense=True, style="height: 100%;"):
                with vuetify.VCol(
                    classes="pa-0",
                    style="border-right: 1px solid #ccc; position: relative;",
                ):
                    view = vtk_widgets.VtkLocalView(
                        render_window,
                    )
                    ctrl.view_update = view.update

if __name__ == "__main__":
    server.start()
