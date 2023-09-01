import pyvista as pv
from pyvista import examples

from trame.app import get_server
from trame.ui.quasar import QLayout
from trame.widgets import quasar, vtk, html

from trame.decorators import TrameApp, change

DEFAULT_CAMERA = [
    (567000.9232163235, 5119147.423216323, 6460.423216322832),
    (562835.0, 5114981.5, 2294.5),
    (-0.4082482904638299, -0.40824829046381844, 0.8164965809277649),
]


def color_to_rgb_float(color_str):
    red = int(color_str[1:3], 16)
    green = int(color_str[3:5], 16)
    blue = int(color_str[5:7], 16)
    return (
        float(red) / 255.0,
        float(green) / 255.0,
        float(blue) / 255.0,
    )


def color_to_rgb_hex(color_float):
    return "#{:02x}{:02x}{:02x}".format(
        int(255 * color_float[0]), int(255 * color_float[1]), int(255 * color_float[2])
    )


@TrameApp()
class StHelens:
    def __init__(self, server=None):
        if server is None:
            server = get_server()

        if isinstance(server, str):
            server = get_server(server)

        server.client_type = "vue3"
        self.server = server
        self._ui = None

        # setup VTK scene
        ds = examples.download_st_helens().warp_by_scalar()
        self.ploter = pv.Plotter()
        self.actor = self.ploter.add_mesh(ds, smooth_shading=True, lighting=True)
        self.ploter.camera_position = DEFAULT_CAMERA
        self.render_window = self.ploter.ren_win
        self.actor.prop.RenderPointsAsSpheresOn()
        self.actor.prop.SetPointSize(4)

        # Set initial values
        self.server.state.update(
            dict(
                actor_edges_show=self.actor.prop.show_edges,
                actor_opacity=self.actor.prop.opacity,
                actor_lighting=self.actor.prop.lighting,
                actor_culling_front=bool(self.actor.prop.GetFrontfaceCulling()),
                actor_culling_back=bool(self.actor.prop.GetBackfaceCulling()),
                actor_ambient=self.actor.prop.ambient,
                actor_diffuse=self.actor.prop.diffuse,
                actor_specular=self.actor.prop.specular,
                actor_specular_power=self.actor.prop.specular_power,
                actor_edge_color=color_to_rgb_hex(self.actor.prop.GetEdgeColor()),
            )
        )

        # Create ui
        self.ui

    @property
    def ctrl(self):
        return self.server.controller

    @property
    def ui(self):
        if self._ui is None:
            with QLayout(self.server, view="hHh lpR fFf") as layout:
                self._ui = layout

                with quasar.QHeader(elevated=True):
                    with quasar.QToolbar():
                        with quasar.QToolbarTitle() as title:
                            quasar.QBtn(
                                dense=True,
                                flat=True,
                                round=True,
                                icon="menu",
                                click="show_drawer = !show_drawer",
                            )
                            title.add_child("VTK - Mt St Helens")
                        quasar.QToggle(
                            v_model=("dark", False),
                            color="black",
                            checked_icon="dark_mode",
                            unchecked_icon="light_mode",
                            update_model_value="utils.quasar.Dark.set($event)",
                        )

                with quasar.QDrawer(
                    v_model=("show_drawer", True),
                    side="left",
                    overlay=False,
                    bordered=True,
                    width=350,
                ):
                    with quasar.QTabs(
                        v_model=("tab_active", "scene"),
                        inline_label=True,
                    ):
                        quasar.QTab(name="scene", label="Scene controller")
                        quasar.QTab(name="actor", label="Actor properties")

                    with quasar.QTabPanels(
                        v_model=("tab_active", "scene"),
                        animated=True,
                        classes="shadow-2 rounded-borders",
                    ):
                        # Scene tab
                        with quasar.QTabPanel(name="scene"):
                            with html.Div(classes="column"):
                                quasar.QToggle(
                                    label="Orientation Widget",
                                    v_model=("scene_orientation_widget", True),
                                )
                                quasar.QBtn(
                                    "Reset Camera",
                                    click=self.ctrl.view_reset_camera,
                                    classes="q-my-sm",
                                )
                                with quasar.QInput(
                                    filled=True,
                                    v_model=("scene_bg_color", "#ffffff"),
                                    dense=True,
                                    classes="q-my-sm",
                                    style=("{ background: scene_bg_color }",),
                                ):
                                    with html.Template(
                                        v_slot_append=True,
                                        __properties=[
                                            ("v_slot_append", "v-slot:append")
                                        ],
                                    ):
                                        with quasar.QIcon(
                                            name="colorize", classes="cursor-pointer"
                                        ):
                                            with quasar.QPopupProxy(
                                                cover=True,
                                                transition_show="scale",
                                                transition_hide="scale",
                                            ):
                                                quasar.QColor(v_model="scene_bg_color")

                        # Actor tab
                        with quasar.QTabPanel(name="actor"):
                            quasar.QItemLabel(
                                "Opacity: {{ actor_opacity }}",
                                caption=True,
                                classes="q-mt-sm",
                            )
                            quasar.QSlider(
                                v_model=("actor_opacity", 1),
                                min=(0,),
                                max=(1,),
                                step=(0.1,),
                            )
                            quasar.QToggle(
                                label="Lighting", v_model=("actor_lighting", True)
                            )
                            quasar.QSelect(
                                label="Interpolation",
                                classes="q-mb-md",
                                v_model=("actor_interpolation", "Flat"),
                                dense=True,
                                options=(
                                    "actor_interpolation_options",
                                    ["Flat", "Phong"],
                                ),
                            )
                            quasar.QToggle(
                                label="Show Edges",
                                v_model=("actor_edges_show", False),
                            )

                            quasar.QItemLabel(
                                "Edges color",
                                v_show="actor_edges_show",
                                caption=True,
                                classes="q-mt-sm",
                            )
                            quasar.QColor(
                                v_show="actor_edges_show",
                                v_model="actor_edge_color",
                                default_view="palette",
                                no_footer=True,
                                no_header_tabs=True,
                            )
                            quasar.QSelect(
                                label="Representation",
                                classes="q-mb-md",
                                v_model=("actor_representation", "Surface"),
                                dense=True,
                                options=(
                                    "actor_representation_options",
                                    ["Surface", "Wireframe", "Points"],
                                ),
                            )
                            with html.Div(classes="row"):
                                quasar.QToggle(
                                    label="Frontface Culling",
                                    v_model=("actor_culling_front", False),
                                    classes="col",
                                )
                                quasar.QToggle(
                                    label="Backface Culling",
                                    v_model=("actor_culling_back", False),
                                    classes="col",
                                )

                            quasar.QItemLabel(
                                "Ambient: {{actor_ambient}}",
                                caption=True,
                                classes="q-mt-sm",
                            )
                            quasar.QSlider(
                                v_model=("actor_ambient", 1),
                                min=(0,),
                                max=(1,),
                                step=(0.1,),
                            )
                            quasar.QItemLabel(
                                "Diffuse: {{actor_diffuse}}",
                                caption=True,
                                classes="q-mt-sm",
                            )
                            quasar.QSlider(
                                v_model=("actor_diffuse", 1),
                                min=(0,),
                                max=(1,),
                                step=(0.1,),
                            )
                            quasar.QItemLabel(
                                "Specular: {{actor_specular}}",
                                caption=True,
                                classes="q-mt-sm",
                            )
                            quasar.QSlider(
                                v_model=("actor_specular", 1),
                                min=(0,),
                                max=(1,),
                                step=(0.1,),
                            )
                            quasar.QItemLabel(
                                "Specular Power: {{actor_specular_power}}",
                                caption=True,
                                classes="q-mt-sm",
                            )
                            quasar.QSlider(
                                label="hello",
                                v_model=("actor_specular_power", 1),
                                min=(0,),
                                max=(100,),
                                step=(1,),
                            )

                with quasar.QPageContainer(classes="fullscreen", style="z-index: 0;"):
                    rw = self.render_window
                    with vtk.VtkRemoteView(rw, interactive_ratio=1) as view:
                        # with vtk.VtkLocalView(rw, interactive_ratio=1) as view:
                        self.ctrl.view_update = view.update
                        self.ctrl.view_reset_camera = view.reset_camera

        return self._ui

    @change("scene_bg_color")
    def on_scene_bg_color_change(self, scene_bg_color, **kwargs):
        color = color_to_rgb_float(scene_bg_color)
        for renderer in self.ploter.renderers:
            renderer.SetBackground(color)
        self.ctrl.view_update()

    @change("scene_orientation_widget")
    def on_axis_visiblity_change(self, scene_orientation_widget, **kwargs):
        for renderer in self.ploter.renderers:
            if scene_orientation_widget:
                renderer.show_axes()
            else:
                renderer.hide_axes()
        self.ctrl.view_update()

    @change("actor_edges_show")
    def on_actor_edges_show_change(self, actor_edges_show, **kwargs):
        self.actor.prop.show_edges = actor_edges_show
        self.ctrl.view_update()

    @change("actor_opacity")
    def on_actor_opacity_change(self, actor_opacity, **kwargs):
        self.actor.prop.opacity = actor_opacity
        self.ctrl.view_update()

    @change("actor_lighting")
    def on_actor_lighting_change(self, actor_lighting, **kwargs):
        self.actor.prop.lighting = actor_lighting
        self.ctrl.view_update()

    @change("actor_interpolation")
    def on_actor_interpolation(self, actor_interpolation, **kwargs):
        if actor_interpolation == "Flat":
            self.actor.prop.SetInterpolationToFlat()
        if actor_interpolation == "Phong":
            self.actor.prop.SetInterpolationToPhong()
        self.ctrl.view_update()

    @change("actor_edge_color")
    def on_actor_edge_color_change(self, actor_edge_color, **kwargs):
        color = color_to_rgb_float(actor_edge_color)
        self.actor.prop.edge_color = color
        self.ctrl.view_update()

    @change("actor_representation")
    def on_actor_representation_change(self, actor_representation, **kwargs):
        if actor_representation == "Points":
            self.actor.prop.SetRepresentationToPoints()
        if actor_representation == "Wireframe":
            self.actor.prop.SetRepresentationToWireframe()
        if actor_representation == "Surface":
            self.actor.prop.SetRepresentationToSurface()
        self.ctrl.view_update()

    @change("actor_culling_front")
    def on_actor_culling_front_change(self, actor_culling_front, **kwargs):
        self.actor.prop.SetFrontfaceCulling(actor_culling_front)
        self.ctrl.view_update()

    @change("actor_culling_back")
    def on_actor_culling_back_change(self, actor_culling_back, **kwargs):
        self.actor.prop.SetBackfaceCulling(actor_culling_back)
        self.ctrl.view_update()

    @change("actor_ambient")
    def on_actor_ambient_change(self, actor_ambient, **kwargs):
        self.actor.prop.ambient = actor_ambient
        self.ctrl.view_update()

    @change("actor_diffuse")
    def on_actor_diffuse_change(self, actor_diffuse, **kwargs):
        self.actor.prop.diffuse = actor_diffuse
        self.ctrl.view_update()

    @change("actor_specular")
    def on_actor_specular_change(self, actor_specular, **kwargs):
        self.actor.prop.specular = actor_specular
        self.ctrl.view_update()

    @change("actor_specular_power")
    def on_actor_specular_power_change(self, actor_specular_power, **kwargs):
        self.actor.prop.specular_power = actor_specular_power
        self.ctrl.view_update()


if __name__ == "__main__":
    app = StHelens()
    app.server.start()
