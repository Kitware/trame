"""
Installation requirements:
    pip install trame trame-vuetify trame-vtk trame-components trame-rca
"""

import paraview.web.venv
from paraview import simple
import asyncio

from trame.app import get_server, asynchronous
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify, trame, html, paraview, rca

# -----------------------------------------------------------------------------
# Global helpers
# -----------------------------------------------------------------------------

PXM = simple.servermanager.ProxyManager()
WAVELET_SCALAR_RANGE = [37.35310363769531, 276.8288269042969]


def generate_contour_values(data_range, number_of_contours):
    delta = (data_range[1] - data_range[0]) / (number_of_contours - 1)
    return [data_range[0] + (delta * float(i)) for i in range(number_of_contours)]


def id_to_proxy(_id):
    try:
        _id = int(_id)
    except Exception:
        return None
    if _id <= 0:
        return None

    return simple.servermanager._getPyProxy(
        simple.servermanager.ActiveConnection.Session.GetRemoteObject(_id)
    )


# -----------------------------------------------------------------------------
# Wavelet Application
# -----------------------------------------------------------------------------
class App:
    def __init__(self, server=None):
        server = get_server(server, client_type="vue2")

        self.server = server
        self.state = server.state
        self.ctrl = server.controller

        # ParaView Async
        self._running = True
        self._ready = False

        # internal state
        self.hidden_pipeline_proxy_ids = []
        self.active_proxy = None
        self.active_representation = None
        self.active_view = None

        # initial state
        self.state.target_fps = 30  # suggested for jpeg.
        self.state.wavelet_size = 10
        self.state.contours_count = 10
        self.state.working_proxy = ""
        self.state.wavelet_id = 0
        self.state.contour_id = 0
        self.state.clip_id = 0
        self.state.threshold_id = 0
        self.state.active_data_info = None

        # controller
        self.ctrl.on_server_ready.add(self.initialize)

        # state listeners
        self.state.change("contours_count")(self.ui_state_contours_update)
        self.state.change("wavelet_size")(self.ui_state_wavelet_update)
        self.state.change("clip_x_origin")(self.ui_state_clip_update)
        self.state.change("slice_x_origin")(self.ui_state_slice_update)
        self.state.change("threshold_range")(self.ui_state_threshold_update)
        self.state.change("target_fps")(self.ui_state_target_fps_change)

    # ---------------------------------------------------------------
    # Instance life cycle
    # ---------------------------------------------------------------

    def initialize(self, **kwargs):
        # Tasks to monitor state change
        asynchronous.create_task(self.monitor_server_status())

        # RemoteControllerArea
        # self._view_handler = ViewAdapter(self.active_view, "view")
        # self.ctrl.rc_area_register(self._view_handler)

        self._ready = True

        print("Server ready")
        self._push_pipeline_to_ui()
        self.ctrl.view_reset_camera()

    # ---------------------------------------------------------------
    # Background async monitoring tasks
    # ---------------------------------------------------------------

    async def monitor_server_status(self):
        while self._running:
            with self.state as state:
                await asyncio.sleep(1 / self.state.target_fps)

                # Spinning
                if state.spinning and self.active_view:
                    self.active_view.GetActiveCamera().Azimuth(1)
                    self.ctrl.view_update()

                # Update client
                state.status_server += 5
                if state.status_server > 360:
                    state.status_server = 0

    # ---------------------------------------------------------------
    # General API
    # ---------------------------------------------------------------

    def setup_demo(self):
        view = simple.GetRenderView()
        hide_list = []

        # wavelet ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.wavelet = simple.Wavelet()
        rep = simple.Show()
        rep.Representation = "Outline"

        # Contour ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.contour = simple.Contour(
            Input=self.wavelet,
            Isosurfaces=generate_contour_values(WAVELET_SCALAR_RANGE, 10),
            ContourBy=["POINTS", "RTData"],
        )
        rep = simple.Show()
        simple.Hide(self.contour)
        hide_list.append(rep)

        # Clip ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.clip = simple.Clip(
            Input=self.contour,
        )
        rep = simple.Show()

        # Slice ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.slice = simple.Slice(
            Input=self.wavelet,
            SliceType="Plane",
        )
        self.slice.SliceType.Normal = [0, 1, 0]
        rep = simple.Show()

        # Threshold ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.threshold = simple.Threshold(
            Input=self.wavelet,
            Scalars=["POINTS", "RTData"],
            LowerThreshold=180,
            UpperThreshold=240,
        )
        rep = simple.Show()

        # Plane ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # create a plane source as a fake widget of the clip
        # make sure to keep them synchronized
        self.plane = simple.Plane(
            Origin=[0, -10, -10],
            Point1=[0, -10, 10],
            Point2=[0, 10, -10],
            XResolution=10,
            YResolution=10,
        )
        rep = simple.Show()
        rep.Representation = "Wireframe"
        self.hidden_pipeline_proxy_ids.append(self.plane.GetGlobalIDAsString())

        # Keep track of view and ids
        self.active_view = view
        self.state.wavelet_id = self.wavelet.GetGlobalIDAsString()
        self.state.contour_id = self.contour.GetGlobalIDAsString()
        self.state.clip_id = self.clip.GetGlobalIDAsString()
        self.state.slice_id = self.slice.GetGlobalIDAsString()
        self.state.threshold_id = self.threshold.GetGlobalIDAsString()

        # Activate wavelet by default
        simple.SetActiveSource(self.wavelet)

    def _push_pipeline_to_ui(self):
        sources = []
        proxies = PXM.GetProxiesInGroup("sources")
        view_proxy = simple.GetActiveView()

        node_map = {}
        for key in proxies:
            proxy = proxies[key]

            source = {"parent": "0"}
            source["name"] = key[0]
            source["id"] = key[1]

            representation = simple.GetRepresentation(proxy=proxy, view=view_proxy)
            source["rep"] = representation.GetGlobalIDAsString()
            source["visible"] = int(representation.Visibility)

            if hasattr(proxy, "Input") and proxy.Input:
                inputProp = proxy.Input
                if hasattr(inputProp, "GetNumberOfProxies"):
                    numProxies = inputProp.GetNumberOfProxies()
                    if numProxies > 1:
                        source["multiparent"] = numProxies
                        for inputIdx in range(numProxies):
                            proxyId = inputProp.GetProxy(inputIdx).GetGlobalIDAsString()
                            if inputIdx == 0:
                                source["parent"] = proxyId
                            else:
                                source[f"parent_{inputIdx}"] = proxyId
                    elif numProxies == 1:
                        source["parent"] = inputProp.GetProxy(0).GetGlobalIDAsString()
                else:
                    source["parent"] = inputProp.GetGlobalIDAsString()

            if key[1] not in self.hidden_pipeline_proxy_ids:
                sources.append(source)

            node_map[source["id"]] = source

        with self.state as state:
            state.git_tree_sources = sources
            state.git_tree_actives = [simple.GetActiveSource().GetGlobalIDAsString()]

    def _push_data_info(self):
        proxy = simple.GetActiveSource()
        info = proxy.GetDataInformation()
        with self.state as state:
            state.active_data_info = dict(
                points=info.GetNumberOfPoints(), cells=info.GetNumberOfCells()
            )

    # ---------------------------------------------------------------
    # GUI callbacks
    # ---------------------------------------------------------------

    def ui_event_pipeline_update(self, active):
        proxy = id_to_proxy(active[0])
        simple.SetActiveSource(proxy)
        self._push_pipeline_to_ui()
        self._push_data_info()

    def ui_event_pipeline_visibility_update(self, selection):
        proxy_id = selection.get("id")
        visible = selection.get("visible")
        proxy = id_to_proxy(proxy_id)
        rep = simple.GetRepresentation(proxy)
        rep.Visibility = visible
        self._push_pipeline_to_ui()
        self.ctrl.view_update()

    def ui_state_contours_update(self, contours_count, **kwargs):
        if not self._ready:
            return

        self.contour.Isosurfaces = generate_contour_values(
            WAVELET_SCALAR_RANGE, contours_count
        )
        self.ctrl.view_update()
        self._push_data_info()

    def ui_state_wavelet_update(self, wavelet_size, **kwargs):
        if not self._ready:
            return

        self.wavelet.WholeExtent = [
            -wavelet_size,
            wavelet_size,
            -wavelet_size,
            wavelet_size,
            -wavelet_size,
            wavelet_size,
        ]

        # update plane
        scaled_offset = self.clip.ClipType.Offset
        self.plane.Origin = [scaled_offset, -wavelet_size, -wavelet_size]
        self.plane.Point1 = [scaled_offset, -wavelet_size, wavelet_size]
        self.plane.Point2 = [scaled_offset, wavelet_size, -wavelet_size]

        self.ctrl.view_update()
        self._push_data_info()

    def ui_state_clip_update(self, clip_x_origin, **kwargs):
        if not self._ready:
            return

        minX, maxX, minY, maxY, minZ, maxZ = self.wavelet.WholeExtent
        scaled_offset = (maxX - minX) * clip_x_origin / 2.0

        # update plane
        self.plane.Origin = [scaled_offset, minY, minZ]
        self.plane.Point1 = [scaled_offset, minY, maxZ]
        self.plane.Point2 = [scaled_offset, maxY, minZ]

        # update clip
        self.clip.ClipType.Offset = scaled_offset

        self.ctrl.view_update()
        self._push_data_info()

    def ui_state_slice_update(self, slice_x_origin, **kwargs):
        if not self._ready:
            return

        minX, maxX, *_ = self.wavelet.WholeExtent
        scaled_offset = (maxX - minX) * slice_x_origin / 2.0
        self.slice.SliceType.Offset = scaled_offset

        self.ctrl.view_update()
        self._push_data_info()

    def ui_state_threshold_update(self, threshold_range, **kwargs):
        if not self._ready:
            return

        self.threshold.LowerThreshold = threshold_range[0]
        self.threshold.UpperThreshold = threshold_range[1]

        self.ctrl.view_update()
        self._push_data_info()

    def ui_state_target_fps_change(self, target_fps, **kwargs):
        if not self._ready:
            return
        # self._view_handler.target_fps = target_fps
        print(target_fps)


# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
app = App(server)
app.setup_demo()

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

with SinglePageWithDrawerLayout(server) as layout:
    with layout.icon:
        vuetify.VIcon("mdi-clock-time-four-outline")

    with layout.title as title:
        title.style = "padding-left: 0;"
        title.set_text("ParaView 5.11")

    with layout.toolbar as toolbar:
        toolbar.dense = True
        vuetify.VSpacer()
        vuetify.VProgressCircular(
            "S",
            color="red",
            size=35,
            width=5,
            rotate=("status_server", 0),
            value=("20",),
            classes="mx-2",
        )
        vuetify.VProgressCircular(
            "C",
            color="teal",
            size=35,
            width=5,
            indeterminate=True,
            classes="mx-2",
        )
        vuetify.VDivider(vertical=True, classes="mx-2")
        vuetify.VCheckbox(
            small=True,
            v_model=("spinning", False),
            dense=True,
            classes="mx-2",
            hide_details=True,
            on_icon="mdi-axis-z-rotate-counterclockwise",
            off_icon="mdi-axis-z-rotate-counterclockwise",
        )
        with vuetify.VBtn(
            icon=True, small=True, click=app.ctrl.view_reset_camera, classes="mx-2"
        ):
            vuetify.VIcon("mdi-crop-free")

    with layout.drawer as drawer:
        drawer.width = 300
        trame.GitTree(
            sources=("git_tree_sources", []),
            actives=("git_tree_actives", []),
            visibility_change=(app.ui_event_pipeline_visibility_update, "[$event]"),
            actives_change=(app.ui_event_pipeline_update, "[$event]"),
        )
        with vuetify.VCard(
            classes="mb-2 mx-1", v_show="git_tree_actives.includes(wavelet_id)"
        ):
            with vuetify.VCardTitle(classes="py-0"):
                html.Div("Wavelet")
                vuetify.VSpacer()
                html.Div("{{ wavelet_size }}")

            vuetify.VDivider()
            with vuetify.VCardText():
                vuetify.VSlider(
                    v_model=("wavelet_size", 10),
                    min=5,
                    max=100,
                    step=1,
                    hide_details=True,
                    dense=True,
                )
        with vuetify.VCard(
            classes="mb-2 mx-1", v_show="git_tree_actives.includes(contour_id)"
        ):
            with vuetify.VCardTitle(classes="py-0"):
                html.Div("Contours")
                vuetify.VSpacer()
                html.Div("{{ contours_count }}")

            vuetify.VDivider()
            with vuetify.VCardText():
                vuetify.VSlider(
                    v_model=("contours_count", 10),
                    min=5,
                    max=100,
                    step=1,
                    hide_details=True,
                    dense=True,
                )
        with vuetify.VCard(
            classes="mb-2 mx-1", v_show="git_tree_actives.includes(clip_id)"
        ):
            with vuetify.VCardTitle(classes="py-0"):
                html.Div("Clip")
                vuetify.VSpacer()
                html.Div("{{ clip_x_origin }}")

            vuetify.VDivider()
            with vuetify.VCardText():
                vuetify.VSlider(
                    v_model=("clip_x_origin", 0),
                    min=-1,
                    max=1,
                    step=0.1,
                    hide_details=True,
                    dense=True,
                )
        with vuetify.VCard(
            classes="mb-2 mx-1", v_show="git_tree_actives.includes(slice_id)"
        ):
            with vuetify.VCardTitle(classes="py-0"):
                html.Div("Slice")
                vuetify.VSpacer()
                html.Div("{{ slice_x_origin }}")

            vuetify.VDivider()
            with vuetify.VCardText():
                vuetify.VSlider(
                    v_model=("slice_x_origin", 0),
                    min=-1,
                    max=1,
                    step=0.1,
                    hide_details=True,
                    dense=True,
                )
        with vuetify.VCard(
            classes="mb-2 mx-1", v_show="git_tree_actives.includes(threshold_id)"
        ):
            with vuetify.VCardTitle(classes="py-0"):
                html.Div("Threshold")
                vuetify.VSpacer()
                html.Div("{{ threshold_range }}")
            vuetify.VDivider()
            with vuetify.VCardText():
                vuetify.VRangeSlider(
                    v_model=("threshold_range", (180, 240)),
                    min=WAVELET_SCALAR_RANGE[0],
                    max=WAVELET_SCALAR_RANGE[1],
                    step=0.5,
                    hide_details=True,
                    dense=True,
                )

        with vuetify.VCard(classes="mb-2 mx-1"):
            with vuetify.VCardTitle(classes="py-0"):
                html.Div("Stats")
                vuetify.VSpacer()
                vuetify.VIcon("mdi-dots-triangle", x_small=True, classes="mr-1")
                html.Div(
                    r"{{ active_data_info?.points.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') | 0 }}",
                    classes="text-caption",
                )
                vuetify.VSpacer()
                vuetify.VIcon("mdi-triangle-outline", x_small=True, classes="mr-1")
                html.Div(
                    r"{{ active_data_info?.cells.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') || 0 }}",
                    classes="text-caption",
                )
            vuetify.VDivider()
            with vuetify.VCardText(style="height: 150px"):
                rca.StatisticsDisplay(
                    name="view",
                    fps_delta=1.5,
                    stat_window_size=10,
                    history_window_size=30,
                    reset_ms_threshold=100,
                    ws_topic="viewport.image.push.subscription",
                    packet_decorator=(
                        """
                        (v) => {
                            return {
                                name: 'view',
                                serverTime: Date.now(),
                                contentSize: v.memsize,
                            };
                        }
                    """,
                    ),
                )

        with vuetify.VCard(classes="my-2 mx-1"):
            with vuetify.VCardTitle(classes="py-0"):
                html.Div("Image Delivery")
            vuetify.VDivider()
            with vuetify.VCardText():
                html.Div("Target: {{ target_fps }} fps", classes="text-subtitle-2 mt-4")
                vuetify.VSlider(
                    v_model=("target_fps", 30),
                    min=10,
                    max=60,
                    step=5,
                    hide_details=True,
                    dense=True,
                )

    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            # rca.RemoteControlledArea(
            #     name="view", display=("active_display_mode", "image")
            # )
            v = paraview.VtkRemoteView(app.active_view, interactive_ratio=1)
            app.ctrl.view_reset_camera = v.reset_camera
            app.ctrl.view_update = v.update

# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
