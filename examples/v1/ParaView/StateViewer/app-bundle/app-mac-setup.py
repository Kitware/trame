from setuptools import setup

ENTRY_POINT = ["PVStateViewer.py"]
DATA_FILES = []

OPTIONS = {
    "argv_emulation": False,
    "strip": True,
    "includes": ["WebKit", "Foundation"],
}

setup(
    app=ENTRY_POINT,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
