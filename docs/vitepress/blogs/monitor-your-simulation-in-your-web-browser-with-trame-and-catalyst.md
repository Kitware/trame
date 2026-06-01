[post](https://www.kitware.com/monitor-your-simulation-in-your-web-browser-with-trame-and-catalyst/)

# Monitor your Simulation in your Web Browser with trame and Catalyst

May 29, 2026

[Corentin Munoz](https://www.kitware.com/author/corentin-munoz/ "Posts by Corentin Munoz")

![trame-catalyst demo](https://www.kitware.com/main/wp-content/uploads/2026/05/image2.gif)

Live visualizing simulation data can be difficult and costly: the data needs to be saved to disk periodically to be analyzed in order to create meaningful images. What if you wanted to monitor your simulation across multiple devices without installing anything locally? What if you wanted to do all of that without spending hours saving simulation data on the disk? Let’s see how it can be done using Kitware’s technologies.

[Trame](https://kitware.github.io/trame/) is a Python framework for creating web applications with a few lines of code. A wide variety of trame widgets enables you to create rich interfaces. For instance, the trame-vtk module can be used to integrate ParaView using remote rendering.

[Catalyst](https://catalyst-in-situ.readthedocs.io/en/latest/index.html) is an In-situ framework that allows you to perform analysis and visualization during a simulation, without suffering from any I/O bottleneck. Its main implementation, [ParaView-Catalyst](https://docs.paraview.org/en/latest/Catalyst/), lets developers visualize and analyze simulation data on every time step using ParaView’s rich collection of filters. You can learn more about ParaView-Catalyst in [this guide](https://kitware.github.io/paraview-catalyst/guide/concepts.html).

![Using Catalyst, the analysis is done after each simulation step, without needing to save the whole simulation data on the disk. The analysis step can output data on the disk every time step, every n time steps, or based on a condition.](https://www.kitware.com/main/wp-content/uploads/2026/05/trame-catalyst-1.jpg)
<p align="center">Using Catalyst, the analysis is done after each simulation step, without needing to save the whole simulation data on the disk. The analysis step can output data on the disk every time step, every n time steps, or based on a condition.</p>

Meet [trame-catalyst](https://gitlab.kitware.com/keu-public/trame-catalyst-demo), a trame application for live visualizing simulation data sent through Catalyst. It can be a good alternative to the ParaView Catalyst live client. In fact, it features a simpler interface, as you can only see the raw data. Since this is a web app, it doesn’t require any client-side installation (other than a web browser), and multiple people can view the results simultaneously. What’s more, it uses remote rendering, so you can easily monitor your simulation from any device, without needing a powerful GPU on each client.

![With trame-catalyst, the client lives in the browser.](https://www.kitware.com/main/wp-content/uploads/2026/05/trame-catalyst-2.jpg)
<p align="center">With trame-catalyst, the client lives in the browser.</p>

## Showcase

This app features a full screen ParaView remote view where the simulation data can be shown. On the left, you can find some information about the simulation (connection status, current time step) and play/pause, connect/disconnect, and reset camera buttons. When connected to a simulation, the simulation channels are listed on the right side, with combo boxes to adjust the representation and the color array.

Let’s try it out with two different simulations:

The first simulation is a toy particle simulation that [you can find here](https://gitlab.kitware.com/keu-public/catalyst/simulator). Simply launch the trame-catalyst app, and then launch the simulation. The application will automatically pause the simulation when it connects.

<iframe loading="lazy" title="Toy Particle Simulation" width="500" height="281" src="https://www.youtube.com/embed/MQn_bkZNahA?feature=oembed" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

The second simulation is an example taken from the [ParaView Catalyst examples repository](https://gitlab.kitware.com/paraview/catalyst-examples/-/tree/master/ParaView/PythonImageData) and integrated into the trame-catalyst demo repository.

<iframe loading="lazy" title="Example taken from the ParaView Catalyst examples repository" width="500" height="281" src="https://www.youtube.com/embed/TehUkXQjpzE?feature=oembed" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Try it yourself

You can try trame-catalyst with your own simulation by downloading the app from [its repository](https://gitlab.kitware.com/keu-public/trame-catalyst-demo)!

Launch the application using PVPython from a [ParaView release](https://www.paraview.org/download/):

```shell
# Create venv
uv sync

# Launch the application
/path/to/paraview/bin/pvpython --venv .venv src/trame_catalyst_demo/app/main.py
```

In parallel, you can launch any simulation that uses Catalyst. If you don’t have any, you can launch the example included in this repository. To run the simulation, you’ll need to build Catalyst with the `CATALYST_WRAP_PYTHON=ON` CMake option.

```shell
# Download the extra python modules needed to run the simulation
uv sync --extra simulation

# Setup environment variables for the simulation
export CATALYST_IMPLEMENTATION_PATHS=/path/to/paraview/lib/catalyst
export PYTHONPATH=/path/to/catalyst/lib/python3.14/site-packages/

# Launch the example simulation
uv run src/trame_catalyst_demo/example/fedriver.py src/trame_catalyst_demo/example/pipeline.py
```

The app will automatically pause the simulation when it is connected. You can unpause it using the play/pause button.

## Conclusion

Although this application can be used as-is, its main purpose is to demonstrate that visualizing simulation data live on the web is very easy with ParaView, Catalyst, and trame.

Looking to take your application to new heights? [Contact our team](https://www.kitware.com/contact/) of experts for development and support services, and fast-track your success with trame.

Tags:

[Catalyst](https://www.kitware.com/tag/catalyst/) | [In Situ](https://www.kitware.com/tag/in-situ/) | [ParaView Catalyst](https://www.kitware.com/tag/paraview-catalyst/) | [Simulation Tools](https://www.kitware.com/tag/simulation-tools/) | [Trame](https://www.kitware.com/tag/trame/) | [Web Visualization](https://www.kitware.com/tag/web-visualization/)
