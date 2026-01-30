[post](https://www.kitware.com/trame-micro-workflow-use-case/)

# trame: Micro-Workflow Use Case

October 1, 2024

[Patrick O'Leary](https://www.kitware.com/author/patrick-oleary/ "Posts by Patrick O'Leary"), [Sebastien Jourdain](https://www.kitware.com/author/sebastien-jourdain/ "Posts by Sebastien Jourdain"), [Berk Geveci](https://www.kitware.com/author/berk-geveci/ "Posts by Berk Geveci"), [Patrick Avery](https://www.kitware.com/author/patrick-avery/ "Posts by Patrick Avery") and [Will Schroeder](https://www.kitware.com/author/will-schroeder/ "Posts by Will Schroeder")

![](https://www.kitware.com/main/wp-content/uploads/2024/09/image6-1.png)

## trame

Kitware has created trame [[1](https://kitware.github.io/trame/)] to spark creativity and empower developers to construct compelling interactive visual applications accessible directly through web browsers. trame, a Python package, functions as a tool for building robust applications without the need for extensive knowledge in web development. Its remarkable adaptability facilitates the creation of desktop applications, Jupyter tools, HPC applications, and client/server cloud applications for various devices, including phones, tablets, laptops, and desktops, without making any changes to the code. Check out our other blogs from the trame series for in-depth information on trame: “trame: Architecture and Capabilities” [[2](https://www.kitware.com/trame-architecture-and-capabilities/)] and “trame: Dashboard Use Case” [[3](https://www.kitware.com/trame-dashboard-use-case/)].

![](https://www.kitware.com/main/wp-content/uploads/2024/09/image6-1024x635.png)

This image depicts the trame-based conceptual modeler application that uses GemPy and machine learning to design geological models for surface and subsurface modeling.

## Micro-Workflows

Imagine a workflow as a carefully choreographed dance of steps, each leading seamlessly to the next, all working together to bring a process to life. However, these elegant workflows often demand the use of complex advanced modeling and simulation (M&S) tools, creating a barrier for many who seek to harness the power of simulation for discovery and innovation.

We’re on a mission to simplify simulation workflows and enhance simulation software’s usability, all to encourage a broader range of people to embrace simulation technology. To achieve this, we break down software usability into two key elements: how easy it is to learn and how easy it is to use.

![](https://www.kitware.com/main/wp-content/uploads/2024/09/image4-1024x475.png)

This is a typical simulation workflow, but many others exist.

Learning the ropes boils down to how powerful and flexible the simulation software is. The more bells and whistles it has, the steeper the learning curve. When end-users have more options, mastering the software becomes more challenging.

The user experience involves manipulating the simulation product to make it work. This could mean running a command-line function or using a graphical user interface (GUI). The GUI, in particular, is designed to enhance ease of use and simplify the learning process, providing the end-user with a supportive tool to navigate the complexity of the software’s functionality and flexibility.

The Department of Energy’s Nuclear Energy Advanced Modeling and Simulation (NEAMS) Toolkit offers powerful tools for designing, analyzing, and licensing advanced nuclear systems and experiments. However, it requires specialized training and skills to use effectively. Simplifying the use and deployment of these tools is crucial to enable analysts and other stakeholders to create high-fidelity simulations. This usability enhancement will pave the way for even more efficient and groundbreaking nuclear energy solutions.

MOOSE [[4](https://www.mooseframework.org/)] is an incredible parallel computing platform created by the Idaho National Laboratory (INL) as part of the NEAMS Toolkit. It’s designed to handle multiphysics and finite-element simulations and has an intuitive interface for advanced nonlinear solver technology. The MOOSE framework is all about being user-friendly and tackling real-world challenges that scientists and engineers encounter. The MOOSE team has considered everything, from making installation a breeze to running simulations on state-of-the-art supercomputers. This attention to detail means that MOOSE can supercharge research, even though getting started with MOOSE can still be tricky.

![](https://www.kitware.com/main/wp-content/uploads/2024/09/image5.png)

![](https://www.kitware.com/main/wp-content/uploads/2024/09/image10-1024x601.png)

Peacock 2.0 (a) simulation definition with domain visualization and (b) simulation definition where we present synced GUI and text editor views side-by-side to improve ease of learning.

We created the trame-base Peacock 2.0 [[5](https://mooseframework.inl.gov/python/peacock.html), [6](https://www.kitware.com/the-evolution-of-peacock-a-powerful-interface-for-moose-simulations/)], a cutting-edge technology encapsulating the entire MOOSE workflow in a user-friendly GUI, offering unlimited functionality and flexibility. After years of meticulous consideration by the MOOSE development team, we simply transformed the engineer’s interaction with the platform by replacing key-clicking with mouse-clicking input. The Peacock 2.0 GUI maintains the same functionality and flexibility as the input deck, ensuring a seamless and user-friendly experience but provides limited improvement in usability.

![](https://www.kitware.com/main/wp-content/uploads/2024/09/image8-1024x602.png)

![](https://www.kitware.com/main/wp-content/uploads/2024/09/image9-1024x603.png)

Peacock 2.0 (a) simulation execution and (b) embedded analysis and visualization.

The lesson learned from this experience is that we should tailor exposed simulator functionality to specific use cases and constrain flexibility to enhance ease of use and learning.

The end-to-end simulation process is a series of tasks connected by data dependencies. To make simulation software more user-friendly, we propose the idea of a micro-workflow. These micro-workflows demonstrate the capabilities of simulation workflows by presenting specific use cases as templates. The end-users can access limited configuration options through a GUI in a trame-based application.

We have explored an interesting set of workflows relevant to the pharmaceutical industry. Pharmaceutical companies often start by developing and optimizing processes on a small scale. Still, they must also ensure these processes work in larger production-scale bioreactors. To do this, many use M-Star Simulations’ advanced computational fluid dynamic (CFD) software [[7](https://mstarcfd.com/)] to forecast the intricate, multi-fluid mixing process. We’ve enhanced these activities by developing ArrowFlow [[8](https://www.kitware.com/arrowflow/)], a micro-workflow application tailored for specific use cases, allowing their analysts to harness this powerful capability.

![](https://www.kitware.com/main/wp-content/uploads/2024/09/Screenshot-2024-05-16-at-16.22.17-1024x763.png)

![](https://www.kitware.com/main/wp-content/uploads/2024/09/Screenshot-2024-05-16-at-16.24.10-1024x763.png)

![](https://www.kitware.com/main/wp-content/uploads/2024/09/Screenshot-2024-05-16-at-16.25.47-1024x763.png)

ArrowFlow, which allows stakeholders to define, run, and analyze simulation use cases with M-Star CFD™ for a range of applications.

The analyst can explore various use cases such as blending time, particle suspension and transportation characteristics, and mean fluid shear and energy dissipation rate. Suppose the analyst selects the blending time use case, for example. In that case, we present a new page where they can adjust micro-workflow parameters like rotation speed, liquid level, and dye injection time. Next, they hit the run button and watch the micro-workflow display the analysis and visualization page with stunning 3D visualizations and interactive 2D charts. The analyst can customize the visualizations by hiding or showing different elements of the 3D simulation domain or plotting different quantities. ArrowFlow makes these micro-workflows easy to learn and use – it’s a game-changer!

trame’s exceptional flexibility and “write once, use everywhere” design make it the perfect choice for improving the usability of simulation software.

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

[1] trame, Software Package, Ver. 3.6.0, Kitware, Inc., Clifton Park, NY, 2024. <https://kitware.github.io/trame/>, DOI 10.5281/zenodo.10957638

[2] trame: Architecture and Capabilities, June 15, 2024. <https://www.kitware.com/trame-architecture-and-capabilities/>

[3] trame: Dashboad Use Case, September 5, 2024. <https://www.kitware.com/trame-dashboard-use-case/>

[4] The MOOSE framework, <https://www.mooseframework.org/>

[5] Peacock, A Graphical User Interface for MOOSE, <https://mooseframework.inl.gov/python/peacock.html>

[6] Schenck, E., Jourdain, S., Avery, P., and O’Leary, P., The Evolution of Peacock: A Powerful Interface for MOOSE Simulations, June 22, 2023. <https://www.kitware.com/the-evolution-of-peacock-a-powerful-interface-for-moose-simulations/>

[7] M-Star Computational Fluid Dynamics (CFD) Software. Real World Models. Real Time Results. <https://mstarcfd.com/>

[8] ArrowFlow, Software Package, Ver. 2024-05-17, Kitware, Inc., Clifton Park, NY, 2024. <https://www.kitware.com/arrowflow/>

Tags:

[ParaView](https://www.kitware.com/tag/paraview/) | [Scientific Computing](https://www.kitware.com/tag/scientific-computing/) | [Scientific Visualization](https://www.kitware.com/tag/scientific-visualization/) | [Simulation Workflows](https://www.kitware.com/tag/simulation-workflows/) | [Trame](https://www.kitware.com/tag/trame/) | [Visualization](https://www.kitware.com/tag/visualization/) | [VTK](https://www.kitware.com/tag/vtk/)

