# From v2 to v3

Trame v3 is right around the corner. The main driver for the version 3 is to support Vue.js 3. Vue3 is already supported in trame v2, but we aim to make it the new default.

On top of making vue3 the new default, we want to shrink the default dependency list by only bundling by default the client and the server. And if the user needs vuetify and/or vtk they will need to list them as dependency of their project (trame-vtk, trame-vuetify). This will allow a leaner core package while still offering the same capabilities as before.

So far we don't have a release date, but while vuetify, vtk and more are already vue2 and 3 compatible. Not everything is available (router, plotly) or will be ported. So until we feel we have a great offering in vue3, we will hold off for the V3 release.

## New defaults

```python
from trame.app import get_server

server = get_server()
server.client_type = "vue3" # instead of 'vue2'
```

## API change

Trame in itself won't have API change but it is possible that vue3 widget will have a different API like you can see between vuetify2 and vuetify3, but in general we'll try to maintain full API compatibility.