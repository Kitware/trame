import types
from trame import get_app_instance, trigger_key


def str_key_prefix(txt):
    if txt.startswith("{") or txt.startswith("`"):
        return ":"

    return ""


def py2js_key(key):
    return key.replace("_", "-")


class AbstractElement:
    _next_id = 1

    def __init__(self, name, __content=None, children=None, **kwargs):
        AbstractElement._next_id += 1
        self._id = AbstractElement._next_id
        self._elem_name = name
        self._allowed_keys = set()
        self._attr_names = []
        self._event_names = []

        self._attributes = {}
        self._txt = None
        self._py_attr = kwargs
        self._children = []

        if __content:
            if isinstance(__content, str):
                self._txt = __content
            elif isinstance(__content, list):
                self._children.extend(__content)
            else:
                self._children.append(__content)

        # Add standard Vue attribute handling
        if children:
            self._children.extend(children)

        # Add standard Vue attr/event handling
        self._attr_names += [
            "id",
            "ref",
            ("classes", "class"),
            "style",
            "v_model",
            "v_if",
            "v_show",
        ]
        self._event_names += ["click", "mousedown", "mouseup"]

    def _attr_str(self):
        return " ".join(self._attributes.values())

    def _update_allowed_keys(self):
        if hasattr(self, "_attr_names") and hasattr(self, "_event_names"):
            for items in [self._attr_names, self._event_names]:
                for item in items:
                    if isinstance(item, str):
                        self._allowed_keys.add(item)
                    else:
                        self._allowed_keys.add(item[0])

    # -------------------------------------------------------------------------
    # Buildin API
    # -------------------------------------------------------------------------

    def __getitem__(self, name):
        return self._py_attr[name]

    def __setitem__(self, name, value):
        if name in self._allowed_keys:
            self._py_attr[name] = value
        else:
            print(f"Attribute {name} is not defined for {self._elem_name}")

    def __getattr__(self, name):
        if name[0] == "_":
            raise AttributeError()

        return self._py_attr[name]

    def __setattr__(self, name, value):
        if name[0] == "_":
            self.__dict__[name] = value
        elif name == "content":
            self._txt = value
        elif name in self._allowed_keys:
            self._py_attr[name] = value
        else:
            self.__dict__[name] = value

        if name in ["_attr_names", "_event_names"]:
            self._update_allowed_keys()

    # -------------------------------------------------------------------------
    # helpers
    # -------------------------------------------------------------------------

    def ttsSensitive(self):
        self._attributes["__tts"] = f':key="`w{self._id}-${{tts}}`"'
        return self

    def attrs(self, *names):
        _app = get_app_instance()
        for _name in names:
            js_key = None
            name = _name
            if isinstance(_name, tuple):
                name = _name[0]
                js_key = _name[1]

            if name in self._py_attr:
                if js_key is None:
                    js_key = py2js_key(name)
                value = self._py_attr[name]

                if value is None:
                    continue

                if isinstance(value, (tuple, list)):
                    if len(value) > 1 and value[0] not in _app.state:
                        _app.state[value[0]] = value[1]

                    if js_key.startswith("v-"):
                        self._attributes[name] = f'{js_key}="{value[0]}"'
                    elif js_key.startswith(":"):
                        self._attributes[name] = f'{js_key}="{value[0]}"'
                    else:
                        self._attributes[name] = f':{js_key}="{value[0]}"'
                elif isinstance(value, bool):
                    if value:
                        self._attributes[name] = js_key
                elif isinstance(value, (str, int, float)):
                    self._attributes[name] = f'{js_key}="{value}"'
                else:
                    print(
                        f"Error: Don't know how to handle attribue name '{name}' with value '{value}' in {self.__class__}::{self._elem_name}"
                    )

        return self

    def events(self, *names):
        _app = get_app_instance()
        for _name in names:
            js_key = None
            name = _name
            if isinstance(_name, tuple):
                name = _name[0]
                js_key = _name[1]
            if name in self._py_attr:
                if js_key is None:
                    js_key = py2js_key(name)
                js_key = f"@{js_key}"
                value = self._py_attr[name]

                if value is None:
                    continue

                if isinstance(value, str):
                    self._attributes[name] = f'{js_key}="{value}"'
                elif isinstance(value, types.FunctionType):
                    trigger_name = trigger_key(value)
                    self._attributes[name] = f"{js_key}=\"trigger('{trigger_name}')\""
                elif isinstance(value, tuple):
                    trigger_name = value[0]
                    if isinstance(trigger_name, types.FunctionType):
                        trigger_name = trigger_key(trigger_name)
                    if len(value) == 1:
                        self._attributes[
                            name
                        ] = f"{js_key}=\"trigger('{trigger_name}')\""
                    if len(value) == 2:
                        self._attributes[
                            name
                        ] = f"{js_key}=\"trigger('{trigger_name}', {value[1]})\""
                    if len(value) == 3:
                        self._attributes[
                            name
                        ] = f"{js_key}=\"trigger('{trigger_name}', {value[1]}, {value[2]})\""
                else:
                    print(
                        f"Error: Don't know how to handle event name '{name}' with value '{value}' in {self.__class__}::{self._elem_name}"
                    )
        return self

    @property
    def content(self):
        return self._txt

    @property
    def children(self):
        return self._children

    @property
    def html(self):
        # Build attributes
        self.attrs(*self._attr_names)
        self.events(*self._event_names)

        # Compute HTML str
        if len(self._children):
            out_buffer = []
            out_buffer.append(f"<{self._elem_name} {self._attr_str()}>")
            for child in self._children:
                if isinstance(child, str):
                    out_buffer.append(child)
                else:
                    out_buffer.append(child.html)
            out_buffer.append(f"</{self._elem_name}>")
            return "\n".join(out_buffer)
        elif self._txt:
            return (
                f"<{self._elem_name} {self._attr_str()}>{self._txt}</{self._elem_name}>"
            )
        else:
            return f"<{self._elem_name} {self._attr_str()} />"


class Element(AbstractElement):
    def __init__(self, __elem_name, __content=None, **kwargs):
        super().__init__(__elem_name, __content, **kwargs)


class Div(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("div", __content, **kwargs)


class Span(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("span", __content, **kwargs)
