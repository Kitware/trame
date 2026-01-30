[post](https://www.kitware.com/faster-simpler-python-application-execution-with-uv-and-trame/)

# Faster, simpler Python application execution with uv and trame

June 21, 2025

[Sebastien Jourdain](https://www.kitware.com/author/sebastien-jourdain/ "Posts by Sebastien Jourdain")

![Gray Scott reaction diffusion model using Numpy with VTK and trame](https://www.kitware.com/main/wp-content/uploads/2025/06/grayscott.png)

## Background & Motivation

Trame has revolutionized how we build interactive scientific visualization applications in Python. By enabling developers to create rich graphical interfaces that seamlessly embed VTK/ParaView, Plotly, Matplotlib, and other visualization libraries with just Python scripts, trame has democratized access to powerful visualization tools. However, this convenience comes with a challenge that many trame developers know all too well: dependency management.

Trame applications require Kitware and third party packages. A typical trame project might need VTK/ParaView for 3D rendering, various plotting libraries, web frameworks, and their respective dependencies. This is where uv transforms the trame delivery experience. As Astral (the company behind uv) describes it: [uv](https://github.com/astral-sh/uv) is “*an extremely fast Python package and project manager, written in Rust*“. While uv is incredible at creating virtual environments, it also provides new ways for dealing with applications and python scripts. Check out [their installation page](https://docs.astral.sh/uv/getting-started/installation/) so you can run the examples in this blog post in seconds.

![](https://www.kitware.com/main/wp-content/uploads/2025/06/uv-speed-1024x271.png)

*Installing [Trio](https://trio.readthedocs.io/)‘s dependencies with a warm cache.*

Normally, when dealing with Python dependencies, you rely on virtual environments to run applications or scripts. But what if we could skip the creation and management of virtual environments?

## The uv way

Since uv is so fast at creating virtual environments, it is offering new ways for dealing with scripts and tools. For tools or applications that live on GitHub or PyPI, you can install them globally and execute them from anywhere without risking breaking your system. In other words, uv keeps them isolated from each other.

### Running Applications

Let’s see what it looks like with two example applications we’ve built at Kitware.

For executables that match their package name, you can simply run `uvx app-name` and skip any install step. uv handles the installation and storage for you. As you can imagine, the first execution will be slower, but any follow-up will be faster.

For example, if you run `uvx parsli`, you should get the following

![](https://www.kitware.com/main/wp-content/uploads/2025/06/parsli-web-1024x744.png)

Parsli is a VTK+trame-based viewer for fault system kinematics that enables fast exploration and export of time animation.

And with `uvx multivariate-view`, you will get

![](https://www.kitware.com/main/wp-content/uploads/2025/06/multivariate-view-1024x838.png)

A multivariate/multimodal volume visualizer inspired by RadVolViz that uses VTK and trame to render multi-channel volumetric datasets.

Both applications are available on PyPI and can load local files to perform interactive 3D visualization. But the other cool thing about these applications is that they will download a sample dataset automatically, so that you can play with them before generating any data yourself.

But what about standalone Python scripts with dependencies?

### Running Scripts

Let’s explore what you can do with a script. With uv, you can describe your dependencies as a comment at the top of your Python file. And when doing so, you can run that script with uv.

While it is common practice to deal with local files, uv is smart enough to handle URLs too. In the examples below, I list the URL directly and skip the manual download step. But I would understand if you want to check the file content first!

Running the following command line should start the application below:

```
uv run https://raw.githubusercontent.com/Kitware/trame/refs/heads/master/examples/06_vtk/04_wasm/app.py
```

![](https://www.kitware.com/main/wp-content/uploads/2025/06/bike-uv-1024x774.png)

Trame example using VTK and VTK.wasm for interactive 3D rendering within the browser, while dynamically updating geometry when interacting with the widget.

Or, you can use that other example that was ported from a [vedo](https://vedo.embl.es/) example using plain VTK and trame.

```
uv run https://raw.githubusercontent.com/Kitware/vtk-scene/refs/heads/main/examples/grayscott.py
```

![](https://www.kitware.com/main/wp-content/uploads/2025/06/grayscott-1024x818.png)

Live Gray Scott reaction diffusion model using Numpy with VTK and trame.

While those two scripts are perfect examples for showcasing the power of uv and trame, they are still demos. What about a solution for dealing with real data from a simulation?

The case below, while remaining a simple script, is relying on Pan3D, VTK, Zarr, and Xarray to access a complex hdf5 data format. The file loaded is generated by a simulation code named PFlotran, which is an open source, parallel subsurface transport code developed at Berkeley Laboratory. Since the format can not be directly read by off-the-shelf software, we authored a small Python script to parse the hdf5 structure and generate a “reference file system” that maps it to a virtual Zarr dataset. Thanks to that trick, we were able to leverage Xarray with a Zarr engine to load it. At the end, the application is able to load subsurface data, color it by any available field, perform time animation, and slice it along any axis for exploration. To simply run the application/script, you can execute the following command line.

```
uv run https://raw.githubusercontent.com/Kitware/vtk-scene/refs/heads/main/examples/remote_pflotran.py
```

![](https://www.kitware.com/main/wp-content/uploads/2025/06/pflotran-1024x777.png)

Pan3D-based viewer for subsurface simulation data, using a PFlotran file with Zarr/Xarray to read and VTK to process and render it.

Wondering how to update your script and enable such an easy to use setup? You can read the full documentation on [the uv website](https://docs.astral.sh/uv/guides/scripts/), or you can glance at those scripts and look at the comment section at the top. What’s even nicer is that you can use a shebang to automate it even further on Linux and macOS systems. That just makes your scripts a standalone executable.

If you’d like to try, you can run the following command to grab any previous url and run it locally. The commands below are using a helper file from parsli repository to run the trame application as a desktop user interface.

```
curl -O https://raw.githubusercontent.com/brendanjmeade/parsli/refs/heads/main/parsli
chmod +x parsli
./parsli
```

![](https://www.kitware.com/main/wp-content/uploads/2025/06/parsli-app-1024x782.png)

And the content of that file is just

```
#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "parsli[app]>=1.2.1",
# ]
# ///
from parsli.viewer.core import Viewer
from multiprocessing import freeze_support

if __name__ == "__main__":
    freeze_support()
    app = Viewer()
    app.server.start(exec_mode="desktop")
```

## Conclusion

Between trame and uv, we are reaching a sweet spot for delivering bespoke applications faster and simpler to a wider audience.

Trame is capable of delivering interactive solutions with complex visualization locally, in the cloud, within Jupyter, or on HPC with ParaView. But uv is making the installation and execution of trame applications a breeze.

At Kitware, we thrive at helping researchers, scientists, and industry reach their goals faster. Our expertise in the frameworks we’ve created (i.e. *cmake*, *vtk*, *paraview*, *trame*), data analysis and visualization, and wide domain knowledge across our team enables us to understand your needs and deliver better solutions.

[Reach out](https://www.kitware.com/contact/), so we can figure out how to best help you in your next endeavor.

## References

**Parsli** is an application developed by Kitware for Brendan Meade, a Professor of Earth & Planetary Sciences at Harvard University. Parsli is a lightweight viewer that enables post-processing of simulation results faster than ever before. (https://github.com/brendanjmeade/parsli)

**Multivariate-view** is an application developed by Kitware under DOE SBIR Award DE-SC0024765 titled “Multivariate Volume Visualization and Machine-Guided Exploration in Tomviz”. By using VTK and trame, we were able to expand the research to be impactful not just for nanoscale imaging, but also for other domains, including medical, chemical, and biological imaging. (https://github.com/Kitware/multivariate-view)

**RadVolViz** is an “information display-inspired transfer function editor for multivariate volume visualization” (https://ieeexplore.ieee.org/document/10091196)

**VTK.wasm** is a bundle of VTK that enables users to mirror a VTK scene inside a browser so that it can be interactively explored without any rendering disparity with pure VTK capabilities. Such technology is integrated inside trame to streamline various deployment needs and constraints. (https://kitware.github.io/vtk-wasm/)

**Gray Scott**: is a reaction-diffusion model example from the book “From Python to Numpy” made by Nicolas Rougier, but extended to use VTK with Numpy and trame (https://www.labri.fr/perso/nrougier/from-python-to-numpy/)

**Pan3D** is a DOE-funded Phase II effort that aims to simplify the creation of 3D visual workflows using Python and VTK. Technical objectives include interoperability with PyData ecosystems such as XArray, improved integration of trame with Jupyter, VTK WebAssembly enhancements, and the creation of web-based data explorers using VTK and trame. For more information, visit https://github.com/Kitware/pan3d/

**Kitware** builds and maintains open source solutions. We support our customers in using these tools, including by adapting them to meet specific needs. For more information on working with Kitware, contact us at https://www.kitware.com/contact/

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

[Python](https://www.kitware.com/tag/python/) | [Scientific Computing](https://www.kitware.com/tag/scientific-computing/) | [Trame](https://www.kitware.com/tag/trame/) | [VTK](https://www.kitware.com/tag/vtk/)

