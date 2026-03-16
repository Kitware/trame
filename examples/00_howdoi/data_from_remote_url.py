#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "trame",
#     "trame-vuetify",
#     "trame-vtk",
#     "vtk",
# ]
# ///

import tempfile
from urllib.error import HTTPError
from urllib.request import urlretrieve

import vtkmodules.vtkRenderingOpenGL2  # noqa
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

# Trame imports
from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vtk as vtk_widgets
from trame.widgets import vuetify3 as v3


class RemoteURL(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)

        self.server.cli.add_argument(
            "--remote-url",
            dest="remote_url",
            help="Remote URL pointing to a VTU file.",
            default="https://github.com/Kitware/trame/raw/master/examples/data/disk_out_ref.vtu",
        )
        args, _ = self.server.cli.parse_known_args()
        self._setup_vtk(args)
        self._build_ui()

    def _setup_vtk(self, args):
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

        renderer = vtkRenderer()
        renderer.SetBackground(1, 1, 1)
        render_window = vtkRenderWindow()
        render_window.AddRenderer(renderer)
        render_window.OffScreenRenderingOn()

        renderWindowInteractor = vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(render_window)
        renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

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

        self.render_window = render_window

    def _build_ui(self):
        self.state.trame__title = "Fetch Remote URL example"

        with SinglePageLayout(self.server) as self.ui:
            self.ui.title.set_text("Unstructured grid from remote URL")

            with self.ui.content:
                with v3.VContainer(fluid=True, classes="fill-height pa-0 ma-0"):
                    with v3.VRow(dense=True, style="height: 100%;"):
                        with v3.VCol(
                            classes="pa-0",
                            style="border-right: 1px solid #ccc; position: relative;",
                        ):
                            vtk_widgets.VtkRemoteView(
                                self.render_window,
                                interactive_ratio=1,
                                ctx_name="view",
                            )


def main():
    app = RemoteURL()
    app.server.start()


if __name__ == "__main__":
    main()
