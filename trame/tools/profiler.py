import math
from pathlib import Path

from trame_client.widgets.core import HtmlElement

from trame.app import TrameApp
from trame.decorators import change
from trame.ui.html import DivLayout
from trame.widgets import client, html

LABEL_WIDTH = 0.25


class Record:
    __slots__ = ["name", "t0", "dt", "valid"]

    def __init__(self, line):
        self.valid = False

        if not line or len(line) < 60:
            return

        self.name = line[:60].strip()
        times = line[60:].split()
        if len(times) < 3:
            return

        self.t0 = float(times[0])
        self.dt = float(times[1])
        self.valid = True

    def expend_time(self, min_value, max_value):
        return (
            min_value if min_value < self.t0 else self.t0,
            max_value if max_value > self.t0 else self.t0 + self.dt / 1000,
        )

    def apply_offset(self, v):
        self.t0 -= v

    @property
    def rect(self):
        return {
            "x": int(self.t0 * 1000),
            "width": round(self.dt + 1),
            "title": f"{self.dt} ms",
        }


class ProfilerAnalyzer:
    def __init__(self, input_file):
        self.min_time = math.inf
        self.max_time = 0
        self.tracks = {}

        # Parse file
        with Path(input_file).open() as file:
            for line in file:
                record = Record(line)
                if not record.valid:
                    continue

                self.min_time, self.max_time = record.expend_time(
                    self.min_time, self.max_time
                )
                self.tracks.setdefault(record.name, []).append(record)

        # Apply offset
        offset = self.min_time - LABEL_WIDTH
        tracks_t0 = []
        for name, records in self.tracks.items():
            tracks_t0.append((name, records[0].t0))
            for record in records:
                record.apply_offset(offset)
        tracks_t0.sort(key=lambda x: x[1])

        self.max_time -= offset
        self.min_time = 0

        # Capture sorted names
        self.track_names = [name for name, _ in tracks_t0]

    def rects(self, height, **add_on):
        all_rects = []
        y = 0
        for name in self.track_names:
            for record in self.tracks[name]:
                all_rects.append({**record.rect, "y": y, "height": height, **add_on})
            y += height
        return all_rects

    def lines(self, height, **add_on):
        all_lines = []
        y = 0
        for _ in self.track_names:
            all_lines.append(
                {"x1": 0, "x2": int(self.max_time * 1000), "y1": y, "y2": y, **add_on}
            )
            y += height
        all_lines.append(
            {"x1": 0, "x2": int(self.max_time * 1000), "y1": y, "y2": y, **add_on}
        )

        # End line
        all_lines.append(
            {
                "x1": int(self.max_time * 1000),
                "x2": int(self.max_time * 1000),
                "y1": 0,
                "y2": y + height,
                **add_on,
            }
        )

        # Time ticks
        for i in range(0, 1 + int(self.width / 1000)):
            all_lines.append(
                {
                    "x1": (i + LABEL_WIDTH) * 1000,
                    "x2": (i + LABEL_WIDTH) * 1000,
                    "y1": y,
                    "y2": y + height,
                    **add_on,
                }
            )

        return all_lines

    def texts(self, height, **add_on):
        all_texts = []
        y = 0
        for name in self.track_names:
            all_texts.append({"text": name, "y": int(y + 0.75 * height), **add_on})
            y += height

        # Time labels
        for i in range(0, 1 + int(self.width / 1000)):
            all_texts.append(
                {
                    "text": f"{i}s",
                    "x": (i + LABEL_WIDTH) * 1000 + 5,
                    "y": int(y + 0.75 * height),
                    "text-anchor": "start",
                    # **add_on,
                }
            )

        return all_texts

    @property
    def width(self):
        return int(self.max_time * 1000)

    @property
    def n_tracks(self):
        return len(self.track_names)


class Rect(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__("rect", **kwargs)
        self._attr_names += ["x", "y", "width", "height"]


class Line(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__("line", **kwargs)


class Text(HtmlElement):
    def __init__(self, txt, **kwargs):
        super().__init__("text", txt, **kwargs)


class Title(HtmlElement):
    def __init__(self, txt, **kwargs):
        super().__init__("title", txt, **kwargs)


HEIGHT = 20


class ProfilerViewer(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)

        self.server.cli.add_argument("--data", required=True)
        args, _ = self.server.cli.parse_known_args()
        self.analyser = ProfilerAnalyzer(args.data)

        self.state.width = self.analyser.width
        self.state.height = (self.analyser.n_tracks + 1) * HEIGHT
        self.state.rects = self.analyser.rects(height=HEIGHT)
        self.state.lines = self.analyser.lines(height=HEIGHT)
        self.state.texts = self.analyser.texts(height=HEIGHT, x=15)

        self._build_ui()

    @change("offset")
    def _on_offset(self, offset, **_):
        self.state.texts = self.analyser.texts(
            height=HEIGHT,
            x=int(15 + 1000 * float(offset)),
        )

    def _build_ui(self):
        with DivLayout(self.server) as self.ui:
            client.Style(f"""
                rect {{ fill:blue; stroke:none; fill-opacity:0.5; }}
                line {{ stroke: black; }}
                text {{ text-anchor: start; font-size: {HEIGHT}px; }}
                rect.bg {{ fill:#BDBDBD; stroke:black; fill-opacity:1; }}
            """)
            html.H1("Trame profiler", style="text-align: center;")
            html.Input(
                type="range",
                min=0,
                step=0.25,
                max=("Math.floor(width/1000)",),
                v_model=("offset", 0),
                style="width:100%; margin-bottom: 20px;",
            )
            client.SizeObserver("viewSize")
            with html.Svg(
                viewBox=(
                    "`${1000 * offset} 0 ${(viewSize?.size?.width||10)} ${height}`",
                ),
                width=("viewSize?.size?.width || 10",),
                height=("height",),
                __properties=["viewBox"],
            ):
                with Rect(v_for="rect, i in rects", key="i", v_bind="rect"):
                    Title("{{ rect.title }}")
                Rect(
                    x=("1000 * offset",),
                    y=0,
                    width=LABEL_WIDTH * 1000,
                    height=(f"height - {HEIGHT}",),
                    classes="bg",
                )
                Line(v_for="line, i in lines", key="i", v_bind="line")
                Text("{{ t.text }}", v_for="t, i in texts", key="i", v_bind="t")


def main():
    app = ProfilerViewer()
    app.server.start()


if __name__ == "__main__":
    main()
