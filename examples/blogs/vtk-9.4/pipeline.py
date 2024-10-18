import vtk

from trame.app import get_server
from trame.ui.vuetify3 import VAppLayout
from trame.widgets import vtk as vtk_widgets, vuetify3 as v3
from trame.decorators import TrameApp, change


def setup_vtk():
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow(off_screen_rendering=True)
    render_window.AddRenderer(renderer)

    render_window_interactor = vtk.vtkRenderWindowInteractor(
        render_window=render_window
    )
    render_window_interactor.interactor_style.SetCurrentStyleToTrackballCamera()

    # Pipeline
    sphere_source = vtk.vtkSphereSource(
        theta_resolution=16,
        phi_resolution=16,
    )

    cone_source = vtk.vtkConeSource(
        radius=0.1,
        height=0.2,
        resolution=30,
    )

    normals = vtk.vtkPolyDataNormals(
        compute_cell_normals=1,
        input_connection=sphere_source.output_port,
    )

    cell_centers = vtk.vtkCellCenters(
        input_connection=normals.output_port,
    )

    glyph_mapper = vtk.vtkGlyph3DMapper(
        orient=True,
        orientation_array="Normals",
        input_connection=cell_centers.output_port,
        source_connection=cone_source.output_port,
    )

    # Rendering
    renderer.AddActor(vtk.vtkActor(mapper=glyph_mapper))
    renderer.ResetCamera()
    render_window.Render()

    return render_window, sphere_source, cone_source


@TrameApp()
class Viewer:
    def __init__(self, server=None):
        self.rw, self.sphere, self.cone = setup_vtk()
        self.server = get_server(server)
        self._build_ui()

    @property
    def ctrl(self):
        return self.server.controller

    @change("cone_resolution", "cone_height", "cone_radius")
    def update_cone(self, cone_resolution, cone_height, cone_radius, **_):
        self.cone.resolution = cone_resolution
        self.cone.height = cone_height
        self.cone.radius = cone_radius
        self.ctrl.view_update()

    @change("sphere_resolution")
    def update_sphere(self, sphere_resolution, **_):
        self.sphere.theta_resolution = sphere_resolution
        self.sphere.phi_resolution = sphere_resolution
        self.ctrl.view_update()

    def _build_ui(self):
        with VAppLayout(self.server, fill_height=True) as self.ui:
            with v3.VCard(
                style="position: absolute; top: 1rem; left: 1rem; z-index: 1; width: 20%;"
            ):
                v3.VCardTitle("Cone")
                v3.VDivider()
                with v3.VCardText():
                    v3.VLabel("Resolution: {{ cone_resolution }}")
                    v3.VSlider(
                        v_model=("cone_resolution", 30),
                        min=3,
                        step=1,
                        max=24,
                        hide_details=True,
                    )
                    v3.VLabel("Height: {{ cone_height }}")
                    v3.VSlider(
                        v_model=("cone_height", 0.2),
                        min=0.01,
                        step=0.01,
                        max=0.5,
                        hide_details=True,
                    )
                    v3.VLabel("Radius: {{ cone_radius }}")
                    v3.VSlider(
                        v_model=("cone_radius", 0.1),
                        min=0.01,
                        step=0.01,
                        max=0.2,
                        hide_details=True,
                    )
                v3.VCardTitle("Sphere")
                v3.VDivider()
                with v3.VCardText():
                    v3.VLabel("Resolution: {{ sphere_resolution }}")
                    v3.VSlider(
                        v_model=("sphere_resolution", 16),
                        min=8,
                        step=1,
                        max=32,
                        hide_details=True,
                    )

            with vtk_widgets.VtkRemoteView(self.rw, interactive_ratio=1) as view:
                self.ctrl.view_update = view.update
                self.ctrl.view_reset_camera = view.reset_camera


def main():
    app = Viewer()
    app.server.start()


if __name__ == "__main__":
    main()
