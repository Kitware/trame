import pyvista as pv
from pyvista import examples
from pyvista.trame.ui import plotter_ui
from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout

pv.OFF_SCREEN = True

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

mesh = examples.load_random_hills()

pl = pv.Plotter()
pl.add_mesh(mesh)

with SinglePageLayout(server) as layout:
    with layout.content:
        view = plotter_ui(pl)

server.start()
