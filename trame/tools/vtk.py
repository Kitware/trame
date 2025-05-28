import sys
from trame.app import TrameApp
from trame.ui.html import DivLayout
from trame.widgets import html


def get_rendering_information():
    try:
        import vtk

        renderer = vtk.vtkRenderer()
        render_window = vtk.vtkRenderWindow()
        render_window.AddRenderer(renderer)
        render_window.Render()

        return render_window.ReportCapabilities()

    except ImportError as err:
        return err.msg


class VtkRenderingInfo(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)

        with DivLayout(self.server) as self.ui:
            html.Pre("{{ report }}")

        self.state.report = get_rendering_information()


def main():
    app = VtkRenderingInfo()
    app.server.start()


if __name__ == "__main__":
    if "--stdout" in sys.argv:
        print(get_rendering_information())
    else:
        main()
