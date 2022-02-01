import os
from urllib.error import HTTPError
from urllib.request import urlretrieve


class RemoteFile:
    def __init__(self, local_path=None, remote_url=None, local_base=None):
        self._url = remote_url
        # setup base path
        self._base = os.getcwd()
        if local_base is not None:
            if os.path.exists(local_base):
                if os.path.isfile(local_base):
                    self._base = os.path.abspath(os.path.dirname(local_base))
                else:
                    self._base = os.path.abspath(local_base)
            else:
                self._base = os.path.abspath(local_base)

        # setup local path
        self._file_path = local_path
        if not os.path.isabs(local_path):
            self._file_path = os.path.abspath(os.path.join(self._base, local_path))

        # Make sure target directory exists
        parent_dir = os.path.dirname(self._file_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

    @property
    def local(self):
        return os.path.exists(self._file_path)

    def fetch(self):
        try:
            print(f"Downloading:\n - {self._url}\n - to {self._file_path}")
            urlretrieve(self._url, self._file_path)
        except HTTPError as e:
            print(RuntimeError(f"Failed to download {self._url}. {e.reason}"))

    @property
    def path(self):
        if not self.local:
            self.fetch()

        return self._file_path
