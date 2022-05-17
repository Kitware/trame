r"""
Version for trame 1.x - https://github.com/Kitware/trame/blob/release-v1/examples/PlainPython/Matplotlib/basic/app.py
Delta v1..v2          - https://github.com/Kitware/trame/commit/75e15e23057dd93b7ff53389a8da544860ad10ee
"""

import numpy as np
import matplotlib.pyplot as plt

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, trame, matplotlib

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Chart examples from:
#   - http://jakevdp.github.io/blog/2013/12/19/a-d3-viewer-for-matplotlib/
# -----------------------------------------------------------------------------


def figure_size():
    if state.figure_size is None:
        return {}

    dpi = state.figure_size.get("dpi")
    rect = state.figure_size.get("size")
    w_inch = rect.get("width") / dpi
    h_inch = rect.get("height") / dpi

    return {
        "figsize": (w_inch, h_inch),
        "dpi": dpi,
    }


def FirstDemo():
    fig, ax = plt.subplots(**figure_size())
    np.random.seed(0)
    ax.plot(
        np.random.normal(size=100), np.random.normal(size=100), "or", ms=10, alpha=0.3
    )
    ax.plot(
        np.random.normal(size=100), np.random.normal(size=100), "ob", ms=20, alpha=0.1
    )

    ax.set_xlabel("this is x")
    ax.set_ylabel("this is y")
    ax.set_title("Matplotlib Plot Rendered in D3!", size=14)
    ax.grid(color="lightgray", alpha=0.7)

    return fig


# -----------------------------------------------------------------------------


def MultiLines():
    fig, ax = plt.subplots(**figure_size())
    x = np.linspace(0, 10, 1000)
    for offset in np.linspace(0, 3, 7):
        ax.plot(x, 0.9 * np.sin(x - offset), lw=5, alpha=0.4)
    ax.set_ylim(-1.2, 1.0)
    ax.text(5, -1.1, "Here are some curves", size=18)
    ax.grid(color="lightgray", alpha=0.7)

    return fig


# -----------------------------------------------------------------------------


def DotsandPoints():
    fig, ax = plt.subplots(**figure_size())
    ax.plot(
        np.random.rand(20),
        "-o",
        alpha=0.5,
        color="black",
        linewidth=5,
        markerfacecolor="green",
        markeredgecolor="lightgreen",
        markersize=20,
        markeredgewidth=10,
    )
    ax.grid(True, color="#EEEEEE", linestyle="solid")
    ax.set_xlim(-2, 22)
    ax.set_ylim(-0.1, 1.1)

    return fig


# -----------------------------------------------------------------------------


def MovingWindowAverage():
    np.random.seed(0)
    t = np.linspace(0, 10, 300)
    x = np.sin(t)
    dx = np.random.normal(0, 0.3, 300)

    kernel = np.ones(25) / 25.0
    x_smooth = np.convolve(x + dx, kernel, mode="same")

    fig, ax = plt.subplots(**figure_size())
    ax.plot(t, x + dx, linestyle="", marker="o", color="black", markersize=3, alpha=0.3)
    ax.plot(t, x_smooth, "-k", lw=3)
    ax.plot(t, x, "--k", lw=3, color="blue")

    return fig


# -----------------------------------------------------------------------------


def Subplots():
    fig = plt.figure(**figure_size())
    fig.subplots_adjust(hspace=0.3)

    np.random.seed(0)

    for i in range(1, 5):
        ax = fig.add_subplot(2, 2, i)
        color = np.random.random(3)
        ax.plot(np.random.random(30), lw=2, c=color)
        ax.set_title("RGB = ({0:.2f}, {1:.2f}, {2:.2f})".format(*color), size=14)
        ax.grid(color="lightgray", alpha=0.7)

    return fig


# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


@state.change("active_figure", "figure_size")
def update_chart(active_figure, **kwargs):
    ctrl.update_figure(globals()[active_figure]())


# -----------------------------------------------------------------------------
# UI
# -----------------------------------------------------------------------------

state.trame__title = "Matplotly"

with SinglePageLayout(server) as layout:
    layout.title.set_text("trame ❤️ matplotlib")

    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VSelect(
            v_model=("active_figure", "FirstDemo"),
            items=(
                "figures",
                [
                    {"text": "First Demo", "value": "FirstDemo"},
                    {"text": "Multi Lines", "value": "MultiLines"},
                    {"text": "Dots and Points", "value": "DotsandPoints"},
                    {"text": "Moving Window Average", "value": "MovingWindowAverage"},
                    {"text": "Subplots", "value": "Subplots"},
                ],
            ),
            hide_details=True,
            dense=True,
        )

    with layout.content:
        with vuetify.VContainer(fluid=True, classes="fill-height pa-0 ma-0"):
            with trame.SizeObserver("figure_size"):
                html_figure = matplotlib.Figure(style="position: absolute")
                ctrl.update_figure = html_figure.update

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
