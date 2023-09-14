# Finite Element Analysis

This example is a translation from a `dash-vtk` code described in that [repository](https://github.com/shkiefer/dash_vtk_unstructured) using trame.

In trame we are exposing 3 approaches:
- client view:
  This application simulate what dash-vtk is doing by defining the 3D scene in plain HTML structure.
- remote/local view:
  Those applications focus on the VTK/Python part by creating and configuring your vtkRenderWindow
  directly and letting the VtkRemoteView or VtkLocalView do their job of presenting it on the client
  side. In the case of the __VtkRemoteView__, the rendering is happening on the server side and images
  are sent to the client. For the __VtkLocalView__ use case, the geometry is sent instead and the client
  is doing the rendering using vtk.js under the cover.

The data files can be found [here in the original project](https://github.com/shkiefer/dash_vtk_unstructured/tree/main/data).

[![Gallery](/assets/images/examples/FiniteElementAnalysis.jpg)](https://github.com/Kitware/trame/tree/master/examples/)

The code is available [here](https://github.com/Kitware/trame/tree/master/examples/06_vtk/Applications/FiniteElementAnalysis)
