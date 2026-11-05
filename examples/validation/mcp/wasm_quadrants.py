"""Stress example: dynamic quadrant grid of VTK WASM scenes, all trame-dataclass.

Run:  python examples/validation/mcp/wasm_quadrants.py --server
Deps: pip install trame-dataclass vtk trame-vtklocal

Then use one of the commands the console prints to start a Claude Code or
Codex session connected to the app. The MCP root is `workspace`:
    object_types()
    object_call("workspace", "set_grid", {"rows": 2, "cols": 2})
    object_call("<scene id>", "add_object", {"type": "cone"})
    object_update("<object id>", {"color": [1, 0, 0], "resolution": 42})

Fully client-reactive UI: the main layout template is written ONCE. Quadrants
and object rows are rendered by Vue from the synced dataclass state (`v-for` +
per-class `generate_gui` templates). Each scene's WASM view is a LocalView in
its own named server template (created once per scene, referenced reactively
via `trame-template`), so object add/remove never remounts a view.

Stress points exercised:
- three-level reachability (workspace -> scenes -> objects)
- structural changes via model methods (grid reconciliation, add/remove
  object); the reference properties holding scenes and objects are read-only
- `object_update` on plain properties (rows/cols) triggering structural watchers
- ServerOnly fields hiding live VTK objects from MCP
- ClientOnly `type` field: readable over MCP, never writable
- the three ways to expose a model: SceneObject opts in every field by mode
  (`all_fields`), Scene every public method minus its lifecycle hooks
  (`all_methods` + `methods` set to False), Workspace only what it marks (no
  class keyword)
- `mcp=` field options: descriptions and constraints (ranges, enums, vector
  lengths) advertised by object_types and enforced on every MCP write;
  unmarked per-browser UI state stays invisible
- agent-facing descriptions next to developer docstrings (`description` on
  SceneObject and Scene, and on Scene's clear_objects method)
- a live entry point (`lambda: self.workspace`)
- model inheritance: SceneObject base, per-type subclasses each with their own
  MCP schema (only resolution-capable objects expose `resolution`)
- no agent-built models (no `@mcp_constructor`): scenes and objects only come
  from set_grid and add_object, which build their VTK pipelines
- a first-class prompt marked on the app (`@mcp_prompt`), built once
- human edits (sliders/checkboxes) and MCP edits converging on the same models
"""

import contextlib
from typing import Annotated, Literal

# Required for rendering/interactor factories
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
from trame.app import TrameApp
from trame.decorators import mcp_method, mcp_prompt
from trame.ui.html import DivLayout
from trame.widgets import client, html, vtklocal
from trame.widgets import dataclass as dc
from trame_dataclass.v2 import (
    ClientOnly,
    ServerOnly,
    StateDataModel,
    Sync,
    get_instance,
    watch,
)
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkCylinderSource,
    vtkSphereSource,
    vtkSuperquadricSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)
from vtkmodules.vtkRenderingFreeType import vtkVectorText

OBJECT_TYPES = ("cone", "sphere", "cylinder", "cube", "torus", "text")
MAX_QUADRANTS = 25
ObjectType = Literal["cone", "sphere", "cylinder", "cube", "torus", "text"]
REPRESENTATIONS = ("surface", "wireframe", "points")

VEC3 = {"minItems": 3, "maxItems": 3}
RGB = {**VEC3, "items": {"type": "number", "minimum": 0, "maximum": 1}}

# Multiple LocalViews need the async wasm runtime, otherwise only one view's
# event loop runs (trame-vtklocal issue #76). Async requires JSPI
# (WebAssembly.Suspending): available by default on recent Chromium, not on
# Firefox. Detect it client-side and degrade to sync (renders fine, but only
# one quadrant's camera is interactive) instead of crashing.
WASM_CONFIG_EXPR = (
    "(utils.get('WebAssembly') || {}).Suspending "
    "? {rendering: 'webgl', exec: 'async'} "
    ": {rendering: 'webgl', exec: 'sync'}"
)

CELL_STYLE = (
    "border: 1px solid #445; border-radius: 6px; padding: 4px; margin: 0; "
    "flex: 1; display: flex; flex-direction: column; min-height: 0; "
    "font-family: sans-serif; font-size: 14px;"
)
ROW_STYLE = "display: flex; gap: 6px; align-items: center;"

