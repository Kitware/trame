# ParaView

ParaView comes with its Python which might be missing some dependencies for your usage.
You can add more Python package into your ParaView by create a virtual environment (not the venv one but [the original](https://virtualenv.pypa.io/en/latest/)) and activate it inside your application.

**First** you need to setup your ParaView add-on python environment in which we will only install `trame` but you could add any other of your Python libraries that are not included in the ParaView bundle.

```bash
virtualenv -p python3.9 pv-lib
source ./pv-lib/bin/activate
pip install trame
deactivate
```

**Note:**
 - You can not use your virtual environment with a `vtk` as your `vtk` library will conflict with the one inside Paraview.
 - Since ParaView include vtk, any VTK example can be run with ParaView assuming you have the proper code to handle the virtual-env loading to get `trame` inside your Python script.

## Making trame available in ParaView

Inside your script at the very top of your script you will need to add the following set of lines

```python
import sys

if "--virtual-env" in sys.argv:
    virtualEnvPath = sys.argv[sys.argv.index("--virtual-env") + 1]
    virtualEnv = virtualEnvPath + "/bin/activate_this.py"
    exec(open(virtualEnv).read(), {"__file__": virtualEnv})
```

After that you should be able to import `trame` and start using it assuming you run your application with the `--virtual-env /path/to/virtual-env/with/trame` argument.

The command line below illustrate how a SimpleCone example can be run on a Mac where ParaView 5.10 has been installed.

```bash
/Applications/ParaView-5.10.0-RC1.app/Contents/bin/pvpython ./examples/ParaView/SimpleCone/RemoteRendering.py --virtual-env ./py-lib
```

## Understanding ParaView example

ParaView use proxies which abstract vtk object handling so they can be easily distributed for handling very large datasets.

For simplified usage, ParaView provide a `simple` package that let you create and interact with those proxies in a easier manner.

The SimpleCone example is extremely basic but provide the core concepts needed to understand what ParaView is doing under the cover.


```python
from paraview import simple

cone = simple.Cone()               # Create a source (reader, filter...)
representation = simple.Show(cone) # Create a representation in a view (if no view, one is created)
view = simple.Render()             # Ask to compute image of active view and return the corresponding view
```

With those 3 simple lines we created a full pipeline with a view. Now we can use our trame magic to show that view to the client.

```python
from trame.html import vuetify, paraview
from trame.layouts import SinglePage

html_view = paraview.VtkRemoteView(view)   # For remote rendering
# html_view = paraview.VtkLocalView(view)  # For local rendering

layout = SinglePage("ParaView cone", on_ready=html_view.update)

with layout.content:
    vuetify.VContainer(
        fluid=True,
        classes="pa-0 fill-height",
        children=[html_view],
    )
```

Now we can start adding some UI to control some of the parameters that we want to edit dynamically.
Let's add a slider to control the resolution of the cone.

Let's create the method to react when `resolution` is changed by the ui. In ParaView proxies, object parameters are simple properties that can be get or set in a transparent manner. At that point we just need to edit `cone.Resolution` and update the view to reflect the change we just made.

```python
@change("resolution")
def update_cone(resolution, **kwargs):
    cone.Resolution = resolution
    html_view.update()
```

Now we can add the UI with that slider

```python
DEFAULT_RESOLUTION = 6

with layout.toolbar:
    vuetify.VSlider(
        v_model=("resolution", DEFAULT_RESOLUTION),
        min=3,
        max=60,
        step=1,
        hide_details=True,
        dense=True,
    )
```

And with those few set of lines we have a 3D cone on which we can adjust the resolution using ParaView.
To learn more about ParaView scripting, you should look into ParaView trace which let you convert your UI interaction into actual Python code that can then be reused in your application.

## Advanced example

With the basics in place, we can go further by using some built-in feature of ParaView like saving and loading a state file. State files are a convinient way for capturing all the setting that were used to generate a visualization with Paraview.

Let's analyse the example in `./examples/ParaView/StateViewer/app.py`.

The core of the example is as follow which setup the UI and do only one action at startup time.

```python
def load_data():
    pass # I'll explain later

layout = SinglePage("State Viewer", on_ready=load_data)
layout.logo.click = "$refs.view.resetCamera()"
layout.title.set_text("ParaView State Viewer")
layout.content.add_child(vuetify.VContainer(fluid=True, classes="pa-0 fill-height"))

if __name__ == "__main__":
    layout.start()
```

Let's focus on what we want to add into that `load_data()` function.
1. Add and process a `--data` argument with the path to the file to load
2. Load the provided file path as state file.
3. Create a view element connected to the view defined in the state
4. Add that view element into the content of our UI

The (1) is achieved with the following set of lines.
More information on CLI are available [here](https://kitware.github.io/trame/docs/howdoi-cli.html).

```python
parser = trame.get_cli_parser()
parser.add_argument("--data", help="Path to state file", dest="data")
args, _ = parser.parse_known_args()

full_path = os.path.abspath(args.data)
working_directory = os.path.dirname(full_path)
```

To achieve (2) with ParaView the following set of lines are needed.
ParaView trace should be able to remove most of the magic by using the UI and looking at the corresponding Python code.


```python
simple.LoadState(
    full_path,
    data_directory=working_directory,
    restrict_to_data_directory=True,
)
view = simple.GetActiveView()
view.MakeRenderWindowInteractor(True)
```

Then (3) is done like before by doing the following.

```python
html_view = paraview.VtkRemoteView(view)
```

Finally for (4) we need to update the layout the same way we were doing it in VTK when switching from Remote to Local.

```python
layout.content.children[0].add_child(html_view)
layout.flush_content()
```

And that's it. You now have a ParaView `trame` application that let you reproduce complex visualization in a web context.