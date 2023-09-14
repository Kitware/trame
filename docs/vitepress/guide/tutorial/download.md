# Download tutorial

```
git clone https://github.com/Kitware/trame-tutorial.git
```

This produces a directory called ***trame-tutorial*** with the following file structure:

```
$ tree .
.
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
│   ├── solution_buttons.py
│   └── solution_final.py
├── 04_application
│   ├── app.py
│   └── solution.py
├── 05_paraview
│   ├── SimpleCone.py
│   └── StateLoader.py
├── README.md
├── data
│   ├── carotid.vtk
│   ├── disk_out_ref.vtu
│   ├── ironProt.vtk
│   ├── pv-state-diskout.pvsm
│   └── pv-state.pvsm
└── presentation.pdf

7 directories, 24 files
```

The remaining tutorial steps assume that the current directory is the `trame-tutorial` root directory.
