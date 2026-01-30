[post](https://www.kitware.com/exposing-web-application-with-paraview-5-13-is-getting-simpler/)

# Exposing Web applications with ParaView 5.13 is getting simpler

September 3, 2024

[Sebastien Jourdain](https://www.kitware.com/author/sebastien-jourdain/ "Posts by Sebastien Jourdain") and [Cory Quammen](https://www.kitware.com/author/cory-quammen/ "Posts by Cory Quammen")

![ParaView Trame Components](https://www.kitware.com/main/wp-content/uploads/2024/08/web-app-output.png)

Thanks to the new `--venv` feature of ParaView 5.13, covered in our previous [post](https://www.kitware.com/using-python-virtual-environments-in-paraview-5-13-0/), we now have a simple path to leverage [trame](https://kitware.github.io/trame/) within ParaView.

Trame is a set of Python packages that makes it simple to put ParaView visualization on the web. Because trame development is progressing rapidly, ParaView binary installers do not include it; any version shipped with ParaView would quickly become outdated. Instead, you can use pip as the distribution mechanism to keep trame up to date by combining a ParaView binary release with the new –venv option and a virtual environment with trame dependencies.

## Setting up a trame environment

To create such virtual environment, you can do the following steps:

```
# create environment locally
python3.10 -m venv .venv 

# activate environment
source .venv/bin/activate 

# install a trame package with some demos
pip install paraview-trame-components

# exit environment by deactivating it
deactivate
```

Now that we have a virtual environment setup with some pre-existing trame applications we can start using it within ParaView.

## Parallel visualization with ParaView and trame

The sample code below will use ParaView MPI to show a sphere color coded by the MPI process that owns each part within a web browser. In order to achieve that we will use pvbatch, an MPI-enabled batch-processing Python interpreter distributed as part of the ParaView suite.

```
# mpiexec and pvbatch are coming from the ParaView bundle          
mpiexec -n 4 pvbatch --venv .venv -m ptc.apps.sphere
```

By running this previous command line, a new tab in your web browser will open with the following content.

![](https://www.kitware.com/main/wp-content/uploads/2024/08/Screenshot-2024-08-14-at-15.39.48-1024x777.png)

If you are wondering what code led to that interactive visualization that run in parallel via MPI, you can find it [here](https://github.com/Kitware/paraview-trame-components/blob/main/ptc/apps/sphere.py) but the listing below is also provided for convenience.

```
from paraview import simple
import ptc

sphere = simple.Sphere()
rep = simple.Show(sphere)
view = simple.Render()

simple.ColorBy(rep, ("POINTS", "vtkProcessId"))

rep.RescaleTransferFunctionToDataRange(True, False)
rep.SetScalarBarVisibility(view, True)

web_app = ptc.Viewer(from_state=True)
web_app.start()
```

As you can see from that example, you can easily leverage ParaView parallel capabilities from a simple Python script and drive the visualization from your browser.

## Interactive data processing and visualization

Trame provides endless options on what you can do with it, but let’s explore another simple example with ParaView doing interactive data processing and visualization.

This time we will use pvpython and loads a different example that lets you change an isovalue interactively. And since you already have everything installed, you just need to run the following command.

```
pvpython --venv .venv -m ptc.apps.demo
```

When your local web browser opens, move the slider and you will see the isosurface change like below.

[](https://www.kitware.com/main/wp-content/uploads/2024/08/anim.mov)

While this visualization is not that appealing, look at the code needed to create such interactive data processing web application.

```
from paraview import simple
import ptc

# ParaView code
wavelet = simple.Wavelet()
contour = simple.Contour(Input=wavelet)
contour.ContourBy = ["POINTS", "RTData"]
contour.Isosurfaces = [157.0909652709961]
contour.PointMergeMethod = "Uniform Binning"
rep = simple.Show(contour)
view = simple.Render()

# Trame WebApp code
web_app = ptc.Viewer()

with web_app.side_top:
    ptc.VSlider(
        v_model=("value", contour.Isosurfaces[0]),
        min=37, max=276, step=0.5,
        color="primary", style="margin: 0 100px;",
    )

@web_app.state.change("value")
def on_contour_value_change(value, **kwargs):
    contour.Isosurfaces = [value]
    web_app.update()

web_app.start()
```

## Where to go from there?

Now that ParaView is able to extend its Python with any external virtual environment, you can easily create bespoke solutions with trame and share the result more easily with anyone. Such applications can come from an external package like the one we use throughout that blog but it can also be a simple standalone file.

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

Tags:

[ParaView](https://www.kitware.com/tag/paraview/) | [Python](https://www.kitware.com/tag/python/) | [Scientific Computing](https://www.kitware.com/tag/scientific-computing/) | [Trame](https://www.kitware.com/tag/trame/)

