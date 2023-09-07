# From v2 to v3

Trame v3 is out and is going to break things up. But it should be easy to migrate. First of all, trame is moving to using a vue3 client by default on January 2024. But both client will remain working for a long time. To use the latest version of trame with your current project, just make sure you set the __client_type__ to vue2.

On top of making vue3 the new default, we want to shrink the default dependency list by only bundling by default the client and the server. And if the user needs vuetify and/or vtk they will need to list them as dependency of their project (trame-vtk, trame-vuetify). This will allow a leaner core package while still offering the same capabilities as before.

So far we don't have a release date, but while vuetify, vtk and more are already vue2 and 3 compatible. Not everything is available (router, plotly) or will be ported. So until we feel we have a great offering in vue3, we will hold off for the V3 release.

## New default client_type

The default client_type will be changing from vue2 to vue3 on January 2024.

```python
from trame.app import get_server

server = get_server()
server.client_type = "vue3" # instead of 'vue2'
```

## New warning due to breaking change

A message will be printed by default at the startup of trame with the v3 version.
We are expecting to remove that message during summer 2024.

    --------------------------------------------------------------------------------
       !!! You are currently using trame@3 which may break your application !!!
    --------------------------------------------------------------------------------

     1. trame@3 only provides by default trame.widgets.[html,client] and remove
        everything else as implicit dependency. Those other widgets will still
        exist and will be supported, but they will need to be defined as a
        dependency of your application.

           $ pip install trame-vtk trame-vuetify trame-plotly

        Import paths are remaining the same.

        For libraries like vuetify since they offer different API between
        their vue2 and vue3 implementation, the widget name will reflect
        which vue version they are referencing. But original naming will remain.

           from trame.widgets import vuetify2, vuetify3


     2. trame@3 aims to use vue3 as a new default. But to smooth the transition
        we will maintain the server.client_type = 'vue2' default until
        December 2023 which is the vue2 EOL.

        After that time, the new default will be switched to 'vue3'.
        Vue2 will still work 'forever' and many of the new widgets will be
        written to support both versions.

        If you have a 'vue2' application and don't need or want to update your code,
        you can still use trame@3 with vue2 by setting `server.client_type='vue2'.

     Actions items
     ~~~~~~~~~~~~~
       a. Make sure you set `server.client_type` to either 'vue2' or 'vue3'.
       b. List the expected dependencies or have a 'trame<3' dependency


To disable that warning you have 2 options. Use environment variable by setting __TRAME_DISABLE_V3_WARNING__ or __disabling logging__ which can be done by the following code snippet.

```python
import logging

logging.getLogger('trame.app').disabled = True
```

or

```python
import os

os.environ["TRAME_DISABLE_V3_WARNING"] = "1"
```

## API change

Trame in itself won't have API change but it is possible that vue3 widget will have a different API like you can see between vuetify2 and vuetify3, but in general we'll try to maintain full API compatibility.

## Widgets compatibility and package name

| Widget name (trame.widget.{name}) | Package name | Supported version |
| --- | --- | --- |
| html | (built-in) | 2 & 3 |
| client | (built-in) | 2 & 3 |
| vuetify, vuetify2, vuetify3 | trame-vuetify | 2 & 3 |
| router | trame-router | 2 & 3 |
| vtk, paraview | trame-vtk | 2 & 3 |
| plotly | trame-plotly | 2 & 3 |
| xterm | trame-xterm | 2 & 3 |
| code | trame-code | 2 & 3 |
| iframe | trame-iframe | 2 & 3 |
| trame | trame-components | 2 (wip for 3) |
| keycloak | trame-keycloak | 2 & 3 (wip) |
| formkit | trame-formkit | 3 |
| leaflet | trame-leaflet | 2 |
| video | trame-video | 2 |
| pvui | trame-pvui | 2 |
| grid | trame-grid-layout | 2 |
| tauri | trame-tauri | 2 |
| vega | trame-vega | 2 |
| simput | trame-simput | 2 |
| rca | trame-rca | 2 (wip for 3) |
| matplotlib | trame-matplotlib | 2 |
| markdown | trame-markdown | 2 |
| deckgl | trame-deckgl | 2 |
