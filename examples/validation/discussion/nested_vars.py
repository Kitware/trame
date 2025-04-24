from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import client, html, vuetify

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------
VAR_NAMES = set(["a123", "a456", "a789"])

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

count = 800

state.update(
    {
        "items": [{"id": "a123"}, {"id": "a456"}, {"id": "a789"}],
        "a123": {
            "range": (10, 90),
            "range_min": 0,
            "range_max": 100,
            "opacity": 1,
        },
        "a456": {
            "range": (20, 80),
            "range_min": 0,
            "range_max": 100,
            "opacity": 1,
        },
        "a789": {
            "range": (30, 70),
            "range_min": 0,
            "range_max": 100,
            "opacity": 1,
        },
    }
)


def add_entry():
    # !!! Vue2 does not support new vars with getter but vue3 should handle it
    global count
    count += 1
    key = f"a{count}"
    state.items.append(dict(id=key))
    state[key] = (
        {
            "range": (0, 100),
            "range_min": 0,
            "range_max": 100,
            "opacity": 0.5,
        },
    )
    state.dirty("items")
    VAR_NAMES.add(key)
    state.change(key)(on_change)
    update_layout()


@state.change(*VAR_NAMES)
def on_change(**_):
    for name in state.modified_keys & VAR_NAMES:
        print(f"Data changed for {name}")
        print(state[name])
        print("-" * 30)

        if name == "a123":
            state.a456["range"] = list(state.a123["range"])
            state.dirty("a456")


def update_layout():
    with SinglePageWithDrawerLayout(server) as layout:
        with layout.toolbar:
            vuetify.VSpacer()
            vuetify.VBtn("Add", click=add_entry)
            vuetify.VBtn("Fast: {{fast}}", click="fast = !fast")
        with layout.drawer:
            with client.Getter(
                v_for="(item, i) in items",
                key="item.id",
                name=("`${item.id}`",),
                key_name="local_name",
                value_name="local_var",
                update_nested_name="update_local",
            ):
                with vuetify.VListItem():  # Must only be 1 child for a Getter
                    vuetify.VRangeSlider(
                        label=("`${local_name}`",),
                        value=("local_var.range",),
                        input="update_local('range', $event)",
                        min=("local_var.range_min",),
                        max=("local_var.range_max",),
                    )
                    vuetify.VSlider(
                        value=("local_var.opacity",),
                        input="update_local('opacity', $event)",
                        min=0,
                        max=1,
                        step=0.01,
                    )

        with layout.content:
            with vuetify.VRow():
                # With static HTML, the proper dependency get captured and state will print faster
                with vuetify.VCol(v_if=("fast", True)):
                    html.Div("Static dependencies", classes="text-h6")
                    for name in VAR_NAMES:
                        html.Pre("%s = {{ %s }}" % (name, name))

                # With method call in template, the refresh is debounced unless proper dep above
                with vuetify.VCol():
                    html.Div("Use method call", classes="text-h6")
                    with html.Div(
                        "State: {{ item.id }}",
                        v_for="item, idx in items",
                        key="item.id",
                    ):
                        html.Pre("{{ get(item.id) }}")


if __name__ == "__main__":
    update_layout()
    server.start()
