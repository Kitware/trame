# Known available widgets

## Vue 2 and 3

| Widget name (trame.widget.{name}) | Package name | Supported version | Number of components |
| --- | --- | --- | --- |
| html | (built-in) | 2 & 3 | 80 |
| client | (built-in) | 2 & 3 | 5 |
| vuetify, vuetify2, vuetify3 | trame-vuetify | 2 & 3 | 146/156 |
| router | trame-router | 2 & 3 | 2 |
| vtk, paraview | trame-vtk | 2 & 3 | 15 |
| plotly | trame-plotly | 2 & 3 | 1 |
| xterm | trame-xterm | 2 & 3 | 1 |
| code | trame-code | 2 & 3 | 1 |
| iframe | trame-iframe | 2 & 3 | 2 |
| trame | trame-components | 2 & 3 | 11 |
| markdown | trame-markdown | 2 & 3 | 1 |
| rca | trame-rca | 2 & 3 | 7 |
| keycloak | trame-keycloak (wip) | 2 & 3 (needs funding) | 1 |
| vtk3d | trame-vtk3d | 2 & 3 | 1 |
| simput | trame-simput | 2 & 3 | 2 |
| vega | trame-vega | 2 & 3 | 1 |
| matplotlib | trame-matplotlib | 2 & 3 | 1 |
| deckgl | trame-deckgl | 2 & 3 | 1 |
| tauri | trame-tauri | 2 & 3 | 2 + utils |
| bbox | trame-bbox (wip) | 2 & 3 | 1 |
| tweakpane | trame-tweakpane | 2 & 3 | 10 |
| vtklocal | trame-vtklocal | 2 & 3 | 1 |

::: warning
- **vuetify**: The set of components are a bit different with API change. Please look at the [upgrade guide](https://vuetifyjs.com/en/getting-started/upgrade-guide/) for more details.
- **markdown**: If coming from v2, the v3 has a different engine configuration while now supporting both vue 2/3.
- **trame**: In the code upgrade to support 2 & 3, some event keys have been updated.
- **keycloak**: This component has been pushed to capture the current development state but is currently lacking funding to complete it.
- **vtklocal**: This component leverage VTK-WASM and therefore requires nightly VTK build with matching wasm package.
:::

## Vue 3 only

| Widget name (trame.widget.{name}) | Package name | Supported version | Number of components |
| --- | --- | --- | --- |
| quasar | trame-quasar | 3 | 123 |
| formkit | trame-formkit | 3 | 2 |
| datagrid | trame-datagrid | 3 | 3 |

## Vue 2 only

| Widget name (trame.widget.{name}) | Package name | Supported version | Number of components |
| --- | --- | --- | --- |
| leaflet | trame-leaflet | 2 | 22 |
| pvui | trame-pvui | 2 | 4 |
| grid | trame-grid-layout | 2 | 2 |

