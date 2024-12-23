# Known available widgets

| Category | Widget name (trame.widget.{name}) | Package name | Vue version | Number of components |
| --- | --- | --- | --- | --- |
| **Front** |
| | html | (built-in) | 2 & 3 | 80 |
| | client | (built-in) | 2 & 3 | 5 |
| | [iframe](https://github.com/Kitware/trame-iframe "Handle cross-origin communication with iframe") | trame-iframe | 2 & 3 | 2 |
| | [react](https://github.com/Kitware/trame-react "React component that wraps trame iframe") | trame-react | 2 & 3 | 2 |
| **GUI** |
| | [datagrid](https://github.com/Kitware/trame-datagrid "RevoGrid spreadsheet") | trame-datagrid | 3 | 3 |
| | [formkit](https://github.com/Kitware/trame-formkit "FormKit widgets") | trame-formkit | 3 | 2 |
| | [goldenlayout](https://github.com/Kitware/trame-goldenlayout "Golden-layout widgets") | trame-goldenlayout | 3 | 1 |
| | [grid](https://github.com/Kitware/trame-grid-layout "Dynamic grid layout containers ") | trame-grid-layout | 2 | 2 |
| | [markdown](https://github.com/Kitware/trame-markdown "Component that renders Markdown syntax") | trame-markdown | 2 & 3 [⚠️](# "If coming from v2, the v3 has a different engine configuration while now supporting both vue 2/3.") | 1 |
| | [pvui](https://github.com/Kitware/trame-pvui "Widgets that may be used in the Paraview user interface") | trame-pvui | 2 | 4 |
| | [quasar](https://github.com/Kitware/trame-quasar "Quasar widgets") | trame-quasar | 3 | 123 |
| | [simput](https://github.com/Kitware/trame-simput "Create forms from model/proxies") | trame-simput | 2 & 3 | 2 |
| | [trame](https://github.com/Kitware/trame-components "Helper components") | trame-components | 2 & 3 [⚠️](# "In the code upgrade to support 2 & 3, some event keys have been updated.") | 11 |
| | [tweakpane](https://github.com/Kitware/trame-tweakpane "Tweakpane widgets") | trame-tweakpane | 2 & 3 | 10 |
| | [vuetify, vuetify2, vuetify3](https://github.com/Kitware/trame-vuetify "Vuetify UI components") | trame-vuetify | 2 & 3 [⚠️](# "The set of components are a bit different with API change. Please look at the 'upgrade guide' for more details.")| 146 & 156 |
| **Charts** | 
| | [matplotlib](https://github.com/Kitware/trame-matplotlib "Renders Matplotlib plots") | trame-matplotlib | 2 & 3 | 1 |
| | [plotly](https://github.com/Kitware/trame-plotly "Renders Plotly charts") | trame-plotly | 2 & 3 | 1 |
| | [vega](https://github.com/Kitware/trame-vega "Figure component that is capable of rendering Vega grammars such as Altair plots") | trame-vega | 2 & 3 | 1 |
| **2D** |
| | [annotations](https://github.com/Kitware/trame-annotations "Widgets for image and video annotations") | trame-annotations | 3 | 4
| | [bbox](https://github.com/Kitware/trame-bbox "Widget to draw and/or interact with bounding boxes") [🏗️](# "Work in progress") | trame-bbox | 2 & 3 | 1 |
| **3D** | 
| | [vtk, paraview](https://github.com/Kitware/trame-vtk "Interface with VTK and/or ParaView") | trame-vtk | 2 & 3 | 15 |
| | [vtk3d](https://github.com/Kitware/trame-vtk3d "Wrapper to WASM bundle of VTK") | trame-vtk3d | 2 & 3 | 1 |
| | 🆕[vtklocal](https://github.com/Kitware/trame-vtklocal "Local Rendering using VTK/WASM to match server side rendering pipeline on the client side") [⚠️](# "This component leverage VTK-WASM and therefore requires nightly VTK build with matching wasm package.") | trame-vtklocal | 2 & 3 | 1 |
| | 3D Slicer [🏗️](# "coming soon") | slicer-trame | TBA | TBA |
| **GIS** |
| | [deckgl](https://github.com/Kitware/trame-deckgl "Components that can interface with PyDeck while being powered by Deck.gl") | trame-deckgl | 2 & 3 | 1 |
| | [large-image](https://github.com/girder/trame-large-image "Serve and visualize large images (geospatial, histology, TIFF) on slippy-maps") | trame-large-image | 2 | 1 |
| | [leaflet](https://github.com/Kitware/trame-leaflet "Leaflet integration to create map views") | trame-leaflet | 2 | 22 |
| **Development** |
| | [code](https://github.com/Kitware/trame-code "Monaco VS code editor") | trame-code | 2 & 3 | 1 |
| | [xterm](https://github.com/Kitware/trame-xterm "Expose xterm.js") | trame-xterm | 2 & 3 | 1 |
| **Connectivity** |
| | [gwc](https://github.com/Kitware/trame-gwc "Girder Web Components to connect with scientifc data storage Python Girder WSGI") | trame-gwc | 2  | 10 |
| | [keycloak](https://github.com/Kitware/trame-keycloak "Keycloak Authentication widget") [🏗️](# "This component has been pushed to capture the current development state but is currently lacking funding to complete it.")| trame-keycloak | 2 & 3 | 1 |
| **Misc** |
| | [rca](https://github.com/Kitware/trame-rca "Infrastructure to display remote generated image based content while allowing interaction forwarding") | trame-rca | 2 & 3 | 7 |
| | [router](https://github.com/Kitware/trame-router "Vue Router components") | trame-router | 2 & 3 | 2 |
| | [tauri](https://github.com/Kitware/trame-tauri "Tauri integration to deploy trame into a desktop application") | trame-tauri | 2 & 3 | 2 + utils |
