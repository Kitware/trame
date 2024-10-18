import vtk

from vtkmodules.util.execution_model import select_ports

from trame.app import get_server
from trame.ui.vuetify3 import VAppLayout
from trame.widgets import html, vtk as vtk_widgets, vuetify3 as v3
from trame.decorators import TrameApp, change

# -----------------------------------------------------------------------------
# VTK pipeline definition
# -----------------------------------------------------------------------------


def setup_vtk():
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow(off_screen_rendering=True)
    render_window.AddRenderer(renderer)

    render_window_interactor = vtk.vtkRenderWindowInteractor(
        render_window=render_window
    )
    render_window_interactor.interactor_style.SetCurrentStyleToTrackballCamera()

    # Sources
    sphere_source = vtk.vtkSphereSource(
        theta_resolution=16,
        phi_resolution=16,
    )
    cone_source = vtk.vtkConeSource(
        radius=0.1,
        height=0.2,
        resolution=30,
    )

    # Pipeline
    glyph_filter = vtk.vtkGlyph3D(
        source_connection=cone_source.output_port,
        orient=True,
        vector_mode=1,  # normals
    )

    pipeline = (
        sphere_source
        >> vtk.vtkPolyDataNormals(compute_cell_normals=1)
        >> vtk.vtkCellCenters()
        >> glyph_filter
    )

    # Rendering
    renderer.AddActor(
        vtk.vtkActor(
            mapper=vtk.vtkPolyDataMapper(
                input_connection=glyph_filter.output_port,
            ),
        )
    )
    renderer.ResetCamera()
    render_window.Render()

    return render_window, sphere_source, cone_source, pipeline


# -----------------------------------------------------------------------------
# GUI helpers
# -----------------------------------------------------------------------------


class TitleWithStatistic(v3.VCardTitle):
    def __init__(self, name, title, width):
        super().__init__(title, classes="d-flex align-center")

        with self:
            v3.VSpacer()
            with v3.VChip(
                size="small",
                variant="outlined",
                classes="mr-2",
                style=f"width: {width}rem;",
            ):
                v3.VIcon("mdi-dots-triangle", start=True)
                html.Span(f"{{{{ {name}_points.toLocaleString() }}}}")
            with v3.VChip(
                size="small",
                variant="outlined",
                style=f"width: {width}rem;",
                v_show=f"{name}_points !== {name}_cells",
            ):
                v3.VIcon("mdi-triangle-outline", start=True)
                html.Span(f"{{{{ {name}_cells.toLocaleString() }}}}")


def slider(title, name, default_value, min_value, max_value, step_value):
    v3.VLabel(f"{ title }: {{{{ {name} }}}}")
    v3.VSlider(
        v_model=(name, default_value),
        min=min_value,
        step=step_value,
        max=max_value,
        hide_details=True,
    )


# -----------------------------------------------------------------------------
# Application
# -----------------------------------------------------------------------------


@TrameApp()
class Viewer:
    def __init__(self, server=None):
        self.rw, self.sphere, self.cone, self.pipeline = setup_vtk()
        self.server = get_server(server)
        self._build_ui()

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    @change("cone_resolution", "cone_height", "cone_radius")
    def update_cone(self, cone_resolution, cone_height, cone_radius, **_):
        self.cone.resolution = cone_resolution
        self.cone.height = cone_height
        self.cone.radius = cone_radius

        # Execute filter for output extraction
        cone_dataset = self.cone()
        output_dataset = self.pipeline()

        # Update UI with new statistics
        self.state.update(
            {
                "cone_points": cone_dataset.number_of_points,
                "cone_cells": cone_dataset.number_of_cells,
                "total_points": output_dataset.number_of_points,
                "total_cells": output_dataset.number_of_cells,
            }
        )

        self.ctrl.view_update()

    @change("sphere_resolution")
    def update_sphere(self, sphere_resolution, **_):
        self.sphere.theta_resolution = sphere_resolution
        self.sphere.phi_resolution = sphere_resolution

        # Execute filter for output extraction
        sphere_dataset = self.sphere()
        output_dataset = self.pipeline()

        # Update UI with new statistics
        self.state.update(
            {
                "sphere_points": sphere_dataset.number_of_points,
                "sphere_cells": sphere_dataset.number_of_cells,
                "total_points": output_dataset.number_of_points,
                "total_cells": output_dataset.number_of_cells,
            }
        )
        self.ctrl.view_update()

    def _build_ui(self):
        with VAppLayout(self.server, fill_height=True) as self.ui:
            with v3.VCard(
                style="z-index: 1;",
                classes="position-absolute w-33 top-0 left-0 ma-4",
            ):
                # Sphere
                TitleWithStatistic("sphere", "Sphere", 4)
                v3.VDivider()
                with v3.VCardText():
                    slider("Resolution", "sphere_resolution", 16, 8, 32, 1)

                # Cone
                v3.VDivider()
                TitleWithStatistic("cone", "Cone", 3)
                v3.VDivider()
                with v3.VCardText():
                    slider("Resolution", "cone_resolution", 30, 3, 24, 1)
                    slider("Height", "cone_height", 0.2, 0.01, 0.5, 0.01)
                    slider("Radius", "cone_radius", 0.1, 0.01, 0.2, 0.01)

                # Result
                v3.VDivider()
                TitleWithStatistic("total", "Result", 5)

            with vtk_widgets.VtkRemoteView(self.rw, interactive_ratio=1) as view:
                self.ctrl.view_update = view.update
                self.ctrl.view_reset_camera = view.reset_camera


def main():
    app = Viewer()
    app.server.start()


if __name__ == "__main__":
    main()
