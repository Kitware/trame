[post](https://www.kitware.com/faster-and-better-3d-slicer-rendering-customization/)

# Faster and better 3D Slicer rendering customization

January 13, 2026

[Thibault Pelletier](https://www.kitware.com/author/thibault-pelletier/ "Posts by Thibault Pelletier") and [Julien Finet](https://www.kitware.com/author/julien-finet/ "Posts by Julien Finet")

![](https://www.kitware.com/main/wp-content/uploads/2025/12/model_glow_example.jpg)

3D Slicer is a very versatile and powerful medical imaging platform that provides plenty of ways for customization; scripted modules allowing the creation of new logic, Qt widgets in both Python and C++, IO plugins for reading custom file formats, segmentation effects for adding new features to the builtin segmentation tools and much more.

With the introduction of the **[SlicerLayerDisplayableManager](https://github.com/KitwareMedical/SlicerLayerDisplayableManager)** module in [3D](link)[Slicer 5.10](https://www.kitware.com/3d-slicer-5-10-now-available-for-download/), extending the rendering pipeline is now significantly easier.

## What can you do with it?

Consider a simple example: adding hover-based highlighting to any model in the scene. Using the new library, an experienced Slicer developer can implement this functionality from scratch in just a couple of hours.

<p align="center">
  <video controls width="720" src="https://www.kitware.com/main/wp-content/uploads/2025/12/slicer_LayerDM_model_glow_example-2025-12-10.mp4">
    <a href="https://www.kitware.com/main/wp-content/uploads/2025/12/slicer_LayerDM_model_glow_example-2025-12-10.mp4">Download video</a>
  </video>
</p>

This [toy example](https://slicerlayerdisplayablemanager.readthedocs.io/en/latest/examples.html) demonstrates how straightforward it is to add selection logic to a custom 3D Slicer module or extension, creating an intuitive user-experience with minimal code.

## Getting started

Install the LayerDisplayableManager extension directly from the Extension Manager in 3D Slicer 5.10 or later.

For examples and detailed API documentation, visit the complete [online documentation](https://slicerlayerdisplayablemanager.readthedocs.io/en/latest/).

![](https://www.kitware.com/main/wp-content/uploads/2025/12/image.png)

<p align="center">Layer Displayable Manager extension in the 3D Slicer Extension Manager</p>

![](https://www.kitware.com/main/wp-content/uploads/2025/12/image-2-1024x875.png)

<p align="center">Online documentation of the Layer Displayable Manager extension</p>

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

Tags:

[3D Slicer](https://www.kitware.com/tag/3d-slicer/) | [Medical Imaging](https://www.kitware.com/tag/medical-imaging/) | [Press Releases](https://www.kitware.com/tag/press/) | [rendering](https://www.kitware.com/tag/rendering/) | [VTK](https://www.kitware.com/tag/vtk/)

