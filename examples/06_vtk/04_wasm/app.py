import vtk

from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageWithDrawerLayout
from trame.widgets import vtklocal, trame as tw, vuetify3 as v3
from trame.decorators import change
from trame.assets.remote import HttpFile
from trame.assets.local import to_url

# -----------------------------------------------------------------------------
# Fetch data / files
# -----------------------------------------------------------------------------
BIKE = HttpFile(
    "bike.vtp",
    "https://github.com/Kitware/trame-app-bike/raw/master/data/bike.vtp",
)
TUNNEL = HttpFile(
    "tunnel.vtu",
    "https://github.com/Kitware/trame-app-bike/raw/master/data/tunnel.vtu",
)
IMAGE = HttpFile(
    "seeds.jpg",
    "https://github.com/Kitware/trame-app-bike/raw/master/data/seeds.jpg",
)

if not BIKE.local:
    BIKE.fetch()

if not TUNNEL.local:
    TUNNEL.fetch()

if not IMAGE.local:
    IMAGE.fetch()

# -----------------------------------------------------------------------------
# Constants setup
# -----------------------------------------------------------------------------
P1 = [-0.4, 0, 0.05]
P2 = [-0.4, 0, 1.5]

INITIAL_STATE = {
    "line_widget": {
        "p1": P1,
        "p2": P2,
    },
    "trame__title": "Bike CFD",
    "trame__favicon": to_url(IMAGE.path),
}


# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------
def create_vtk_pipeline():
    K_RANGE = [0.0, 15.6]
    resolution = 50

    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.OffScreenRenderingOn()

    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

    bikeReader = vtk.vtkXMLPolyDataReader()
    bikeReader.SetFileName(BIKE.path)

    tunnelReader = vtk.vtkXMLUnstructuredGridReader()
    tunnelReader.SetFileName(TUNNEL.path)
    tunnelReader.Update()

    lineSeed = vtk.vtkLineSource()
    lineSeed.SetPoint1(*P1)
    lineSeed.SetPoint2(*P2)
    lineSeed.SetResolution(resolution)
    lineSeed.Update()

    lineWidget = vtk.vtkLineWidget2()
    lineWidgetRep = lineWidget.GetRepresentation()
    lineWidgetRep.SetPoint1WorldPosition(P1)
    lineWidgetRep.SetPoint2WorldPosition(P2)
    lineWidget.SetInteractor(renderWindowInteractor)

    streamTracer = vtk.vtkStreamTracer()
    streamTracer.SetInputConnection(tunnelReader.GetOutputPort())
    streamTracer.SetSourceConnection(lineSeed.GetOutputPort())
    streamTracer.SetIntegrationDirectionToForward()
    streamTracer.SetIntegratorTypeToRungeKutta45()
    streamTracer.SetMaximumPropagation(3)
    streamTracer.SetIntegrationStepUnit(2)
    streamTracer.SetInitialIntegrationStep(0.2)
    streamTracer.SetMinimumIntegrationStep(0.01)
    streamTracer.SetMaximumIntegrationStep(0.5)
    streamTracer.SetMaximumError(0.000001)
    streamTracer.SetMaximumNumberOfSteps(2000)
    streamTracer.SetTerminalSpeed(0.00000000001)

    tubeFilter = vtk.vtkTubeFilter()
    tubeFilter.SetInputConnection(streamTracer.GetOutputPort())
    tubeFilter.SetRadius(0.01)
    tubeFilter.SetNumberOfSides(6)
    tubeFilter.CappingOn()
    tubeFilter.Update()

    bike_mapper = vtk.vtkPolyDataMapper()
    bike_actor = vtk.vtkActor()
    bike_mapper.SetInputConnection(bikeReader.GetOutputPort())
    bike_actor.SetMapper(bike_mapper)
    renderer.AddActor(bike_actor)

    stream_mapper = vtk.vtkPolyDataMapper()
    stream_actor = vtk.vtkActor()
    stream_mapper.SetInputConnection(tubeFilter.GetOutputPort())
    stream_actor.SetMapper(stream_mapper)
    renderer.AddActor(stream_actor)

    lut = vtk.vtkLookupTable()
    lut.SetHueRange(0.7, 0)
    lut.SetSaturationRange(1.0, 0)
    lut.SetValueRange(0.5, 1.0)

    stream_mapper.SetLookupTable(lut)
    stream_mapper.SetColorModeToMapScalars()
    stream_mapper.SetScalarModeToUsePointData()
    stream_mapper.SetArrayName("k")
    stream_mapper.SetScalarRange(K_RANGE)

    renderWindow.Render()
    renderer.ResetCamera()
    renderer.SetBackground(0.4, 0.4, 0.4)

    lineWidget.On()

    return renderWindow, lineSeed, lineWidget, bike_actor


# -----------------------------------------------------------------------------
# Trame app
# -----------------------------------------------------------------------------
class App(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)

        # VTK setup
        self.rw, self.seed, self.widget, self.bike_actor = create_vtk_pipeline()

        # GUI setup
        self._build_ui()

        # Initial state
        self.state.update(INITIAL_STATE)

    @change("bike_opacity")
    def _on_opacity(self, bike_opacity, **_):
        self.bike_actor.property.opacity = bike_opacity
        self.ctrl.view_update()

    @change("line_widget")
    def _on_widget_update(self, line_widget, **_):
        if line_widget is None:
            return

        p1 = line_widget.get("p1")
        p2 = line_widget.get("p2")

        self.seed.SetPoint1(p1)
        self.seed.SetPoint2(p2)

        if line_widget.get("widget_update", False):
            self.widget.representation.point1_world_position = p1
            self.widget.representation.point2_world_position = p2

        self.ctrl.view_update()

    def _build_ui(self):
        with SinglePageWithDrawerLayout(self.server, full_height=True) as layout:
            self.ui = layout  # for jupyter integration

            # Toolbar
            with layout.toolbar as toolbar:
                toolbar.density = "compact"
                layout.title.set_text("Bike CFD")
                v3.VSpacer()
                v3.VSlider(
                    v_model=("bike_opacity", 1),
                    min=0,
                    max=1,
                    step=0.05,
                    density="compact",
                    hide_details=True,
                )
                v3.VBtn(icon="mdi-crop-free", click=self.ctrl.view_reset_camera)

            # Drawer
            with layout.drawer:
                tw.LineSeed(
                    image=to_url(IMAGE.path),
                    point_1=("line_widget.p1",),
                    point_2=("line_widget.p2",),
                    bounds=("[-0.399, 1.80, -1.12, 1.11, -0.43, 1.79]",),
                    update_seed="line_widget = { ...$event, widget_update: 1 }",
                    n_sliders=2,
                )

            # Content
            with layout.content:
                with vtklocal.LocalView(self.rw, throttle_rate=20) as view:
                    self.ctrl.view_update = view.update_throttle
                    self.ctrl.view_reset_camera = view.reset_camera

                    # Bind state to 3D widget interaction event
                    widget_id = view.register_vtk_object(self.widget)
                    view.listeners = (
                        "wasm_listeners",
                        {
                            widget_id: {
                                "InteractionEvent": {
                                    "line_widget": {
                                        "p1": (
                                            widget_id,
                                            "WidgetRepresentation",
                                            "Point1WorldPosition",
                                        ),
                                        "p2": (
                                            widget_id,
                                            "WidgetRepresentation",
                                            "Point2WorldPosition",
                                        ),
                                    }
                                },
                            },
                        },
                    )


def main():
    app = App()
    app.server.start()


if __name__ == "__main__":
    main()
