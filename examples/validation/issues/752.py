import matplotlib.pyplot as plt
import io
import base64

from trame.app import TrameApp
from trame.widgets import html, vuetify3 as v3
from trame.ui.vuetify3 import SinglePageLayout


def text_to_base64_png(
    text: str, width: int = 600, height: int = 200, dpi: int = 100
) -> str:
    # Convert pixels to inches for figsize
    figsize = (width / dpi, height / dpi)

    # Create the figure
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.axis("off")  # Hide axes

    # Add text at the center
    ax.text(0.5, 0.5, text, fontsize=14, ha="center", va="center")

    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=dpi)
    plt.close(fig)
    buf.seek(0)

    # Convert to base64
    img_base64 = base64.b64encode(buf.read()).decode("ascii")
    return f"data:image/png;base64,{img_base64}"


# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------


class TabImages(TrameApp):
    def __init__(self, name=None):
        super().__init__(server=name)

        self.state.left_logo_img = text_to_base64_png(
            "Left Logo Image", width=512, height=488
        )
        self.state.right_logo_img = text_to_base64_png(
            "Right Logo Image", width=490, height=300
        )
        self.state.main_canvas_left_img = text_to_base64_png(
            "Left Main Canvas Image", width=700, height=488
        )
        self.state.main_canvas_right_img = text_to_base64_png(
            "Right Main Canvas Image", width=700, height=488
        )
        self.build_ui()

    def build_ui(self):
        with SinglePageLayout(self.server) as layout:
            layout.title.set_text("Dummy GUI")
            layout.icon.hide()

            # Toolbar with left and right logos
            with layout.toolbar:
                with v3.VRow(classes="align-center"):
                    with v3.VCol(cols=6):
                        html.Img(src=("left_logo_img",), style="height: 80px;")
                    with v3.VCol(cols=6, classes="d-flex justify-end"):
                        html.Img(src=("right_logo_img",), style="height: 80px;")

            # Tabs
            with layout.content:
                with v3.VTabs(v_model=("active_tab", "main"), grow=True):
                    v3.VTab("Main", value="main")
                    v3.VTab("Logic", value="logic")
                    v3.VTab("Overview", value="overview")

                with v3.VTabsWindow(v_model="active_tab"):
                    # Main tab
                    with v3.VTabsWindowItem(value="main"):
                        with v3.VContainer(fluid=True):
                            with v3.VRow():
                                with v3.VCol(cols=12, md=6):
                                    html.Img(
                                        src=("main_canvas_left_img",),
                                        style="width: 100%; height: auto;",
                                    )
                                with v3.VCol(cols=12, md=6):
                                    html.Img(
                                        src=("main_canvas_right_img",),
                                        style="width: 100%; height: auto;",
                                    )

                    # Logic tab
                    with v3.VTabsWindowItem(value="logic"):
                        with v3.VContainer(fluid=True):
                            with v3.VRow():
                                with v3.VCol(cols=12, md=6):
                                    html.Img(
                                        src=("main_canvas_left_img",),
                                        style="width: 100%; height: auto;",
                                    )
                                with v3.VCol(cols=12, md=6):
                                    html.Img(
                                        src=("main_canvas_right_img",),
                                        style="width: 100%; height: auto;",
                                    )

                    # Overview tab
                    with v3.VTabsWindowItem(value="overview"):
                        with v3.VContainer(fluid=True):
                            with v3.VRow():
                                with v3.VCol(cols=12, md=6):
                                    html.Img(
                                        src=("main_canvas_left_img",),
                                        style="width: 100%; height: auto;",
                                    )
                                with v3.VCol(cols=12, md=6):
                                    html.Img(
                                        src=("main_canvas_right_img",),
                                        style="width: 100%; height: auto;",
                                    )


if __name__ == "__main__":
    app = TabImages()
    app.server.start()
