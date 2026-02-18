# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "trame",
#     "trame-vtklocal",
#     "trame-vtk",
#     "trame-vuetify",
#     "vtk>=9.6",
# ]
# ///

# Required for rendering initialization, not necessary for
# local rendering, but doesn't hurt to include it
import vtkmodules.vtkRenderingOpenGL2  # noqa
from vtkmodules.vtkCommonColor import vtkNamedColors

# Required for interactor initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa
from vtkmodules.vtkInteractionWidgets import vtkScalarBarWidget
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

from trame.app import TrameApp
from trame.ui.vuetify3 import VAppLayout
from trame.widgets import vtklocal, vtk


class App(TrameApp):
    def __init__(self, server=None, widget=True):
        super().__init__(server)

        self.server.cli.add_argument("--no-widget", action="store_true")
        self.server.cli.add_argument("--wasm", action="store_true")
        args, _ = self.server.cli.parse_known_args()
        if args.no_widget:
            widget = False

        self._setup_vtk(widget)
        self._build_ui(args.wasm)

    def _setup_vtk(self, has_widget):
        renderer = vtkRenderer()
        renderWindow = vtkRenderWindow()
        renderWindow.AddRenderer(renderer)

        renderWindowInteractor = vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)
        renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

        # Create lut
        colormin = vtkNamedColors().GetColor3d("blue")
        colormax = vtkNamedColors().GetColor3d("red")
        color = vtkColorTransferFunction()
        color.AddRGBPoint(0.0, *colormin)
        color.AddRGBPoint(1.0, *colormax)

        # Create a scalar bar
        scalarBar = vtkScalarBarActor()
        scalarBar.SetTitle("Scalar Bar")
        scalarBar.SetNumberOfLabels(4)
        scalarBar.SetLookupTable(color)
        scalarBar.SetPosition(0.5, 0.5)

        self.render_window = renderWindow
        self.widget = None

        if has_widget:
            # create the scalar_bar_widget
            scalar_bar_widget = vtkScalarBarWidget()
            scalar_bar_widget.SetInteractor(renderWindowInteractor)
            scalar_bar_widget.SetScalarBarActor(scalarBar)
            scalar_bar_widget.On()
            self.widget = scalar_bar_widget
        else:
            renderer.AddActor2D(scalarBar)

    def _build_ui(self, use_wasm):
        print(f"{use_wasm=}")
        with VAppLayout(self.server, full_height=True) as self.ui:
            if use_wasm:
                vtklocal.LocalView(self.render_window, ctx_name="view")
                if self.widget:
                    self.ctx.view.register_vtk_object(self.widget)
            else:
                vtk.VtkRemoteView(
                    self.render_window,
                    ctx_name="view",
                    interactive_ratio=1,
                )


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    app = App()
    app.server.start()