# VTK Set/Get pairs that are internals, not user-facing geometry properties
VTK_PROPERTY_EXCLUDE = {
    "AbortExecute",
    "AbortOutput",
    "Debug",
    "GlobalWarningDisplay",
    "ObjectName",
    "OutputPointsPrecision",
    "Progress",
    "ProgressShiftScale",
    "ProgressText",
    "ReferenceCount",
    "ReleaseDataFlag",
}


def vtk_scalar_properties(obj):
    """Introspect a VTK object for its scalar/vector Set/Get property pairs.

    Returns {name: {"value": ..., "min": ..., "max": ...}} — min/max only for
    properties that advertise bounds (VTK's Get<Name>MinValue convention).
    """
    result = {}
    for attr in dir(obj):
        if not attr.startswith("Set"):
            continue
        name = attr[3:]
        if (
            not name
            or name in VTK_PROPERTY_EXCLUDE
            or name.endswith(("MinValue", "MaxValue"))
        ):
            continue
        getter = getattr(obj, f"Get{name}", None)
        if getter is None:
            continue
        try:
            value = getter()
        except TypeError:  # getter requires arguments -> not a plain property
            continue
        is_scalar = isinstance(value, (bool, int, float, str))
        is_vector = (
            isinstance(value, tuple)
            and bool(value)
            and all(isinstance(v, (int, float)) for v in value)
        )
        if not (is_scalar or is_vector):
            continue
        entry = {"value": list(value) if is_vector else value}
        for bound, suffix in (("min", "MinValue"), ("max", "MaxValue")):
            bound_getter = getattr(obj, f"Get{name}{suffix}", None)
            if bound_getter is not None:
                with contextlib.suppress(TypeError):
                    entry[bound] = bound_getter()
        result[name] = entry
    return result


# -----------------------------------------------------------------------------
# Data models
# -----------------------------------------------------------------------------


class SceneObject(  # options inherited by every object type
    StateDataModel,
    mcp={"description": "An object drawn in a scene.", "all_fields": True},
):
    """Base class for anything that can live in a Scene."""

    # ClientOnly: read-only over MCP by field mode; subclasses redeclare the
    # default and inherit the description
    type = ClientOnly(str, "", mcp="Object type")
    color = Sync(
        list[float],
        lambda: [0.9, 0.9, 0.9],
        mcp={"description": "RGB, 0-1 each", "schema": RGB},
    )
    position = Sync(
        list[float],
        lambda: [0.0, 0.0, 0.0],
        mcp={"description": "[x, y, z]", "schema": VEC3},
    )
    scale = Sync(
        list[float],
        lambda: [1.0, 1.0, 1.0],
        mcp={"description": "[sx, sy, sz]", "schema": VEC3},
    )
    rotation = Sync(
        list[float],
        lambda: [0.0, 0.0, 0.0],
        mcp={"description": "Degrees around x, y, z", "schema": VEC3},
    )
    opacity = Sync(
        float,
        1.0,
        mcp={
            "description": "0 = transparent, 1 = opaque",
            "schema": {"minimum": 0, "maximum": 1},
        },
    )
    representation = Sync(
        str, "surface", mcp={"schema": {"enum": list(REPRESENTATIONS)}}
    )
    visible = Sync(bool, True)

    source = ServerOnly(object)
    actor = ServerOnly(object)
    scene = ServerOnly(object)  # backref, not a dataclass field -> no MCP cycle

    SOURCE_CLASS = None  # set by concrete subclasses

    @classmethod
    def generate_gui(cls, trame_server=None) -> str:
        with html.Div(
            trame_server=trame_server,
            v_if="self_available && self._id",
            style=ROW_STYLE,
        ) as root:
            cls._gui_row(root)
        return root.html

    @classmethod
    def _gui_row(cls, _root):
        html.Span("{{ self.type }} #{{ self._id }}", style="min-width: 5.5em;")
        html.Span("visible")
        html.Input(type="checkbox", v_model="self.visible")
        html.Button("remove", click=(cls.ui_remove, "[self._id]"))

    @classmethod
    def ui_remove(cls, object_id):
        obj = get_instance(object_id)
        if obj is not None and obj.scene is not None:
            obj.scene.remove_object(object_id)

    @mcp_method(read_only=True)
    def vtk_source_properties(self) -> dict:
        """Advanced: list every scalar/vector property of this object's
        underlying VTK source, beyond the declared properties.

        Returns {name: {value, min?, max?}}; set them with
        set_vtk_source_property. Prefer the declared properties when one
        covers the same thing (e.g. resolution).
        """
        if self.source is None:
            msg = "Object has no VTK source yet"
            raise RuntimeError(msg)
        return vtk_scalar_properties(self.source)

    @mcp_method
    def set_vtk_source_property(
        self, name: str, value: float | int | bool | str | list[float]
    ) -> str:
        """Advanced: set a VTK source property by name, as listed by
        vtk_source_properties (e.g. Height or Radius on a cone).

        Vector-valued properties take a list. Changes render immediately but
        are not tracked as model properties.
        """
        properties = vtk_scalar_properties(self.source)
        if name not in properties:
            msg = (
                f"Unknown VTK property {name!r} on {type(self.source).__name__}. "
                f"Available: {sorted(properties)}"
            )
            raise ValueError(msg)
        setter = getattr(self.source, f"Set{name}")
        if isinstance(value, list):
            setter(*value)
        else:
            setter(value)
        self.scene.request_render()
        return f"{type(self.source).__name__}.{name} = {value}"

    def build(self, scene):
        self.scene = scene
        self.source = self.SOURCE_CLASS()
        self._setup_source()
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(self.source.GetOutputPort())
        self.actor = vtkActor()
        self.actor.SetMapper(mapper)
        self._apply_resolution()
        self._apply_appearance()
        return self.actor

    def _setup_source(self):
        """Subclass hook to configure the freshly created source."""

    def _apply_resolution(self):
        """No resolution on the base class (see ResolutionObject)."""

    def _apply_appearance(self):
        prop = self.actor.GetProperty()
        prop.SetColor(*self.color[:3])
        prop.SetOpacity(max(0.0, min(float(self.opacity), 1.0)))
        representation = str(self.representation).lower()
        if representation == "wireframe":
            prop.SetRepresentationToWireframe()
        elif representation == "points":
            prop.SetRepresentationToPoints()
            prop.SetPointSize(4)
        else:
            prop.SetRepresentationToSurface()
        self.actor.SetPosition(*self.position[:3])
        self.actor.SetScale(*self.scale[:3])
        self.actor.SetOrientation(*self.rotation[:3])
        self.actor.SetVisibility(bool(self.visible))

    @watch(
        "color",
        "position",
        "scale",
        "rotation",
        "opacity",
        "representation",
        "visible",
        sync=True,
    )
    def _on_appearance(self, *_):
        if self.actor is None:
            return
        self._apply_appearance()
        self.scene.request_render()


