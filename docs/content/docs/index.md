# Trame

Trame is available on PyPI and conda-forge. Its documentation include a [tutorial](https://kitware.github.io/trame/docs/tutorial.html), a [2h course](https://kitware.github.io/trame/docs/course_intro.html), [API](https://trame.readthedocs.io/en/latest/), [many examples](https://kitware.github.io/trame/#examples) along with various guides on the [main documentation page](https://kitware.github.io/trame/docs/).

## Overview

Trame is an open-source platform for creating interactive and powerful visual analytics applications. Based on Python, and leveraging platforms such as VTK, ParaView, and Vega, it is possible to create web-based applications in minutes.

## What is Trame

Trame is a Python integration framework to easily build web applications with minimal knowledge of web development or technology. Before trame, building such applications typically required a full-stack developer at least a day. Now any Python developer can build applications in minutes.

![trame](/trame/images/tutorial-carotid.jpg)


## Why Trame

There are variety of tools and frameworks available for building web applications, but very few are capable of providing interactive 3D visualization.  Trame does this by leveraging VTK and/or ParaView (as well as integrating other tools such as Vega). Trame is the culmination of decades of work: VTK/ParaView, ParaViewWeb, and vtk.js are just some of the components that trame builds upon, but does so in such a way as to hide the complexity of these underlying systems. For example, by using vtk.js and JavaScript it is possible to build powerful web applications, but this requires significant web-development knowledge. But with trame, the full power of frameworks such as VTK/ParaView are available without the burden of web development.

* Open-source - You can confidently build, deploy, and commercialize applications without the usual hassles associated with proprietary systems, and with the knowledge that trame will not disappear - it is not tied to the fortunes of any proprietary vendor.
* All-in-one platform - Unlike other libraries or platforms, trame comes with most all the components you need to build visualization analytics applications; and if a capability is missing it can easily be added.
* Design - Trame apps look beautiful out of the box. Our built-in Material Design widget library enables you to create beautiful desktop-like GUI components.
* Real apps - With Trame, you get high-performing interactive applications that can operate locally, or across the web.

## How Trame works

Building apps with Trame is this simple:

1. **Install trame** - Create a Python virtual environment and `pip install trame`. Once working locally, deploy it using Docker or as Desktop app bundle.
2. **Business logic** - Create your processing functions in plain Python and the **state** that needs to be shared with the UI.
3. **State reactivity** - Define methods which respond to state change (e.g. a slider changing a sampling parameter).
4. **Design your UI** - Build beautiful, accessible user interfaces by defining the layout of your application and connecting your **state** and **functions** to your UI elements directly.
5. **Run it anywhere** - Once working, you can choose to run it locally as a desktop or client/server application, or deploy it in the cloud and use it as a service.

![trame](/trame/images/trame-architecture.jpg)

At the end of the day, building a trame application is just a matter of orchestrating the various pieces in a convenient and transparent manner thanks to the trame shared state, and associated controller for dealing with event management.

## Getting started

The best way to get familiar with trame is to follow the [tutorial](https://kitware.github.io/trame/docs/tutorial.html), or use the [Cookie Cutter](https://github.com/Kitware/trame-cookiecutter) template to build a new application.

Also check out the demonstrative example [CheatSheet](./cheatsheet.html), and short [getting started guide](./getting_started.html).
