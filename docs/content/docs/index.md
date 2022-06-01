# Trame

Trame v2 is out and available via `pip install trame` and therefore the documentation is now reporting the updated API and capabilities. If you were already working with Trame v1 you can look at our [migration guide](./trame_v2_migration.html).

## Overview

Trame is an Open Source platform for creating interactive and capable applications in plain Python in minutes.

## What is Trame

Trame is a Python framework to simply build ubiquitous applications with a web front-end with no knowledge in web development or technology. Before Trame, building any application would require a full-stack developer at least a day. Now any Python developer can be running in less than a couple of minutes.

![trame](/trame/images/tutorial-carotid.jpg)


## Why Trame

There are variety of tools and frameworks available to you when building web applications, but very few are capable of doing interactive 3D visualization in an efficient manner by leveraging VTK or ParaView. VTK/ParaView Web was really the first, then vtk.js also enable Scientific Visualization in plain JavaScript. But with Trame, which is based on VTK/ParaView Web, you get the full power of such framework without the burden of web development.

* Open-source - You can build, deploy and sell your own application with confidence knowing trame will always be around and you won't have any fee or subscription to worry about.
* All-in-one platform - Unlike other libraries or platforms, trame comes with all the components you need and if we are missing anything you can easily add your own simply.
* Design - Trame apps loo beautiful out of the box. Our built-in Material Design widget library let you create beautiful desktop like components.
* Real apps - With Trame, you get hight-performing interactive applications.

## How Trame works

Building apps with Trame has never been that simpple

1. **Install trame** - Create a Python virtual environment and `pip install trame`. Once working locally, deploy it using Docker or as Desktop app bundle.
2. **Business logic** - Create your processing functions in plain Python and the **state** that needs to be shared with the UI.
3. **State reactivity** - Connect any method to react to state change (i.e. slider changing a sampling parameter)
4. **Design your UI** - Build beautiful, accessible user interfaces by defining the layout of your application and connecting your **state** and **functions** to your UI elements directly.
5. **Run it anywhere** - Once working, you can choose to run it locally as a desktop application, as a client/server or deploy it in the cloud and use it as a service.

![trame](/trame/images/trame-architecture.jpg)

At the end of the day, building a trame application is just a matter of orchestrating the various pieces in a convenient and transparent manner thanks to trame shared state and controller for dealing with event management.

## Getting started

The best way to get familiar with trame is by following our [tutorial](https://kitware.github.io/trame/docs/tutorial.html) or use our [Cookie Cutter](https://github.com/Kitware/trame-cookiecutter) when starting your new application.

Also we have some kind of [CheatSheet](./cheatsheet.html) and small [getting started guide](./getting_started.html).
