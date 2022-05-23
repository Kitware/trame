# -*- coding: utf-8 -*-
"""Set up sys.path to include ParaView, if available

This checks the TRAME_PARAVIEW environment variable and the --paraview
argument in sys.argv. The specified path will then be automatically
searched for the python library directory and, if found, it will be
added to the sys.path so that the ParaView libraries may be imported.

To use: specify one of the following, and then import this file:
 - `--paraview /path/to/paraview/release` argument
 - environment variable `TRAME_PARAVIEW=/path/to/paraview/release`
"""
import os
import platform
import sys

from . import utils

PV_LOADED = False

PV_HOME = utils.find_env_setting("--paraview", "TRAME_PARAVIEW")

RAISE_ERRORS = os.getenv("TRAME_PARAVIEW_FAIL_SILENTLY") is None

if PV_HOME is None and RAISE_ERRORS:
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


def windows_paths():
    return ["bin/Lib/site-packages"]


search_paths_dict = {
    "Linux": linux_paths,
    "Windows": windows_paths,
}

if PV_HOME:
    if platform.system() == "Darwin":
        env_paths = {
            "PYTHONPATH": ["Contents/Python"],
            "DYLD_LIBRARY_PATH": ["Contents/Libraries"],
        }
        utils.rerun(PV_HOME, env_paths, ["PV_VENV", "VTK_VENV"])
    else:
        PV_LOADED = utils.prepend_python_path(PV_HOME, search_paths_dict)
        if not PV_LOADED and RAISE_ERRORS:
            raise Exception(f"Failed to add paraview python libraries at {PV_HOME}")
