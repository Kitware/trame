[post](https://www.kitware.com/how-trame-powers-todays-visualizations/)

# How trame Powers Today’s Visualizations

August 4, 2025

[Sebastien Jourdain](https://www.kitware.com/author/sebastien-jourdain/ "Posts by Sebastien Jourdain"), [Patrick Avery](https://www.kitware.com/author/patrick-avery/ "Posts by Patrick Avery") and [Samantha Schmitt](https://www.kitware.com/author/samantha-schmitt/ "Posts by Samantha Schmitt")

![The standalone application is now an integral part of their toolchain for performing data analysis and interactive visualization. Thanks to the fact that the application is published to the Python Package Index (PyPI), users can install and run it on any computer from a simple command line.](https://www.kitware.com/main/wp-content/uploads/2025/08/trame-feature4.jpg)

Many scientific and engineering applications are still built as standalone desktop tools. While these solutions may have served teams well in the past, they often present modern-day challenges: they’re difficult to share, hard to maintain, and disconnected from today’s collaborative and distributed workflows.

As research increasingly spans labs, institutions, and even continents, tools must adapt. They need to be flexible, accessible, and built for the environments where users and data live—whether that’s on a laptop, in a Jupyter notebook, or on a high-performance computing (HPC) system.

trame is an open source Python framework designed for exactly that. With best-in-class integration with visualization technologies like VTK and ParaView, trame helps research teams turn complex, domain-specific workflows into interactive, browser-based applications. With trame, you can:

* Run applications on desktops, in browsers, in notebooks, or on remote servers
* Share tools via simple URLs—no installation required
* Build tailored UIs with little to no front-end development experience
* Stay entirely within the Python ecosystem

Across domains, researchers are finding new ways to simplify and scale their work using trame. Whether it’s accelerating interactive visualizations in a lightweight environment or making data tools more accessible across remote teams, the shift toward browser-based applications is opening new possibilities. We’ve seen this firsthand as we have helped many customers transition to web applications.

## Real Projects, Real Impact: Custom trame Solutions

**Case Study 1: Speed and Simplicity for Academic Researchers**

Our collaborators from a top-ranked U.S. research university—consistently ranked among the top 5 globally—were using a research pipeline that relied on Matplotlib for rendering within JupyterLab to analyze and visualize simulation output. While this setup worked for analysis, it wasn’t built to scale. Rendering their full dataset was painfully slow, often taking hours to generate the full set of timesteps as a movie. The team was also unable to validate their data until after it went through this time-consuming export process, which meant they had to go through the render process again if they discovered any issues.

To address these limitations, Kitware incorporated trame and VTK into their workflows. This allowed the team to validate their data in real time before beginning the rendering export process. These platforms also drastically reduced the time it took to export their data, taking only a minute instead of hours to complete.

Key technical enhancements included:

* **900x performance improvement** achieved by offloading rendering from Matplotlib to VTK while using multi-threading for encoding the images to disk
* A **Python-only codebase**, with trame serving as the front end and controller, so the researcher could maintain and extend the tool without requiring constant support from Kitware

The standalone application is now an integral part of their toolchain for performing data analysis and interactive visualization. Thanks to the fact that the application is published to the Python Package Index (PyPI), users can install and run it on any computer from a simple command line.

![The standalone application is now an integral part of their toolchain for performing data analysis and interactive visualization. Thanks to the fact that the application is published to the Python Package Index (PyPI), users can install and run it on any computer from a simple command line.](https://www.kitware.com/main/wp-content/uploads/2025/08/trame-feature-1024x816.jpg)

**Case Study 2: Improving Accessibility and Collaboration at Lawrence Berkeley National Laboratory**

The team at the National Center for Electron Microscopy (NCEM) at Lawrence Berkeley National Laboratory (LBNL) used a Qt-based desktop application to explore 4D STEM materials science datasets collected during electron microscopy experiments. The application interfaced with complex imaging data—often hundreds of gigabytes in size—and included custom widgets for interactively exploring the data in both real space and diffraction space.

While effective in the lab, the application became a burden once experiments concluded. Remote users needed to:

1. Download and install the Qt application, which required platform-specific builds and challenges due to unfamiliar installation processes.
2. Manually transfer very large datasets, which sometimes could not be loaded into the application on a user’s computer due to memory constraints.

Kitware proposed replacing the desktop solution with a trame-powered web application. This new approach mirrored the functionality of the original Qt tool but introduced key improvements:

* Users can now **access the application through any modern browser** or integrate it directly into JupyterLab, using the same backend.
* The application is deployed on an internal server co-located with the experimental data, **eliminating the need to transfer files**.
* Kitware developed **custom trame widgets** that mimicked the key Qt UI elements—such as panning/zooming and ROI controls—while improving responsiveness and modularity.
* The **architecture was redesigned** to be server-client, allowing the heavy lifting (e.g., rendering, file I/O) to occur near the data while keeping the front end light and responsive.

This migration allowed NCEM researchers to bypass installation and data transfer altogether. With a single URL, users can now relaunch their analysis sessions from anywhere, interactively explore large datasets in real time, and share insights with collaborators more easily than ever before.

## Why Teams Choose trame—and Kitware

Both of these projects demonstrate what’s possible when domain-specific workflows are paired with scalable, interactive visualization platforms. With trame, teams can move beyond the limitations of static visualization inside Jupyter, desktop-bound tools, and into a more agile, cloud-ready development model without abandoning the Python-based ecosystems they already rely on.

Whether you need to offload GPU rendering to accelerate performance, embed custom UIs into Jupyter workflows, or deploy visual applications alongside large-scale data on HPC infrastructure, trame provides the flexibility to meet you where your research lives. It’s not just a framework—it’s a bridge between scientific code and modern, user-facing tools. In fact, trame, along with VTK, ParaView, and Catalyst, is part of an infrastructure that we are building to make it easy to develop bespoke visualization workflows that are just right for the domain-specific problems that you might be interested in solving. The ability to quickly develop visual workflows that are just right for the problem at hand—no more, no less—represents the next generation of production data analysis, visualization, and visual workflow applications.

And with Kitware’s help, that bridge can be built quickly and robustly. Our engineers work alongside your team to:

* Design modular, maintainable architectures
* Develop custom components tailored to your data and users
* Integrate with your existing infrastructure, whether cloud-based or on-premises
* Deliver production-grade applications that evolve with your needs

If you’re currently maintaining a legacy application—or just starting to prototype a new one—trame offers a modern foundation. And Kitware can help you bring it to life.

**Interested in accelerating your own visualization tools?**  
Join our free webinar on August 13th to see trame in action.

[Register Now](https://www.kitware.com/webinars/whats-new-in-trame-bespoke-workflows-for-better-productivity/)

**Ready to modernize your application?**  
Contact Kitware for a consultation with our developers.

[Request at Meeting](https://www.kitware.com/contact/)

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

[Trame](https://www.kitware.com/tag/trame/) | [VTK](https://www.kitware.com/tag/vtk/)

