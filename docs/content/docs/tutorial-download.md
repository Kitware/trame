## Download ***trame***

```
git clone https://github.com/Kitware/trame-tutorial.git
```

There is now a directory called ***trame-tutorial*** with the following file structure:

```
$ tree .
.
└── trame-tutorial
    ├── 00_setup
    │   └── app.py
    ├── 01_vtk
    │   ├── CarotidFlow.py
    │   ├── README.md
    │   ├── SimpleRayCast.py
    │   └── app.py
    ├── 02_layouts
    │   ├── FullScreenPage-app.py
    │   ├── SinglePage-app.py
    │   └── SinglePageWithDrawer-app.py
    ├── 03_html
    │   ├── app-callback.py
    │   ├── app-with.py
    │   └── app.py
    ├── 04_application
    │   ├── __pycache__
    │   │   └── app.cpython-39.pyc
    │   └── app.py
    ├── 05_paraview
    │   ├── SimpleCone.py
    │   └── StateLoader.py
    ├── README.md
    └── data
        ├── carotid.vtk
        ├── disk_out_ref.vtu
        ├── ironProt.vtk
        └── pv-state.pvsm

9 directories, 21 files
```

In the following steps of the tutorial we will assume to be inside the `trame-tutorial` root directory.