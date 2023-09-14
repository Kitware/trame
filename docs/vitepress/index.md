---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: trame
  text: The core of your next Web Application
  tagline: Efficiently building interactive applications
  actions:
    - theme: brand
      text: Getting started
      link: /guide/
    - theme: alt
      text: Support
      link: https://www.kitware.com/contact/

features:
  - title: 3D Visualization (VTK/ParaView)
    icon:
      src: /assets/vtk.c9c12cb3.svg
      alt: Pure Python
    details: With best-in-class platforms at its core, trame provides complete control of 3D visualizations and data processing. Developers benefit from a write-once environment from trame.
    link: https://www.paraview.org/
  - title: Open Source
    icon:
      src: /assets/opensource.8f0bc901.svg
      alt: Pure Python
      width: 22
    details: trame is an open source project licensed under Apache License Version 2.0 which allows users to create open source or commercial applications without any licensing worries.
    link: https://www.kitware.com/open-source/
  - title: Rich Features
    icon:
      src: /assets/python.5aa959ac.svg
      alt: Pure Python
      width: 22
    details: trame leverages existing libraries and tools such as Vuetify, Altair, Vega, deck.gl, VTK, ParaView, and more, to create vivid content for visual analytics applications. Trame can be integrated in any Python environment using PyPI or Conda.
    link: https://pypi.org/project/trame/
  - title: Problem Focused
    icon: 🔍
    details: By relying simply on Python and HTML, trame focuses on one's data and associated analysis and visualizations while hiding the complications of web development.
    link: /examples/
  - title: Desktop, cloud, Jupyter and HPC
    icon:
      src: /assets/jupyter.1a86c226.svg
      alt: Jupyter and more
      width: 40
    details: Trame applications can be deployed on a desktop, in the cloud, within a Jupyter cell or on HPC environments. Trame simply make your application ubiquitous.
    link: /guide/deployment/desktop
  - title: Support and Services
    icon:
      src: /assets/kitware.c9978938.svg
      alt: Kitware Inc.
      width: 28
    details: Kitware can help you get started, create custom components, or even build full applications. Our team is here to help.  Please contact us
    link: https://www.kitware.com/contact/
---

<!-- Force assets to be bundled with sha -->
<img src="/assets/logos/trame-text.svg" style="display: none;" />
<img src="/assets/logos/jupyter.svg" style="display: none;" />
<img src="/assets/logos/kitware.svg" style="display: none;" />
<img src="/assets/logos/python.svg" style="display: none;" />
<img src="/assets/logos/opensource.svg" style="display: none;" />
<img src="/assets/logos/vtk.svg" style="display: none;" />
<img src="/assets/logos/vtk.svg" style="display: none;" />