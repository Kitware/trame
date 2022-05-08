import os
from setuptools import setup

ENTRY_POINT = ["Cone.py"]
DATA_FILES = []

OPTIONS = {
    "argv_emulation": False,
    "strip": True,
    "iconfile": "trame.icns",
    "includes": ["WebKit", "Foundation"],
}

setup(
    app=ENTRY_POINT,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
