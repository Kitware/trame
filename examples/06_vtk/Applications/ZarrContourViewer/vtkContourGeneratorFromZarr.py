import os
import sys

import vtk
import zarr
from vtk.util import numpy_support as np_s


class vtkContourGeneratorFromZarr(object):
    def __init__(self, basepath):
        self.zarrPath = os.path.normpath(basepath)
        if not os.path.exists(self.zarrPath):
            print(f"Path ({self.zarrPath}) is not valid")
            sys.exit(1)

        # set up zarr stuff
        self.zarrStore = zarr.open(self.zarrPath, mode="r")
        self.multiscales = self.zarrStore.attrs["multiscales"][0]
        self.datasets = self.multiscales["datasets"]
        self.root = self.zarrStore["/"]
        self.maxLevel = len(self.datasets) - 1

        self.contour = vtk.vtkFlyingEdges3D()
        self.contour.ComputeScalarsOff()
        self.contour.ComputeNormalsOn()
        self.contour.ComputeGradientsOff()

    def getVolume(self, scale, dataset):
        origin = self.getScaleOrigin(scale)
        spacing = self.getScaleSpacing(scale)

        path = dataset["path"]
        dims = self.root[path].attrs["_ARRAY_DIMENSIONS"]
        shape = self.root[path].shape
        xIdx = dims.index("x")
        yIdx = dims.index("y")
        zIdx = dims.index("z")

        ds = vtk.vtkImageData()
        ds.SetOrigin(origin)
        ds.SetSpacing(spacing)
        ds.SetDimensions(shape[xIdx], shape[yIdx], shape[zIdx])

        array = np_s.numpy_to_vtk(self.root[path][:].flatten())
        array.SetName("Content")
        ds.GetPointData().SetScalars(array)

        return ds

    def getMaxLevel(self):
        return self.maxLevel

    def getScaleOrigin(self, scale):
        origin = [0.0, 0.0, 0.0]
        origin[0] = self.root[str(scale) + "/x"][0]
        origin[1] = self.root[str(scale) + "/y"][0]
        origin[2] = self.root[str(scale) + "/z"][0]
        return origin

    def getScaleSpacing(self, scale):
        spacing = [0.0, 0.0, 0.0]
        spacing[0] = self.root[str(scale) + "/x"][1] - self.root[str(scale) + "/x"][0]
        spacing[1] = self.root[str(scale) + "/y"][1] - self.root[str(scale) + "/y"][0]
        spacing[2] = self.root[str(scale) + "/z"][1] - self.root[str(scale) + "/z"][0]
        return spacing

    def contourForLevel(self, level, contours=[1]):
        # Update contours values
        ctrIdx = 0
        self.contour.SetNumberOfContours(len(contours))
        for value in contours:
            self.contour.SetValue(ctrIdx, value)
            ctrIdx += 1

        if level > self.maxLevel:
            print(f"level {level} > max level {self.maxLevel}")

        volume = self.getVolume(level, self.datasets[level])
        self.contour.SetInputData(volume)
        self.contour.Update()

        _ds = self.contour.GetOutput()
        nb_points = _ds.GetNumberOfPoints()
        nb_cells = _ds.GetNumberOfCells()
        return nb_points, nb_cells

    def getContour(self):
        return self.contour
