import mimetypes


MIMETYPE_OVERRIDES = {
    # On Windows, mimetypes pulls this from the registry, which is
    # wrong. Override it.
    "application/javascript": ".js",
}


def decorate_mimetypes_init():
    """
    Decorate the mimetypes.init() method with our function that
    afterwards adds any mimetype overrides that were saved.
    """

    original_init = mimetypes.init

    def new_init(*args, **kwargs):
        original_init(*args, **kwargs)
        for key, value in MIMETYPE_OVERRIDES.items():
            mimetypes.add_type(key, value)

    mimetypes.init = new_init


def add_mimetype_override(type, ext):
    """
    Add a mimetype both now and when mimetypes.init() is called.

    :param type: mimetype
    :type type: str
    :param ext: file extension for which the mimetype applies
    :type ext: str
    """
    # Add it to the overrides that are performed if init() is called
    MIMETYPE_OVERRIDES[type] = ext

    # Also override it right now
    mimetypes.add_type(type, ext)


def to_mime(file_path):
    """
    Return the mime type from a given path

    :param file_path: Path to analyse
    :type file_path: str

    :return: Mime type
    :rtype: str
    """
    return mimetypes.guess_type(file_path)[0]


# Decorate the mimetypes.init() method
decorate_mimetypes_init()
