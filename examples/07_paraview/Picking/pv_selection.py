# import asyncio
from trame.app import get_server, asynchronous
from trame.assets.local import LocalFileManager
from trame.widgets import vuetify, paraview
from trame.ui.vuetify import SinglePageLayout

from pathlib import Path

from paraview import simple

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller

ICON_SIZE = 16

ASSETS = LocalFileManager(__file__)
ASSETS.url("select_surface_point", "icons/pqSurfaceSelectionPoint.svg")
ASSETS.url("select_surface_cell", "icons/pqSurfaceSelectionCell.svg")
ASSETS.url("select_frustrum_points", "icons/pqFrustumSelectionPoint.svg")
ASSETS.url("select_frustrum_cells", "icons/pqFrustumSelectionCell.svg")
# ASSETS.url("select_poly_points", "icons/pqPolygonSelectSurfacePoint.svg")
# ASSETS.url("select_poly_cells", "icons/pqPolygonSelectSurfaceCell.svg")
ASSETS.url("select_block", "icons/pqSelectBlock.svg")
# ASSETS.url("select_hover_point", "icons/pqSurfaceHoveringPoint.svg")
# ASSETS.url("select_hover_cell", "icons/pqSurfaceHoveringCell.svg")

MODE_TO_METHOD = dict(
    select_surface_point=simple.SelectSurfacePoints,
    select_surface_cell=simple.SelectSurfaceCells,
    select_frustrum_points=simple.SelectPointsThrough,
    select_frustrum_cells=simple.SelectCellsThrough,
    select_block=simple.SelectSurfaceBlocks,
)

# -----------------------------------------------------------------------------
# ParaView code
# -----------------------------------------------------------------------------

DATA_FILE_PATH = str(Path(__file__).parent.parent.parent / "data/can.ex2")

dataset = simple.OpenDataFile(DATA_FILE_PATH)
representation = simple.Show(dataset)
view = simple.Render()


@ctrl.set("on_selection_change")
def on_box_selection(event):
    fn = MODE_TO_METHOD[state.selection_mode]
    min_x, max_x, min_y, max_y = event.get("selection")
    fn(Rectangle=[int(min_x), int(min_y), int(max_x), int(max_y)], Modifier=None)
    ctrl.view_update()
    state.selection_mode = None


@state.change("selection_mode")
def on_mode_change(selection_mode, **kwargs):
    # Use box for selection
    state.box_selection = selection_mode in [
        "select_surface_point",
        "select_surface_cell",
        "select_frustrum_points",
        "select_frustrum_cells",
        "select_block",
    ]

    # Toggle from interactive to selection
    if selection_mode is None:
        view.InteractionMode = "3D"
    else:
        view.InteractionMode = "Selection"

    # Handle hover with live update
    # => attempt to do hover selection...
    # state.send_mouse = selection_mode in ["select_hover_point", "select_hover_cell"]
    # if state.send_mouse:
    #     asynchronous.create_task(animate())


# async def animate():
#     while state.send_mouse:
#         await asyncio.sleep(0.1)
#         ctrl.view_update()

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

with SinglePageLayout(server) as layout:
    layout.icon.click = ctrl.view_reset_camera
    layout.title.set_text("ParaView Selection")

    with layout.toolbar:
        vuetify.VSpacer()
        with vuetify.VBtnToggle(v_model=("selection_mode", None)):
            for name, value in ASSETS.assets.items():
                with vuetify.VBtn(value=name, small=True):
                    vuetify.VImg(
                        src=value,
                        contain=True,
                        height=ICON_SIZE,
                        width=ICON_SIZE,
                    )

    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            html_view = paraview.VtkRemoteView(
                view,
                ref="view",
                interactive_ratio=1,
                enable_picking=("send_mouse", False),
                box_selection=("box_selection", False),
                box_selection_change=(ctrl.on_selection_change, "[$event]"),
            )
            ctrl.view_reset_camera = html_view.reset_camera
            ctrl.view_update = html_view.update

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main():
    server.start()


if __name__ == "__main__":
    main()
