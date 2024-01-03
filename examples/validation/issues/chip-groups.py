from trame.app import get_server
from trame.widgets import vuetify
from trame.ui.vuetify import SinglePageLayout

# -----------------------------------------------------------------------------
# Trame initialization
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state = server.state

state.chips = [
    dict(name="hello", id=1, show=True),
    dict(name="world", id=2, show=True),
    dict(name="seb", id=3, show=True),
]


@state.change("chip_group")
def on_active(chip_group, **kwargs):
    print("chip_group", chip_group)


def remove(chip_id):
    print("remove", chip_id)
    for item in state.chips:
        if item.get("id") == chip_id:
            item["show"] = False
    state.dirty("chips")


# -----------------------------------------------------------------------------
# GUI layout
# -----------------------------------------------------------------------------

with SinglePageLayout(server) as layout:
    with layout.content:
        with vuetify.VContainer(fluid=True, classes="fill-height pa-0 ma-0"):
            with vuetify.VChipGroup(
                v_model=("chip_group", None), active_class="primary", mandatory=True
            ):
                vuetify.VChip("Dashboard", value="dashboard", label=True, outlined=True)
                vuetify.VChip(
                    "{{ item.name }}",
                    v_for="item, idx in chips",
                    key="idx",
                    value=("item.id",),
                    v_show="item.show",
                    close=True,
                    click_close=(remove, "[item.id]"),
                    label=True,
                    outlined=True,
                )

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