class ResolutionObject(SceneObject):
    """Scene object with a tessellation resolution (cone, cylinder, sphere, torus)."""

    resolution = Sync(
        int,
        16,
        mcp={
            "description": "Tessellation resolution",
            "schema": {"minimum": 3, "maximum": 128},
        },
    )

    @classmethod
    def _gui_row(cls, _root):
        html.Span("{{ self.type }} #{{ self._id }}", style="min-width: 5.5em;")
        html.Span("visible")
        html.Input(type="checkbox", v_model="self.visible")
        html.Span("resolution")
        html.Input(
            type="range",
            min=3,
            max=64,
            v_model_number="self.resolution",
            style="flex: 1;",
        )
        html.Button("remove", click=(cls.ui_remove, "[self._id]"))

    def _apply_resolution(self):
        self.source.SetResolution(max(3, min(int(self.resolution), 128)))

    @watch("resolution", sync=True)
    def _on_resolution(self, _resolution):
        if self.source is None:
            return
        self._apply_resolution()
        self.scene.request_render()


class ConeObject(ResolutionObject):
    type = ClientOnly(str, "cone")
    SOURCE_CLASS = vtkConeSource


class CylinderObject(ResolutionObject):
    type = ClientOnly(str, "cylinder")
    SOURCE_CLASS = vtkCylinderSource


class SphereObject(ResolutionObject):
    type = ClientOnly(str, "sphere")
    SOURCE_CLASS = vtkSphereSource

    def _apply_resolution(self):
        resolution = max(3, min(int(self.resolution), 128))
        self.source.SetThetaResolution(resolution)
        self.source.SetPhiResolution(resolution)


class CubeObject(SceneObject):
    type = ClientOnly(str, "cube")
    SOURCE_CLASS = vtkCubeSource


