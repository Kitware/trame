from trame import get_app_instance
from trame.html import AbstractElement

MODULE = None


def use_module(m):
    global MODULE
    MODULE = m
    _app = get_app_instance()
    _app.enable_module(m)


class VtkAlgorithm(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("vtk-algorithm", children, **kwargs)
        self._attr_names += ["port", "vtk_class", "state"]


class VtkCellData(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("vtk-cell-data", children, **kwargs)


class VtkDataArray(AbstractElement):
    def __init__(self, **kwargs):
        super().__init__("vtk-data-array", **kwargs)
        self._attr_names += [
            "name",
            "registration",
            "type",
            "values",
            "number_of_components",
        ]


class VtkFieldData(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("vtk-field-data", children, **kwargs)


class VtkGeometryRepresentation(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("vtk-geometry-representation", children, **kwargs)
        self._attr_names += [
            "id",
            "color_map_preset",
            "color_data_range",
            "actor",
            "mapper",
            "property",
        ]


class VtkGlyphRepresentation(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("vtk-glyph-representation", children, **kwargs)
        self._attr_names += [
            "color_map_preset",
            "color_data_range",
            "actor",
            "mapper",
            "property",
        ]


class VtkMesh(AbstractElement):
    def __init__(
        self,
        name,
        dataset=None,
        field_to_keep=None,
        point_arrays=None,
        cell_arrays=None,
        **kwargs,
    ):
        super().__init__("vtk-mesh", **kwargs)
        self.__name = name
        self.__dataset = dataset
        self.__field_to_keep = field_to_keep
        self.__point_arrays = point_arrays
        self.__cell_arrays = cell_arrays
        self._attr_names += ["port", "state"]
        if dataset:
            self._attributes["state"] = f':state="{name}"'
            self.update()

    def set_dataset(self, dataset):
        self.__dataset = dataset
        self.update()

    def update(self, **kwargs):
        if self.__dataset:
            _app = get_app_instance()
            _app.set(
                self.__name,
                MODULE.mesh(
                    self.__dataset,
                    field_to_keep=kwargs.get("field_to_keep", self.__field_to_keep),
                    point_arrays=kwargs.get("point_arrays", self.__point_arrays),
                    cell_arrays=kwargs.get("cell_arrays", self.__cell_arrays),
                ),
            )


class VtkPointData(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("vtk-point-data", children, **kwargs)


class VtkPolyData(AbstractElement):
    def __init__(self, name, children=None, dataset=None, **kwargs):
        super().__init__("vtk-polydata", children, **kwargs)
        self.__name = name
        self.__dataset = dataset
        self._attr_names += [
            "port",
            "verts",
            "lines",
            "polys",
            "strips",
            "connectivity",
        ]
        if dataset:
            self._attributes["bind"] = f'v-bind="{name}.mesh"'
            self.update()

    def set_dataset(self, dataset):
        self.__dataset = dataset
        self.update()

    def update(self):
        if self.__dataset:
            _app = get_app_instance()
            _app.set(self.__name, MODULE.mesh(self.__dataset))


class VtkReader(AbstractElement):
    def __init__(self, **kwargs):
        super().__init__("vtk-reader", **kwargs)
        self._attr_names += [
            "parse_as_array_buffer",
            "parse_as_text",
            "port",
            "render_on_update",
            "reset_camera_on_update",
            "url",
            "vtk_class",
        ]


class VtkRemoteLocalView(AbstractElement):
    def __init__(self, view, **kwargs):
        super().__init__("vtk-remote-local-view", **kwargs)
        __ns = kwargs["namespace"]

        # !!! HACK !!!
        # Allow user to configure view mode by providing (, local/remote)
        __rmode = "remote"
        __mode_arg = kwargs.get("mode", (f"{__ns}Mode",))
        if __mode_arg and isinstance(__mode_arg, (tuple, list)) and len(__mode_arg) > 1:
            __rmode = __mode_arg[1]
            self._attributes["mode"] = f':mode="{__mode_arg[0]}"'
        elif __mode_arg and isinstance(__mode_arg, (tuple, list)):
            self._attributes["mode"] = f':mode="{__mode_arg[0]}"'
        elif __mode_arg and isinstance(__mode_arg, str):
            self._attributes["mode"] = f'mode="{__mode_arg}"'
        # !!! HACK !!!

        self.__scene_id = f"{__ns}Scene"
        self.__view_id = MODULE.id(view)
        self.__view = view
        self.__wrapped_view = MODULE.view(view, __ns, mode=__rmode)

        self._attributes["wsClient"] = ':wsClient="wsClient"'
        self._attributes["ref"] = f'ref="{kwargs.get("ref", __ns)}"'
        self._attributes["view_id"] = f'id="{self.__view_id}"'
        self._attributes["view_state"] = f':viewState="{self.__scene_id}"'

        self._attr_names += [
            # "mode", # <--- Managed by hand above
            "context_name",
            "interactive_ratio",
            "interactor_events",
            "interactor_settings",
            "namespace",
        ]
        self._event_names += kwargs.get("interactor_events", [])

    def update_geometry(self):
        _app = get_app_instance()
        _app.set(self.__scene_id, MODULE.scene(self.__view))

    def update_image(self):
        MODULE.push_image(self.__view)

    @property
    def view(self):
        return self.__wrapped_view


class VtkRemoteView(AbstractElement):
    @staticmethod
    def push_image(view):
        MODULE.push_image(view)

    def __init__(self, view, ref="view", **kwargs):
        super().__init__("vtk-remote-view", **kwargs)
        self.__view = view
        self._attributes["wsClient"] = ':wsClient="wsClient"'
        self._attributes["ref"] = f'ref="{ref}"'
        self._attributes["view_id"] = f'id="{MODULE.id(view)}"'
        self._attr_names += [
            "enable_picking",
            "interactive_quality",
            "interactive_ratio",
            "interactor_events",
        ]
        self._event_names += kwargs.get("interactor_events", [])

    def update(self):
        MODULE.push_image(self.__view)


class VtkShareDataset(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("vtk-share-dataset", children, **kwargs)
        self._attr_names += ["port", "name"]


class VtkSyncView(AbstractElement):
    def __init__(self, view, ref="view", **kwargs):
        super().__init__("vtk-sync-view", **kwargs)
        self.__scene_id = f"scene_{self._id}"
        self.__view = view
        self.__ref = ref
        self._attributes["ref"] = f'ref="{ref}"'
        self._attributes["wsClient"] = ':wsClient="wsClient"'
        self._attributes["view_state"] = f':viewState="{self.__scene_id}"'
        self._attr_names += ["interactor_events", "interactor_settings", "context_name"]
        self._event_names += kwargs.get("interactor_events", [])
        self.update()

    def update(self):
        _app = get_app_instance()
        _app.set(self.__scene_id, MODULE.scene(self.__view))

    def reset_camera(self):
        _app = get_app_instance()
        _app.update(ref=self.__ref, method="resetCamera")


class VtkLocalView(VtkSyncView):
    pass


class VtkView(AbstractElement):
    def __init__(self, children=None, ref="view", **kwargs):
        super().__init__("vtk-view", children, **kwargs)
        self._ref = ref
        self._attributes["ref"] = f'ref="{ref}"'
        self._attr_names += [
            "background",
            "cube_axes_style",
            "interactor_settings",
            "picking_modes",
            "show_cube_axes",
        ]
        self._event_names += [
            "hover",
            "click",
            "select",
            "resize",
        ]

    def reset_camera(self):
        _app = get_app_instance()
        _app.update(ref=self._ref, method="resetCamera")
