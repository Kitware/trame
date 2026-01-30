[post](https://www.kitware.com/scientific-visualization-in-2022/)

# Scientific Visualization in 2022

January 18, 2022

[Berk Geveci](https://www.kitware.com/author/berk-geveci/ "Posts by Berk Geveci"), [Bob O'Bara](https://www.kitware.com/author/bob-obara/ "Posts by Bob O'Bara"), [Patrick O'Leary](https://www.kitware.com/author/patrick-oleary/ "Posts by Patrick O'Leary"), [Will Schroeder](https://www.kitware.com/author/will-schroeder/ "Posts by Will Schroeder"), [Utkarsh Ayachit](https://www.kitware.com/author/utkarsh-ayachit/ "Posts by Utkarsh Ayachit"), [Sebastien Jourdain](https://www.kitware.com/author/sebastien-jourdain/ "Posts by Sebastien Jourdain"), [Cory Quammen](https://www.kitware.com/author/cory-quammen/ "Posts by Cory Quammen") and [Chris Harris](https://www.kitware.com/author/chris-harris/ "Posts by Chris Harris")

![Scientific visualization of jellyfish](https://www.kitware.com/main/wp-content/uploads/2022/01/JellyfishCropped.png)

![](https://www.kitware.com/main/wp-content/uploads/2022/01/JellyFish-1024x719.png)

[Kitware’s Scientific Computing Team](https://www.kitware.com/teams/scientific-computing/) is looking forward to another year of groundbreaking technical advances. Building off of the success our world class open source platforms VTK and ParaView, we will be introducing new capabilities that dramatically increase performance and ease of use; significantly improve end-to-end workflows for large-scale simulation and experimental science; support ongoing advances in AR/VR hardware and rendering; and introduce a new Python-based, web integration framework that weaves together visual analytics tools for large scale data analysis. In the following, we provide high-level summaries of a small subset of the work we are undertaking this year, with contact information if you’d like to learn more. Throughout the year, we’ll be announcing these tools as they arrive, in many cases we will be looking for help from the community to test, evaluate, and guide our development efforts.

## ParaView / VTK

Development of [VTK](https://vtk.org/) and [ParaView](https://www.paraview.org/) continues at a ferocious pace. The next VTK 9.2 release is expected in the spring of 2022 and 9.3 in the fall of 2022. ParaView 5.10.0 was released in January, and we expect to release 5.11.0 in May and 5.12.0 in October. Other notable goals include:

* VTK’s ongoing performance improvements due to CPU threading (vtkSMPTools) and GPU accelerators (vtk-m).
* Improving accuracy for statistical filters when operating on point fields by adding support for ghost points.
* Adding support for meshes used in simulations based on discontinuous Galerkin methods.

##### Contact: [Cory Quammen](mailto:cory.quammen@kitware.com)

## VTK-m

[VTK-m](https://m.vtk.org/) is a toolkit of scientific visualization algorithms for emerging processor architectures, especially GPUs. It provides the building blocks for portable algorithm development and a number of core visualization algorithm implementations. In 2022, our focus will be on continuing the port of VTK-m to new GPU architectures including AMD and Intel GPUs. We are also pushing tighter integration of VTK-m into VTK and ParaView where users will be able to choose a runtime option to replace certain filters with their VTK-m counterparts. We hope to demonstrate the use of VTK-m in end-to-end simulation workflows through the Catalyst and Ascent in situ libraries on next generation supercomputers.

##### Contact: [Berk Geveci](mailto:berk.geveci@kitware.com)

## Next Generation ParaView: ParaView async

Over the past couple of years the Scientific Computing Team has envisioned an improved ParaView that is more interactive and responsive no matter the computational load. With a concerted effort now underway, the major objectives are designing and implementing concurrent pipelines, in which rendering and data processing pipelines do not block one another; and supporting pervasive interruptibility, ensuring that filters can be interrupted or aborted at any time to provide application responsiveness. We expect a public prototype to be available for comment and experimentation by early summer, with an early release available for SuperComputing 2022.

##### Contact: [Utkarsh Ayachit](mailto:utkarsh.ayachit@kitware.com)

## CMB: Computational Model Builder

Modeling and simulation are tasks pervasive to the design and manufacturing of modern, high-quality products. However such simulation workflows are typically highly specific to a domain, requiring complex combinations of sophisticated computing tools to implement. [CMB](https://www.computationalmodelbuilder.org/) is a framework that simplifies developing simulation frameworks, enabling scientists and engineers to focus on their domain expertise rather than worrying about the integration of disparate software and simulation codes. Recent developments in CMB provide seamless integration of pre-, post-, and simulation workflows including deployment to large supercomputing systems and servers, and the ability to support multiphysics analyses. In 2022, major goals include supporting simulation workflows with multiple analysis stages, and providing the capability to postprocess results on HPC machines after performing simulation configuration and setup on the local desktop.

##### Contact: [Bob O’Bara](mailto:bob.obara@kitware.com)

## AR / VR

Currently there is extreme interest in AR/VR technologies, and we have several active areas of development underway. Some notable goals for 2022 include:

* Support OpenXR-based VR visualization for consumer headsets in VTK/ParaView; and enhance the existing ParaView VRPlugin for CAVE-like systems.
* Add support for Hololens in VTK/ParaView/3DSlicer.
* Enable actors to be placed into other coordinate systems such as physical coordinates and device coordinates. This makes it easier to position actors in VR/AR scenes that move with devices or are fixed to the physical space.
* Roll out support for WebXR in VTK.js and add controller/interaction support similar for VTK C++.
* Consolidate APIs between the OpenVR, OpenXR, Cave and Zspace systems.

##### Contact: [Cory Quammen](mailto:cory.quammen@kitware.com)

## Chemistry / Material Design

[Tomviz](https://tomviz.org/) is an application for the characterization of materials at the nano- and meso-scale with emphasis on transmission and scanning transmission electron microscopes (S/TEM). Tomviz is tailored for visualizing and processing the associated large-scale electron tomography data. We have recently been adding features to support X-ray tomography datasets. Building on the success of Tomviz, we have also been developing an application for the calibration and analysis of X-ray diffraction experiments; through the Highly Extensible X-Ray Diffraction Toolkit (HEXRD). Our current focus is improving support for 3D X-ray diffraction (3DXRD). A major goal of our current work is to scale our applications to support datasets of even larger scales which reflect the ever increasing data resolution available to experimentalists. In the area of 4D-STEM, we are harnessing the power of HPC to support high throughput processing of very large experimental datasets.

##### Contact: [Chris Harris](mailto:chris.harris@kitware.com)

## Trame: Web-based, Python Integration Framework

The Python-based integration framework [trame](https://kitware.github.io/trame/index.html) enables non-web-developers to create powerful, complex client-server web applications supporting large-scale data processing and visualization without the need to understand web technologies or frameworks. Based on decades of experience with VTK, ParaView, ParaViewWeb, and VTK.js, trame transparently leverages these visualization tools along with web technologies (including GUI tools) and the Python ecosystem. Extensive resources have been developed including [the trame web site](https://kitware.github.io/trame/), along with a [video](https://vimeo.com/651667960) that follows the trame [tutorial](https://kitware.github.io/trame/docs/tutorial.html). The ease by which complex web applications can be built is exceptional: we expect this platform will grow into another core platform for the Scientific Computing Team.

##### Contact: [Sebastien Jourdain](mailto:sebastien.jourdain@kitware.com) & [Patrick O’Leary](mailto:patrick.oleary@kitware.com)

## Catalyst

[Catalyst](https://catalyst-in-situ.readthedocs.io) is an API specification developed for simulations to analyze and visualize data in situ. It includes a light-weight implementation of the Catalyst API and an SDK to develop implementations of the API to perform data processing and visualization tasks. The Catalyst API uses ‘C’ and is binary compatible with different implementations of the API making it easier to change the implementation at runtime. Starting with 5.9, ParaView releases are packages with an implementation of the Catalyst API. This implementation can be used in lieu of the stub to analyze and visualize simulation results using ParaView’s data-processing and visualization capabilities. We are super excited about this capability and in the coming year will be working hard at replacing previous ParaView Catalyst implementations with this new approach.

##### Contact: [Berk Geveci](mailto:berk.geveci@kitware.com)

## Happy New Year!

We hope you join us in the coming year as the Scientific Computing Team works towards these and many other exciting goals. Please feel free to reach out, we’d enjoy hearing from you and are open to suggestions, guidance, and collaboration.

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

[AR](https://www.kitware.com/tag/ar/) | [Catalyst](https://www.kitware.com/tag/catalyst/) | [Chemistry](https://www.kitware.com/tag/chemistry/) | [CMB](https://www.kitware.com/tag/cmb/) | [Material Design](https://www.kitware.com/tag/material-design/) | [ParaView](https://www.kitware.com/tag/paraview/) | [Trame](https://www.kitware.com/tag/trame/) | [vr](https://www.kitware.com/tag/vr/) | [VTK](https://www.kitware.com/tag/vtk/)

