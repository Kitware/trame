from __future__ import annotations


class ClientFile:
    """
    Helper class that make it easier to handle file from the trame state

    This class behave like a decorator to the state variable so you can easily access its various properties and content.
    """

    def __init__(self: ClientFile, file_state_variable: dict | None = None) -> None:
        """Pass the state variable you want to decorate as arg"""
        self._name = None
        self._size = None
        self._time = None
        self._mime_type = None
        self._content = None
        if file_state_variable is not None:
            self._name = file_state_variable.get("name")
            self._size = file_state_variable.get("size")
            self._time = file_state_variable.get("lastModified")
            self._mime_type = file_state_variable.get("type")
            self._content = file_state_variable.get("content")
            if isinstance(self._content, list):
                self._content = b"".join(self._content)

    @property
    def is_empty(self: ClientFile) -> bool:
        """Return true if the file is empty"""
        return self._content is None

    @property
    def name(self: ClientFile) -> str | None:
        """File name"""
        return self._name

    @property
    def size(self: ClientFile) -> int | None:
        """File size in Bytes"""
        return self._size

    @property
    def modified_time(self: ClientFile) -> int | None:
        """Modified time"""
        return self._time

    @property
    def mime_type(self: ClientFile) -> str | None:
        """Mime type of the file"""
        return self._mime_type

    @property
    def content(self: ClientFile) -> bytes | None:
        """Bytes content of the file"""
        return self._content

    @property
    def info(self: ClientFile) -> str:
        """Return a string summarizing the file information"""
        return f"File: {self.name} of size {self.size} and type {self.mime_type}"
