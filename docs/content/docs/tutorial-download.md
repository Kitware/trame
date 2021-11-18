## Download ***trame***

```
git clone https://github.com/Kitware/trame-tutorial.git
```

There is now a directory called ***trame-tutorial*** with the following file structure:

```
$ tree .
.
└── trame-tutorial
    ├── README.md
    ├── presentation.pdf
    ├── trame-tutorial.pdf
    ├── 00_setup
    │   └── app.py
    ├── 01_vtk
    │   ├── app_cone.py
    │   ├── app_flow.py
    │   ├── solution_cone.py
    │   ├── solution_flow.py
    │   └── solution_ray_cast.py
    ├── 02_layouts
    │   ├── app_cone.py
    │   ├── solution_FullScreenPage.py
    │   ├── solution_SinglePage.py
    │   └── solution_SinglePageWithDrawer.py
    ├── 03_html
    │   ├── app_cone.py
    │   ├── solution_buttons_a.py
    │   ├── solution_buttons_b.py
    │   └── solution_final.py
    ├── 04_application
    │   ├── app.py
    │   └── solution.py
    ├── 05_paraview
    │   ├── SimpleCone.py
    │   └── StateLoader.py
    └── data
        ├── carotid.vtk
        ├── disk_out_ref.vtu
        ├── ironProt.vtk
        ├── pv-state-diskout.pvsm
        └── pv-state.pvsm

8 directories, 26 files
```

In the following steps of the tutorial we will assume to be inside the `trame-tutorial` root directory.