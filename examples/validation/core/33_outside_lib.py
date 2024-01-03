from trame.app import get_server
from trame.ui.html import DivLayout
from trame.widgets import html, helper

# From: https://quasar.dev/start/umd

module = dict(
    scripts=[
        "https://cdn.jsdelivr.net/npm/quasar@2.11.5/dist/quasar.umd.prod.js",
    ],
    styles=[
        "https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900|Material+Icons",
        "https://cdn.jsdelivr.net/npm/quasar@2.11.5/dist/quasar.prod.css",
    ],
    vue_use=[
        "Quasar",
    ],
)

QSlider = helper.create_class(
    "QSlider",
    "q-slider",
    module=module,
    properties=[
        "min",
        "max",
    ],
)

QBtn = helper.create_class(
    "QBtn",
    "q-btn",
    module=module,
    properties=[
        "label",
    ],
    events=[
        "click",
    ],
)

QCircularProgress = helper.create_class(
    "QCircularProgress",
    "q-circular-progress",
    module=module,
    properties=[
        "value",
        "indeterminate",
        "size",
        "thickness",
        "color",
        "center_color",
    ],
)

# -----------------------------------------------------------------------------
# Trame usage
# -----------------------------------------------------------------------------

server = get_server(client_type="vue3")


def reset():
    server.state.value = 5


with DivLayout(server) as layout:
    with html.Div(classes="q-pa-md"):
        with html.Div(classes="row items-center"):
            html.Div("{{ value }}", classes="col-2")
            QBtn(label="Hello", classes="col", click=reset)
            QCircularProgress(
                indeterminate=True,
                size="75px",
                thickness=0.6,
                color="lime",
                center_color="grey-8",
                classes="q-ma-md col",
            )
            QSlider(
                v_model_number=("value", 0),
                min=("1",),
                max=("100",),
                step=("1",),
                classes="col",
            )
            QCircularProgress(
                size="75px",
                thickness=0.6,
                color="lime",
                center_color="grey-8",
                classes="q-ma-md col",
                value=("value",),
            )

server.start()
