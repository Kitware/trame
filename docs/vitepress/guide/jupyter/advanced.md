# Advanced usecase

Now that you know we rely on an __`<iframe />`__ to serve the trame application, let's explore how you can tune various parameters to get the most of trame within Jupyter.

## Network / iframe builder 

Jupyter provide various way to help network application to still work in their environment. You will often find a server proxy extension available, but we also created an extension for trame to better manage the network. But either way, it boils down to selecting an __iframe_builder__. In some case we try to make that selection for you automatically, but sometime you may want to override the default behavior. 

Let's review the various available options

```python
from module import App

app = App()  
await app.ui.ready
app.ui.iframe_builder = "..." # <= force an iframe builder
app.ui
```

| iframe_builder | URL | Default if |
| --- | --- | --- |
| default | {iframe_base_url}:{server.port}/ | Default when nothing is set |
| serverproxy | {iframe_base_url}/{server.port}/ | - |
| jupyter-extension | ENV(TRAME_JUPYTER_WWW)/servers/{server.name}/ | Extension loaded and available |
| jupyter-hub | ENV(JUPYTERHUB_SERVICE_PREFIX)proxy/{server.port}/ | If JUPYTERHUB_SERVICE_PREFIX exist |
| jupyter-hub-host | ENV(JUPYTERHUB_SERVICE_PREFIX)proxy/{host}:{server.port}/ | Never a default |

The selection can also be done via the __TRAME_IFRAME_BUILDER__ environment variable.

On top of those presets, you can directly set a function as the iframe_builder. Below is 

## Configurable properties

On top of the __iframe_builder__, the following set of attributes can be set by the user.

| Property name | Default value | Layout constructor |
| --- | --- | --- |
| iframe_style | `border: none; width: 100%; height: 600px;` | `width="100%", height="600px",` 
| iframe_attrs | `{}` | - |
| iframe_base_url | `http://localhost` | `base_url="http://localhost"` |