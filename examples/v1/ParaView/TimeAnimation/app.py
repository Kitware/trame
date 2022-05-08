from paraview.web import venv  # Available in PV 5.10-RC2+
import os
import json
import asyncio

from trame import get_cli_parser, state
from trame.html import vuetify, paraview
from trame.layouts import SinglePage

import paraview as pv
from paraview import simple

animation_scene = simple.GetAnimationScene()
time_keeper = animation_scene.TimeKeeper

parser = get_cli_parser()
metadata = None
layout = None
time_values = []
representation = None


def load_data(**kwargs):
    global time_values, representation
    # CLI
    args, _ = parser.parse_known_args()
    full_path = os.path.abspath(args.data)
    base_path = os.path.dirname(full_path)
    files = []
    reader_props = {}

    with open(full_path, "r") as f:
        metadata = json.load(f)
        reader_props = metadata.get("reader_properties", {})
        fields = metadata.get("fields", [])
        for name in metadata.get("files", []):
            files.append(os.path.join(base_path, name))

    reader = simple.OpenDataFile(files)
    for key, value in reader_props.items():
        reader.GetProperty(key).SetData(value)

    reader.UpdatePipeline()
    representation = simple.Show(reader, view)
    time_values = list(time_keeper.TimestepValues)

    update_color_by(0, fields, "remote")
    state.time_value = time_values[0]
    state.times = len(time_values) - 1
    state.fields = fields

    simple.ResetCamera()
    view.CenterOfRotation = view.CameraFocalPoint
    update_view("local", flush=False)


# -----------------------------------------------------------------------------
# ParaView pipeline
# -----------------------------------------------------------------------------

# Rendering setup
view = simple.GetRenderView()
view.UseColorPaletteForBackground = 0
view.Background = [0.8, 0.8, 0.8]
view.OrientationAxesVisibility = 0
view = simple.Render()

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


@state.change("active_array")
def update_color_by(active_array, fields, viewMode="remote", **kwargs):
    array = fields[active_array]
    simple.ColorBy(representation, (array.get("location"), array.get("text")))
    representation.RescaleTransferFunctionToDataRange(True, False)
    name = pv.make_name_valid(array.get("text"))
    lut = simple.GetColorTransferFunction(name)
    pwf = simple.GetOpacityTransferFunction(name)
    _min, _max = array.get("range")
    lut.RescaleTransferFunction(_min, _max)
    pwf.RescaleTransferFunction(_min, _max)
    update_view(viewMode)


@state.change("time")
def update_time(time, viewMode, **kwargs):
    # print("update_time", time)
    if time >= len(time_values):
        time = 0
        state.time = time
    time_value = time_values[time]
    time_keeper.Time = time_value
    state.time_value = time_value
    update_view(viewMode)


@state.change("play")
def update_play(play, **kwargs):
    loop = asyncio.get_event_loop()
    loop.create_task(animate())


@state.change("viewMode")
def update_view(viewMode, flush=True, **kwargs):
    html_view.update_image()
    if viewMode == "local":
        html_view.update_geometry()
        if flush:
            # can only flush once protocol is initialized (publish)
            state.flush("viewScene")


async def animate():
    keep_going = True
    while keep_going:
        if state.play:
            state.time += 1
            update_time(state.time, state.viewMode)
            state.flush("time", "time_value")
        await asyncio.sleep(0.1)


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------
html_view = paraview.VtkRemoteLocalView(view, namespace="view")

layout = SinglePage("ParaView", on_ready=load_data)
layout.title.set_text("Time")
layout.logo.click = html_view.reset_camera

with layout.toolbar:
    vuetify.VSpacer()
    vuetify.VSelect(
        v_model=("active_array", 0),
        items=("fields", []),
        style="max-width: 200px",
        hide_details=True,
        dense=True,
    )
    vuetify.VTextField(
        v_model=("time_value", 0),
        disabled=True,
        hide_details=True,
        dense=True,
        style="max-width: 200px",
        classes="mx-2",
    )
    vuetify.VSlider(
        v_model=("time", 0),
        min=0,
        max=("times", 1),
        hide_details=True,
        dense=True,
        style="max-width: 200px",
    )

    vuetify.VCheckbox(
        v_model=("play", False),
        off_icon="mdi-play",
        on_icon="mdi-stop",
        hide_details=True,
        dense=True,
        classes="mx-2",
    )

    with vuetify.VBtn(icon=True, click="$refs.view.resetCamera()"):
        vuetify.VIcon("mdi-crop-free")

    vuetify.VCheckbox(
        v_model=("viewMode", "remote"),
        true_value="remote",
        false_value="local",
        off_icon="mdi-rotate-3d",
        on_icon="mdi-video-image",
        hide_details=True,
        dense=True,
        classes="mx-2",
    )

    vuetify.VProgressLinear(
        indeterminate=True,
        absolute=True,
        bottom=True,
        active=("busy",),
    )

with layout.content:
    vuetify.VContainer(
        fluid=True,
        classes="pa-0 fill-height",
        children=[html_view],
    )


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    parser.add_argument("--data", help="Path to state file", dest="data")
    layout.start()
