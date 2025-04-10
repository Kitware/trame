from trame.app import get_server

from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.ui.router import RouterViewLayout
from trame.widgets import vtk, html, vuetify, router, trame

from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

# Required for interactor initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa

# Required for rendering initialization, not necessary for
# local rendering, but doesn't hurt to include it
import vtkmodules.vtkRenderingOpenGL2  # noqa

# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

cone_source = vtkConeSource()
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cone_source.GetOutputPort())
actor = vtkActor()
actor.SetMapper(mapper)

renderer.AddActor(actor)
renderer.ResetCamera()
renderWindow.Render()


# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller


@state.change("resolution")
def update_resolution(resolution, **kwargs):
    cone_source.SetResolution(resolution)
    ctrl.view_update()


layout = SinglePageWithDrawerLayout(server)

# There are two ways to register a route
with RouterViewLayout(server, "/"):
    trame.LifeCycleMonitor(name="Home", events="['created', 'destroyed']")
    with vuetify.VCard():
        vuetify.VCardTitle("This is home {{ resolution }}")

with RouterViewLayout(server, "/foo"):
    trame.LifeCycleMonitor(name="Foo", events="['created', 'destroyed']")
    with vuetify.VCard():
        vuetify.VCardTitle("This is foo")
        with vuetify.VCardText():
            vuetify.VBtn("Take me back {{ resolution }}", click="$router.back()")
            with html.Div(classes="mt-6", style="height: 400px; min-height: 400px;"):
                view = vtk.VtkLocalView(renderWindow)
                view.update()
                ctrl.view_update.add(view.update)

# or use the contextmanager 'with_route'
with RouterViewLayout(server, "/bar/:id"):
    trame.LifeCycleMonitor(name="Bar", events="['created', 'destroyed']")
    with vuetify.VCard():
        vuetify.VCardTitle(
            "This is bar with ID '{{ $route.params.id }}' with resolution {{ resolution }}"
        )
        with vuetify.VCardText(classes="red lighten-5 pa-0"):
            with html.Div(style="height: 400px; min-height: 400px;"):
                view = vtk.VtkRemoteView(renderWindow)
                view.update()
                ctrl.view_update.add(view.update)
            with html.Div(style="height: 400px; min-height: 400px;"):
                view = vtk.VtkLocalView(renderWindow)
                view.update()
                ctrl.view_update.add(view.update)

# add <router-view />
with layout:
    layout.title.set_text("Multi-Page demo")
    trame.LifeCycleMonitor(name="Root", events="['created', 'destroyed']")

    with layout.toolbar as tb:
        vuetify.VSpacer()
        tb.add_child("{{ resolution }}")
        vuetify.VSlider(
            v_model=("resolution", 6),
            min=3,
            max=60,
            step=1,
            dense=True,
            hide_details=True,
            style="max-width: 300px;",
        )

    with layout.content:
        with vuetify.VContainer():
            router.RouterView()

    # add router buttons to the drawer
    with layout.drawer:
        with vuetify.VList(shaped=True, v_model=("selectedRoute", 0)):
            vuetify.VSubheader("Routes")

            with vuetify.VListItem(to="/"):
                with vuetify.VListItemIcon():
                    vuetify.VIcon("mdi-home")
                with vuetify.VListItemContent():
                    vuetify.VListItemTitle("Home")

            with vuetify.VListItem(to="/foo"):
                with vuetify.VListItemIcon():
                    vuetify.VIcon("mdi-food")
                with vuetify.VListItemContent():
                    vuetify.VListItemTitle("Foo")

            with vuetify.VListGroup(value=("true",), sub_group=True):
                with vuetify.Template(v_slot_activator=True):
                    vuetify.VListItemTitle("Bars")
                with vuetify.VListItemContent():
                    for i in range(5):
                        with vuetify.VListItem(to=f"/bar/{i + 1}"):
                            with vuetify.VListItemIcon():
                                vuetify.VIcon("mdi-peanut-outline")
                            with vuetify.VListItemContent():
                                vuetify.VListItemTitle("Bar {{ resolution }}")
                                vuetify.VListItemSubtitle(f"ID {i + 1}")

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    ctrl.view_update()
    server.start()
