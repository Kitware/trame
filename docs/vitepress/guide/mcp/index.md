# Agents (MCP)

AI agents such as Claude Code or Codex can drive a Trame application through
the [Model Context Protocol](https://modelcontextprotocol.io) (MCP). While an
agent works, users see its changes appear in their browsers in real time.

As the developer, you decide what an agent is allowed to do in the
application. Trame serves these capabilities from the application's existing
web server, under the path `/mcp`, so no extra process is needed. An agent
running inside the application's own process can use the same capabilities.
Declaring them doesn't turn agent access on: agents can use the application
only after you enable access, in code or with the `--mcp` flag at launch.

## Quick start

Below is a minimal Trame application, written with the modern `TrameApp` and
`TrameComponent` classes. A few extra lines of code define precisely what an
agent can do.

```python
from typing import Annotated

from trame.app import TrameApp, TrameComponent
from trame.decorators import mcp  # [!code highlight]
from trame.ui.html import DivLayout
from trame.widgets import html


class Cone(TrameComponent):
    """A cone in the scene."""

    def __init__(self, server, name):
        super().__init__(server)
        self.resolution_key = f"{name}_resolution"  # the state key the page shows
        self.state[self.resolution_key] = 6

    @mcp.property # [!code highlight]
    def resolution(self) -> int:
        """Number of facets."""
        return self.state[self.resolution_key]

    @mcp.method # [!code highlight]
    def set_resolution(
        self, resolution: Annotated[int, {"minimum": 3, "maximum": 60}]
    ) -> str:
        """Set the number of facets of this cone."""
        self.state[self.resolution_key] = resolution
        return f"Resolution set to {resolution}"


class ConeApp(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self.left_cone = Cone(self.server, "left_cone")
        self.right_cone = Cone(self.server, "right_cone")
        # The names agents use, and which cone each one is
        self.left_cone.mcp_expose("left_cone", description="The cone on the left.") # [!code highlight]
        self.right_cone.mcp_expose("right_cone", description="The cone on the right.") # [!code highlight]
        with DivLayout(self.server):
            html.H1("{{ left_cone_resolution }} and {{ right_cone_resolution }} facets")

    @mcp.tool # [!code highlight]
    def reset_resolution(self) -> str:
        """Put both cones back to 6 facets."""
        self.left_cone.set_resolution(6)
        self.right_cone.set_resolution(6)
        return "Both cones reset"


if __name__ == "__main__":
    app = ConeApp()
    app.mcp.enabled = True  # serve agents (or launch with --mcp) [!code highlight]
    app.server.start()
```

An agent interacts with an application by calling tools. The three decorators
in this example give it access in two different ways.

**`@mcp.tool` turns a method into a top-level tool.** The agent finds
`reset_resolution` in its list of tools, next to the other tools it has, and
can call it directly:

```
reset_resolution()
```

A tool has a single, fixed name, so it cannot tell two instances of a class
apart. For that reason, `@mcp.tool` should only decorate methods of classes
that the application creates once, such as the application class itself.

**`@mcp.method` and `@mcp.property`, on the other hand, belong to each
instance.** The example above has two `Cone` components, and each one has its
own `set_resolution` method and `resolution` property. The agent needs a way to
tell the two cones apart, which is what `mcp_expose()` is for: it gives the
agent access to each cone under its own name.

`@mcp.method` and `@mcp.property` don't add top-level tools to the MCP server.
Instead, the agent reaches the properties and methods of each instance through
a few tools built into Trame. Their first argument is the name the object was
given with `mcp_expose`:

```
object_call("left_cone", "set_resolution", {"resolution": 12})   # calls left_cone.set_resolution(12)
object_get("right_cone")                                         # reads the properties of right_cone
```

The agent learns what each tool, method and property does from your
docstrings and type hints. The `Annotated[int, {"minimum": 3, "maximum": 60}]`
hint also limits the values it accepts, so a call with `{"resolution": 2}` is
rejected before `set_resolution` runs. Any change the agent makes appears in
the browser immediately.

Declaring what agents may use doesn't serve anything to them yet: agent access
must also be turned on, which this example does in its `__main__` block. You
can also turn it on at launch, with the `--mcp` command-line flag.

### Plain functions and state

Simpler Trame applications may not use `TrameApp` and `TrameComponent` at all.
In such applications, you can still give agents access to state variables and
plain functions:

```python
from trame.app import get_server

server = get_server()

server.state.resolution = 6
server.state.mcp_expose( # [!code highlight]
    "resolution", type=int, schema={"minimum": 3, "maximum": 60},
    description="Number of facets of the cone",
)


@server.mcp.tool # [!code highlight]
def reset_resolution() -> str:
    """Reset the resolution to its default value."""
    server.state.resolution = 6
    return "Resolution reset to 6"


server.mcp.enabled = True # [!code highlight]
server.start()
```

Here the agent calls `reset_resolution` as a tool. The `resolution` state
variable appears to the agent as a property of a built-in object named
`"state"`. The agent reads it with `object_get("state")` and changes it with
`object_update("state", {"resolution": 12})`, and values outside the schema
are rejected.

## Connecting an agent

When agent access is on, agents in other processes connect over HTTP, the
default transport. The endpoint is the application's own address followed by
`/mcp`, which by default is `http://localhost:8080/mcp`. This command starts a
Claude Code session connected to it:

```bash
claude --mcp-config '{"mcpServers":{"trame":{"type":"http","url":"http://localhost:8080/mcp"}}}'
```

The equivalent command for Codex is:

```bash
codex -c 'mcp_servers.trame.url="http://localhost:8080/mcp"'
```

Both commands add the application to that session only, alongside any MCP
servers you have already configured. You don't need to remember them,
because the application prints both, with the correct port and name, as soon
as agents can connect: when access is on and HTTP is among the transports.

If the application listens on addresses beyond this machine, for example with
`--host 0.0.0.0`, the endpoint requires a bearer token. The application then
generates a token and includes it in the commands it prints, unless you set
your own with `--mcp-http-token`, `TRAME_MCP_HTTP_TOKEN` or `server.mcp.http.token`. A token
you set appears in the commands as `<token>`.

### From inside the application

An agent can also run inside the application's own process. An example is an
assistant panel that calls a language model with the user's own API key. Such
an agent needs no endpoint. `server.mcp.client()` gives it the same view and the same
rules as an agent connected over HTTP: access still follows `enabled`, and
permissions still apply.

```python
client = server.mcp.client("assistant")  # the name shown in the call log

client.instructions                      # what agents receive when they connect
tools = await client.list_tools()        # each with name, description, inputSchema
result = await client.call_tool("object_list")
result["content"]                        # what to hand back to the model
result.get("isError")                    # True when the tool failed

def show(value, total, message): ...     # e.g. update a progress bar
await client.call_tool("object_call", {...}, on_progress=show)
```

A tool that fails still returns a result, with `isError` set, and the agent
hands it back to its model like any other result. A request the application
can't serve at all, such as a call to an unknown tool, raises `MCPError`.
Cancelling the task that awaits a call cancels the call. With `on_progress`,
the call receives the progress its method reports, as described in
[Reporting progress](#reporting-progress).

To allow only agents inside the process, turn off the transports for agents
in other processes with `server.mcp.transports = []`. See
[Options, launch flags and security](#options-launch-flags-and-security) for
details.

## What agents see

This section looks at the quick start's cone application from the agent's
side.

When it connects, the agent receives a short overview of the application:

```
A live trame app, shared with its users: they see your changes at once.
Objects: left_cone (Cone: The cone on the left.), right_cone (Cone: The cone on the right.); object_list() lists them, object_types() describes their types.
```

It also receives these tools:

| Tool | Provided by | Purpose |
| --- | --- | --- |
| `reset_resolution()` | Your `@mcp.tool` | Puts both cones back to 6 facets |
| `object_list(offset?)` | Trame (built in) | Lists the objects your application named, with their types and descriptions |
| `object_types(type_names?, include_inherited?)` | Trame (built in) | Gives an overview of the objects' types. With `type_names`, it describes types such as `"Cone"`, or single members such as `"Cone.set_resolution"`, in detail |
| `object_get(target, properties?, depth?)` | Trame (built in) | Reads the properties of an object, and those of the objects it refers to, up to `depth` levels away |
| `object_update(target, values)` | Trame (built in) | Sets properties of an object. Every value is checked before any of them is applied |
| `object_call(target, method, args?)` | Trame (built in) | Calls a method of an object |
| `object_batch(steps, results?)` | Trame (built in) | Batches multiple object operations into a single tool call |

The six `object_*` tools are built into Trame, and they are
the same in every application.

Their `target` argument tells them which object to use. It can be the name
you gave the object with `mcp_expose`, such as `"left_cone"`, or the object's
id. Every object has an id, a short hex string such as `"0x1f"` that
identifies it uniquely. Replies include it, so in the session below
`left_cone` appears with the id `"0x1"`. Ids are also how agents refer to the
objects they find through the properties of other objects, which have no name.

A typical session looks like this:

```json
→ object_list()
← {"objects": {"left_cone": {"type": "Cone", "description": "The cone on the left."},
               "right_cone": {"type": "Cone", "description": "The cone on the right."}}}

→ object_types()
← {"types": {"Cone": {"about": "A cone in the scene.",
                      "properties": ["resolution"], "methods": ["set_resolution"]}}}

→ object_types(["Cone"])
← {"types": {"Cone": {
     "description": "A cone in the scene.",
     "properties": {"resolution": {"type": "integer", "description": "Number of facets.",
                                   "read_only": true}},
     "methods": {"set_resolution": {
       "description": "Set the number of facets of this cone.",
       "parameters": {"type": "object",
                      "properties": {"resolution": {"type": "integer", "minimum": 3, "maximum": 60}},
                      "required": ["resolution"], "additionalProperties": false},
       "returns": {"type": "string"}}}}}}

→ object_get("left_cone")
← {"result": {"id": "0x1"},
   "objects": {"0x1": {"type": "Cone", "names": ["left_cone"], "values": {"resolution": 6}}}}

→ object_call("left_cone", "set_resolution", {"resolution": 12})
← Resolution set to 12

→ object_call("right_cone", "set_resolution", {"resolution": 2})
← (error) Invalid arguments for Cone.set_resolution: args.resolution: must be at least 3, got 2

→ object_update("left_cone", {"resolution": 20})
← (error) Nothing was applied. Rejected on Cone 0x1: resolution (read-only). Writable: none.
  Methods: set_resolution; object_types(["Cone"]) says what they do.

→ reset_resolution()
← Both cones reset
```

A few things are worth noticing in this exchange.

- **The descriptions and schemas come from your code.** They are built from
  your docstrings and type hints, and from any
  `Annotated[T, "description", {json-schema}]` hints you add. Trame checks
  every value an agent sends against them before your code runs, which is why
  the call with a resolution of 2 never reached the cone.
- **`object_get` returns two parts.** `result` identifies what was read, and
  `objects` contains each object that was read, keyed by its id. When an
  object refers to other objects, it shows each reference as `{"id"}` if the
  other object is included in `objects`, and as `{"id", "type"}` if it is not.
  The `depth` argument controls how far the reading goes.
- **Methods return their values as they are.** A string reaches the agent as
  text, and other values as JSON, so `None` arrives as `null`. When the value
  contains objects, it is formatted like an `object_get` reply. Your own tools
  behave the same way. A method that changes something is more useful to the
  agent when it returns a short description of the change, as
  `set_resolution` does.
- **Errors tell the agent how to proceed.** For example, the rejected update
  of the read-only `resolution` property points the agent to
  `set_resolution`.
- **Users see every change immediately.** Trame runs each agent call inside a
  `with state:` block, so your `@state.change` callbacks run and the connected
  browsers update.
- **Replies are kept short.** The built-in tools shorten long lists and
  strings unless the agent asks for them specifically, and keep each reply
  under `server.mcp.max_response_tokens`. Anything left out is listed under `more`,
  along with the call that retrieves it when there is one.

## Marking methods and properties

This section describes the decorators and their options in more detail.

```python
from typing import Annotated

from trame.app import TrameComponent
from trame.decorators import mcp


class Dataset(TrameComponent):
    @mcp.method(annotations={"destructiveHint": True})
    def clear(self) -> None:
        """Unload the data."""

    @mcp.method(read_only=True, concurrent=True)
    async def center(self) -> Annotated[list[float], "[x, y, z]"]: ...

    @mcp.property(requires="files")
    def data_path(self) -> Annotated[str, "File the data is read from"]:
        return self._path

    @data_path.setter(requires="scripts")
    def data_path(self, value: str):
        self.load(value)
```

`@mcp.method` accepts these options:

- `name` sets the name agents call the method by. It defaults to the method's
  own name.
- `description` sets the text agents read. It defaults to the docstring, with
  its wrapped lines joined.
- `read_only`: with `True`, the method declares that it changes nothing.
  Agents can call read-only methods even on objects they are only allowed to
  read (see [Naming objects](#naming-objects-and-read-only-access)).
- `annotations` takes MCP tool annotations, such as
  `{"destructiveHint": True}`. Agents see them when they describe the type.
- `concurrent`: with `True`, the method may run while other agent calls are in
  progress. By default, agent calls run one at a time.
- `requires` lists the permissions the method needs (see
  [Permissions](#permissions)).

Methods can be async. Their parameters are described by their type hints. When
a parameter's type is a component or model class, the agent passes the name or
id of such an object, and your method receives the object itself.

`@mcp.property` accepts these options:

- `description` sets the text agents read. It defaults to the text in the
  getter's return type, as in the example, or else to the getter's docstring.
- `requires` lists the permissions the property needs, both to read and to
  write it.

Its setter accepts one option:

- `requires` lists the permissions that only writing needs. In the example,
  agents need `files` to read `data_path`, and both `files` and `scripts` to
  change it.

Without a setter, agents can read the property but cannot assign it a new
value. That doesn't make the value itself read-only: when the property returns
an object, agents can still call that object's methods and set its
properties. What they can do with it depends on the name through which they
reached it (see [Naming objects](#naming-objects-and-read-only-access)).

These decorators describe what agents may do with the instances of a class,
but they don't give agents access to any instance. Agents reach an instance
once your application names it with `mcp_expose`, or through a property of an
object they can already reach (see
[Naming objects](#naming-objects-and-read-only-access)). Models from
trame-dataclass follow the same rule.

### Class options

Instead of decorating each member, a class can list what agents see in its
`mcp=` keyword. A subclass can use it to change what it inherits:

```python
class Viewport(TrameComponent, mcp={"description": "A 3D view, as the user sees it.",
                                    "methods": ["reset_camera", "set_view_up"]}):
    def reset_camera(self): ...
    def set_view_up(self, axis: str): ...


class LockedViewport(Viewport, mcp={"methods": {"set_view_up": False}}): ...  # one less
class OffscreenViewport(Viewport, mcp=False): ...  # never exposed
```

The keyword takes a dictionary of options, or `False`, which hides the class.
`True` makes the class visible to agents without other options, and on a
model it also shows all of its fields. The options are:

- `description` sets the text agents read about the class. It defaults to the
  class docstring.
- `methods` and `properties` accept a list of names, or a dictionary that maps
  each name to `True`, `False`, a description, or a dictionary of options such
  as `requires`. `False` hides a member, even one that a base class exposes.
- `"all_methods": True` exposes every public method, except Trame's own API
  and the callbacks registered with `@change`, `@trigger`, `@controller` or
  `@watch`.
- `constructor` lets agents create instances of the class (see
  [Creating objects](#creating-objects)).
- Models also accept `all_fields` (see
  [trame-dataclass models](#trame-dataclass-models)).

A class with options exposes only the members its options list, plus those
marked with decorators. Options are combined from the base classes down, so
subclasses inherit them, except `description`, which each class sets for
itself.

Agents see a subclass in terms of its base class. `object_types` names the
base under `"extends"`, lists what the subclass adds, and marks with `false`
what it removes.

### Tools, resources and prompts

Besides tools, MCP lets an application offer resources, which are documents
the agent can read, and prompts, which are predefined instructions that the
agent's user can invoke. A class that your application creates once, such as
the application itself or a panel of tools, can provide all three:

```python
from trame.app.mcp import Image
from trame.decorators import mcp


class AgentTools(TrameComponent):
    @mcp.tool(read_only=True)  # same options as @mcp.method
    def screenshot(self) -> Image: ...

    @mcp.resource("app://guide", mime_type="text/markdown")
    def guide(self) -> str: ...

    @mcp.prompt
    def review_session(self) -> str: ...
```

Trame registers them when the instance is created and removes them when it is
unbound. Creating a second instance while the first one is still bound raises
an error, because the names would collide. The instance needs no name for
them to work, and they don't give agents access to the instance itself.

Without a class, the `@server.mcp.tool`, `@server.mcp.resource(uri)` and
`@server.mcp.prompt` decorators do the same for plain functions.

### Reporting progress

A method or tool that takes a while can tell the agent how far it has got.
Declare a parameter of type `Progress`, with `None` as its default, on an
`async` method:

```python
import asyncio

from trame.app.mcp import Progress


class Simulation(TrameComponent):
    @mcp.method
    async def run(self, steps: int, progress: Progress | None = None) -> str:
        """Run the simulation."""
        job = self.solver.start(steps)  # the long operation, started elsewhere
        while not job.done:
            if progress:
                await progress(job.step, total=steps, message=f"Step {job.step}")
            await asyncio.sleep(0.5)
        return f"Ran {steps} steps"
```

The agent doesn't see the parameter. When it calls the method, Trame passes a
reporter in that parameter. If the agent asked for no progress, the reporter
does nothing. When your application calls the method itself, the parameter keeps its
default, `None`.

Pass `progress` a number that increases from one call to the next, and
optionally a `total` and a `message`. When reports arrive faster than the
client can use them, Trame sends only the latest.

In a call to `object_batch`, the agent receives a decimal progress value, and
the total is the number of steps. The integer part of the value is the current
step, counted from 0. The decimal part comes from the reports of that step's
method:

- with a `total`, it is the fraction of the step done: 30 of 100 in the third
  step gives 2.3;
- without a `total`, it is an arbitrary value that increases with each report,
  such as 2.00000001, then 2.00000002.

The parameter requires an `async` function, because reports are awaited; a
plain function declaring it is rejected. To report on blocking work, such as a
long VTK update, run that work with `asyncio.to_thread` and report while you
await it.

## Naming objects and read-only access

```python
class ConeApp(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self.left_cone = Cone(self.server, "left_cone")
        self.right_cone = Cone(self.server, "right_cone")
        self.active = self.left_cone  # the cone the user selected
        self.left_cone.mcp_expose("left_cone", read_only=True)
        self.right_cone.mcp_expose("right_cone", read_only=True)
        self.mcp.expose_object(
            lambda: self.active,
            "active_cone",
            description="The cone the user is working on.",
        )
```

`obj.mcp_expose(name)` gives an object a name, and an object can have several
names. Each name refers to a single object. Exposing a name that already
refers to a different object raises an error, so that two components cannot
take the same name by accident. To reuse a name, withdraw it first with
`self.mcp.unexpose_object(name)`. `obj.mcp_unexpose()` withdraws all of an
object's names at once, and unbinding a component does this automatically.
Even then, agents can still reach the object through a property of another
object they reach, if one refers to it.

Names go through the server's translator, as state keys do. A component that
your application builds on several child servers can therefore use the same
name in each one. On a child server created with
`server.create_child_server(prefix="left_")`, `mcp_expose("cone")` gives the
name `left_cone`, and that is the name agents see.

The `description` option tells agents what the object is for in your
application. The class docstring already says what a `Cone` is. The name's
description says which cone this one is, and why an agent would use it.
Agents read it next to the name, in the list of objects that
`object_list()` returns. The instructions they receive when they connect
include its first sentence.

`self.mcp.expose_object(source, name)` takes the same options. Its source can
be an object, or a function that returns an object, or `None` when there is
nothing to expose. Trame calls the function again on every agent request, so
`lambda: self.active` always refers to the cone that is currently active,
and you never have to expose it again when it changes. To let agents reach a
list of objects, give each one its own name, as above, or return the list from
an `@mcp.property` of an object they can already reach.

With `read_only=True`, agents can read the object and call its read-only
methods, but they cannot call its other methods or change its properties.
This holds whether the agent targets the object by that name or by its id,
and it also covers the objects agents reach only through it. An object that
agents can also reach another way, under a writable name or through a
property of a writable object, stays writable. A name whose function returns
the object counts as one of those ways. In the example above, both cones are
read-only under their own names, but the active one is also exposed as
`active_cone`, so it is the only one agents can change.

## trame-dataclass models

Models from trame-dataclass work like components: you mark their methods with
`@mcp.method`, name them with `mcp_expose`, and agents reach them by the same
rules. The difference is that fields take the place of properties.

```python
from trame.decorators import mcp
from trame_dataclass.v2 import ServerOnly, StateDataModel, Sync


class Label(StateDataModel, mcp={"all_fields": True, "constructor": "default"}):
    text = Sync(str, "")
    position = Sync(list[float], lambda: [0.0, 0.0, 0.0], mcp="[x, y, z]")


class Scene(StateDataModel):                # no keyword: only what is marked
    labels = Sync(list[Label], list, has_dataclass=True, mcp=True)
    path = ServerOnly(str, mcp={"read_only": True})

    @mcp.method
    def add_label(self, label: Label) -> None:
        self.labels = [*self.labels, label]

    @mcp.constructor(description="An empty scene")
    @classmethod
    def create(cls, server) -> "Scene":
        return cls(server)


scene = Scene(server)
scene.mcp_expose("scene")
```

### Fields

The class decides which fields agents see:

- With `mcp=True` on the class, or `"all_fields": True` in its
  [class options](#class-options), agents see all of its fields except the
  `ServerOnly` ones. `Label` does this.
- Otherwise, agents see only the fields you mark, as in `Scene`.

A field's descriptor (`Sync`, `ClientOnly` or `ServerOnly`) decides what
agents can do with it:

| Descriptor | Agents can |
| --- | --- |
| `Sync` | Read and write it |
| `ClientOnly` | Read it |
| `ServerOnly` | Nothing, unless you mark it. A marked `ServerOnly` field must state `read_only`, as `path` does |

You mark a field with its `mcp=` argument, which accepts:

- `True`, to show the field;
- `False`, to hide it, even when the class shows all of its fields;
- a string, to show it with that description, as `position` does;
- a dictionary with `description`, `read_only` and `schema`. `read_only`
  overrides what the field's descriptor allows, and `schema` adds JSON Schema
  keywords, such as `minimum`, that the values agents write must satisfy.

### Reaching models

Agents reach a model the way they reach a component: by its name, or by its id
when a visible property of an object they reach refers to it. In the example,
exposing `scene` is enough for agents to reach every label in `scene.labels`.
If `scene` is exposed with `read_only=True`, those labels are read-only too.

To set a field that holds models, agents pass the ids of those models.

## Creating objects

Agents can create a component or a model only if its class gives them a
constructor, and only inside `object_batch`. A class can give agents a
constructor in one of two ways:

- **The class's own constructor.** With `"constructor": "default"` in the class
  options, as `Label` has, agents pass values for the fields they can write,
  and Trame calls `Label(server, **values)`. A component has no fields, so
  Trame calls `Cls(server)`, and agents can set its properties in a later
  step. If `__init__` can't be called that way, Trame logs a warning and
  agents get no constructor.
- **A classmethod.** Mark it with `@mcp.constructor`, as `Scene.create` is. It
  receives the server as its first argument, and agents pass its other
  parameters. For a class you can't decorate, name the classmethod in the
  class options instead: `"constructor": "create"`.

Subclasses inherit the constructor. To turn it off in a subclass, set
`"constructor": False`.

Agents can only create objects of the types they already know about: the
types of the objects they can reach, and of the values those objects'
properties can hold.

In a batch, a `new` step creates an object. Its `as` key names the result, and
later steps refer to it by that name with an `@` in front. This batch creates
a label and adds it to the scene, in a single call:

```
→ object_batch([{"new": "Label", "args": {"text": "Skull"}, "as": "skull"},
                {"call": "scene", "method": "add_label", "args": {"label": "@skull"}}])
← {"results": [{"id": "0x2"}, null], "objects": {"0x2": {"type": "Label"}}}
```

The reply has one result per step, in order: the id of the new label, then
`null`, because `add_label` returns nothing. By default (`results="links"`),
each object in the reply shows only its references to other objects. With
`results="full"`, it shows all of its values.

An object that the batch creates but never attaches to anything is listed
under `unattached` in the reply, and then discarded.

## Plain state

You can give agents access to state variables without writing a class:

```python
server.state.mcp_expose("resolution", type=int, schema={"minimum": 3},
                        description="Facets of the cone", read_only=False)
server.state.mcp_unexpose("resolution")
```

Agents see the exposed variables as properties of a built-in object named
`state`. A variable exposed through a child server appears under its full,
prefixed name.

## Permissions

The people running your application may not want an agent to have some
capabilities, such as reading files or running code. You can declare these
capabilities as permissions, which can then be turned off while the
application runs or at launch.

First, declare each permission with a name and a description:

```python
server.mcp.permissions.declare("files", "Read files on this computer")
server.mcp.permissions.declare("scripts", "Run Python code the agent writes",
                               requires="files", allowed=False)
```

The description says what the permission lets an agent do. Agents read it
when a call needs the permission while it is off. A permission starts
allowed, unless you declare it with `allowed=False`, as `scripts` is. Its
`requires` option is described [below](#permissions-that-require-others).

Then, give each tool, method, property, property setter or constructor the
permissions it needs, with its own `requires=` option:

```python
class Editor(TrameComponent):
    @mcp.method(requires="files")
    def open(self, path: str) -> str: ...
```

Sometimes only some calls need a permission, depending on their arguments.
In that case, leave `requires=` out and call `server.mcp.permissions.require()`
inside the method instead. While the permission is allowed, it does nothing.
While the permission is off, it raises an error that stops the call:

```python
SAMPLES = {"skull", "engine"}


class Dataset(TrameComponent):
    @mcp.method
    def load(self, name: str) -> str:
        """Load a bundled sample by name, or a file by its path."""
        if name not in SAMPLES:  # a file on this computer
            self.mcp.permissions.require("files", what=f"Loading {name}")
        ...
```

With `files` off, agents can still load the samples, but loading a file fails.
The agent receives the error's message, which starts with the `what` option
(by default, "This call"):

```
Loading /data/head.vti: permission "files" (Read files on this computer) is off; only the people running the app can turn it on.
```

You can turn permissions on and off in code at any time, for example from a
switch in your UI. `server.mcp.permissions` works like a dictionary that maps each
permission's name to whether it is allowed:

```python
server.mcp.permissions["scripts"] = True                 # allow it
server.mcp.permissions["scripts"] = False                # deny it
server.mcp.permissions.update(files=True, scripts=True)  # several at once
server.mcp.permissions["files"]                          # True while it is allowed
```

While a permission is off, anything that requires it disappears from the tool
list and from `object_types`, and calls to it are rejected. A property
whose setter requires it becomes read-only. An agent that listed its tools
before the permission was turned off keeps them in its list until it lists
them again, but its calls are rejected. The overview that agents receive when
they connect lists the permissions that are off.

### Permissions that require others

A permission can itself require other permissions, with `requires=` in
`declare()`. It is then allowed only while they are. Use this when one
permission grants another anyway. In the example, a script can read files, so
`scripts` requires `files`:

- Denying `files` also denies `scripts`.
- Allowing `scripts` while `files` is denied raises an error. Allow both in a
  single call instead, with `update(files=True, scripts=True)`.

In your UI, disable the `scripts` switch while `files` is off.

### Denying permissions at launch

The `--mcp-deny` flag and the `TRAME_MCP_DENY` environment variable deny
permissions for the whole run, and neither code nor UI can turn them back on.
`server.mcp.permissions.locked` lists them, along with the permissions that require
them, so that your UI can disable the corresponding switches.

## Classes you don't own

Decorators and the `mcp=` keyword only work in classes you write. For a
component or model class from another library, call its `mcp_describe()`
method instead. It takes the same options as the
[`mcp=` keyword](#class-options):

```python
from some_library import Camera

Camera.mcp_describe(description="The camera of the 3D view.",
                    properties={"position": "[x, y, z]"}, methods=["reset"])
```

- The options also apply to the class's subclasses. `Camera.mcp_describe(False)`
  hides the class.
- These settings apply to the whole process, and only one `mcp_describe` call
  per class may change them.
- Call `mcp_describe` before you expose an instance of the class. Exposing an
  instance of a class that declares nothing for agents raises an error. An
  instance created before the call can still be exposed after it.
- `Cls.mcp_describe()` without arguments returns the class's current options,
  and `server.mcp.describe(Cls)` returns what agents see of it, which is
  useful in tests.

## Options, launch flags and security

### Options

`server.mcp.configure(...)` sets several options at once, and each option is also an
attribute of `server.mcp`. A `TrameApp` can turn agent access on when it's built, with `super().__init__(server, mcp_enabled=True)`, which
does the same as setting `enabled`.

| Option | Default | Description |
| --- | --- | --- |
| `enabled` | `False` | Turns agent access on or off, whichever way agents connect. It can change at any time |
| `transports` | `("http",)` | How agents outside the application's process connect. It can change at any time |
| `name` | the server's name | The name reported to agents and used in the connection commands |
| `instructions` | `None` | Text sent to agents before the generated overview |
| `concurrent_calls` | `False` | Lets every agent call run while others are in progress, instead of one at a time |
| `structured_content` | `False` | Also sends dictionary results as `structuredContent` |
| `max_response_tokens` | `8000` | The maximum size, in tokens, of a reply from the built-in tools |

A *transport* is the way an agent running in another process reaches the
application. The only transport today is HTTP: an endpoint on the same port as
the application, which is the default. With `transports=[]`, no transport is
served, and only agents running inside the application's own process can use
the application, through [`server.mcp.client()`](#from-inside-the-application). `enabled` turns
their access on and off as well. Like `enabled`, `transports` can change while
the application runs, so a switch in its interface can let agents in other
processes in and out. While HTTP is left out, its endpoint answers that it is
off.

The HTTP transport has its own options on `server.mcp.http`, set the same way:
`server.mcp.http.configure(...)` sets several at once, and each one is also an
attribute.

| Option | Default | Description |
| --- | --- | --- |
| `token` | `None` | The bearer token agents must send. One is generated when the application listens beyond this machine |
| `allowed_origins` | `()` | Additional browser origins allowed to call the endpoint |
| `path` | `"/mcp"` | The path of the endpoint. It cannot change once the server has started |
| `url` | | The endpoint's URL, as agents on this machine reach it (read-only) |

### Launch flags

The people who run your application can set some of these options when they
launch it, without changing its code. Some flags can also be given as
environment variables:

```bash
python app.py --mcp --mcp-deny scripts
```

| Flag | Environment variable | Description |
| --- | --- | --- |
| `--mcp`, `--no-mcp` | | Turns agent access on or off. `--no-mcp` holds for the whole run: no transport is served, and agents inside the process are refused too |
| `--mcp-transport T[,T]` | | Chooses the transports to start with, overriding the application's choice: `http`, or `none` to start with agents inside the process only. It doesn't turn access on |
| `--no-mcp-transport` | | Serves no transport for the whole run: only agents inside the process can use the application |
| `--mcp-http-token TOKEN` | `TRAME_MCP_HTTP_TOKEN` | Sets the HTTP transport's bearer token |
| `--mcp-log` | `TRAME_MCP_LOG` | Logs one line per agent call, at INFO on the `trame_server.mcp` loggers |
| `--mcp-deny P[,P]` | `TRAME_MCP_DENY` | Denies permissions for the whole run; the application can't allow them again |

Until the server starts, launch flags take precedence over the values set in
code. After that, the application's own changes apply, except that what
`--no-mcp`, `--no-mcp-transport` and `--mcp-deny` withhold stays withheld for
the whole run. For example, `--mcp --mcp-transport none` turns access on for
an assistant inside the application and keeps agents in other processes out
until the application lets them in, while `--mcp --no-mcp-transport` keeps
them out for good. `server.mcp.enabled_locked` and `server.mcp.transports_locked` tell the
application's interface when its switches have no effect.

As elsewhere in Trame, `--mcp-log` only sets a logging level, so the lines
appear once your application configures logging, for example with
`logging.basicConfig(level=logging.INFO)`. Each line names the agent's
session, what it called with its arguments shortened, how the call ended and
how long it took.

### Security

The HTTP endpoint checks the `Origin` header and rejects requests coming from web
pages on other sites. Without a token, it also rejects requests addressed to
any host name other than a loopback address (`localhost`, `127.0.0.1` or
`::1`). It is served by aiohttp, Trame's default web server.

## Examples

The [`examples/10_mcp`](https://github.com/Kitware/trame/tree/master/examples/10_mcp)
directory contains complete applications:

| Example | What it shows |
| --- | --- |
| `00_quickstart.py` | The quick start without classes: one state variable and one tool |
| `01_class_based.py` | The quick start's two cones, with sliders and a switch that turns agent access on and off |
| `02_address_book.py` | trame-dataclass models that agents create and attach in a batch |
| `03_permissions.py` | Permissions on a tool, methods and a property setter, switched from the UI or with `--mcp-deny`, and a method marked destructive |
| `04_exposure.py` | A class from another library, a subclass that hides a method, read-only names, a name that follows the selection and has a description, a resource and a prompt |

[`examples/validation/mcp/wasm_quadrants.py`](https://github.com/Kitware/trame/tree/master/examples/validation/mcp)
is a larger stress test, with a grid of VTK WASM scenes and models nested
three levels deep.
