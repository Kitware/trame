import os
from collections import defaultdict

from trame.internal.app import get_app_instance

BASE = os.path.abspath(os.path.dirname(__file__))

from trame.layouts import SinglePage
from trame.html import vuetify, widgets
from trame import state


class PipelineManager:
    DEFAULT_NODE = {"name": "undefined", "visible": 0, "collapsed": 0}

    def __init__(self, state, name):
        self._state = state
        self._name = name
        self._next_id = 1
        self._nodes = {}
        self._children_map = defaultdict(set)

    def _update_hierarchy(self):
        self._children_map.clear()
        for node in self._nodes.values():
            self._children_map[node.get("parent")].add(node.get("id"))

        self.update()

    def _add_children(self, list_to_fill, node_id):
        for child_id in self._children_map[node_id]:
            node = self._nodes[child_id]
            list_to_fill.append(node)
            if node.get("collapsed"):
                continue
            self._add_children(list_to_fill, node.get("id"))

        return list_to_fill

    def update(self):
        result = self._add_children([], "0")
        self._state[self._name] = result
        return result

    def add_node(self, parent="0", **item_keys):
        _id = f"{self._next_id}"
        self._next_id += 1

        node = {
            **PipelineManager.DEFAULT_NODE,
            "id": _id,
            "parent": parent,
            **item_keys,
        }
        self._nodes[_id] = node
        self._update_hierarchy()

        return _id

    def remove_node(self, _id):
        for id in self._children_map[_id]:
            self.remove_node(_id)
        self._nodes.pop(_id)
        self._update_hierarchy()

    def toggle_collapsed(self, _id, icons=["collapsed", "collapsable"]):
        node = self.get_node(_id)
        node["collapsed"] = not node["collapsed"]

        # Toggle matching action icon
        actions = node.get("actions", [])
        for i in range(len(actions)):
            action = actions[i]
            if action in icons:
                actions[i] = icons[(icons.index(action) + 1) % 2]

        self.update()
        return node["collapsed"]

    def toggle_visible(self, _id):
        node = self.get_node(_id)
        node["visible"] = not node["visible"]
        self.update()
        return node["visible"]

    def get_node(self, _id):
        return self._nodes.get(f"{_id}")


pipeline = PipelineManager(state, "git_tree")

id_root = pipeline.add_node(
    name="root", visible=0, color="#9C27B0", actions=["test", "delete"]
)
id_a = pipeline.add_node(
    parent=id_root,
    name="a",
    visible=1,
    color="#42A5F5",
    actions=["collapsable", "delete"],
)
id_b = pipeline.add_node(
    parent=id_root, name="b", visible=1, color="#00ACC1", actions=["collapsable"]
)
id_aa = pipeline.add_node(
    parent=id_a, name="aa", visible=1, color="#2962FF", actions=["test", "delete"]
)
id_aaa = pipeline.add_node(parent=id_aa, name="aaa", visible=1, color="black")
id_ba = pipeline.add_node(
    parent=id_b, name="ba", visible=1, color="#004D40", actions=["collapsable"]
)
id_bb = pipeline.add_node(
    parent=id_b, name="bb", visible=1, color="#80CBC4", actions=["collapsable"]
)
id_bba = pipeline.add_node(parent=id_bb, name="bba", visible=1, color="#00838F")
id_bbb = pipeline.add_node(parent=id_bb, name="bbb", visible=1, color="#4DB6AC")

pipeline.update()

app = get_app_instance()  # need cleanup
ICONS = {
    "test": app.url(os.path.join(BASE, "icons/abacus.svg")),
    "delete": app.url(os.path.join(BASE, "icons/trash-can-outline.svg")),
    "collapsed": app.url(os.path.join(BASE, "icons/chevron-up.svg")),
    "collapsable": app.url(os.path.join(BASE, "icons/chevron-down.svg")),
}

# -----------------------------------------------------------------------------
# Callback
# -----------------------------------------------------------------------------

# @state.change("git_tree")
# def pipeline_changed(git_tree, **kwargs):
#     print(git_tree)


def on_action(event):
    print("on_action", event)
    _id = event.get("id")
    _action = event.get("action")
    if _action.startswith("collap"):
        print(pipeline.toggle_collapsed(_id))


def on_event(event):
    print(event)


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

layout = SinglePage("Git Tree")
layout.title.set_text("Git Tree")

with layout.content:
    widgets.GitTree(
        sources=("git_tree",),
        action_map=("icons", ICONS),
        action_size=25,
        action=(on_action, "[$event]"),
        # visibility_change=(on_event, "[$event]"),
        # actives_change=(on_event, "[$event]"),
    )

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
