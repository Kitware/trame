from trame import get_app_instance
from trame.html import AbstractElement

MODULE = None


def use_module(m):
    global MODULE
    MODULE = m
    _app = get_app_instance()
    _app.enableModule(m)


class VtkAlgorithm(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("vtk-algorithm", __content, **kwargs)
        self._attr_names += ["port", "vtkClass", "state"]


class VtkCellData(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("vtk-cell-data", __content, **kwargs)


class VtkDataArray(AbstractElement):
    def __init__(self, **kwargs):
        super().__init__("vtk-data-array", **kwargs)
        self._attr_names += [
            "name",
            "registration",
            "type",
            "values",
            "numberOfComponents",
        ]


class VtkFieldData(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("vtk-field-data", __content, **kwargs)


class VtkGeometryRepresentation(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("vtk-geometry-representation", __content, **kwargs)
        self._attr_names += [
            "id",
            "colorMapPreset",
            "colorDataRange",
            "actor",
            "mapper",
            "property",
        ]


class VtkGlyphRepresentation(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("vtk-glyph-representation", __content, **kwargs)
        self._attr_names += [
            "colorMapPreset",
            "colorDataRange",
            "actor",
            "mapper",
            "property",
        ]


class VtkMesh(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("vtk-mesh", __content, **kwargs)
        self._attr_names += ["port", "state"]


class VtkPointData(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("vtk-point-data", __content, **kwargs)


class VtkPolyData(AbstractElement):
    def __init__(self, name, __content=None, dataset=None, **kwargs):
        super().__init__("vtk-polydata", __content, **kwargs)
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
            "parseAsArrayBuffer",
            "parseAsText",
            "port",
            "renderOnUpdate",
            "resetCameraOnUpdate",
            "url",
            "vtkClass",
        ]


class VtkRemoteLocalView(AbstractElement):
    def __init__(self, view, **kwargs):
        super().__init__("vtk-remote-local-view", **kwargs)
        __ns = kwargs["namespace"]

        # !!! HACK !!!
        # Allow user to configure view mode by providing (, local/remote)
        __rmode = "remote"
        __mode_arg = kwargs.get("mode", False)
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
            "contextName",
            "interactiveRatio",
            "interactorEvents",
            "interactorSettings",
            "namespace",
        ]
        self._event_names += kwargs.get("interactorEvents", [])

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
            "enablePicking",
            "interactiveQuality",
            "interactiveRatio",
            "interactorEvents",
        ]
        self._event_names += kwargs.get("interactorEvents", [])

    def update(self):
        MODULE.push_image(self.__view)


class VtkShareDataset(AbstractElement):
    def __init__(self, __content=None, **kwargs):
        super().__init__("vtk-share-dataset", __content, **kwargs)
        self._attr_names += ["port", "name"]


class VtkSyncView(AbstractElement):
    def __init__(self, view, ref="view", **kwargs):
        super().__init__("vtk-sync-view", **kwargs)
        self.__scene_id = f"scene_{self._id}"
        self.__view = view
        self._attributes["ref"] = f'ref="{ref}"'
        self._attributes["wsClient"] = ':wsClient="wsClient"'
        self._attributes["view_state"] = f':viewState="{self.__scene_id}"'
        self._attr_names += ["interactorEvents", "interactorSettings", "contextName"]
        self._event_names += kwargs.get("interactorEvents", [])
        self.update()

    def update(self):
        _app = get_app_instance()
        _app.set(self.__scene_id, MODULE.scene(self.__view))


class VtkView(AbstractElement):
    def __init__(self, __content=None, ref="view", **kwargs):
        super().__init__("vtk-view", __content, **kwargs)
        self._attributes["ref"] = f'ref="{ref}"'
        self._attr_names += [
            "background",
            "cubeAxesStyle",
            "interactorSettings",
            "pickingModes",
            "showCubeAxes",
        ]
