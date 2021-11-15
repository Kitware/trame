from trame.html.vtk.common import (
    VtkView,
    VtkRemoteView,
    VtkLocalView,
    VtkRemoteLocalView,
    VtkAlgorithm,
    VtkCellData,
    VtkDataArray,
    VtkFieldData,
    VtkGeometryRepresentation,
    VtkGlyphRepresentation,
    VtkMesh,
    VtkPointData,
    VtkPolyData,
    VtkReader,
    VtkShareDataset,
    use_module,
)
from pywebvue.modules import VTK

use_module(VTK)
