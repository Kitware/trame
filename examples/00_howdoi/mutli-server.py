r"""
Multi-server setup

Installation requirements:
    pip install trame trame-vuetify
"""

import asyncio

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify


server1 = get_server("server1", client_type="vue2")
state1 = server1.state
state1.trame__title = "Server1"

server2 = get_server("server2", client_type="vue2")
state2 = server2.state
state2.trame__title = "Server2"


def send_to_server1(message):
    with state1:
        state1.received = message


def send_to_server2(message):
    with state2:
        state2.received = message


with SinglePageLayout(server1) as layout:
    layout.title.set_text("Server1")

    with layout.content:
        with vuetify.VCard(classes="pa-4"):
            vuetify.VTextField(
                v_model=("message", "Hi from server 1"),
            )
            vuetify.VBtn(
                "Send message to server 2",
                click=(send_to_server2, "[message]"),
            )
            vuetify.VTextField(readonly=True, v_model=("received", "<message here>"))

with SinglePageLayout(server2) as layout:
    layout.title.set_text("Server2")

    with layout.content:
        with vuetify.VCard(classes="pa-4"):
            vuetify.VTextField(
                v_model=("message", "Hi from server 2"),
            )
            vuetify.VBtn(
                "Send message to server 1",
                click=(send_to_server1, "[message]"),
            )
            vuetify.VTextField(
                readonly=True,
                v_model=("received", "<message here>"),
            )


if __name__ == "__main__":
    task1 = server1.start(exec_mode="task", port=8080)
    task2 = server2.start(exec_mode="task", port=8081)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(task1, task2))
