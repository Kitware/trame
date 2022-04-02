"""Set up sys.path to include ParaView, if available

This checks the TRAME_PARAVIEW environment variable and the --paraview
argument in sys.argv. The specified path will then be automatically
searched for the python library directory and, if found, it will be
added to the sys.path so that the ParaView libraries may be imported.

To use: specify one of the following, and then import this file:
 - `--paraview /path/to/paraview/release` argument
 - environment variable `TRAME_PARAVIEW=/path/to/paraview/release`
"""
import platform
import sys

from .utils import prepend_python_path, find_env_setting

PV_LOADED = False

PV_HOME = find_env_setting("--paraview", "TRAME_PARAVIEW")

if PV_HOME is None:
    msg = (
        "trame.env.paraview was imported, but the paraview location was not "
        "defined. Define it with either the argument '--paraview <path>' or "
        "the TRAME_PARAVIEW environment variable"
    )
    raise Exception(msg)


# Each of the following functions returns a list of paths to try
# for the specified OS.
def linux_paths():
    py_major, py_minor = sys.version_info[:2]
    return [f"lib/python{py_major}.{py_minor}/site-packages"]


def mac_paths():
    return ["Contents/Python"]


def windows_paths():
    return ["bin/Lib/site-packages"]


search_paths_dict = {
    "Linux": linux_paths,
    "Darwin": mac_paths,
    "Windows": windows_paths,
}

if platform.system() == "Darwin":
    # We haven't been able to successfully run this on the Mac yet. So warn
    # the user that it might fail.
    print("WARNING: prepending the ParaView environment on Mac has not been "
          "demonstrated to work successfully. It will likely fail.")

PV_LOADED = prepend_python_path(PV_HOME, search_paths_dict)
if not PV_LOADED:
    raise Exception(f"Failed to add paraview python libraries at {PV_HOME}")
