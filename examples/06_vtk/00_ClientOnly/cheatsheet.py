from trame.app import TrameApp  # Base class for a trame app
from trame.ui.vuetify3 import SinglePageLayout  # UI layout
from trame.widgets import vuetify3 as v3, vtk  # UI widgets
from trame.decorators import change  # Method decorators for TrameApp class


class Cone(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)  # enable self.server, self.state, self.ctrl
        self._build_ui()

    def reset_resolution(self):
        self.state.resolution = 6

    @change("resolution")  # When resolution change, execute fn
    def _on_resolution_change(self, resolution, **_):
        print(f"Slider updating resolution to {resolution}")

    def _build_ui(self):
        """Build the user interface"""
        with SinglePageLayout(self.server) as self.ui:
            # Toolbar customization (add-on)
            with self.ui.toolbar as toolbar:
                toolbar.density = "compact"  # Update toolbar attribute
                v3.VSpacer()  # Push things to the right
                v3.VSlider(  # Add slider
                    v_model=(
                        "resolution",
                        6,
                    ),  # bind variable with an initial value of 6
                    min=3,
                    max=60,
                    step=1,  # slider min/max/step
                    density="compact",
                    hide_details=True,  # presentation options
                )

                # Bind methods (from ctrl or self) to 2 buttons with icons
                v3.VBtn(icon="mdi-crop-free", click=self.ctrl.reset_camera)
                v3.VBtn(icon="mdi-undo", click=self.reset_resolution)

            # Content setup
            with self.ui.content:
                # vtk.js view for local rendering
                with vtk.VtkView() as vtk_view:
                    # Bind method to controller
                    self.ctrl.reset_camera = vtk_view.reset_camera
                    with (
                        vtk.VtkGeometryRepresentation()
                    ):  # Add representation to vtk.js view
                        vtk.VtkAlgorithm(  # Add ConeSource to representation
                            vtk_class="vtkConeSource",  # Set attribute value with no JS eval
                            state=(
                                "{ resolution }",
                            ),  # Set attribute value with JS eval
                        )


def main():
    app = Cone()
    app.server.start()


if __name__ == "__main__":
    main()
