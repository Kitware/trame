import base64
import mimetypes
from pathlib import Path

mimetypes.init()


def to_mime(file_path):
    return mimetypes.guess_type(file_path)[0]


def to_txt(full_path):
    with open(full_path) as txt_file:
        return str(txt_file.read())


def to_base64(full_path):
    with open(full_path, "rb") as bin_file:
        return base64.b64encode(bin_file.read()).decode("ascii")


def to_url(full_path):
    encoded = to_base64(full_path)
    mime = to_mime(full_path)
    return f"data:{mime};base64,{encoded}"


class AssetManager:
    def __init__(self, base_path):
        _base = Path(base_path)

        # Ensure directory
        if _base.is_file():
            _base = _base.parent

        self._root = Path(str(_base.resolve().absolute()))
        self._assests = {}

    def __getattr__(self, name):
        return self._assests.get(name)

    def _to_path(self, file_path):
        _input_file = Path(file_path)
        if _input_file.is_absolute():
            return str(_input_file.resolve().absolute())

        return str(self._root.joinpath(file_path).resolve().absolute())

    def base64(self, key, file_path=None):
        if file_path is None:
            file_path, key = key, file_path

        data = to_base64(self._to_path(file_path))

        if key is not None:
            self._assests[key] = data

        return data

    def url(self, key, file_path):
        if file_path is None:
            file_path, key = key, file_path

        data = to_url(self._to_path(file_path))

        if key is not None:
            self._assests[key] = data

        return data

    def txt(self, key, file_path):
        if file_path is None:
            file_path, key = key, file_path

        data = to_txt(self._to_path(file_path))

        if key is not None:
            self._assests[key] = data

        return data

    @property
    def assets(self):
        return self._assests

    def get_assets(self, *keys):
        if len(keys) == 0:
            return self.assets

        _assets = {}
        for key in keys:
            _assets[key] = self._assests.get(key)

        return _assets
