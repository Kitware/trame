[post](https://www.kitware.com/trame-architecture-and-capabilities/)

# trame: Architecture and Capabilities

August 9, 2024

[Patrick O'Leary](https://www.kitware.com/author/patrick-oleary/ "Posts by Patrick O'Leary"), [Sebastien Jourdain](https://www.kitware.com/author/sebastien-jourdain/ "Posts by Sebastien Jourdain"), [Berk Geveci](https://www.kitware.com/author/berk-geveci/ "Posts by Berk Geveci"), [Will Schroeder](https://www.kitware.com/author/will-schroeder/ "Posts by Will Schroeder") and [Patrick Avery](https://www.kitware.com/author/patrick-avery/ "Posts by Patrick Avery")

![](https://www.kitware.com/main/wp-content/uploads/2024/08/image2-1.jpg)

Kitware has developed the trame [[1](https://kitware.github.io/trame/)] platform to inspire developers like you to create impactful interactive browser-based visual applications. trame, a Python package, is your gateway to building powerful applications without the need for extensive web development knowledge. Its versatility is truly remarkable – it allows for creating desktop applications, Jupyter tools, HPC applications, or client/server cloud applications used with phones, tablets, laptops, and desktops without any code changes. This adaptability makes it a powerful tool for a diverse range of tasks. trame builds on top of VTK [[2](http://www.vtk.org)] and ParaView [[3](http://www.paraview.org)], as well as a set of web utilities. It allows for the easy definition of unlimited workflows in Python for pre-processing, processing, and post-processing. It seamlessly integrates modern user interface (UI) elements with three-dimensional (3D) renderings, charts, tables, and more to create a visually appealing user experience.

![](https://www.kitware.com/main/wp-content/uploads/2024/08/fig1-1024x465.png)

***Figure**: (a) The trame architecture allows developers access to states, events, widgets, and user interfaces (UI) through Python, hiding the complexity of web development. (b) The result is an application that can run nearly everywhere (phones, tablets, laptops, and desktops) in various computational environments (desktop, Jupyter, HPC, and Cloud).*

While trame shares some similarities with tools like Plotly Dash, Bokeh, or Streamlit, its underlying foundations are distinct. Unlike traditional web servers that rely on stateless servers, a trame application utilizes a dedicated stateful server process per client. This design offers two key advantages. Firstly, it enables faster interactions, such as remote rendering of a 3D scene with VTK, by leveraging data in memory without relying on any caching infrastructure. Secondly, it ensures the application does not share objects or memory with other end users. To serve multiple end users on shared hardware, trame provides pre-configured Docker images that manage the individual processes, facilitating basic cloud deployment.

![](https://www.kitware.com/main/wp-content/uploads/2024/08/fig2-1024x258.png)

***Figure**: A trame application for analysis, inspection, and reduction of multi-detector data produced by the Small-Angle Neutron Scattering (SANS) instruments. The end-user uses the same code for (a) a desktop application, (b) a Jupyter utility, and (c) a traditional client/server web application for use in high-performance computing and cloud environments.*

Vuetify is a UI toolkit seamlessly integrated with trame that offers a wide range of interactive widgets, enhancing the appearance of applications. It organizes the UI using a hierarchical structure of widgets, similar to HTML, but trame expresses the UI design in plain Python code. Furthermore, trame provides various integrations with popular Python libraries for different analyses and visualizations, such as VTK, ParaView, Markdown, Matplotlib, Plotly, Altair, Vega, PyDeck, and more. Even if trame lacks a specific feature, it’s usually straightforward to integrate, particularly if the components already have web implementations.

![](https://www.kitware.com/main/wp-content/uploads/2024/08/fig3-1024x657.jpg)

***Figure**: This image depicts interactive explainable artificial intelligence (XAI) toolkit [[4](https://github.com/XAITK/xaitk-saliency-web-demo)] visualizations in a trame-based machine learning inference application that leverages PyTorch-trained models.*

trame is a platform that offers two straightforward methods to connect the back-end and front-end of an application. It provides a reactive shared state infrastructure that binds variables between processing/analyzing and UI representations/visualizations. Additionally, trame allows Python methods to directly bind to user interface elements that react to end-user events like clicks, touches, or mouse interactions. This user-friendly approach and flexibility make trame a powerful tool for developers of all levels of expertise.

![](https://www.kitware.com/main/wp-content/uploads/2024/08/fig4-1024x359.png)

***Figure**: (a) Vuetify UI is produced automatically using the trame-simput package. (b) Custom HTML/CSS widgets and visualizations using VTK and Plotly.*

With trame’s flexibility and “write once, use everywhere” design, you are the winner when you select to build on top of the trame framework.

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

[2] Schroeder, W., Martin, K., and Lorensen, B. (2006), The Visualization Toolkit (4th ed.), Kitware, ISBN 978-1-930934-19-1. <http://www.vtk.org>

[3] Ahrens, J., Geveci, B., and Law, C., ParaView: An End-User Tool for Large Data Visualization, Visualization Handbook, Elsevier, 2005, ISBN-13: 9780123875822[4] Explainable AI trame application, Software Package, Ver. 2.4.2, Kitware, Inc. Clifton Park, NY, 2024. <http://www.paraview.org>

[4] Explainable AI trame application, Software Package, Ver. 2.4.2, Kitware, Inc. Clifton Park, NY, 2024. <https://github.com/XAITK/xaitk-saliency-web-demo>

Tags:

[ParaView](https://www.kitware.com/tag/paraview/) | [Scientific Computing](https://www.kitware.com/tag/scientific-computing/) | [Trame](https://www.kitware.com/tag/trame/) | [VTK](https://www.kitware.com/tag/vtk/) | [Web Visualization](https://www.kitware.com/tag/web-visualization/)

