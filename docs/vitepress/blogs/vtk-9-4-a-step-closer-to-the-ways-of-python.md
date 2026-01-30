[post](https://www.kitware.com/vtk-9-4-a-step-closer-to-the-ways-of-python/)

# VTK 9.4: A Step Closer to the Ways of Python

October 29, 2024

[Jaswant Panchumarti](https://www.kitware.com/author/jaswant-panchumarti/ "Posts by Jaswant Panchumarti"), [Berk Geveci](https://www.kitware.com/author/berk-geveci/ "Posts by Berk Geveci") and [Sebastien Jourdain](https://www.kitware.com/author/sebastien-jourdain/ "Posts by Sebastien Jourdain")

![](https://www.kitware.com/main/wp-content/uploads/2024/10/Screenshot-2024-10-18-at-16.35.59.png)

The Visualization Toolkit (VTK) is a widely used open-source solution for desktop post-processing analysis. Even though the library is written in C++, its sophisticated wrapping infrastructure allows developers to build entire visualization applications in Python and Java.

Until recently, the python wrapper naively exposed the C++ functions to Python. For example, a C++ member function `vtkRenderWindow::SetSize` got wrapped into the python member function `SetSize`. While that is uninspiring for many, it was already challenging to get to that point. Recall that python wrapping in VTK was developed long before [pybind11](https://github.com/pybind/pybind11) existed. David Gobbi from the University of Calgary, Prabhu Ramachandran from IIT Bombay and Ken Martin formerly at Kitware contributed extensively to the the wrapper subsystems and provided implementations for the Python wrappers. Over the years, the wrapper subsystem was extended to include more capabilities for developer convenience. One of the feature David added for VTK 9.3 was the introduction of interface files (.pyi) that PyCharm and other development tools use to provide more information, such as PEP 484 type hints.

Starting with the upcoming 9.4 release, Jaswant’s extension to the wrapper subsystem enables access to properties of a VTK object in a pythonic style, initialization of VTK objects through specifying keyword arguments in the constructor, and finally, a convenient syntax to connect VTK algorithms and data objects and reuse the resulting pipelines with different inputs.

## Class properties

Many classes in VTK rely on C++ macros to describe properties for generating setters and getters methods with the proper checks. For instance, the code snippet below comes from `vtkConeSource.h`.

```
vtkSetClampMacro(Height, double, 0.0, VTK_DOUBLE_MAX);
vtkGetMacro(Height, double);

vtkSetClampMacro(Radius, double, 0.0, VTK_DOUBLE_MAX);
vtkGetMacro(Radius, double);

vtkSetClampMacro(Resolution, int, 0, VTK_CELL_SIZE);
vtkGetMacro(Resolution, int);

vtkSetVector3Macro(Center, double);
vtkGetVectorMacro(Center, double, 3);

vtkSetVector3Macro(Direction, double);
vtkGetVectorMacro(Direction, double, 3);

vtkSetMacro(Capping, vtkTypeBool);
vtkGetMacro(Capping, vtkTypeBool);
vtkBooleanMacro(Capping, vtkTypeBool);
```

In Python, you could make use of those methods as described below.

```
import vtk

cone_source = vtk.vtkConeSource()

cone_source.SetHeight(12)
cone_source.SetRadius(0.9)
cone_source.SetResolution(60)
cone_source.SetCenter(0, 0, 0)
cone_source.SetDirection(1, 1, 1)
cone_source.SetCapping(False)
cone_source.SetOutputPointsPrecision(vtk.vtkAlgorithm.SINGLE_PRECISION)

print(cone_source.GetDirection())
```

As you can see that is not what you could expect from a Python library. Therefore, we made our wrapper generate Python properties to enable the following syntax.

```
import vtk

cone_source = vtk.vtkConeSource()

cone_source.height = 12
cone_source.radius = 0.9
cone_source.resolution = 60
cone_source.center = (0, 0, 0)
cone_source.direction = (1, 1, 1)
cone_source.capping = False
cone_source.output_points_precision = vtk.vtkAlgorithm.SINGLE_PRECISION

print(cone_source.direction)
```

Those properties internally forward the calls to the Getter and Setter methods of the C++ layer, resulting in a code that is much more Pythonic.

## Constructor parameters

VTK by design does not support parameters in the constructor. However, due to a greater control over the generation of the wrappers, VTK is able to intercept the keyword arguments used in a constructor and map them to the class properties, enabling us to rewrite the previous snippet of code in a much more compact way as shown below.

```
import vtk

cone_source = vtk.vtkConeSource(
  height = 12,
  radius = 0.9,
  resolution = 60,
  center = (0, 0, 0),
  direction = (1, 1, 1),
  capping = False,
)

print(cone_source.direction)
```

## VTK Pipeline

One of the foundations of VTK is its pipeline. The VTK pipeline lets you connect data sources and filters in a way that the data will automatically flow across filters when something changes on any filter or source.

Let’s explore the following example that generates a sphere and positions a cone at the center of each cell on the sphere, aligned with the face normal.

```
sphere_source = vtk.vtkSphereSource(
    theta_resolution=16,
    phi_resolution=16,
)

cone_source = vtk.vtkConeSource(
    radius=0.1,
    height=0.2,
    resolution=30,
)

normals = vtk.vtkPolyDataNormals(
    compute_cell_normals = 1,
    input_connection = sphere_source.output_port,
)

cell_centers = vtk.vtkCellCenters(
    input_connection=normals.output_port,
)

glyph_filter = vtk.vtkGlyph3D(
    orient = True,
    vector_mode = 1, # Normals
    input_connection = cell_centers.output_port,
    source_connection = cone_source.output_port,
)
```

We see some benefit with the new property syntax but we can still do better. Now let’s see how that can be written using the new pipeline syntax.

```
sphere_source = vtk.vtkSphereSource(
    theta_resolution=16,
    phi_resolution=16,
)

cone_source = vtk.vtkConeSource(
    radius=0.1,
    height=0.2,
    resolution=30,
)

glyph_filter = vtk.vtkGlyph3D(
    source_connection=cone_source.output_port,
    orient=True,
    vector_mode=1,  # normals
)

pipeline = (
    sphere_source
    >> vtk.vtkPolyDataNormals(compute_cell_normals=1)
    >> vtk.vtkCellCenters()
    >> glyph_filter
)
```

Thanks to that new syntax, the code can be compact and inlined with the Python philosophy of simplicity. Additional information on that new syntax is also available on that [vtk examples website page](https://examples.vtk.org/site/PythonicAPIComments/).

Now lets see how we could turn that VTK code into an interactive solution with trame.

## Usage example with trame

Trame lets you create an interactive user interface in pure Python. Now let’s explore the current pipeline example and see how we can turn it into an interactive visualization. Using the previously described example we made a trame application that can be found [here](https://github.com/Kitware/trame/blob/master/examples/blogs/vtk-9.4/pipeline.py).

To setup your environment and run the example, you can use a Python environment like described below.

```
python3 -m venv .venv
source .venv/bin/activate
pip install trame trame-vtk trame-vuetify
pip install "vtk>=9.4.0rc2" --extra-index-url https://wheels.vtk.org

# Fetch demo code
curl -O https://raw.githubusercontent.com/Kitware/trame/refs/heads/master/examples/blogs/vtk-9.4/pipeline.py

# Run example
python ./pipeline.py
```

At that point, a browser window should appear with the following application.

![](https://www.kitware.com/main/wp-content/uploads/2024/10/Screenshot-2024-10-18-at-16.35.59-1024x915.png)

The application leverages its reactive nature to implement two methods that automatically modify the cone or the sphere source, compute statistics on the newly generated mesh, and update the view.

Below we are only showing one method to illustrate the benefit of the new syntax.

```
@change("cone_resolution", "cone_height", "cone_radius")
def update_cone(self, cone_resolution, cone_height, cone_radius, **_):
    # Update source
    self.cone.resolution = cone_resolution
    self.cone.height = cone_height
    self.cone.radius = cone_radius

    # Execute filter for output extraction
    cone_dataset = self.cone()
    output_dataset = self.pipeline()

    # Update UI with new statistics
    self.state.update(
        {
            "cone_points": cone_dataset.number_of_points,
            "cone_cells": cone_dataset.number_of_cells,
            "total_points": output_dataset.number_of_points,
            "total_cells": output_dataset.number_of_cells,
        }
    )

    # Update 3D view
    self.ctrl.view_update()
```

And the user interface definition is captured in the method below to also illustrate how trame can efficiently be used for creating an interactive graphical user environment.

```
def _build_ui(self):
    with VAppLayout(self.server, fill_height=True) as self.ui:
        with v3.VCard(
            style="z-index: 1;",
            classes="position-absolute w-33 top-0 left-0 ma-4",
        ):
            # Sphere
            TitleWithStatistic("sphere", "Sphere", 4)
            v3.VDivider()
            with v3.VCardText():
                create_slider("Resolution", "sphere_resolution", 16, 8, 32, 1)

            # Cone
            v3.VDivider()
            TitleWithStatistic("cone", "Cone", 3)
            v3.VDivider()
            with v3.VCardText():
                create_slider("Resolution", "cone_resolution", 30, 3, 24, 1)
                create_slider("Height", "cone_height", 0.2, 0.01, 0.5, 0.01)
                create_slider("Radius", "cone_radius", 0.1, 0.01, 0.2, 0.01)

            # Result
            v3.VDivider()
            TitleWithStatistic("total", "Result", 5)

        with vtk_widgets.VtkRemoteView(self.rw, interactive_ratio=1) as view:
            self.ctrl.view_update = view.update
            self.ctrl.view_reset_camera = view.reset_camera
```

But as always with OpenSource, you can look at the full code which is available [here](https://github.com/Kitware/trame/blob/master/examples/blogs/vtk-9.4/pipeline.py).

## Support and Services

Looking to take your application to new heights? [Get in touch](https://www.kitware.com/contact/) with Kitware for expert development and support services to fast-track your success with Kitware's open source frameworks.

  <!-- Icon/link tiles -->
<table>
  <tr>
    <td align="center" width="33%">
      <img src="https://www.kitware.com/main/wp-content/uploads/2021/11/icon_collaboration.svg" width="50"><br>
      <strong><a href="https://www.kitware.com/training/">Training</a></strong><br>
      <small>Learn how to confidently use and customize 3D Slicer from the expert developers at Kitware.</small>
    </td>
    <td align="center" width="33%">
      <img src="https://www.kitware.com/main/wp-content/uploads/2021/12/icon_research_develop.svg" width="50"><br>
      <strong><a href="https://www.kitware.com/support/">Support</a></strong><br>
      <small>Our experts can assist your team as you build your application and establish in-house expertise.</small>
    </td>
    <td align="center" width="33%">
      <img src="https://www.kitware.com/main/wp-content/uploads/2021/11/icon_custom_software.svg" width="50"><br>
      <strong><a href="https://www.kitware.com/contact">Custom Development</a></strong><br>
      <small>Leverage Kitware's 25+ years of experience to quickly build your application.</small>
    </td>
  </tr>
</table>

## Acknowledgment

This work is partially funded by the US Department of Energy’s Office of Biological and Environmental Research (BER) to develop Pan3D, an open-source toolkit supporting scalable and reproducible scientific workflows for 3D data analytics (DE-SC0022365). The project is led by Aashish Chaudhary, the Principal Investigator (PI), with John Tourtellot as the technical lead, who contributed to this work through their leadership and vision of further improving VTK to support complex 3D workflows.

Tags:

[Python](https://www.kitware.com/tag/python/) | [Trame](https://www.kitware.com/tag/trame/) | [VTK](https://www.kitware.com/tag/vtk/)
