[post](https://www.kitware.com/vtk-wasm-and-its-trame-integration/)

# VTK.wasm and its trame integration

October 16, 2024

[Jaswant Panchumarti](https://www.kitware.com/author/jaswant-panchumarti/ "Posts by Jaswant Panchumarti") and [Sebastien Jourdain](https://www.kitware.com/author/sebastien-jourdain/ "Posts by Sebastien Jourdain")

![](https://www.kitware.com/main/wp-content/uploads/2024/09/Screenshot-2024-09-12-at-17.10.35.png)

The Visualization Toolkit (VTK) is a widely used open-source solution for post-processing analysis on a desktop. The library is written in C++ but can be used in Python and Java thanks to wrapping infrastructure.

A JavaScript library (vtk.js) is also available but lacks the decades of investment and development from which the C++ library benefits. Moreover, the goal of that JavaScript library was never to fully match VTK capabilities, especially in terms of data processing. In short, vtk.js focused on bridging VTK toward web visualization by enabling VTK data structures to be rendered natively in a browser. Unfortunately, not all the advanced visualization techniques available in plain VTK have been implemented in JavaScript.

This dichotomy made the usage of VTK in the Web non-trivial. Thanks to trame, things became much easier with its uniform approach via Python. But that also highlighted the shortcomings of vtk.js compared to VTK. Now with the maturity of WASM we are reaching another level of integration that is worth sharing with the community.

## The rise of WASM

WebAssembly or Wasm is a technology that allows native code like VTK (C++) to be compiled into bytecode that can then be run in a browser. With years in the making, runtimes and tools have reached a point where this can be used in production.

At Kitware we started to leverage WASM for IO and data processing and with the investigation and contribution of [dicehub](https://dicehub.com/welcome/) we have also enabled 3D rendering.

Today, most of the VTK.wasm rendering works with WebGL2. There is active effort pushing for a WebGPU implementation to enable cross-platform compatibility for desktop and Web. This takes advantage of the latest graphics API for higher performance. Once that work reaches completion, users of VTK.wasm will get native performance and consistent look and feel without any code change on their end.

## New VTK infrastructure for better WASM integration

Thanks to the groundwork done for WASM, we made it a viable solution for VTK on the Web. To further leverage the use of VTK.wasm across projects, we created a new set of classes that allow users to capture a server-side VTK scene and synchronize the contents of the scene with a WASM implementation. This new infrastructure aims to be as generic as possible with many implications that go beyond WASM.

Such design is based on 2 main elements:

* an automated serialization/deserialization system
* an object manager that can track instances of VTK classes and rebuild/update them from a state

## VTK Object Marshaling

One of the core constraints for data synchronization is serialization and deserialization. With VTK being a library with more than 3,000 classes we could not go with a manual approach. We leveraged our wrapping infrastructure along with a macro annotation system to automate generation of code to (de)serialize properties of a VTK class.. So far we only focused on the rendering classes in VTK but additional modules could be added as needed. The current implementation only provides marshaling capabilities with 18 classes that have manual implementations and 366 classes with auto-generated implementations.

This marshaling infrastructure is being used by a new ***VTK::SerializationManager*** module to enable object synchronization.

## New Object Manager

The vtkObjectManager is a new class that relies on the previously described marshaling infrastructure to extract states and rebuild the corresponding instance and its dependent objects from those given states.

With this manager, a user can register any serializable vtkObject (like a vtkRenderWindow) and extract a serializable representation of the object tree so it can be transferred over the network and rebuilt somewhere else. In this case, we leverage WASM to rebuild the same VTK classes as the server side and produce the full interactive 3D scene.

## Trame integration

With that new VTK infrastructure, we created a new trame widget (trame-vtklocal) that encapsulates our VTK wasm module and our protocol to handle the synchronization over the network. This new implementation adds a more robust solution to local rendering with VTK and trame than the current one which relies on vtk.js.

This new widget preserves the usage patterns from the pure JavaScript predecessor trame-vtk. When creating such a widget, you only need to pass it a vtkRenderWindow instance to control the graphics displayed on the client side. After that, the widget takes care of the rest. Each time you modify the scene by changing anything (filter parameter, actor property…), you just need to call the update method on the widget instance to trigger the scene synchronization and enable the browser to display the latest version of the 3D scene.

### Simple code example

With trame we define the full application as a standalone Python script with the VTK logic and graphical user interface definition and interaction binding.

You can use VTK.wasm today by installing it from Kitware’s package registry, and the object manager supportwill be available from pypi.org beginning with the upcoming VTK 9.4 release. To run the following example, you should set a virtual environment as follows.

```
python -m venv .venv
source .venv/bin/activate
pip install trame trame-vtklocal
pip install "vtk==9.4.0rc2" --extra-index-url https://wheels.vtk.org
```

In the example below we simplified the vtk imports for better readability so we can focus on a simple VTK pipeline that we modify interactively in trame while enabling local rendering via VTK wasm. [code available here](https://github.com/Kitware/trame-vtklocal/blob/master/examples/demo/basic.py)

```
import vtk

from trame.app import get_server
from trame.ui.html import DivLayout
from trame.widgets import html, client, vtklocal
from trame.decorators import TrameApp, change, trigger

FULL_SCREEN = "position:absolute; left:0; top:0; width:100vw; height:100vh;"
TOP_RIGHT = "position: absolute; top: 1rem; right: 1rem; z-index: 10;"
TOP_LEFT = "position: absolute; top: 1rem; left: 1rem; z-index: 10;"

def create_vtk_pipeline():
    renderer = vtk.vtkRenderer()
    rw = vtk.vtkRenderWindow()
    rw.AddRenderer(renderer)
    rwi = vtk.vtkRenderWindowInteractor(render_window=rw)
    rwi.interactor_style.SetCurrentStyleToTrackballCamera()

    cone = vtk.vtkConeSource()
    mapper = vtk.vtkPolyDataMapper(input_connection=cone.output_port)
    actor = vtk.vtkActor(mapper=mapper)

    renderer.AddActor(actor)
    renderer.background = (0.1, 0.2, 0.4)
    renderer.ResetCamera()

    return rw, cone

@TrameApp()
class WasmApp:
    def __init__(self, server=None):
        self.server = get_server(server)
        self.render_window, self.cone = create_vtk_pipeline()
        self._build_ui()

    @property
    def ctrl(self):
        return self.server.controller

    @change("resolution")
    def on_resolution_change(self, resolution, **_):
        self.cone.SetResolution(int(resolution))
        self.ctrl.view_update()

    def _build_ui(self):
        with DivLayout(self.server) as layout:
            client.Style("body { margin: 0; }")

            html.Button(
                "Reset Camera",
                click=self.ctrl.view_reset_camera,
                style=TOP_RIGHT,
            )
            html.Input(
                type="range",
                v_model=("resolution", 6),
                min=3, max=60, step=1,
                style=TOP_LEFT,
            )

            with html.Div(style=FULL_SCREEN):
                with vtklocal.LocalView(self.render_window) as view:
                    view.update_throttle.rate = 20  # max update rate
                    self.ctrl.view_update = view.update_throttle
                    self.ctrl.view_reset_camera = view.reset_camera

def main():
    app = WasmApp()
    app.server.start()

if __name__ == "__main__":
    main()
```

The code above produces the following application.

![](https://www.kitware.com/main/wp-content/uploads/2024/09/Screenshot-2024-09-12-at-15.33.15-1024x728.png)

Minimalistic VTK.wasm example with trame using the VTK cone source to illustrate geometry change and code usage

### 3D widget example

The example that we are going to look at below requires bi-directional communication to update the server side data processing while tracking the 3D widget interactions on the client side.

The full code example is available [here](https://github.com/Kitware/trame-vtklocal/blob/master/examples/demo/widget.py) but we will illustrate how things work with the following callback and the graphical user interface definition.

```
    @change("line_widget")
    def _on_widget_update(self, line_widget, **_):
        if line_widget is None:
            return

        self.seed.SetPoint1(line_widget.get("p1"))
        self.seed.SetPoint2(line_widget.get("p2"))
        self.ctrl.view_update()

    def _build_ui(self):
        with DivLayout(self.server):
            client.Style("body { margin: 0; }")
            with html.Div(style=FULL_SCREEN):
                with vtklocal.LocalView(self.rw) as view:
                    view.update_throttle.rate = 20
                    self.ctrl.view_update = view.update_throttle
                    self.widget_id = view.register_widget(self.widget)
                    view.listeners = (
                        "listeners",
                        {
                            self.widget_id: {
                                "InteractionEvent": {
                                    "line_widget": {
                                        "p1": (
                                            self.widget_id,
                                            "WidgetRepresentation",
                                            "Point1WorldPosition",
                                        ),
                                        "p2": (
                                            self.widget_id,
                                            "WidgetRepresentation",
                                            "Point2WorldPosition",
                                        ),
                                    },
                                },
                            },
                        },
                    )
```

From the code above we can see that the UI is similar to what was done before except that now, we register a widget and attach some listeners.

By registering the widget we allow it to be tracked and therefore allow us to attach a VTK listener. That listener’s only role is to extract data and bind it to the trame state. That way we can update our processing pipeline on that state change.

The way listeners definition are structured is as follows:

```
[id of wasm object to add listener to]: {
  [name of the vtk event to observe]: {
    [variable name of the trame state to update]: {
      [key name]: ([wasm id], [state key to extract], [nested key], ...),
      [key fullstate]: [wasm id],
    }
  }
}
```

Then because in our definition we are updating `line_widget` with p1 and p2 from `Point1WorldPosition` of the `WidgetRepresentation` of the widget `self.widget_id`, we create a change listener to reflect those point locations to the vtk seed for the streamline filter. And then we just ask for the view to update the geometry. You can see in the video below how the interaction feels.

<center><iframe src="https://player.vimeo.com/video/1014522115?dnt=1&app_id=122963" width="640" height="360" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></center>

## Future work

While the current architecture is sound, we are expecting to see reports of serialization issues either with missing serializers or incomplete state synchronization. Those should be reported [here for serializer missing](https://github.com/Kitware/trame-vtklocal/issues/14) while for an incomplete state synchronization, please create a new issue with a self contained example code.

In order to support cell/point selections, we will need to provide a way to invoke methods on the WASM objects by providing the name of the C++ function, and arguments in JSON. We aim to leverage our wrapping infrastructure to implement this functionality, so we’ll be targeting that next and hope to have it completed by VTK 9.5.

If you want to help speed up the development, please [reach out to Kitware](https://www.kitware.com/trame/support/) to discuss how you can help.

## Support and Services

Looking to take your application to new heights? [Get in touch](https://www.kitware.com/contact/) with Kitware for expert development and support services to fast-track your success with Kitware's open source frameworks.

  <!-- Icon/link tiles -->
<table>
  <tr>
    <td align="center" width="33%">
      <img src="https://www.kitware.com/main/wp-content/uploads/2021/11/icon_collaboration.svg" width="50"><br>
      <strong><a href="https://www.kitware.com/training/">Training</a></strong><br>
      <small>Learn how to confidently use and customize 3D Slicer from the expert developers at Kitware.</small>
    </td>
    <td align="center" width="33%">
      <img src="https://www.kitware.com/main/wp-content/uploads/2021/12/icon_research_develop.svg" width="50"><br>
      <strong><a href="https://www.kitware.com/support/">Support</a></strong><br>
      <small>Our experts can assist your team as you build your application and establish in-house expertise.</small>
    </td>
    <td align="center" width="33%">
      <img src="https://www.kitware.com/main/wp-content/uploads/2021/11/icon_custom_software.svg" width="50"><br>
      <strong><a href="https://www.kitware.com/contact">Custom Development</a></strong><br>
      <small>Leverage Kitware's 25+ years of experience to quickly build your application.</small>
    </td>
  </tr>
</table>

## Acknowledgement

This work is partially funded by the US Department of Energy’s Office of Biological and Environmental Research (BER) to develop Pan3D, an open-source toolkit supporting scalable and reproducible scientific workflows for 3D data analytics (DE-SC0022365). The project is led by Aashish Chaudhary, the Principal Investigator (PI), with John Tourtellot as the technical lead, who contributed to this work through their leadership and vision of further improving VTK to support complex 3D workflows.

Tags:

[Trame](https://www.kitware.com/tag/trame/) | [VTK](https://www.kitware.com/tag/vtk/) | [vtk-wasm](https://www.kitware.com/tag/vtk-wasm/)