class TorusObject(ResolutionObject):
    type = ClientOnly(str, "torus")
    thickness = Sync(
        float,
        0.3,
        mcp={
            "description": "Ring thickness",
            "schema": {"minimum": 0.01, "maximum": 1},
        },
    )
    SOURCE_CLASS = vtkSuperquadricSource

    def _setup_source(self):
        self.source.ToroidalOn()
        self.source.SetThickness(max(0.01, min(float(self.thickness), 1.0)))

    def _apply_resolution(self):
        resolution = max(3, min(int(self.resolution), 128))
        self.source.SetThetaResolution(resolution)
        self.source.SetPhiResolution(resolution)

    @watch("thickness", sync=True)
    def _on_thickness(self, thickness):
        if self.source is None:
            return
        self.source.SetThickness(max(0.01, min(float(thickness), 1.0)))
        self.scene.request_render()


class TextObject(SceneObject):
    type = ClientOnly(str, "text")
    text = Sync(str, "hello", mcp="Displayed text")
    SOURCE_CLASS = vtkVectorText

    def _setup_source(self):
        self.source.SetText(self.text or " ")

    @classmethod
    def _gui_row(cls, _root):
        html.Span("{{ self.type }} #{{ self._id }}", style="min-width: 5.5em;")
        html.Span("visible")
        html.Input(type="checkbox", v_model="self.visible")
        html.Input(v_model="self.text", style="flex: 1;")
        html.Button("remove", click=(cls.ui_remove, "[self._id]"))

    @watch("text", sync=True)
    def _on_text(self, text):
        if self.source is None:
            return
        self.source.SetText(str(text) or " ")
        self.scene.request_render()


TYPE_TO_CLASS = {
    "cone": ConeObject,
    "sphere": SphereObject,
    "cylinder": CylinderObject,
    "cube": CubeObject,
    "torus": TorusObject,
    "text": TextObject,
}


