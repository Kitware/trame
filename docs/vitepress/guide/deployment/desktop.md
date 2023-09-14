# Desktop

Trame applications can be bundled into a standalone desktop application and presented to the user like a native application without the need of a browser to expose the UI.

For that part we usually rely on [PyInstaller](https://pyinstaller.org/en/stable/#) to bundle the Python part of the code into something executable. Then you can either rely on [PyWebView](https://pywebview.flowrl.com/) or [Tauri](https://tauri.app/) to hide the browser and enable a native app look.

The [trame-cookiecutter](https://github.com/Kitware/trame-cookiecutter) provide an initial example for using PyWebView under `bundles/desktop/*`.

For tauri, you can look at an example [here](https://github.com/Kitware/trame-tauri/tree/master/examples/simple-cone). Then you can browse around for more...

```bash
pip install \
    trame trame-vuetify trame-vtk \ # Demo app requirement
    pywebview # Simple Python app view for web content

# Run simple example app
python -m trame.app.demo --app
```

![Simple trame app](/assets/images/deployment/cone-app.png)