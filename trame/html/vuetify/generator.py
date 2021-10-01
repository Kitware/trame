import argparse
import json

# ----------------------------------------
# Helpers
# ----------------------------------------

module_header = """
from trame import get_app_instance
from trame.html import AbstractElement

# Make sure used module is available
_app = get_app_instance()
if "vuetify" not in _app.vue_use:
    _app.vue_use += ["vuetify"]


"""


def get_attributes(tag):
    if len(tag.get("attributes")) == 0:
        return None

    attributes = []
    for attribute in tag.get("attributes"):
        name = attribute.get("name")
        if "(" in name:
            entry = expand_parenthetical(name, attributes)
        else:
            entry = '"' + name.replace("-", "_") + '",'
            types = attribute.get("value", {}).get("type")
            if "function" in types:
                entry += " # JS functions unimplemented"
            attributes.append(entry)

    joined_attributes = "\n            ".join(attributes)
    return f"""
        self._attr_names += [
            {joined_attributes}
        ]"""


def get_events(tag):
    if len(tag.get("events")) == 0:
        return None

    events = []
    for event in tag.get("events"):
        entry = event.get("name")
        if "<" in entry:
            expand_dom_events(entry, events)
        else:
            if entry in ["mouseup", "mousedown", "click"]:
                entry = f"# {entry}, #Implemented in AbstractElement parent class"
            elif "-" in entry or ":" in entry:
                _entry = entry.replace(":", "_").replace("-", "_")
                entry = f'("{_entry}", "{entry}"),'
            else:
                entry = f'"{entry}",'
            events.append(entry)

    joined_events = "\n            ".join(events)
    return f"""
        self._event_names += [
            {joined_events}
        ]"""


def expand_parenthetical(attribute, attributes):
    sizes = ["sm", "md", "lg", "xl"]
    numbers = list(range(13)) if "0" in attribute else list(range(1, 13))

    prefix = ""
    if "offset-" in attribute:
        prefix = "offset_"
    if "order-" in attribute:
        prefix = "order_"

    for size in sizes:
        for number in numbers:
            attributes.append(f'    "{prefix}{size}{number}",')


def expand_dom_events(event, events):
    dom_events = [
        "click",
        "dblclick",
        "mousedown",
        "mouseenter",
        "mouseleave",
        "mousemove",
        "mouseover",
        "mouseout",
        "mouseup",
        "focus",
    ]
    for dom_event in dom_events:
        events.append(f'("{dom_event}_date", "{dom_event}:date"),')
        events.append(f'("{dom_event}_month", "{dom_event}:month"),')
        events.append(f'("{dom_event}_year", "{dom_event}:year"),')


# ----------------------------------------
# Generator
# ----------------------------------------


def generate_vuetify(input_file, output_file):
    with open(input_file) as vuetify_input:
        loaded = json.loads(vuetify_input.read())
    tags = loaded.get("contributions", {}).get("html", {}).get("tags")

    generated_module = module_header

    for tag in tags:
        name = tag.get("name")
        tag_name = tag.get("doc-url").replace("https://www.vuetifyjs.com/api/", "")
        attributes = get_attributes(tag)
        events = get_events(tag)

        class_def = f"""
class {name}(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("{tag_name}", __content, **kwargs)"""

        if attributes is not None:
            class_def += attributes

        if events is not None:
            class_def += events

        generated_module += class_def

    with open(output_file, "w") as vuetify_module:
        vuetify_module.write(generated_module)


# ----------------------------------------
# Command line interface
# ----------------------------------------


def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]",
        description="Generate vuetify module for Trame",
    )
    parser.add_argument("-i", "--input")
    parser.add_argument("-o", "--output")
    return parser


if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()
    if not args.input:
        raise Exception("Sorry, I need an input")
    output = args.output or "_generated.py"

    try:
        generate_vuetify(args.input, output)
    except (FileNotFoundError, IsADirectoryError) as err:
        print(f"{sys.argv[0]}: {file}: {err.strerror}", file=sys.stderr)
