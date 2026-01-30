[post](https://www.kitware.com/a-framework-for-next-generation-visual-workflows-in-scientific-computing/)

# A Framework for Next-Generation Visual Workflows in Scientific Computing

December 4, 2025

[Berk Geveci](https://www.kitware.com/author/berk-geveci/ "Posts by Berk Geveci"), [Patrick O'Leary](https://www.kitware.com/author/patrick-oleary/ "Posts by Patrick O'Leary"), [Cory Quammen](https://www.kitware.com/author/cory-quammen/ "Posts by Cory Quammen"), [Bob O'Bara](https://www.kitware.com/author/bob-obara/ "Posts by Bob O'Bara") and [David Thompson](https://www.kitware.com/author/david-thompson/ "Posts by David Thompson")

![Screenshots of several scientific visualizations and simulations.](https://www.kitware.com/main/wp-content/uploads/2025/12/SC25-Blog-Feature.jpg)

The 21st century has witnessed remarkable advances in computational and experimental sciences, with processing power expanding from terascale to exascale—a million-fold increase in capability—and experimental devices achieving unprecedented scales of data collection. Visualization technologies have kept pace, as modern GPUs now enable the analysis and rendering of complex datasets that were once out of reach. At the same time, artificial intelligence has disruptively reshaped research by not only augmenting existing methods but also transforming the problems we can address and the ways we solve them. Scientific and engineering work now depends on the integration of experiments, large-scale computation, and AI, involving diverse participants from domain experts to decision-makers. Yet, traditional tools such as documents, charts, spreadsheets, and static visualizations are no longer sufficient to support collaboration.

Visual workflows address this gap by providing interactive, domain-aware environments that make complex pipelines understandable and actionable. They democratize access to AI, simulations, and experiments by lowering technical barriers, enabling the transfer of expertise by providing both specialists and non-specialists with productive entry points, and enhancing analysis and communication by allowing users to interrogate results dynamically and present them clearly to diverse audiences. Interactive visual workflows enable activities such as AI/experiment/simulation-to-insight exploration, AI-assisted validation, automated report generation, and migration of traditional desktop tools into collaborative web applications. Their visual nature allows users to see and then manipulate the workflow process, not just the experimental or simulation data. By making processes transparent, adaptive, and inclusive, visual workflows shorten iteration cycles, accelerate discovery, and empower all participants to contribute insights directly.

The next generation of research and design will rely on such interactive visual workflows, which, by extending powerful tools beyond computational specialists to entire collaborative communities, can unlock new levels of innovation and discovery.

## Visualization as a Tool for Accessibility and Insight

Visualization is fundamental to interactive visual workflows because it transforms raw data into forms the human eye and brain can quickly grasp. Numbers in files or static tables cannot match the speed and clarity of visual analysis, where patterns, anomalies, and structures often emerge only through inspection. By working visually, scientists, engineers, and researchers expand cognitive bandwidth, accelerate understanding, and foster collaboration. Well-designed visualizations make insights accessible to both experts and non-experts, creating a shared ground for decision-making.

## Challenges

Modern research and engineering workflows are difficult to manage. They involve massive datasets that must be cleaned, wrangled, streamed, and stored at scale. They span many stages—from simulation and experiment setup to AI-driven analysis and visualization—and depend on diverse tools that rarely interoperate smoothly. Each step adds layers of complexity, from managing workflow attributes and assets to ensuring data integrity and reproducibility. While the AI, simulation, or experiment may complete in only weeks on 21st-century computational platforms, the resulting data can be so large that analysis and visualization are constrained to a read-once, derive-once workflow, in which each dataset is read only once to produce a reduced or derived product. Even under this limited approach, the process can take many months and may spill into the next computational allocation cycle.. This delay becomes a major barrier, slowing iteration and extending the time-to-discovery. The central challenge is not the absence of capable tools, but the difficulty of integrating them into coherent workflows that support collaboration, efficiency, and timely insight.

| Challenge | Value Proposition |
| --- | --- |
| **Democratization of Advanced Capabilities** |  |
| Powerful AI, simulation, experiment, analysis, and visualization tools remain concentrated in the hands of specialists, leaving non-experts dependent on intermediaries and slowing collaborative progress. | Democratizing advanced capabilities empowers all participants in a workflow to contribute to insights directly, fostering inclusive collaboration and innovation. |
| **Seamless Transfer of Expertise** |  |
| The flow of expertise between developers of AI, simulations, and experiments and their end users is slow and inefficient. Specialists become bottlenecks, and tools are often either too simple or too complex. | Interactive visual workflows that speed expertise transfer and provide customizable, domain-specific environments allow experts and non-experts to engage productively without unnecessary complexity. |
| **Insightful Analysis and Communication** |  |
| Traditional tools for analysis and visualization are too rigid or too general. Researchers need to explore results dynamically, while stakeholders need clear and compelling views. | Interactive visual workflows accelerate discovery and facilitate the communication of insights across diverse audiences, enabling more informed and collaborative decision-making. |
| **Shortening Time-to-Discovery** |  |
| Complex workflows and fragmented tools often result in lengthy delays between data generation and actionable insights. While simulations, experiments, or AI runs may finish in only weeks, the analysis and visualization of their results can take months. | Integrated, interactive visual workflows shorten the path from raw data to understanding. By reducing months of post-processing into immediate, adaptive visual exploration, they enable faster prototyping, validation, and decision-making. |

## Toward a Next Generation Platform

Over the past two decades, the visualization community has developed systems capable of interactively handling vast datasets. Tools such as ParaView exemplify these capabilities, but they remain monolithic and best suited for experts. What is needed now is a flexible platform that spans various use cases, encompassing desktop, Jupyter, and web environments while lowering development effort.

The urgency is apparent. Today, scientists, engineers, and researchers can complete an extensive simulation, experiment, or AI campaign in a matter of weeks on advanced computational platforms. Yet, the analysis and visualization of the resulting data can still exceed computational allocation boundaries, delaying discovery and slowing innovation. This gap between data generation and actionable insight is now one of the most pressing barriers in scientific and engineering practice.

The answer lies in a modular platform. This platform must build on decades of investment in frameworks like VTK and ParaView while adopting modern interface technologies. It should support workflows ranging from physics-based AI to combined experiment–simulation pipelines, end-to-end simulations, and cross-disciplinary analytics. By addressing the challenges of democratization, expertise transfer, communication, and time-to-discovery, this platform can collapse months of post-processing into interactive visual workflows that deliver insight at the pace of computation.

At Kitware, we have been developing components for this platform while transforming our existing frameworks to support the future of visual workflows. The core is written in C++ (with CUDA, HIP, and SYCL) for optimal performance, and Python is used as the integration language to reduce barriers to entry while maintaining flexibility and speed. On top of this foundation, we employ trame, our visual workflow integration framework, which allows developers to build components, combine them into complex workflows, and deliver them seamlessly on desktops, in Jupyter notebooks, or on the web. Backed by HPC resources such as cloud or supercomputers, these workflows reduce the cycle from months to days.

## Core Components

### Run-Everywhere Front-End

Modern workflows demand applications that run seamlessly across desktops, Jupyter notebooks, and the web. Our front-end layer provides this portability, ensuring that visual workflows are accessible wherever researchers and engineers work, and that deliver the same components across environments without duplication of effort.

**Trame** is the glue that binds the platform together. As a Python-based framework for creating interactive visual workflows, trame integrates scientific libraries, AI tools, and modern web UI components. It lowers technical barriers, supports rapid development, and ensures interoperability between front-end and computational backend frameworks. By doing so, it creates an environment where visual workflows can be composed, extended, and shared.

### Backend Frameworks

We built the core of the platform on proven frameworks that address the significant gaps in today’s workflows:

* **VTK** provides a comprehensive set of libraries for I/O, data models, analysis, rendering, and graphics.
* **ParaView** builds on VTK to provide distributed computing client–server operation while scaling from laptops to supercomputers. Together VTK and ParaView handle massive datasets, ensure high performance, and provide the visualization backbone needed for both experts and non-experts to interrogate complex results.
* **SMTK** addresses the complexity of workflow attributes and asset management, enabling users to define, track, and reuse workflow resources, including parameters, geometries, meshes, materials, and boundary conditions. SMTK supports flexible integration with the other frameworks, enabling interactive workflows that connect setup, execution, analysis, and visualization as well as providing ways of decomposing a workflow into a set of interactive tasks.
* **Fides** simplifies access to simulation and experimental outputs by streaming data at scale, reducing friction in moving results from producers to consumers.
* **Catalyst** enables the in-situ coupling of simulations and experiments with analysis and visualization, ensuring the processing of data as it is generated, rather than months later. Fides and Catalyst close gaps between data producers and data consumers, allowing workflows to incorporate real-time analysis, AI training, and experimental streaming without costly intermediate steps.

Together, these backend frameworks tackle the most challenging tasks: massive data volumes, data cleaning and wrangling, multi-stage workflows that rely on diverse tools, and the complexities of managing assets and ensuring reproducibility.

### Desktop Applications

For off-the-shelf use, our desktop applications make these capabilities directly accessible to scientists and engineers:

* **ParaView** for scalable visualization and analysis of massive datasets.
* **CMB** (Computational Model Builder) for building and managing complex simulation workflows.
* **Tomviz** for interactive analysis and visualization of large-scale tomography data.

These applications embody the power of the backend frameworks while providing usable, production-ready environments. They serve both as entry points for new users and as full-featured platforms for experts.

## Examples

<table>
  <tr>
    <td align="center" width="33%">
      <a href="#example-01">
        <img src="https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-1.jpg" width="240" alt="Example 1">
      </a>
    </td>
    <td align="center" width="33%">
      <a href="#example-02">
        <img src="https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-2.jpg" width="240" alt="Example 2">
      </a>
    </td>
    <td align="center" width="33%">
      <a href="#example-03">
        <img src="https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-3.jpg" width="240" alt="Example 3">
      </a>
    </td>
  </tr>
  <tr>
    <td align="center" width="33%">
      <a href="#example-04">
        <img src="https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-4.jpg" width="240" alt="Example 4">
      </a>
    </td>
    <td align="center" width="33%">
      <a href="#example-05">
        <img src="https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-5.jpg" width="240" alt="Example 5">
      </a>
    </td>
    <td align="center" width="33%">
      <a href="#example-06">
        <img src="https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-6.jpg" width="240" alt="Example 6">
      </a>
    </td>
  </tr>
  <tr>
    <td align="center" width="33%">
      <a href="#example-07">
        <img src="https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-7.jpg" width="240" alt="Example 7">
      </a>
    </td>
    <td align="center" width="33%">
      <a href="#example-08">
        <img src="https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-8.jpg" width="240" alt="Example 8">
      </a>
    </td>
    <td align="center" width="33%">
      <a href="#example-09">
        <img src="https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-9.jpg" width="240" alt="Example 9">
      </a>
    </td>
  </tr>
  <tr>
    <td align="center" width="33%">
      <a href="#example-10">
        <img src="https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-10.jpg" width="240" alt="Example 10">
      </a>
    </td>
    <td align="center" width="33%">
      <a href="#example-11">
        <img src="https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-11.jpg" width="240" alt="Example 11">
      </a>
    </td>
    <td align="center" width="33%">
      <a href="#example-12">
        <img src="https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-12.jpg" width="240" alt="Example 12">
      </a>
    </td>
  </tr>
  <tr>
    <td align="center" width="33%">
      <a href="#example-13">
        <img src="https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-13.jpg" width="240" alt="Example 13">
      </a>
    </td>
    <td align="center" width="33%">
      <a href="#example-14">
        <img src="https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-14.jpg" width="240" alt="Example 14">
      </a>
    </td>
    <td align="center" width="33%">
      <a href="#example-15">
        <img src="https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-15.jpg" width="240" alt="Example 15">
      </a>
    </td>
  </tr>
  <tr>
    <td align="center" width="33%">
      <a href="#example-16">
        <img src="https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-16.jpg" width="240" alt="Example 16">
      </a>
    </td>
    <td align="center" width="33%">
      <a href="#example-17">
        <img src="https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-17.jpg" width="240" alt="Example 17">
      </a>
    </td>
    <td align="center" width="33%">
      <a href="#example-18">
        <img src="https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-18.jpg" width="240" alt="Example 18">
      </a>
    </td>
  </tr>
  <tr>
    <td align="center" width="33%">
    </td>
    <td align="center" width="33%">
        <a href="#example-19">
        <img src="https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-19.jpg" width="240" alt="Example 20">
      </a>
    </td>
    <td align="center" width="33%">
    </td>
  </tr>
</table>

The power of this platform is best understood through concrete use cases. By combining run-everywhere front ends, trame, robust backend frameworks, and production-ready desktop applications, researchers can assemble visual workflows that address real challenges. The following examples illustrate how these components work together to manage massive datasets, streamline data movement, connect simulations with analysis, and simplify complex workflows into environments that accelerate discovery.

<a id="example-01"></a>
Convergent Science uses ParaView and Catalyst in their CONVERGE software to improve capture of high-speed physical phenomena inside internal combustion engines such as knocking. Catalyst allows saving isosurfaces at a rate much higher than is possible than saving full datasets and can reduce file output from ~100 gigabytes to ~100 megabytes in a typical simulation. Read the blog post [In Situ Data Analysis Brings Faster Results and Accelerated Insights](https://www.kitware.com/in-situ-data-analysis-brings-faster-results-and-accelerated-insights/) to find out more.   
  
Frameworks used: ParaView, Catalyst

![](https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-1.jpg)

<a id="example-02"></a>
This figure shows an OpenFoam simulation of a boat inside a virtual wave tank. The application was created for Sandia National Laboratories’ Water Power Technologies Program. Applications like this can greatly reduce expenses – compared to either a physical wave tank or the manual creation of simulation inputs.   
  
Frameworks used: SMTK, CMB, VTK, ParaView.

![](https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-2.jpg)

<a id="example-03"></a>
This figure shows an OpenFOAM workflow Kitware created for Sandia National Laboratories to evaluate the reactions of objects to wave motion. What’s shown is a ship being inserted into the tank. The box around the aft portion of the vessel is a preview of the OpenFOAM overset mesh (snapped to the ship exterior) that has been crinkle-clipped to reveal the forward part of the ship.This allows inspection of meshes before running a simulation.   
  
Frameworks used: SMTK, VTK, ParaView

![](https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-3.jpg)

<a id="example-04"></a>
Simulation workflows often demand diverse computational resources. For instance, a high-energy physics workflow, leveraging SLAC’s Advanced Computational Electromagnetics 3D Parallel (ACE3P) tools, is employed in the design of particle accelerators and related instrumentation. In this scenario, the user initiates the workflow on their local machine, while the intensive computations are executed on the High-Performance Computing (HPC) resources at NERSC. Users have the flexibility to perform remote post-processing on the HPC machine or conveniently transfer results for local processing, all within the same integrated tool.

Frameworks used: SMTK, CMB, ParaView, VTK

![](https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-4.jpg)

<a id="example-05"></a>
Developed for the Cleveland Clinic, this workflow showcases the intricate process of creating and annotating anatomical models. This involves segmenting and processing medical images and meshes. Users needed efficient ways to create and edit surface selections, remesh surfaces, and generate volumetric meshes from them, as well as to incorporate detailed ontologies into the annotation process.
  

Frameworks used: SMTK, CMB, ParaView, VTK

![](https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-5.jpg)

<a id="example-06"></a>
Computational fluid dynamics workflows, like OpenFOAM-based wind tunnel simulation shown above, require users to perform various tasks: problem setup, mesh generation, simulation processing, and post-processing. Decomposing these complex workflows into manageable, guided tasks is crucial for effective user management.

Frameworks used: VTK, CMB ParaView, SMTK.

![](https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-6.jpg)

<a id="example-07"></a>
Computational fluid dynamics (CFD) is integral to whole-body circulatory system workflows, supporting the development of new surgical procedures and patient health monitoring. These workflows often run continuously, necessitating in situ visualization for real-time observation by physicians and researchers.

The accompanying images illustrate work from the Randles Lab at Duke University, where methods for whole-body circulatory system simulation are being developed, modeling down to individual blood cells using the HARVEY fluid dynamics solver. The video showcases blood flow within a representative human aorta, originating at the ascending aorta, traversing the aortic arch, and concluding at the descending aorta. As the fluid enters the aortic arch, it diverges into the right and left subclavian and common arteries. To mimic in vivo circulation, the flow constantly pulses throughout the animation. Frameworks used: ParaView, ParaView Catalyst

Frameworks used: ParaView, Catalyst

![](https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-7.jpg)

<a id="example-08"></a>
Parsli is a VTK-based viewer for fault system kinematics that enables rapid exploration and export of time-based animations. By leveraging advanced 3D graphics, interactive visualization, and high performance, we’ve transformed a workflow that once took days into one that now takes minutes—or even seconds—for initial validation and analysis. Its ease of use and installation has also encouraged the community to revisit past runs, uncovering phenomena that previously slipped through the cracks of the previous toolchain.

Frameworks used: Trame, VTK

![](https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-8.jpg)

<a id="example-09"></a>
Visualizing and exploring multivariate/multimodal volumes, common in material modeling and medical simulations, demands innovative techniques. These techniques are crucial for revealing significant trends and effectively communicating discoveries to both domain experts and general audiences. As an example, the accompanying figure presents an x-ray fluorescence tomography dataset of a mixed ionic-electronic conductor (MIEC), analyzed using Kitware’s MultivariateView tool.

Frameworks Used: trame, VTK

![](https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-9.jpg)

<a id="example-10"></a>
High-resolution 3D characterization is crucial for workflows in materials science and nanoscience. This requires advanced image processing, data analysis, visualization, and reproducibility. Integrating these features into a single environment streamlines the entire research pipeline, from raw data to publication-quality 3D renderings. Furthermore, incorporating capabilities like Python scripting and custom extensions expands its applicability to diverse workflows. Tomviz is an example that offers visualization, processing, and analysis for tomographic data. The image above from Tomviz demonstrates drawing a cropping region around 3D reconstructed PtCu nanoparticles, known for their effectiveness as fuel cell electrocatalysts.

![](https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-10.jpg)

<a id="example-11"></a>
QuickView is a Trame + ParaView-powered tool for exploring atmospheric output from the E3SM Atmosphere Model (EAM). It provides an intuitive, no-scripting interface for multivariate visualization, model validation & verification and supports EAM v2, v3 (and in development v4) data formats – which simplifies the atmosphere modeling and analysis workflows.

![](https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-11.jpg)

<a id="example-12"></a>
Pan3D is a fast, highly interactive visualization tool for Xarray datasets — a standard format for large, multidimensional arrays in climatology and other geospatial fields. Built on Trame and VTK, it leverages seamless interoperability between VTK and Xarray for efficient data exchange. A defining feature of Pan3D is its collection of Explorers (pictured above): lightweight, task-focused analysis apps that cut through the clutter of traditional, full-featured visualization tools such as ParaView. These explorers enable teams to craft bespoke, purpose-driven solutions, fostering collaboration and clear role separation.

Platforms: VTK and trame

![](https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-12.jpg)

<a id="example-13"></a>
In collaboration with NASA and the University of Colorado Boulder, Kitware is expanding the Catalyst in situ analysis platform to enable powerful AI models to access simulation data in memory at runtime for advanced model training and inference to improve upon existing simulation results. This approach empowers existing, validated simulation codes to leverage modern AI tools without complex and costly code integrations.

![](https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-13.jpg)

<a id="example-14"></a>
Rotorcraft simulation workflows present a complex, multidisciplinary challenge, as they necessitate the integration of moving-body aerodynamics with structural dynamics for rotor blade deformation, and vehicle flight dynamics and controls. Furthermore, the extensive data generated during a rotorcraft CFD simulation, stemming from numerous timesteps, can be substantial.

By incorporating in situ capabilities directly into the simulation workflow, developers and analysts can scrutinize crucial variables at each timestep, thereby avoiding the significant overhead associated with I/O and storage. This methodology not only optimizes HPC resource utilization but also facilitates real-time steering, swift validation, and more insightful diagnostics during protracted simulations. The accompanying images illustrate this approach using CREATE’s HELIOS framework, which leverages ParaView Catalyst for in situ visualization and analysis.

![](https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-14.jpg)

<a id="example-15"></a>
ArrowFlow, focuses on broadening simulation usage by allowing domain scientists to easily create templates and expose them to remote engineers. Its curated web interface for input simulation parameters and easy to use post-processing tools enables quick exploration for validation of settings to use with factory mixer, drier or any machinery setup into the system.
ArrowFlow relies on M-Star CFD™ for its solver and ParaView for its post-processing. Trame is exposing templates, solver and post-processing visualization in an easy to use solution.

Frameworks used: Trame, ParaView

![](https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-15.jpg)

<a id="example-16"></a>
Displaying complex microstructural data is an integral part of many material science workflows and enables researchers to explore and understand the intricate geometries and properties of materials. This integration is crucial for analyzing simulated and experimental data, facilitating insights into material behavior, and accelerating the discovery of new materials with desired characteristics. The above image shows 3D precipitate morphology from a nickel based superalloy. Reconstruction was performed by DREAM3D-NX and subsequently visualized within DREAM3D-NX using VTK to provide advanced 3D rendering and visualization capabilities essential for material science research.

![](https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-16.jpg)

<a id="example-17"></a>
Acoustic modal analysis of a car cabin by [Undabit Acoustic Simulations](https://undabit.com/). Identifying vibration modes that may impact acoustic properties is crucial, as acoustic resonances can amplify noise generated by the engine, a phenomenon often referred to as “booming.” Understanding the frequencies at which resonance occurs and the spatial distribution of the resonant field is essential. Visualization with ParaView’s advanced ray-tracing capabilities. Source: [Automotive Acoustic Simulation Post-processing with ParaView](https://www.kitware.com/automotive-acoustic-simulation-post-processing-with-paraview/)

![](https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-17.jpg)

<a id="example-18"></a>
[![Topological analysis of terrain elevation is crucial for surface water workflows, such as estimating water runoff zones. This analysis allows for the identification and classification of critical points like peaks and pits, the segmentation of watershed boundaries, and the highlighting of ridges and valleys. These elements are essential for understanding the terrain’s structure. In the accompanying figure, colored regions indicate areas feeding into the blue river network, while red paths denote ridges. Platforms used: ParaView and its Topology Toolkit (TTK) plugin. For more information, see [Practical Use Cases for TTK](https://www.kitware.com/practical-use-cases-for-ttk/).

![](https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-18.jpg)

<a id="example-19"></a>
Live visualization of a drive train digital twin. Data from 30 temperature sensors on an electric motor are interpolated onto a digital twin model for live display in ParaView. This allows engineers from TotalEnergies to have direct access to a visualization showcasing the measured elements as it is running, and perform analysis and visualization within ParaView, either using the whole set of existing filters or even implementing their own. Platforms used: ParaView. More information at [Build, Control and Run Digital Twins with ParaView](https://www.kitware.com/build-control-and-run-digital-twins-with-paraview/).

![](https://www.kitware.com/main/wp-content/uploads/2025/10/supercomputing-2025-19.jpg)

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

[Artificial Intelligence](https://www.kitware.com/tag/artificial-intelligence/) | [Catalyst](https://www.kitware.com/tag/catalyst/) | [CMB](https://www.kitware.com/tag/cmb/) | [Data Visualization](https://www.kitware.com/tag/data-visualization/) | [ParaView](https://www.kitware.com/tag/paraview/) | [Scientific Computing](https://www.kitware.com/tag/scientific-computing/) | [simulations](https://www.kitware.com/tag/simulations/) | [SMTK](https://www.kitware.com/tag/smtk/) | [Tomviz](https://www.kitware.com/tag/tomviz/) | [Trame](https://www.kitware.com/tag/trame/) | [Visual Workflows](https://www.kitware.com/tag/visual-workflows/) | [VTK](https://www.kitware.com/tag/vtk/)
