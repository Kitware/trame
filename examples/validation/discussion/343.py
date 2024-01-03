import time
import asyncio

import pyvista as pv

from pyvista.trame.ui import plotter_ui
from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout

pv.OFF_SCREEN = True

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

cyl = pv.Cylinder(resolution=8, direction=(0, 1, 0))

pl = pv.Plotter()
pl.background_color = (0.1, 0.2, 0.4)
pl.add_mesh(cyl, name="cyl")

keep_rotate = True


@ctrl.add_task("on_server_ready")
async def _update(**kwargs):
    await asyncio.sleep(5)
    while keep_rotate:
        cyl.rotate_x(10.0, inplace=True)
        cyl.rotate_y(-5.0, inplace=True)
        pl.add_mesh(cyl, name="cyl")
        pl.render()
        ctrl.view_update()
        await asyncio.sleep(0.5)


with SinglePageLayout(server) as layout:
    with layout.content:
        view = plotter_ui(pl)
        ctrl.view_update = view.update

server.start()
