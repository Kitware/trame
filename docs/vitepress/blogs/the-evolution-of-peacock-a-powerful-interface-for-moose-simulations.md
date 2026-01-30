[post](https://www.kitware.com/the-evolution-of-peacock-a-powerful-interface-for-moose-simulations/)

# The Evolution of Peacock: A Powerful Interface for MOOSE Simulations

June 22, 2023

[Elim Schenck](https://www.kitware.com/author/elim-schenck/ "Posts by Elim Schenck"), [Sebastien Jourdain](https://www.kitware.com/author/sebastien-jourdain/ "Posts by Sebastien Jourdain"), [Patrick Avery](https://www.kitware.com/author/patrick-avery/ "Posts by Patrick Avery") and [Patrick O'Leary](https://www.kitware.com/author/patrick-oleary/ "Posts by Patrick O'Leary")

![Exodus Viewer of Peacock](https://www.kitware.com/main/wp-content/uploads/2023/06/featured-image.jpg)

## Introduction

Advanced modeling and simulations play a crucial role in designing and optimizing the efficiency and safety of nuclear reactors and fuels in nuclear energy. MOOSE (Multiphysics Object-Oriented Simulation Environment)(1) is a widely used software framework for performing physics simulations. MOOSE is developed and supported through the Nuclear Energy Advanced Modeling and Simulation (NEAMS) program(2), a U.S. Department of Energy-Office of Nuclear Energy (DOE-NE) program that develops advanced modeling and simulation tools and capabilities to accelerate the deployment of advanced nuclear energy technologies, such as light-water reactors (LWRs), non-light-water reactors (non-LWRs), and advanced fuels. MOOSE leverages finite element analysis and meshes to simulate various physics phenomena.

To configure, execute, and analyze MOOSE applications, a graphical interface called Peacock(3) was developed by Derek Gaston nearly a decade ago. However, the original version of Peacock had some limitations and built up some technical debt over the years. In this article, we will explore the evolution of Peacock, its new version, and the innovative features that make it a powerful tool for MOOSE simulations.

## MOOSE

MOOSE is a powerful software framework that nuclear energy scientists and engineers use to perform physics simulations using finite element analysis. It allows for analyzing and optimizing nuclear reactors and fuels, helping to improve efficiency and safety. MOOSE applications traditionally consist of an executable and an input file configuring the simulation. Although configuring and executing MOOSE simulations is simple, it can seem complex and time-consuming for novice end-users of advanced modeling and simulation. That’s where Peacock comes in.

![Figure 1: An example MOOSE input file. Brackets denote blocks, which are groupings of parameters. For example, the mesh block configures aspects of the mesh. This mesh comes from a file, reactor.e. Blocks can have sub-blocks. For example, the Variables block has no parameters, just sub-blocks.](https://www.kitware.com/main/wp-content/uploads/2023/06/image8.png)

**Figure 1:** An example MOOSE input file. Brackets denote blocks, which are groupings of parameters. For example, the mesh block configures aspects of the mesh. This mesh comes from a file, reactor.e. Blocks can have sub-blocks. For example, the Variables block has no parameters, just sub-blocks.

## Peacock: The Original Interface

![Screenshot of the Peacock software showing the input definition screen.](https://www.kitware.com/main/wp-content/uploads/2023/06/image4.png)

![Screenshot of the Peacock software showing the simulation execution screen.](https://www.kitware.com/main/wp-content/uploads/2023/06/image7.png)

![Screenshot of the Peacock software showing the analysis and visualization](https://www.kitware.com/main/wp-content/uploads/2023/06/image2-2.png)

**Figure 2:** Peacock consists of three pages: input definition, simulation execution, and analysis and visualization.

Peacock serves as a graphical interface for configuring and analyzing MOOSE simulations. It provides a user-friendly environment that simplifies creating input files, executing simulations, and visualizing the results. Peacock, the original graphical interface for MOOSE, was initially developed in Python using the Qt framework. While it served its purpose most of the time, there were some lingering issues with its usability, maintenance, and remote usage. The interface could have been more intuitive, but everything made sense once you were an experienced end-user. Development of physics for nuclear energy applications keeps the core MOOSE development team busy, and knowledge of MOOSE, Python, Qt, and VTK concentrate with developers in extremely high demand. Thus, over time, the maintenance of Peacock has become a burden. Additionally, using Peacock remotely, a critical use case for nuclear energy codes, needed to be more straightforward and align better with the Open OnDemand environment.

## Revisiting Peacock

To address the limitations of the original Peacock interface, a new version was developed using Kitware’s trame(4) framework. The new Peacock is written in Python and focuses on simplifying remote execution and integration with high-performance computing (HPC) scheduling. With trame, Peacock is now almost entirely written in Python, with only a few custom widgets implemented in JavaScript and maintained in the core trame framework. This evolution simplifies maintenance and allows future developers to work seamlessly within Python. This new client-server version of Peacock now provides access to the front end from various devices and environments and a back end to provide secure computations.

## Enhanced Input Configuration

As mentioned previously, the input file configuration is essential to MOOSE simulations. In the new version of Peacock, we determine the input file schema from the MOOSE executable. The MOOSE executable can output the schema as a JSON file, providing valuable information about the available configuration blocks, parameters, and types. Furthermore, the executable can create and output the input mesh as an ExodusII file, which is useful when the input file specifies a description of the mesh rather than a file. Peacock leverages this data and maps it to a SimPut(5) schema, which automates the user interface (UI) generation for editing and updating the input file. To parse the blocks, parameters, and types of the input file, Peacock utilizes the pyhit(6) library.

![Screenshot of the input tab](https://www.kitware.com/main/wp-content/uploads/2023/06/image5.png)

**Figure 3:** The input tab.

The core input file tab in Peacock allows users to create and edit input files for MOOSE simulations. The tab features a tree view representing the input file syntax specific to the simulation application. This tree view is automatically populated via SimPut with blocks and parameters from an existing input file, making it easier for users to navigate and modify the input file structure.

## GUI and Text Editor Integration

While Peacock’s graphical user interface (GUI) dramatically simplifies the input file configuration, some advanced end-users may prefer to edit the file directly. Peacock integrates a file editor directly into the interface to cater to both types of end-users. This editor is synced with the GUI, ensuring immediate reflection of changes made in either the GUI or the editor. Peacock utilizes the web-based Monaco editor, the same editor used in VS Code, for its text editing capabilities. We integrated syntax highlighting for the MOOSE custom grammar, and a language server provides hover hints and auto-completion. This integration makes editing the input file more efficient and flexible for advanced end-users. That capability is even now available for everyone to enjoy in trame-code (7).

![Synced GUI and Text Editor.](https://www.kitware.com/main/wp-content/uploads/2023/06/image1-1-1024x601.png)

**Figure 4:** Synced GUI and Text Editor.

## Streamlined Execution

The execution of MOOSE simulations is a vital step in the workflow. Peacock provides a streamlined execution process through its executor component. The executor leverages the widely adopted web-based terminal Xterm.js used in various development environments like VS Code and JupyterLab. Xterm.js via trame-xterm(8) enhances the readability of MOOSE executable output, ensuring a seamless execution experience for end-users. This feature has been integrated into the core trame framework, enabling other applications to leverage it going forward.

![The executor with minimal options.](https://www.kitware.com/main/wp-content/uploads/2023/06/image3-1024x602.png)

**Figure 5:** The executor with minimal options.

## Enhanced Visualization with ParaView

The analysis and visualization of simulation results are essential aspects of MOOSE simulations. Peacock uses ParaView, a robust analysis and visualization tool, to enhance its analysis and visualization capabilities. ParaView provides a wide range of analysis and visualization techniques, capabilities, and features, including three-dimensional (3D) visualizations, charts, and annotations. Peacock also utilizes ParaView’s VTK (Visualization Toolkit) library for mesh visualization.

![The EXODUS Viewer.](https://www.kitware.com/main/wp-content/uploads/2023/06/image6-1024x603.png)

**Figure 6:** The EXODUS Viewer.

## Opportunities available using trame

Peacock is only scratching the surface of what trame has to offer. The client-server architecture of trame allows utilization of such an application as a plain desktop one (like the previous Peacock), embedded inside Jupyter (for data analysis and exploration workflows), installed and deployed via Python anywhere (pip/mamba install), and integrated into an HPC suite using OnDemand.

While most of those features come organically with trame, we must expose them appropriately. In Peacock’s case, we need a special UI breakdown to best leverage Jupyter’s cell-level workflow. And for OnDemand, we must create additional forms for job submission to accommodate Peacock code launching. All of these tasks are simple. The good news is that those paths are now possible if needed.

## Future Directions and Research Focus

While the new version of Peacock has significantly enhanced the usability and functionality of the interface, there are still ongoing efforts to improve its capabilities further. Automation and abstraction will continue to be a focus. Our next immediate task is to have Peacock automate the integration of new analysis and visualization techniques by leveraging ParaView proxies and the SimPut framework. By simply defining the desired analysis or visualization and selecting the relevant options, Peacock could generate the corresponding GUI elements on the fly. This would reduce the amount of programming required and make it easier for end-users to explore and analyze their simulation results and customize their workflows effortlessly. Additionally, the team aims to abstract the automation process to accommodate more general modeling and simulation codes, expanding the applicability of Peacock across various computational domains.

## Conclusion

The trame-based evolution of Peacock has transformed it into a more capable interface for MOOSE modeling and simulation. Peacock offers improved design, functionality, and remote execution capabilities. The integration of GUI and text editing, streamlined execution, and enhanced visualization with ParaView make Peacock a comprehensive tool for configuring, executing, and analyzing MOOSE-based applications.

However, the journey continues. As Peacock continues to evolve and expand its capabilities, it promises to simplify further and enhance the MOOSE modeling and simulation workflow. Whether a novice or an experienced end-user, Peacock provides a user-friendly and efficient environment for modeling and simulation needs.

So, why not give Peacock a try and experience the benefits of simplified MOOSE modeling and simulation firsthand? Discover how Peacock can streamline your analysis, optimize your designs, and unlock new insights into nuclear reactors and fuels.

<center>
<iframe src="https://player.vimeo.com/video/838073269?dnt=1&app_id=122963" width="500" height="351" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>
</center>

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

## References

1. [MOOSE Framework](https://www.mooseframework.org/)
2. [Nuclear Energy Advanced Modeling and Simulation (NEAMS)](https://neams.inl.gov/)
3. [Peacock: A Graphical Interface for MOOSE](https://mooseframework.inl.gov/python/peacock.html)
4. [Kitware’s trame Framework](https://github.com/kitware/trame)
5. [SimPut: Automate create web forms/ui using trame](https://github.com/Kitware/trame-simput)
6. [PyHIT: Reading, writing, and manipulating these files MOOSE input HIT format](https://mooseframework.inl.gov/python/pyhit/)
7. [trame-code: Monaco VS code editor widget for trame](https://github.com/Kitware/trame-code)
8. [trame-xterm: trame widget to expose xterm.js](https://github.com/Kitware/trame-xterm)
9. [trame: Visual Analytics Everywhere](https://www.kitware.com/trame-visual-analytics-everywhere/)
10. [trame Developers Course](https://www.kitware.com/trame-developers-course/)

Tags:

[MOOSE Simulations](https://www.kitware.com/tag/moose-simulations/) | [ParaView](https://www.kitware.com/tag/paraview/) | [Peacock](https://www.kitware.com/tag/peacock/) | [Trame](https://www.kitware.com/tag/trame/)