class Scene(
    StateDataModel,
    mcp={
        "description": "One quadrant of the grid: a 3D view and the objects in it.",
        "all_methods": True,
        "methods": {
            "build_pipeline": False,
            "request_render": False,
            # the docstring is written for developers
            "clear_objects": "Remove every object from this scene.",
        },
    },
):
    name = Sync(str, "Scene", mcp="Label shown in the quadrant header")
    background = Sync(
        list[float],
        lambda: [0.12, 0.12, 0.18],
        mcp={"description": "Background RGB, 0-1 each", "schema": RGB},
    )
    # structural changes go through add_object / remove_object, which keep
    # the renderer in step: read-only for agents
    objects = Sync(list[SceneObject], list, has_dataclass=True, mcp={"read_only": True})
    # per-browser UI state: not marked, not exposed
    overlay_open = ClientOnly(bool, True)

    renderer = ServerOnly(object)
    render_window = ServerOnly(object)
    interactor = ServerOnly(object)
    view = ServerOnly(object)

    @classmethod
    def generate_gui(cls, trame_server=None) -> str:
        with html.Div(
            trame_server=trame_server,
            v_if="self_available && self._id",
            style=CELL_STYLE,
        ) as root:
            # header: editable name + add-object buttons + camera reset
            with html.Div(style=ROW_STYLE):
                html.Input(v_model="self.name", style="width: 6em;")
                for object_type in OBJECT_TYPES:
                    html.Button(
                        f"+{object_type}",
                        click=(cls.ui_add_object, f"[self._id, '{object_type}']"),
                    )
                html.Button("reset view", click=(cls.ui_reset_camera, "[self._id]"))

            # the WASM view lives in a per-scene server template, created once
            # in build_pipeline() and referenced reactively by name here
            with html.Div(style="flex: 1; min-height: 100px; position: relative;"):
                client.ServerTemplate(name=("`scene_view_${self._id}`",))

                # object rows float over the top of the 3D view; minimizable,
                # capped to the quadrant height, scrollable when crowded
                with html.Div(
                    style=(
                        "position: absolute; top: 4px; left: 4px; z-index: 1; "
                        "max-height: calc(100% - 8px); "
                        "max-width: calc(100% - 8px); "
                        "display: flex; flex-direction: column; "
                        "background: rgba(255, 255, 255, 0.65); "
                        "backdrop-filter: blur(2px); "
                        "border-radius: 4px; padding: 2px 6px;"
                    ),
                    v_if="self.objects.length",
                ):
                    with html.Div(style=ROW_STYLE):
                        html.Span(
                            "objects ({{ self.objects.length }})",
                            style="font-weight: bold;",
                        )
                        html.Button(
                            "{{ self.overlay_open ? '-' : '+' }}",
                            click="self.overlay_open = !self.overlay_open",
                            style="margin-left: auto;",
                        )
                    with html.Div(
                        v_show="self.overlay_open",
                        style=(
                            "overflow-y: auto; min-height: 0; "
                            "display: flex; flex-direction: column; gap: 2px;"
                        ),
                    ):
                        with html.Div(v_for="obj in self.objects", key=("obj._id",)):
                            dc.Gui(instance=("obj._id",))
        return root.html

    @classmethod
    def ui_add_object(cls, scene_id, object_type):
        scene = get_instance(scene_id)
        if scene is not None:
            scene.add_object(object_type)

    @classmethod
    def ui_reset_camera(cls, scene_id):
        scene = get_instance(scene_id)
        if scene is not None:
            scene.reset_camera()

    def _next_free_position(self):
        # First default slot along X not occupied by an existing object, so a
        # new object never overlaps survivors of earlier removals
        taken = {round(o.position[0] / 1.2) for o in self.objects if o is not None}
        slot = 0
        while slot in taken:
            slot += 1
        return [slot * 1.2, 0.0, 0.0]

    def build_pipeline(self):
        self.renderer = vtkRenderer()
        self.renderer.SetBackground(*self.background[:3])
        self.render_window = vtkRenderWindow()
        self.render_window.OffScreenRenderingOn()
        self.render_window.AddRenderer(self.renderer)
        # The WASM remote session requires an interactor on the mirrored window
        self.interactor = vtkRenderWindowInteractor()
        self.interactor.SetRenderWindow(self.render_window)
        self.interactor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

        # One LocalView per scene, in its own named template, created exactly
        # once - object add/remove never remounts it
        with DivLayout(
            self.server,
            template_name=f"scene_view_{self._id}",
            style="position: absolute; inset: 0;",
        ):
            self.view = vtklocal.LocalView(
                self.render_window,
                throttle_rate=20,
                config=(WASM_CONFIG_EXPR,),
            )

    def request_render(self, push_camera=False):
        if self.render_window is None:
            return
        self.render_window.Render()
        if self.view is not None:
            if push_camera:
                self.view.update(push_camera=True)
            else:
                self.view.update_throttle()

    @watch("background", sync=True)
    def _on_background(self, background):
        if self.renderer is None:
            return
        self.renderer.SetBackground(*background[:3])
        self.request_render()

    def add_object(self, type: ObjectType) -> dict:
        """Add a new object to this scene and return its id.

        Change its appearance with object_update on that id; the properties
        of each object type are listed by object_types.
        """
        if type not in TYPE_TO_CLASS:
            msg = f"Unknown type {type!r}. Available types: {list(TYPE_TO_CLASS)}"
            raise ValueError(msg)

        obj = TYPE_TO_CLASS[type](self.server)
        obj.position = self._next_free_position()
        self.renderer.AddActor(obj.build(self))
        self.objects = [*self.objects, obj]

        self.renderer.ResetCamera()
        self.request_render(push_camera=True)
        return {"id": obj._id, "type": type}

    def remove_object(self, object_id: str) -> str:
        """Remove an object from this scene by its id."""
        live = [o for o in self.objects if o is not None]
        match = [o for o in live if o._id == object_id]
        if not match:
            msg = (
                f"No object {object_id!r} in scene {self.name!r}. "
                f"Object ids: {[o._id for o in live]}"
            )
            raise ValueError(msg)
        self.renderer.RemoveActor(match[0].actor)
        self.objects = [o for o in live if o._id != object_id]
        self.request_render()
        return f"Removed {object_id}"

    def clear_objects(self) -> str:
        """Remove every object from this scene.

        Also recovers from any corrupted entries by removing all actors from
        the renderer, including strays with no backing object.
        """
        self.renderer.RemoveAllViewProps()
        self.objects = []
        self.request_render()
        return "Scene cleared"

    def reset_camera(self) -> str:
        """Reset this scene's camera to fit all visible objects."""
        self.renderer.ResetCamera()
        self.request_render(push_camera=True)
        return "Camera reset"


