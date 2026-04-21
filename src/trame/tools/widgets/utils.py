import re

camel_pattern = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_dash(value):
    "MySuperWidget => my-super-widget"
    return camel_pattern.sub("-", value).lower()


def attr_to_py(value):
    """
    top-left                => "top_left"
    top-left:default        => ("top_left_default", "top-left:default")
    v-slot:default.modifier => ("v_slot_default_modifier", "v-slot:default.modifier")
    """
    py_name = value.replace("-", "_")
    if "." in value or ":" in value:
        py_name = py_name.replace(".", "_").replace(":", "_")
        return [py_name, value]
    return py_name
