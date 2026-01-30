[post](https://www.kitware.com/numerical-plasma-dynamics-from-the-comfort-of-your-web-browser-with-trame/)

# Numerical plasma dynamics from the comfort of your web browser with trame

December 8, 2022

[Julien Finet](https://www.kitware.com/author/julien-finet/ "Posts by Julien Finet") and [Helene Grandmontagne](https://www.kitware.com/author/helene-grandmontagne/ "Posts by Helene Grandmontagne")

![](https://www.kitware.com/main/wp-content/uploads/2022/12/Sans-titre3.png)

Showing off [boltzplatz](https://boltzplatz.eu/)’s expertise in numerical plasma dynamics and how [trame](https://kitware.github.io/trame/index.html) – a web framework from Kitware – was crucial in the rapid development of boltzplatz’s web application.

## boltzplatz – numerical plasma dynamics GmbH

boltzplatz is a Stuttgart-based company offering engineering and consulting services for high-tech companies focusing on vacuum- and plasma-based technologies. They develop and maintain the open-source library [PICLas,](https://github.com/piclas-framework/piclas/) cooperatively with the Institute of Space Systems (University of Stuttgart). PICLas is a flexible particle-based plasma simulation suite for numerical simulation of rarefied plasma flows under the influence of electromagnetic interactions.

As the topic of numerical plasma dynamics is very complex in its own right, naturally, PICLas offers many parameters that a user can configure, including what particle species appear in the simulation together with their energy levels, vibrational states and so on. On top of that, depending on the input mesh and boundary conditions, computing the simulation on one’s desktop computer becomes infeasible.

The company’s goal thus was to develop a web application that would allow users to configure simulations through a simplified UI, run the simulations on a remote server, share their results and create analyses and graphics with ParaView to illustrate their outputs.

![](https://www.kitware.com/main/wp-content/uploads/2022/12/Sans-titre-1024x555.png)

Fig 1. Pre-processed input mesh file showing a section of a vacuum pump rendered with [ParaView-Visualizer](https://github.com/Kitware/paraview-visualizer/)

## trame for fast, simple and powerful development

What was outlined above defines a complex web application that involves a lot of user interaction with the server. With trame, all that is simplified to one programming language. Building an application becomes more about defining your feature set rather than building pieces of your infrastructure.

Thanks to the powerful, yet simple-to-use web framework, Kitware was able to develop a prototype within a few days and a full web application within a few weeks, which lets users configure, run and post-analyze numerical plasma dynamic simulations. And all done in Python.

The web application’s UI has a modern feel since trame comes with components built upon Vuetify. The UI to configure PICLas is created dynamically through [SimPut](https://github.com/Kitware/trame-simput/), which is fully supported by trame.

![](https://www.kitware.com/main/wp-content/uploads/2022/12/Sans-titre2-1024x644.png)

Fig 2. SimPut in action configuring the particle species and their interactions in a simulation

## Acknowledgements

If you want to find out more about boltzplatz or particle-based plasma simulation, visit their website here: <https://boltzplatz.eu/>

For a more in-depth look at how trame makes developing your next web application fast, simple and powerful: <https://www.kitware.com/trame-visual-analytics-everywhere/>. If you want to try out trame for yourself, check out our [developer’s course](https://www.kitware.com/trame-developers-course/).

The trame-based web application consulting and development work was performed by Kitware Europe ([www.kitware.eu](http://www.kitware.eu)) as part of boltzplatz’ participation in the European Space Agency Business Incubation Centre in Baden-Württemberg.

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

[Customer Spotlight](https://www.kitware.com/tag/customer-spotlight/) | [ParaView](https://www.kitware.com/tag/paraview/) | [Simulation](https://www.kitware.com/tag/simulation/) | [Trame](https://www.kitware.com/tag/trame/) | [Visualization](https://www.kitware.com/tag/visualization/) | [Visualizer](https://www.kitware.com/tag/visualizer/) | [Web Visualization](https://www.kitware.com/tag/web-visualization/)