class Workspace(StateDataModel):  # no keyword: only what it marks
    """The quadrant grid, one scene per quadrant."""

    rows = Sync(
        int,
        1,
        mcp={
            "description": "Grid rows",
            "schema": {"minimum": 1, "maximum": MAX_QUADRANTS},
        },
    )
    cols = Sync(
        int,
        1,
        mcp={
            "description": "Grid columns",
            "schema": {"minimum": 1, "maximum": MAX_QUADRANTS},
        },
    )
    # grid size drives the scenes (set_grid, rows/cols): read-only for agents
    scenes = Sync(list[Scene], list, has_dataclass=True, mcp={"read_only": True})

    @mcp_method
    def set_grid(
        self, rows: Annotated[int, {"minimum": 1}], cols: Annotated[int, {"minimum": 1}]
    ) -> str:
        """Set the quadrant grid to rows x cols (max 25 quadrants total).

        Each quadrant holds one scene; shrinking the grid destroys trailing
        scenes and their objects.
        """
        if rows < 1 or cols < 1 or rows * cols > MAX_QUADRANTS:
            msg = f"Grid must be at least 1x1 and at most {MAX_QUADRANTS} quadrants (got {rows}x{cols})"
            raise ValueError(msg)
        self.rows = rows
        self.cols = cols
        return f"Grid set to {rows}x{cols} ({len(self.scenes)} scenes)"

    @watch("rows", "cols", sync=True)
    def _on_grid(self, rows, cols):
        # Clamp direct property writes (object_update / UI)
        rows, cols = max(1, int(rows)), max(1, int(cols))
        while rows * cols > MAX_QUADRANTS:
            if cols > rows:
                cols -= 1
            else:
                rows -= 1
        self.rows, self.cols = rows, cols  # no-op when already equal
        self.reconcile()

    def reconcile(self):
        desired = self.rows * self.cols
        scenes = list(self.scenes)

        while len(scenes) > desired:
            scenes.pop()
        while len(scenes) < desired:
            scene = Scene(self.server, name=f"Scene {len(scenes) + 1}")
            scene.build_pipeline()
            scenes.append(scene)

        if [s._id for s in scenes] != [s._id for s in self.scenes]:
            self.scenes = scenes


# -----------------------------------------------------------------------------
# Application
# -----------------------------------------------------------------------------


class WasmQuadrantsApp(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self.mcp.configure(
            name="wasm-quadrants",
            enabled=True,
            instructions=(
                "This app shows a grid of 3D scenes rendered in the browser. "
                "Use set_grid to size the quadrant grid, add_object on a scene, "
                "and object_update on objects to change color/position/resolution."
            ),
        )

        self.workspace = Workspace(self.server)
        self.mcp.expose_object(lambda: self.workspace, "workspace")
        self.workspace.reconcile()  # initial 1x1 grid
        self._build_ui()  # built once - everything after this is reactive

    @mcp_prompt
    def demo_script(self) -> str:
        """Suggested walkthrough of the quadrants app."""
        return (
            "Create a 2x2 grid of scenes. Put a red cone in the first scene, "
            "a blue sphere in the second, a green cylinder in the third and a "
            "yellow cube in the last one, then describe the workspace."
        )

    def _ui_adjust_grid(self, d_rows, d_cols):
        ws = self.workspace
        rows = max(1, ws.rows + d_rows)
        cols = max(1, ws.cols + d_cols)
        if rows * cols <= MAX_QUADRANTS:
            ws.rows, ws.cols = rows, cols  # sync watcher reconciles

    def _build_ui(self):
        with DivLayout(
            self.server,
            style="height: 100vh; display: flex; flex-direction: column; font-family: sans-serif;",
        ):
            with self.workspace.provide_as("w"):
                with html.Div(style=ROW_STYLE + "padding: 6px;"):
                    html.B("Grid {{ w.rows }} x {{ w.cols }}")
                    html.Span("rows:")
                    html.Button("-", click=(self._ui_adjust_grid, "[-1, 0]"))
                    html.Button("+", click=(self._ui_adjust_grid, "[1, 0]"))
                    html.Span("cols:")
                    html.Button("-", click=(self._ui_adjust_grid, "[0, -1]"))
                    html.Button("+", click=(self._ui_adjust_grid, "[0, 1]"))
                    html.Span(
                        "({{ w.scenes.length }} scenes, max " + str(MAX_QUADRANTS) + ")"
                    )

                grid_style = (
                    "`flex: 1; display: grid; gap: 6px; padding: 6px; min-height: 0; "
                    "grid-template-columns: repeat(${w.cols}, 1fr); "
                    "grid-template-rows: repeat(${w.rows}, 1fr);`"
                )
                with html.Div(style=(grid_style,)):
                    with html.Div(
                        v_for="scene in w.scenes",
                        key=("scene._id",),
                        style="min-height: 0; display: flex;",
                    ):
                        dc.Gui(instance=("scene._id",), style="flex: 1; display: flex;")


def main():
    app = WasmQuadrantsApp()
    app.server.start()


if __name__ == "__main__":
    main()
