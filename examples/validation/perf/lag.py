import asyncio
import time

import numpy as np
import pandas as pd
import plotly.express as px

from trame.app import TrameApp
from trame.decorators import change
from trame.ui.html import DivLayout
from trame.widgets import client, html, plotly


def now():
    return time.perf_counter()


class LagApp(TrameApp):
    def __init__(self, server=None, buffer_size=100):
        super().__init__(server)
        self.index = 0
        self.buffer_size = buffer_size
        self.state.dt_array = [0 for _ in range(buffer_size)]

        self.np_array = np.zeros((buffer_size,), dtype=np.uint8)

        self.pending_tasks = set()
        self._build_ui()

    def _build_ui(self):
        self.state.setdefault("animate", False)
        self.state.setdefault("timestamp", 0)
        self.state.setdefault("ct", 0)
        self.state.setdefault("max_dt", 0)
        self.state.setdefault("avg_dt", 0)

        with DivLayout(self.server) as self.ui:
            client.ClientStateChange(value="timestamp", change="ct = $event")
            html.Button("Toggle animation", click="animate = !animate")
            html.Input(
                type="range",
                min=5,
                step=1,
                max=100,
                v_model_number=("wait_ms", 100),
            )
            html.Div(
                "{{ wait_ms }}ms - {{ (1000/wait_ms).toFixed(0) }} fps - {{ avg_dt }} / {{ max_dt }}"
            )
            # html.Div("{{ dt_array }}")
            # html.Div("{{ avg_dt }} / {{ max_dt }}")
            plotly.Figure(ctx_name="fig")

    @change("animate")
    def animate(self, animate, **_):
        if animate:
            task = asyncio.create_task(self._animate())
            self.pending_tasks.add(task)
            task.add_done_callback(self.pending_tasks.discard)

    @change("ct")
    def _on_client_time(self, ct, **_):
        st = now()
        dt = st - ct
        self.np_array[self.index] = min(255, round(1000 * dt))
        self.state.dt_array = self.np_array.tolist()
        self.state.max_dt = int(self.np_array.max())
        self.state.avg_dt = int(round(int(self.np_array.sum()) / self.buffer_size))

        fig = px.violin(pd.DataFrame(self.np_array, columns=["dt"]), y="dt")
        fig.update_yaxes(range=[0, 20])
        self.ctx.fig.update(fig)

        if self.index < self.buffer_size - 1:
            self.index += 1
        else:
            self.index = 0

    async def _animate(self):
        while self.state.animate:
            await asyncio.sleep(self.state.wait_ms / 1000)
            with self.state as s:
                s.timestamp = now()


def main():
    app = LagApp()
    app.server.start()


if __name__ == "__main__":
    main()
