[post](https://www.kitware.com/trame-dashboard-use-case/)

# trame: Dashboard Use Case

September 5, 2024

[Patrick O'Leary](https://www.kitware.com/author/patrick-oleary/ "Posts by Patrick O'Leary"), [Sebastien Jourdain](https://www.kitware.com/author/sebastien-jourdain/ "Posts by Sebastien Jourdain"), [Patrick Avery](https://www.kitware.com/author/patrick-avery/ "Posts by Patrick Avery"), [Berk Geveci](https://www.kitware.com/author/berk-geveci/ "Posts by Berk Geveci") and [Will Schroeder](https://www.kitware.com/author/will-schroeder/ "Posts by Will Schroeder")

![](https://www.kitware.com/main/wp-content/uploads/2024/08/image5-1.png)

## trame

Kitware’s trame [[1](https://kitware.github.io/trame/)] platform is designed to spark creativity and empower developers to build compelling interactive visual applications that can be accessed directly through web browsers. trame, a Python package, serves as a conduit for building robust applications without necessitating extensive web development proficiency. Its remarkable versatility allows for the creation of desktop applications, Jupyter tools, HPC applications, and client/server cloud applications for various devices such as phones, tablets, laptops, and desktops, without the need for any code modifications. Check out our first blog in this series for in-depth information on trame: “trame: Architecture and Capabilities” [[2](https://www.kitware.com/trame-architecture-and-capabilities/)].

![](https://www.kitware.com/main/wp-content/uploads/2024/08/image16-1024x745.jpg)

**Figure**: trame-based application to examine Uber ridesharing pick-ups and drop-offs in New York City over time.

## Dashboards

A dashboard is an analysis and visualization tool that provides at-a-glance views of data and information, especially key metrics or performance indicators, that drive organizational decision-making processes. It combines several interactive reports and is becoming the most common visualization application.

![](https://www.kitware.com/main/wp-content/uploads/2024/08/image1-1024x643.png)

**Figure**: A simple [trame-based US population dashboard](https://github.com/Kitware/trame-app-dashboard) that utilizes state-of-the-art data visualization tools (Altair/Vega, Matplotlib, Plotly, and Markdown), all native in trame.

There are three main types of dashboards:

* ***Operational*** for displaying real-time data
* ***Strategic*** for showing patterns and trends over time
* ***Analytical*** for more advanced analytics

trame shines in producing science and engineering dashboards that often have three-dimensional (3D) visualizations.

![](https://www.kitware.com/main/wp-content/uploads/2024/08/image17.png)

**Figure**: ParaView visualization of a rock sample obtained from an Austin Chalk Formation outcrop [[3](http://www.digitalrocksportal.org/)].

trame leverages existing widgets and visualization libraries and tools to create vivid content for visual analytics applications.

![](https://www.kitware.com/main/wp-content/uploads/2024/08/image8-300x212.png)

![](https://www.kitware.com/main/wp-content/uploads/2024/08/image13-1-1024x580.png)

![](https://www.kitware.com/main/wp-content/uploads/2024/08/image15-1024x665.png)

![](https://www.kitware.com/main/wp-content/uploads/2024/08/Untitled-1.png)

**Figure**: U.S. population (a) a MatPlotLib growth chart over time, (b) a Plotly choropleth map for 2016, (c) an Altair Vega plot of year versus state, (d) a Markdown plot of states with the great gains and losses, and (e) a Vuetify progress plot of top states.

Big Data, often compared to new oil, requires refining and processing for effective utilization. Data from various sources can create scientific and engineering dashboards and powerful tools, making data easily accessible and understandable and empowering end-users with visual representations of key information.

Dashboards are essential tools in various scientific and engineering endeavors, and trame supports creating dashboards by organizations, including the Nuclear Energy Advanced Modeling and Simulation (NEAMS) program of the U.S. Department of Energy-Office of Nuclear Energy (DOE-NE).

The NEAMS program develops advanced modeling and simulation tools and capabilities to expedite the deployment of advanced nuclear energy technologies, including light-water reactors (LWRs), non-light-water reactors (non-LWRs), and advanced fuels. One of the NEAMS Toolkit codes is the Virtual Environment for Reactor Analysis (VERA). VERA is the NEAMS LWR multiphysics code suite. It integrates physics components based on science-based models and state-of-the-art numerical methods (see <https://vera.ornl.gov/> and <https://neams.inl.gov/>).

We have innovatively created a [trame-based science and engineering dashboard for VERA](https://github.com/Kitware/VERACore) called VERACore [[4](https://www.kitware.com/veracore-trame-in-application/)], a tool that holds immense potential in the analysis and visualization of VERA results as researchers search for solutions and insights for the design, operation, safety, and performance optimization of current and future nuclear light-water reactors.

![](https://www.kitware.com/main/wp-content/uploads/2024/08/image3-1024x727.png)

**Figure**: The Virtual Environment for Reactor Applications (VERA) dashboard with VTK interactive visualization, Plotly graphs, and custom visualization widgets for navigating to specific pin locations in a 73-thousand-plus pin light-water reactor.

VERACore leverages existing widget and visualization libraries and tools like Vuetify and Plotly.

![](https://www.kitware.com/main/wp-content/uploads/2024/08/image4.png)

![](https://www.kitware.com/main/wp-content/uploads/2024/08/image6.png)

![](https://www.kitware.com/main/wp-content/uploads/2024/08/image7.png)

**Figure**: (a) a Plotly axial plot component, (b) a Vuetify Table component, and (c) a Plotly time plot.

VERACore utilizes VTK for 3D volume visualization views.

![](https://www.kitware.com/main/wp-content/uploads/2024/08/image11.png)

**Figure**: A ParaView volume visualization component.

If necessary or desired, trame allows for the creation and seamless integration of specialized components based on HTML/CSS, Vue, and more. VERACore uses sophisticated custom widgets to navigate these massive data sets from core view down to pellet view.

![](https://www.kitware.com/main/wp-content/uploads/2024/08/image14.png)

![](https://www.kitware.com/main/wp-content/uploads/2024/08/image12-493x1024.png)

![](https://www.kitware.com/main/wp-content/uploads/2024/08/image5-1.png)

**Figure**: Custom navigational widgets (a) core view for assembly navigation, (b) axial view for vertical navigation, and (c) assembly view for pin/pellet navigation.

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

[2] trame: trame: Architecture and Capabilities, June 15, 2024. <https://www.kitware.com/trame-architecture-and-capabilities/>

[3] Heidari, Z., and Posenato Garcia, A., “Austin Chalk”, Digital Rocks Portal, 2016. [Online]. Available: <http://www.digitalrocksportal.org>. [Assessed: 24-May-2024]

[4] Avery, P., Jourdain, S., O’Leary, P., and Schroeder, W., VERACore: trame in Application, January 18, 2023. <https://www.kitware.com/veracore-trame-in-application/>

Tags:

[ParaView](https://www.kitware.com/tag/paraview/) | [Scientific Computing](https://www.kitware.com/tag/scientific-computing/) | [Trame](https://www.kitware.com/tag/trame/) | [Visualization](https://www.kitware.com/tag/visualization/) | [VTK](https://www.kitware.com/tag/vtk/) | [web](https://www.kitware.com/tag/web/)

