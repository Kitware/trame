import os
from urllib.error import HTTPError
from urllib.request import urlretrieve


def download_file_from_google_drive(id, destination):
    import requests

    URL = "https://docs.google.com/uc"

    session = requests.Session()
    response = session.get(
        URL, params={"id": id, "confirm": "t", "export": "download"}, stream=True
    )
    token = get_confirm_token(response)

    if token:
        params = {"id": id, "confirm": token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


class AbstractRemoteFile:
    """
    AbstractRemoteFile provide infrastructure for RemoteFile where
    only the method fetch() needs to be defined for a concreate implementation.
    """

    def __init__(self, local_path=None, local_base=None):
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
        """Return true if the file is available locally on the File System"""
        return os.path.exists(self._file_path)

    def fetch(self):
        """Perform the action needed to fetch the content and store it locally"""
        pass

    @property
    def path(self):
        """Return the actual local file path"""
        if not self.local:
            self.fetch()

        return self._file_path


class GoogleDriveFile(AbstractRemoteFile):
    """
    Helper file to manage caching and retrieving of file available on Google Drive
    """

    def __init__(self, local_path=None, google_id=None, local_base=None):
        """
        Provide the information regarding where the file should be located
        and where to fetch it if missing.

        :param local_path: relative or absolute path
        :param google_id: Resource ID from google
        :param local_base: Absolute path when local_path is relative
        """
        super().__init__(local_path, local_base)
        self._gid = google_id

    def fetch(self):
        try:
            print(f"Downloading:\n - {self._gid}\n - to {self._file_path}")
            download_file_from_google_drive(self._gid, self._file_path)
        except HTTPError as e:
            print(RuntimeError(f"Failed to download {self._gid}. {e.reason}"))


class HttpFile(AbstractRemoteFile):
    """
    Helper file to manage caching and retrieving of file available on HTTP servers
    """

    def __init__(self, local_path=None, remote_url=None, local_base=None):
        """
        Provide the information regarding where the file should be located
        and where to fetch it if missing.

        :param local_path: relative or absolute path
        :param remote_url: http(s):// url to fetch the file from
        :param local_base: Absolute path when local_path is relative
        """
        super().__init__(local_path, local_base)
        self._url = remote_url

    def fetch(self):
        try:
            print(f"Downloading:\n - {self._url}\n - to {self._file_path}")
            urlretrieve(self._url, self._file_path)
        except HTTPError as e:
            print(RuntimeError(f"Failed to download {self._url}. {e.reason}"))


__all__ = [
    "AbstractRemoteFile",
    "GoogleDriveFile",
    "HttpFile",
]
