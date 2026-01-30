[post](https://www.kitware.com/trame-revolutionizing-visual-analytics-with-python/)

# trame: Revolutionizing Visual Analytics with Python

August 3, 2023

[Sebastien Jourdain](https://www.kitware.com/author/sebastien-jourdain/ "Posts by Sebastien Jourdain"), [Patrick Avery](https://www.kitware.com/author/patrick-avery/ "Posts by Patrick Avery"), [Will Schroeder](https://www.kitware.com/author/will-schroeder/ "Posts by Will Schroeder") and [Patrick O'Leary](https://www.kitware.com/author/patrick-oleary/ "Posts by Patrick O'Leary")

![](https://www.kitware.com/main/wp-content/uploads/2023/08/trame-featured2.jpg)

In today’s data-driven world, the ability to effectively analyze and visualize complex information is crucial. Visual analytics combines analytical reasoning with interactive visual interfaces to facilitate the exploration, analysis, and understanding of complex data and systems. The ability to visually represent data interactively and intuitively allows end-users to discover patterns, trends, and insights that may otherwise go unnoticed. However, creating visual analytics tools that are versatile, user-friendly, and compatible across various computing platforms can be a daunting task.

## The Challenges of Building Visual Analytics Tools

Creating effective visual analytics tools can be challenging, especially when considering modern applications’ diverse computing environments and requirements. Some of these challenges include:

* Supporting various computing platforms, including mobile, desktop, Jupyter, high-performance computing (HPC), and cloud.
* Ensuring compatibility with different operating systems, such as Linux, macOS/iOS, and Windows.
* Integrating with various programming languages, such as Python, C++, and JavaScript.
* Working with diverse graphics libraries, including OpenGL, Vulkan, Metal, ANARI, and WebGPU.
* Developing client-server applications that handle large data processing and computational loads.
* Creating portable user interfaces (UIs) across computing platforms.
* Developing web-based applications at a rapidly changing web pace.

## Introducing trame: A Breakthrough in Visual Analytics

![NYC Uber Ridesharing Data. Showing visualizations of data from around NYC, JFK Airport, La Guardia Airport and Newark Airport.](https://www.kitware.com/main/wp-content/uploads/2023/08/image6-1024x585.jpg)

*[trame](https://kitware.github.io/trame/index.html)* is a powerful and innovative solution that addresses the challenges of building visual analytics tools. Its open source Python framework enables developers to create visually stunning and interactive applications with scientific visualizations. trame simplifies the process of building web-based applications with its seamless integration of open source components, including VTK, ParaView, and Plotly. This allows developers to focus on the data analysis and visualization aspects without needing extensive web development knowledge.

1. **Cross-Platform Compatibility:** trame supports various computing platforms, including mobile, desktop, Jupyter, HPC, and cloud.
2. **Integration with Open-Source Libraries:** trame seamlessly weaves together powerful open source components, including VTK and ParaView, to provide a simple and easy-to-use platform for creating visual analytics applications with scientific visualizations.
3. **Easy-to-Use UI Creation:** trame provides a simple and intuitive way to create UIs for visual analytics applications. By incorporating the Vuetify library, developers can easily design beautiful and interactive UI components, making their applications more user-friendly and visually appealing.
4. **Python Integration:** trame is primarily built on Python, making it accessible to many developers. With trame, developers can leverage the integration capabilities to utilize existing platforms like Altair, Vega, Plotly, Matplotlib, PyVista, and Vuetify and incorporate new open platforms like FormKit, Grid-Layout, Monaco, and Xterm into visual analytics applications.
5. **Seamless Client-Server Communication:** trame handles client-server coordination and state transfer transparently, enabling seamless communication between the front-end and back-end of the application. This capability allows for efficient processing and rendering, whether it’s performed on the client-side or server-side.

## The Benefits of trame: Simple, Powerful, and Innovative

The name ***trame*** means “***the core that ties things together***” in French, which reflects the framework’s purpose of simplifying the development process. trame offers several key advantages that set it apart from other frameworks:

### Simplicity

trame simplifies the development process by providing a clear and intuitive API for building applications. With trame, developers can focus on the data, analysis, and visualization without the complexities of web development. The framework enables developers to build powerful applications without extensive knowledge of web technologies quickly.

![Orchestration of components from application to trame.](https://www.kitware.com/main/wp-content/uploads/2023/08/image7-1024x370.jpg)

Building a trame application is just a matter of orchestrating the various components of the application leveraging the Python API for interacting with state, events, widgets, and UI conveniently and transparently.

### Power and Flexibility

Various tools and frameworks are available to build visual analytics applications, but only trame can provide full-featured interactive 3D visualization. trame harnesses the power of industry-leading, best-in-class platforms like VTK and ParaView to provide complete control over the processing for analysis and 3D visualization. Developers can leverage the extensive capabilities of these platforms while benefiting from trame’s simplified integration. And the flexibility of either local rendering or remote rendering is seamlessly exposed in trame through a single method call.

![Screenshot of the Mesh Viewer](https://www.kitware.com/main/wp-content/uploads/2023/08/image4-1024x585.jpg)

### Rich Features and Integration

trame leverages existing state-of-the-art libraries and tools. This integration enables developers to utilize the full capabilities of these libraries and tools within their trame applications to create compelling user interfaces and interactive visualizations without reinventing the wheel. trame’s integration capabilities extend beyond the built-in libraries and tools, enabling seamless integration with other popular systems like PyVista and PyTorch.

![trame altair charts showing US Income by state](https://www.kitware.com/main/wp-content/uploads/2023/08/image2-1024x586.jpg)

![trame altair chart showing scatter matrix](https://www.kitware.com/main/wp-content/uploads/2023/08/image1-1024x586.jpg)

### Portability and Deployment

trame applications can be deployed on local desktops to remote clouds. This flexibility allows end-users to access web-based trame client-server across different computing environments. Wherever the application runs, trame provides a seamless, consistent experience.

![MStar Simulation](https://www.kitware.com/main/wp-content/uploads/2023/08/image8-1024x675.jpg)

### Open Source

trame is open source and licensed under the Apache License Version 2.0, allowing developers to create their own open source or commercial applications without licensing restrictions. Whether you’re building applications for research, commercial use, or personal projects, trame offers a flexible and reliable platform to bring your visual analytics ideas to life.

## Getting Started with trame

You can start building interactive visual analytics applications with trame by following these simple steps.

**Get hands-on guidance from one of the trame developers at Kitware! Register for our upcoming “[Intro to trame](https://www.kitware.com/courses/trame/)” training course.**

1. **Install trame –** Begin by installing trame using pip, a package manager for Python:

```
pip install trame trame-vuetify trame-vtk
```

2. **Define application logic –** Next, create the processing functions in plain Python and define the state shared with the UI. This task includes defining the data analysis algorithms and any parameters the end-user can adjust.

3. **Reactive to state changes –** Define methods that respond to changes in the shared state. For example, if a slider is used to adjust a sampling parameter, define a method that updates the sampling algorithm based on the new slider value.

4. **Design the UI –** Build a beautiful and accessible UI by defining the layout of your application and connecting the state and functions to the UI elements directly. trame provides a built-in Material Design widget library accessible through Vuetify (https://vuetifyjs.com/en/components/all/), making creating visually appealing UI components easy.

5. **Run the Application –** Once the application is ready, it can be run locally as a desktop (still a client-server) application.

```
python app.py --port 1234
```

![Python code for trame](https://www.kitware.com/main/wp-content/uploads/2023/08/image3-751x1024.png)

![Screenshot of VTK Local Rendering of a triangle shape](https://www.kitware.com/main/wp-content/uploads/2023/08/image5-1024x833.png)

## Make Your Data Come to Life with trame

trame is a game-changer in the field of visual analytics. With its focus on analysis and visualization, trame removes the complexities of web development and enables developers to focus on what matters most: unlocking insights in their data. Start exploring trame and see how it can revolutionize your data analysis workflows. For more information, including tutorials, the discourse forum, and other helpful resources, visit the [trame website](https://kitware.github.io/trame/).

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

[Open Source](https://www.kitware.com/tag/open-source/) | [Python](https://www.kitware.com/tag/python/) | [Trame](https://www.kitware.com/tag/trame/) | [visual analytics](https://www.kitware.com/tag/visual-analytics/) | [Visual Data](https://www.kitware.com/tag/visual-data/)

