import base64
from pathlib import Path

from trame.app.mimetypes import to_mime


def to_txt(full_path):
    """
    Return the text content of the file path

    :param file_path: Path to the file to read
    :type file_path: str

    :return: File content
    :rtype: str
    """
    with open(full_path) as txt_file:
        return str(txt_file.read())


def to_base64(full_path):
    """
    Return the base64 content of the file path

    :param file_path: Path to the file to read
    :type file_path: str

    :return: File content encoded in base64
    :rtype: str
    """
    with open(full_path, "rb") as bin_file:
        return base64.b64encode(bin_file.read()).decode("ascii")


def to_url(full_path):
    """
    Return the base64 encoded URL of the file path

    :param file_path: Path to the file to read
    :type file_path: str

    :return: Inlined bas64 encoded url (data:{mime};base64,{content})
    :rtype: str
    """
    encoded = to_base64(full_path)
    mime = to_mime(full_path)
    return f"data:{mime};base64,{encoded}"


class LocalFileManager:
    """LocalFileManager provide convenient methods for handling local files"""

    def __init__(self, base_path):
        """
        Provide the base path on which relative path should be based on.

        :param base_path: A file or directory path
        :type base_path: str
        """
        _base = Path(base_path)

        # Ensure directory
        if _base.is_file():
            _base = _base.parent

        self._root = Path(str(_base.resolve().absolute()))
        self._assests = {}

    def __getitem__(self, name):
        return self._assests.get(name)

    def __getattr__(self, name):
        return self._assests.get(name)

    def _to_path(self, file_path):
        _input_file = Path(file_path)
        if _input_file.is_absolute():
            return str(_input_file.resolve().absolute())

        return str(self._root.joinpath(file_path).resolve().absolute())

    def base64(self, key, file_path=None):
        """
        Store a base64 file content under the provided key name

        :param key: name for that content which can then be accessed
                    by the [] or . notation
        :type key: str

        :param file_path: A file or directory path
        :type file_path: str

        :return: Return the stored content
        :rtype: str
        """
        if file_path is None:
            file_path, key = key, file_path

        data = to_base64(self._to_path(file_path))

        if key is not None:
            self._assests[key] = data

        return data

    def url(self, key, file_path):
        """
        Store a url encoded file content under the provided key name

        :param key: name for that content which can then be accessed
                    by the [] or . notation
        :type key: str

        :param file_path: A file or directory path
        :type file_path: str

        :return: Return the stored content
        :rtype: str
        """
        if file_path is None:
            file_path, key = key, file_path

        data = to_url(self._to_path(file_path))

        if key is not None:
            self._assests[key] = data

        return data

    def txt(self, key, file_path):
        """
        Store a file content (text) under the provided key name

        :param key: name for that content which can then be accessed
                    by the [] or . notation
        :type key: str

        :param file_path: A file or directory path
        :type file_path: str

        :return: Return the stored content
        :rtype: str
        """
        if file_path is None:
            file_path, key = key, file_path

        data = to_txt(self._to_path(file_path))

        if key is not None:
            self._assests[key] = data

        return data

    @property
    def assets(self):
        """Return the full set of assets as a dict"""
        return self._assests

    def get_assets(self, *keys):
        """Return a filtered out dict using the provided set of keys"""
        if len(keys) == 0:
            return self.assets

        _assets = {}
        for key in keys:
            _assets[key] = self._assests.get(key)

        return _assets


__all__ = [
    "LocalFileManager",
    "to_mime",
    "to_txt",
    "to_base64",
    "to_url",
]
