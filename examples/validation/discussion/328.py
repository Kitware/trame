import plotly.graph_objects as go
import plotly.express as px

from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify, plotly

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller


def contour_plot():
    """https://plotly.com/python/contour-plots/"""
    return go.Figure(
        data=go.Contour(
            z=[
                [10, 10.625, 12.5, 15.625, 20],
                [5.625, 6.25, 8.125, 11.25, 15.625],
                [2.5, 3.125, 5.0, 8.125, 12.5],
                [0.625, 1.25, 3.125, 6.25, 10.625],
                [0, 0.625, 2.5, 5.625, 10],
            ]
        )
    )


def bar_plot(color="Gold"):
    return go.Figure(data=go.Bar(y=[2, 3, 1], marker_color=color))


def scatter():
    df = px.data.iris()

    fig = px.scatter(
        df,
        x="sepal_width",
        y="sepal_length",
        color="species",
        title="Using The add_trace() method With A Plotly Express Figure",
    )

    fig.add_trace(
        go.Scatter(
            x=[2, 4],
            y=[4, 8],
            mode="lines",
            line=go.scatter.Line(color="gray"),
            showlegend=False,
        )
    )

    return fig


card_config = {}

card_config["plots"] = {
    "type": "figure",
    "plot_list": [
        {"text": "Contour", "value": contour_plot},
        {"text": "Bar", "value": bar_plot},
        {"text": "Scatter", "value": scatter},
    ],
    "title": "Plots",
}

card_config["else"] = {
    "type": "figure",
    "plot_list": [
        {"text": "Bar", "value": bar_plot},
        {"text": "Contour", "value": contour_plot},
        {"text": "Scatter", "value": scatter},
    ],
    "title": "Else",
}


def on_event(type, e):
    print(type, e)


def _ui_card(title, ui_name):
    with vuetify.VCard(v_show=f"active_ui == '{ui_name}'"):
        vuetify.VCardTitle(
            title,
            classes="grey lighten-1 py-1 grey--text text--darken-3",
            style="user-select: none; cursor: pointer",
            hide_details=True,
            dense=True,
        )
        content = vuetify.VCardText(classes="py-2")
    return content


def add_card(key, value):
    with _ui_card(value["title"], key):
        with vuetify.VList(rounded=True):
            with vuetify.VListItemGroup(
                v_model=("active_plot", "Contour"), color="primary", mandatory=True
            ):
                for key in value["plot_list"]:
                    with vuetify.VListItem(value=key["text"]):
                        with vuetify.VListItemContent():
                            vuetify.VListItemTitle(key["text"])


@state.change("active_plot")
def update_plot(active_plot, **kwargs):
    if state.active_ui:
        for item in card_config[state.active_ui]["plot_list"]:
            if item["text"] == active_plot:
                ctrl.figure_update(item["value"]())


@state.change("visualization_mode")
def __update_mode(visualization_mode, **kwargs):
    for key in card_config.keys():
        if visualization_mode == key:
            state.active_ui = key
    state.active_plot = card_config[state.active_ui]["plot_list"][0]["text"]
    update_plot(state.active_plot)


state.trame__title = "Plotly"

with SinglePageWithDrawerLayout(server) as layout:
    layout.title.set_text("trame ❤️ plotly")

    with layout.drawer:
        with vuetify.VRadioGroup(
            v_model=("visualization_mode", next(iter(card_config))),
            classes="ml-4",
            height=100,
        ):
            for key, value in card_config.items():
                vuetify.VRadio(label=value["title"], value=key)
        for key, value in card_config.items():
            add_card(key, value)
    with layout.content:
        with vuetify.VContainer(fluid=True):
            with vuetify.VRow(dense=True):
                vuetify.VSpacer()
                figure = plotly.Figure(
                    display_logo=False,
                    display_mode_bar="true",
                    # click=(on_event, "['selected', utils.safe($event)]"),
                    # hover=(on_event, "['hover', utils.safe($event)]"),
                    # selecting=(on_event, "['selecting', $event]"),
                    # unhover=(on_event, "['unhover', $event]"),
                )
                ctrl.figure_update = figure.update
                vuetify.VSpacer()

if __name__ == "__main__":
    server.start()
