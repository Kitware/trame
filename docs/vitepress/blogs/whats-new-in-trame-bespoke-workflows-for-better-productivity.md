[post](https://www.kitware.com/whats-new-in-trame-bespoke-workflows-for-better-productivity/)

# What’s New in trame: Bespoke Workflows for Better Productivity

October 13, 2025

[Sebastien Jourdain](https://www.kitware.com/author/sebastien-jourdain/ "Posts by Sebastien Jourdain") and [Riley Sheedy](https://www.kitware.com/author/riley-sheedy/ "Posts by Riley Sheedy")

![Developing interactive applications for scientific and engineering workflows often requires bridging complex visualization backends with responsive user interfaces. Traditional web frameworks can introduce additional overhead, demanding expertise outside the core domain of research and simulation.](https://www.kitware.com/main/wp-content/uploads/2025/10/trame-feature.jpg)

Developing interactive applications for scientific and engineering workflows often requires bridging complex visualization backends with responsive user interfaces. Traditional web frameworks can introduce additional overhead, demanding expertise outside the core domain of research and simulation.

trame, an open source framework from Kitware, addresses this challenge by enabling the creation of interactive, production-ready applications entirely in Python. Over the past year, trame has introduced a range of updates that improve performance, extend integration options, and simplify the development of bespoke workflows.

## Recent Enhancements with Expanded Ecosystem

We added a better superset for Jupyter by adding a dedicated extension for supporting cloud deployments and network handling. With this work, you can also enable full-screen usage of your trame application within the Jupyter tab infrastructure.

Then we added a new set of widgets that brings more capabilities for your next application:

* [vtklocal](https://kitware.github.io/trame/examples/vtk/wasm.html) – A widget for doing local rendering using VTK.wasm, using a similar API as our current ones. This means you can easily upgrade your existing application with just a few lines and start leveraging WASM instead.
* [dockview](https://github.com/Kitware/trame-dockview/) – Dockable panel layouts for complex drag and drop user interface freedom.
* [image-tools](https://github.com/Kitware/trame-image-tools), [react](https://github.com/Kitware/trame-react), and [slicer-trame](https://kitware.github.io/trame/examples/apps/trame-slicer.html) (in progress) – Additional widgets that help extend functionalities around image annotations, react integration, and medical image processing.

![You can also see trame in action through our on-demand webinar, which demonstrates recent enhancements and provides practical takeaways for applying them in your own applications.](https://www.kitware.com/main/wp-content/uploads/2025/10/trame-1.jpg)

You can also see trame in action through our [on-demand webinar](https://www.youtube.com/watch?v=P6t9iOTyi4Y&t=3201s), which demonstrates recent enhancements and provides practical takeaways for applying them in your own applications.

## Why trame

trame abstracts the complexity of web application development while maintaining the performance and flexibility required for scientific computing:

* Interfaces are defined entirely in Python.
* Reactive state management synchronizes client and server seamlessly.
* Event handling directly connects UI interactions with Python methods.
* The new VTK multiple rendering backends (X, EGL, OSMesa) support streamlined trame deployment regardless of whether you are targeting cloud, Jupyter, Desktop, or HPC.

This architecture enables developers to treat distributed or remote workflows as though they were local, accelerating the path from concept to application.

Trame has been adopted across organizations in diverse domains and technical areas:

* Energy and Manufacturing – Simulation workflows, in-situ computing, and engineering design.
* Healthcare and Life Sciences – Surgical planning, digital pathology, and imaging systems.
* Defense and Intelligence – AI-driven analysis, 3D reconstruction, and interactive cyber-physical simulations.

By providing tailored user interfaces to complex backends, trame helps experts focus on analysis and innovation rather than infrastructure.

![By providing tailored user interfaces to complex backends, trame helps experts focus on analysis and innovation rather than infrastructure.](https://www.kitware.com/main/wp-content/uploads/2025/10/trame-2-1024x864.jpg)

## Partnering with Kitware

At Kitware, we don’t just adapt to evolving workflows—we help define them. As the creators of platforms such as Catalyst, VTK, ParaView, and trame, we bring decades of expertise in high-performance computing, large-scale visualization, and open science. This foundation enables research and engineering teams to accelerate the path from simulation to insight with tools that are efficient, scalable, and built for demanding real-world applications.

If you’d like to learn more about trame or explore how it can support your workflows, [contact our team](https://www.kitware.com/contact/).

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

[Python](https://www.kitware.com/tag/python/) | [Scientific and Engineering Workflows](https://www.kitware.com/tag/scientific-and-engineering-workflows/) | [Trame](https://www.kitware.com/tag/trame/)

