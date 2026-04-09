# Setup environment

***trame*** requires Python 3.10+ but since ParaView 6 is bundling Python 3.12 we will use Python 3.12 in this tutorial. Also for uniformity across OS we will be using [uv](https://docs.astral.sh/uv/).

```bash
uv venv -p 3.12
source ./.venv/bin/activate
uv pip install trame      # Install trame core
uv pip install trame-vuetify trame-vtk # Install widgets that we'll be using
uv pip install vtk                     # Install the VTK library
```

## Running the application

```bash
python ./00_setup/app.py --port 1234
```

Your browser should open to `http://localhost:1234/`

![Hello trame](/assets/images/tutorial/hello-trame.jpg)

**Notes**:
 - The default port is 8080, but since this is very common we will use 1234 for our Tutorial.
 - If you are running this on a remote machine, you may have to set the host to 0.0.0.0 to allow any external connection. (`python ./app.py --port 1234 --host 0.0.0.0`)

<div class="print-break"></div>

## Annotation of Hello ***trame*** Application

We start by importing the basic building blocks for our client-server application.

```python
from trame.app import get_server
from trame.ui.vuetify3 import SinglePageLayout
```

from ***trame***'s `app`, we import the factory function for retrieving a server instance on which we will bind our UI and business logic. We also import a skeleton for a single page client application that relies on vuetify (our main widget library) from `trame.ui.vuetify`.

Next, we define the graphical user interface (GUI) by passing the server to which it should be bound. Then with that layout we update the toolbar's title to read `"Hello trame"`.

```python
server = get_server()

with SinglePageLayout(server) as layout:
    layout.title.set_text("Hello trame")
```

Finally, we start the Web server using:

```python
if __name__ == "__main__":
    server.start()
```

`start` can take an optional argument of a *port* number. However, this can be set with command-line arguments (`--port 1234`).

**Running the Application**

```bash
$ python ./00_setup/app.py --port 1234

 App running at:
 - Local:   http://localhost:1234/
 - Network: http://192.168.1.34:1234/

Note that for multi-users you need to use and configure a launcher.
And to prevent your browser from opening, add '--server' to your command line.
```

Your browser should open automatically to `http://localhost:1234/`.
