# ParaView Picking

This example shows how to drive ParaView's selection tools from a remotely-rendered view. A toolbar lets you pick a selection mode (surface points, surface cells, frustum, or block), then drag a rectangle over the view; the rectangle's screen coordinates are forwarded to the server and converted into the matching ParaView selection call (`SelectSurfacePoints`, `SelectCellsThrough`, etc.).

[![ParaView Picking](/assets/images/examples/pv_picking.png)](https://github.com/Kitware/trame/tree/master/examples/07_paraview/Picking)

<<< @/../../examples/07_paraview/Picking/pv_selection.py 