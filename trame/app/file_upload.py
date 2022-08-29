class ClientFile:
    def __init__(self, file_state_variable=None):
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
    def is_empty(self):
        """Return true if the file is empty"""
        return self._content is None

    @property
    def name(self):
        """File name"""
        return self._name

    @property
    def size(self):
        """File size in Bytes"""
        return self._size

    @property
    def modified_time(self):
        """Modified time"""
        return self._time

    @property
    def mime_type(self):
        """Mime type of the file"""
        return self._mime_type

    @property
    def content(self):
        """Bytes content of the file"""
        return self._content

    @property
    def info(self):
        return f"File: {self.name} of size {self.size} and type {self.mime_type}"
