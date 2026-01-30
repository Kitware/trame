[post](https://www.kitware.com/a-year-of-innovation-our-most-impactful-projects-and-technologies-in-2024/)

# A Year of Innovation: Our Most Impactful Projects and Technologies in 2024

December 2, 2024

[Samantha Schmitt](https://www.kitware.com/author/samantha-schmitt/ "Posts by Samantha Schmitt")

![A Year of Innovation: Our Most Impactful Projects and Technologies in 2024](https://www.kitware.com/main/wp-content/uploads/2024/12/2024-Year-of-Innovation-Feature.jpg)

As 2024 comes to a close, we want to take a moment to reflect on a year marked by remarkable achievements and technological strides at Kitware. From transforming environmental monitoring to advancing medical research and training, Kitware’s collaborative efforts have resulted in innovative solutions that positively impact our partners and community. This article highlights some of our most impactful projects and open source tools in 2024 and demonstrates our commitment to solving real-world challenges with cutting-edge technology in the years to come.

## Transforming Environmental Monitoring with Edge Computing

![Left: Adam Romlein, senior R&D engineer at Kitware, prepares for a test flight out of Nome, AK.
Right: The 9-camera system we installed in the belly of the aircraft. Three color cameras are at the top, three UV cameras are in the middle, and three IR cameras are at the bottom. This configuration captures a wide swath of imagery in flight to maximize the area covered.](https://www.kitware.com/main/wp-content/uploads/2024/12/year-innovation-1-1024x492.jpg)

Left: Adam Romlein, senior R&D engineer at Kitware, prepares for a test flight out of Nome, AK.  
Right: The 9-camera system we installed in the belly of the aircraft. Three color cameras are at the top, three UV cameras are in the middle, and three IR cameras are at the bottom. This configuration captures a wide swath of imagery in flight to maximize the area covered.

In 2024, the **NOAA KAMERA** project stood out for its innovative edge computing solution designed to enhance environmental monitoring through advanced real-time imaging and analysis. Kitware’s **KAMERA** system has a robust 9-camera setup and can capture images across ultraviolet, infrared, and color modalities, enabling precise detection of marine mammals. Equipped with ruggedized compute units and GPUs, the system enables real-time deep learning processing and immediate data analysis, significantly speeding up survey results. Field tests confirmed **KAMERA’s** durability in challenging Arctic conditions and its ability to synchronize and map imagery seamlessly. With its real-time processing and precise geospatial capabilities, this system overcomes the limitations of traditional, time-intensive data review processes. This innovative technology will empower policy-makers with timely, reliable information for informed decision-making, aiding in conserving vital species and ecosystems.

To learn more about this project, read our [NOAA KAMERA Project Spotlight](https://www.kitware.com/project-spotlight-noaa-kamera/).

## Geospatial Analysis for Real-world Applications

![Illustration of two-stage heavy construction prediction. In the first stage, we run “Broad Area Search” (BAS) on a large region to identify candidate construction sites. The second stage, “Activity Characterization” (AC), refines the event boundary and estimates the probability of each construction stage over time.](https://www.kitware.com/main/wp-content/uploads/2024/12/year-innovation-2-1024x492.jpg)

Illustration of two-stage heavy construction prediction. In the first stage, we run “Broad Area Search” (BAS) on a large region to identify candidate construction sites. The second stage, “Activity Characterization” (AC), refines the event boundary and estimates the probability of each construction stage over time.

**GeoWATCH** is an AI-driven tool for analyzing sequential imagery from multiple sensors. Originally developed to find heavy construction sites and track stages of construction, such as site preparation, active building, and post-construction phases, GeoWATCH uses multi-sensor data from sources like Landsat-8, Sentinel-2, and WorldView-3. Its adaptable data sampling and neural network capabilities allow it to process different resolutions and revisit rates, making it suitable for a wide range of applications. Beyond construction, GeoWATCH supports critical efforts in disaster response and building damage assessment, providing rapid, actionable insights where they are most needed. It is also being tested for tracking honey bee movement and monitoring algal blooms, showcasing the technology’s versatility. GeoWATCH can operate in challenging conditions where space and power are limited, extending its utility from edge computing environments to field-deployed systems. With applications across environmental monitoring, agriculture, and commercial industries, we are excited about the potential GeoWATCH is bringing to geospatial analysis.

To learn more about **GeoWATCH**, [read our recent blog post](https://www.kitware.com/geowatch/).

*Acknowledgment: This research is based upon work supported in part by the Office of the Director of National Intelligence (ODNI), Intelligence Advanced Research Projects Activity (IARPA), via 2021-201100005. The views and conclusions contained herein are those of the authors and should not be interpreted as necessarily representing the official policies, either expressed or implied, of ODNI, IARPA, or the U.S. Government. The U.S. Government is authorized to reproduce and distribute reprints for governmental purposes, notwithstanding any copyright annotation therein.*

## Setting a New Standard for Interactive Web-Based Visualization

![trame-based application to examine Uber ridesharing pick-ups and drop-offs in New York City over time.](https://www.kitware.com/main/wp-content/uploads/2024/12/year-innovation-3-1024x745.jpg)

trame-based application to examine Uber ridesharing pick-ups and drop-offs in New York City over time.

**trame** has become a standout innovation, revolutionizing how interactive web-based visual applications are built. This powerful Python package bridges the gap between complex data visualization and intuitive web development, enabling users to create sophisticated web interfaces without needing extensive coding expertise. By leveraging open-source frameworks like VTK and ParaView, **trame** empowers developers to seamlessly integrate advanced 3D rendering and visualization capabilities into their web projects. The tool simplifies the deployment of visualization solutions, making high-level simulation and data analysis more accessible than ever. With micro-workflow features that streamline user interactions and offer customizable templates, **trame** allows for effortless configuration and enhanced usability. Its rapid adoption by a range of organizations underscores its impact on how researchers and developers share complex simulations and insights online. By providing a flexible and scalable platform, **trame** has redefined the landscape of web-based visualization, enhancing both user experience and collaborative opportunities.

Read the most recent blog post in our [series about trame](https://www.kitware.com/trame-micro-workflow-use-case/) to learn more about its capabilities and applications.

## Faster Simulation Results with In Situ Data Analysis

![Timeline of traditional post-processing versus in situ analysis. In a traditional simulation where post-processing is performed after the simulation is complete, a lot of time is spent writing data to disk. Post-processing then takes additional time afterward. With in situ analysis, some additional time is spent performing analysis during simulation, but significantly less time is spent writing data to disk, and results are available for review as soon as the simulation is finished.](https://www.kitware.com/main/wp-content/uploads/2024/12/year-innovation-4-1024x393.jpg)

Timeline of traditional post-processing versus in situ analysis. In a traditional simulation where post-processing is performed after the simulation is complete, a lot of time is spent writing data to disk. Post-processing then takes additional time afterward. With in situ analysis, some additional time is spent performing analysis during simulation, but significantly less time is spent writing data to disk, and results are available for review as soon as the simulation is finished.

**ParaView Catalyst** is an open source solution that integrates in situ data analysis directly within simulation workflows. This technology bypasses the traditional bottlenecks of writing large data files to disk, accelerating simulation processes and enabling immediate analysis as the simulation runs. By embedding the analysis into the simulation, engineers can access real-time results, leading to quicker design iterations and faster product development. In situ analysis significantly reduces file storage needs by producing compact analysis outputs, enabling higher-frequency data capture that reveals critical design phenomena. For example, in the automotive industry, tools like CONVERGE use **ParaView Catalyst** to analyze engine phenomena such as autoignition, capturing crucial data without excessive storage demands. This approach not only cuts down simulation time by up to 20% but also transforms how complex physical processes are understood and optimized. In situ technology like **ParaView Catalyst** drives innovation and efficiency in automotive and other engineering fields.

Read more on how [ParaView Catalyst](https://www.kitware.com/in-situ-data-analysis-brings-faster-results-and-accelerated-insights/) brings faster results and accelerated insights.

## Boosting Developer Productivity Through Exciting New CMake Feature

![An example CMake file showcasing C++20 modules.](https://www.kitware.com/main/wp-content/uploads/2024/12/year-innovation-5-1024x578.jpg)

An example CMake file showcasing C++20 modules.

Earlier this year, we announced that CMake now supports **C++20 modules**. Since CMake is the de-facto standard for building C++ code, with over 2 million downloads per month, this update will have a significant impact on the development community. This was an exciting effort involving the creation of a new standard file format that compilers need to provide to build tools like CMake. With this new feature in CMake, users can experiment with and deploy **C++20 modules**, which promises to enhance code organization and reduce compilation times. Unlike traditional header files, **C++20 modules** provide improved encapsulation and help prevent issues like multiple definitions. This development reflects Kitware’s dedication to staying at the forefront of software build innovation and aligning with the latest C++ standards. We are also continuing to add more support for modules, ensuring CMake evolves to meet the needs of developers. By facilitating faster and more manageable builds, this integration is set to benefit developers across diverse industries and applications.

Read the first blog post in our series about [C++ modules in CMake](https://www.kitware.com/import-cmake-the-experiment-is-over/).

## Ushering in ​​A New Era in Cross-Platform Dependency Management

![Spack can now be installed on Windows, in addition to Linux and MacOS.](https://www.kitware.com/main/wp-content/uploads/2024/12/year-innovation-6-1024x902.jpg)

Spack can now be installed on Windows, in addition to Linux and MacOS.

Kitware achieved a major milestone in 2024 by successfully porting **Spack** to the Windows platform, following years of collaboration with the Lawrence Livermore National Laboratory (LLNL) and other U.S. Department of Energy labs. This achievement marks a significant step forward in cross-platform dependency management, providing Windows users with access to the same powerful, configurable software stack management that Linux and macOS users have benefited from for years. By bringing **Spack** to Windows, Kitware has bridged an essential gap, enabling developers to maintain consistency when building and deploying software across different operating systems. This advancement simplifies workflows, reduces the need for manual dependency handling, and offers a unified approach to managing software environments. The impact is transformative for organizations and researchers who rely on multi-platform support for their development and deployment needs. Kitware’s work underscores its dedication to enhancing open-source tools and driving forward innovation in software development. With **Spack** now available on Windows, developers can enjoy a more comprehensive and flexible approach to cross-platform dependency management.

Read this blog post to learn more about [Spack on Windows](https://www.kitware.com/spack-on-windows-a-new-era-in-cross-platform-dependency-management/).

## Advancing Neuroimaging Analysis and Research

![Browsing results of an OTM analysis using the vtk.js viewer.](https://www.kitware.com/main/wp-content/uploads/2024/12/year-innovation-7-1024x320.jpg)

Browsing results of an OTM analysis using the vtk.js viewer.

**Web-OTM (Optimal Transport Morphometry)** set a new standard in neuroimaging analysis, providing researchers with advanced tools for comprehensive population-level studies. This web-based application leverages Unbalanced Optimal-Transport Based Morphometry to identify subtle and complex changes in neuroimaging data that traditional voxel-based morphometry might miss. By distinguishing between shifts in the amount of brain matter and its location, **Web-OTM** enables more precise and meaningful analyses. Built on VTK.js, the tool provides robust, interactive visualization powered by WebGL for smooth performance right in the browser. Researchers can effortlessly upload and preprocess their data, conduct quality control, and customize clinical variable analyses. The application’s advanced result visualization supports comprehensive exploration and interpretation, enriching neuroimaging research. With scalable deployment, **Web-OTM** puts cutting-edge analysis tools in the hands of researchers and clinicians, pushing the frontiers of neuroimaging studies forward.

Watch [Web-OTM](https://www.kitware.com/introducing-web-otm-optimal-transport-morphometry-a-web-based-application-for-advanced-neuroimaging-population-analysis/) in action.

*Acknowledgment: Research reported in this publication was supported by the National Institute Of Mental Health of the National Institutes of Health under Award Number R42MH118845. The content is solely the responsibility of the authors and does not necessarily represent the official views of the National Institutes of Health. The percentage and dollar amount of the total program or project costs are financed with federal money, and the percentage and dollar amount of the total costs are financed by nongovernmental sources.*

## Innovative De-Identification Technology for Medical Research

![ImageDePHI summarizes what metadata will be kept, deleted, or changed for each image. (Note: The data presented above is synthetic, and the slides contain mouse tissue samples.)](https://www.kitware.com/main/wp-content/uploads/2024/12/year-innovation-8-1024x512.jpg)

ImageDePHI summarizes what metadata will be kept, deleted, or changed for each image. (Note: The data presented above is synthetic, and the slides contain mouse tissue samples.)

Kitware has developed sophisticated de-identification tools for whole slide imaging (WSI) data through the NIH’s **ImageDePHI** program. This technology automatically detects and redacts protected health information (PHI) while preserving crucial clinical metadata, enabling important research on rare conditions, such as pediatric cancers. The software is built to address complex challenges like large file sizes and overlapping barcodes, ensuring secure and precise data handling. Kitware’s efforts help researchers share medical images while safeguarding patient privacy, promoting greater collaboration in the medical field. As the project progresses into Phase 2, Kitware is incorporating user feedback to refine the software, adding features like command-line interfaces and improving its adaptability for real-world use. By offering these tools as open source solutions, Kitware is empowering the research community with accessible, reliable resources. **ImageDePHI** is poised to have a significant impact on medical research, enabling secure data sharing and the comprehensive analysis of valuable imaging data.

Learn more about the [ImageDePHI program](https://www.kitware.com/preserving-privacy-advancing-research-solutions-for-medical-image-sharing/).

## Supporting Disease Research with Whole Slide Image Analysis Software for Digital Pathology

![HistomicsTK allows researchers to easily create annotations and view millions of annotations simultaneously.](https://www.kitware.com/main/wp-content/uploads/2024/12/year-innovation-9-1024x643.jpg)

HistomicsTK allows researchers to easily create annotations and view millions of annotations simultaneously.

**HistomicsTK**, Kitware’s open source digital pathology software, is a powerful solution for analyzing and managing whole slide imaging (WSI) data. Developed with scalability and adaptability at its core, **HistomicsTK** provides researchers with a seamless platform for conducting detailed image analysis through an easy-to-use interface. Its open source foundation invites customization, allowing institutions to modify and extend the tool to meet their unique research needs. This software enhances workflows by facilitating detailed image annotation, segmentation, and quantitative analysis, making studying medical images faster and more efficient. The ability to handle large WSI datasets accurately and at scale is crucial for medical research, where quick and reliable data processing is essential. By enabling more effective analysis and data sharing, **HistomicsTK** supports a deeper understanding of diseases and promotes collaborative research efforts. This innovation is pivotal for advancing pathology research, fostering discoveries, and paving the way for important medical breakthroughs.

Watch this video to learn more about [HistomicsTK](https://youtu.be/lA2cDHZk6wk).

## Next-Gen Medical Training with Realistic Patient Simulations

![The Pulse Explorer is used to test and demonstrate training scenarios interactively with a virtual mechanical ventilator.](https://www.kitware.com/main/wp-content/uploads/2024/12/year-innovation-10-1024x336.jpg)

The Pulse Explorer is used to test and demonstrate training scenarios interactively with a virtual mechanical ventilator.

Kitware’s **Pulse Physiology Engine** stood out for its significant contributions to enhancing medical training through advanced simulation. One notable application was its use in the Air Force Research Laboratory’s mechanical ventilation simulation project, where it addressed key training challenges clinicians face, especially in military and high-stress environments where a lack of mechanical ventilation skills can be detrimental to patient care. **Pulse** offers a physics-based, real-time simulation of whole-body physiology, allowing trainees to practice with realistic patient scenarios and benefit from automated feedback, minimizing reliance on human trainers and ensuring patient safety during training. This project integrated a sophisticated ventilator simulator with a lung model and complex algorithms to accurately mimic respiratory distress. Validated training scenarios were supported, aligning with ARDSnet and Joint Trauma Clinical Practice Guidelines to ensure clinical relevance. Such effective training solutions are vital for both public and military healthcare providers, preparing them for unexpected situations like pandemics or mass casualty events to maintain high-quality patient care.

Read more about how Pulse was used to advance [mechanical ventilation training](https://www.kitware.com/project-spotlight-afrl-mechanical-ventilation-simulation/).

## What’s Next in 2025

The achievements highlighted here are not just milestones but stepping stones for even greater advancements in the future. As we look ahead to 2025, we remain committed to driving technology forward, embracing new challenges, and making a meaningful impact in diverse fields. Here’s to continuing our journey of discovery and excellence—together.

If you would like more information about any of the projects or technologies mentioned in this article, please [contact us](https://www.kitware.com/contact/).

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

[CMake](https://www.kitware.com/tag/cmake/) | [Geospatial Intelligence](https://www.kitware.com/tag/geospatial-intelligence/) | [GeoWATCH](https://www.kitware.com/tag/geowatch/) | [HistomicsTK](https://www.kitware.com/tag/histomicstk/) | [ImageDePHI](https://www.kitware.com/tag/imagedephi/) | [KAMERA](https://www.kitware.com/tag/kamera/) | [NOAA](https://www.kitware.com/tag/noaa/) | [ParaView Catalyst](https://www.kitware.com/tag/paraview-catalyst/) | [Pulse](https://www.kitware.com/tag/pulse/) | [spack](https://www.kitware.com/tag/spack-2/) | [Trame](https://www.kitware.com/tag/trame/) | [Web-OTM](https://www.kitware.com/tag/web-otm/)

