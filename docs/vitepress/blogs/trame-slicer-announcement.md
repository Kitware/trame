[post](https://www.kitware.com/trame-slicer-announcement/)

# trame-slicer: Bringing the power of 3D Slicer to the web

November 20, 2025

[Thibault Pelletier](https://www.kitware.com/author/thibault-pelletier/ "Posts by Thibault Pelletier") and [Julien Finet](https://www.kitware.com/author/julien-finet/ "Posts by Julien Finet")

![](https://www.kitware.com/main/wp-content/uploads/2025/11/Screenshot-2025-11-20-082509.png)

Kitware is pleased to announce the launch of **trame Slicer**.

trame Slicer is a Python library to create modern Vue-based web applications by leveraging the [trame framework](https://www.kitware.com/trame/). It provides access to core [3D Slicer](https://www.slicer.org/) functionalities, such as segmentation, registration, and volume rendering, directly through Python, greatly improving the development experience.

The library acts as a bridge between the 3D Slicer core components and the trame web server, allowing web native access to 3D Slicer features and enabling the development of rich medical workflows. This integration will make it possible to build scalable web applications for medical image data visualization and analytics.

![](https://www.kitware.com/main/wp-content/uploads/2025/11/trame-slicer-medical-app-example-1-1024x614.png)

*Figure 1: Segmented mandibular and maxillary from [Dental Segmentator](https://github.com/gaudot/SlicerDentalSegmentator)*

## Why does it matter?

3D Slicer is a robust and feature-rich platform that brings together over 200 specialized medical modules, making it highly effective for data exploration and medical processing tasks. It supports a wide range of use cases, particularly for expert users who require deep access to tools and customization.

However, 3D Slicer is desktop-only application, which can make deployment, collaboration, and accessibility challenging especially in modern medical and research environments that increasingly rely on web and cloud-based workflows. Bringing these powerful capabilities to the browser is both important and technically demanding: medical imaging applications require real-time 3D rendering, large-volume processing, and secure data handling, all of which must be delivered efficiently over the web.

This is where **trame Slicer** makes a difference.

As a web application framework, trame Slicer enables the development of lightweight, browser-accessible interfaces tailored to specific clinical or research needs. It bridges 3D Slicer’s native power with trame’s modern web architecture, allowing developers to deploy Slicer’s segmentation, registration, and visualization tools directly through Python—all without requiring a local installation.

By offloading workloads to the server, trame Slicer reduces hardware demands on the client side, making advanced capabilities like AI segmentation accessible on any device. Data such as DICOM files remains securely on the server for processing and rendering, supporting both performance and compliance. This design not only handles massive datasets efficiently but also ensures patient data never leaves the secure environment.

Ultimately, trame Slicer makes powerful Slicer components available to Python application developers, simplifying the creation of focused medical applications for the web.

![](https://www.kitware.com/main/wp-content/uploads/2025/10/20251020-kidney-box-2-1024x731.png)

*Figure 2: Volume rendering and markups interactions powered by 3D Slicer*

## How to get started?

Although the library is still in development, core features are already available and production-ready. To get started, the following options are available :

### trame Slicer library

The [trame Slicer library](https://github.com/KitwareMedical/trame-slicer) is available for Python-only integration, making it easy to incorporate into custom environments and cloud Docker and Kubernetes deployment. At present, publicly available 3D Slicer core functionality Python wheels have only been provided for Python 3.10 and Linux / Windows.

Windows and Linux 3D Slicer wheels are [provided for download](https://github.com/KitwareMedical/trame-slicer?tab=readme-ov-file#downloading-the-latest-wheels), and the trame Slicer library itself can be downloaded and installed directly from [PyPI](https://pypi.org/project/trame-slicer/).

Work is underway with the 3D Slicer community to provide pre-built 3D Slicer wheels directly by the 3D Slicer continuous integration for stable 3D Slicer releases.

### Slicer trame extension

The [Slicer trame extension](https://github.com/KitwareMedical/SlicerTrame) provides access to trame Slicer directly from the 3D Slicer application. The extension is available from Slicer 5.9 nightly release onward and available for all nightly release versions.

This setup provides direct access to all 3D Slicer’s internal libraries and installed modules, though direct compatibility with trame Slicer is not guaranteed at the moment.

This extension is ideal for early access to the trame Slicer features across all platforms.

## Support and Services

Looking to take your application to new heights? [Get in touch](https://www.kitware.com/contact/) with Kitware for expert development and support services to fast-track your success with trame Slicer.

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

## Credits

The effort behind the trame Slicer library has been partially financed by the [Cure Overgrowth Syndromes (COSY)](https://rhu-cosy.com/en/accueil-english/) RHU Project (ANR-18-RHUS-0005), the [Handling heterogeneous Imaging and signal data for analysing the Neurodevelopmental Trajectories of premature newborns (HINT)](https://anr-hint.pages.in2p3.fr/) ANR project (ANR-22-CE45-0034) and Kitware Europe early-adopter customers.

Tags:

[3D Slicer](https://www.kitware.com/tag/3d-slicer/) | [Medical Imaging](https://www.kitware.com/tag/medical-imaging/) | [Press Releases](https://www.kitware.com/tag/press/) | [Trame](https://www.kitware.com/tag/trame/) | [Web Applications](https://www.kitware.com/tag/web-applications/)

