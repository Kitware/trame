import inspect
import os

BASE_DIRECTORY = None


def base_directory():
    global BASE_DIRECTORY
    if BASE_DIRECTORY:
        return BASE_DIRECTORY

    frame = inspect.stack()[2]
    module = inspect.getmodule(frame[0])
    if module is None:
        BASE_DIRECTORY = os.getcwd()
    else:
        BASE_DIRECTORY = os.path.abspath(os.path.dirname(module.__file__))
    return BASE_DIRECTORY
