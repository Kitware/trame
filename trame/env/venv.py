# -*- coding: utf-8 -*-
"""Activate venv for current interpreter:

Use `import trame.env.venv` along one of the following
 - `--venv /path/to/venv/base` argument
 - environment variable `TRAME_VENV=/path/to/venv/base`

This can be used when you must use an existing Python interpreter, not the venv bin/python.
"""

import os
import site
import sys

VENV_BASE = None
VENV_LOADED = False

if os.environ.get("TRAME_VENV"):
    VENV_BASE = os.path.abspath(os.environ.get("TRAME_VENV"))

if "--venv" in sys.argv:
    VENV_BASE = os.path.abspath(sys.argv[sys.argv.index("--venv") + 1])

if not VENV_LOADED and VENV_BASE and os.path.exists(VENV_BASE):
    VENV_LOADED = True
    # Code inspired by virutal-env::bin/active_this.py
    bin_dir = os.path.join(VENV_BASE, "bin")
    os.environ["PATH"] = os.pathsep.join(
        [bin_dir] + os.environ.get("PATH", "").split(os.pathsep)
    )
    os.environ["VIRTUAL_ENV"] = VENV_BASE
    prev_length = len(sys.path)
    python_libs = os.path.join(
        VENV_BASE,
        f"lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages",
    )
    site.addsitedir(python_libs)
    sys.path[:] = sys.path[prev_length:] + sys.path[0:prev_length]
    sys.real_prefix = sys.prefix
    sys.prefix = VENV_BASE
    #
    print(f"Trame is using venv: {VENV_BASE}")
