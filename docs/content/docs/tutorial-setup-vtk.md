## Setup environment for VTK

***trame*** requires Python 3.6+

```bash
python3 -m venv .venv
source ./.venv/bin/activate
python -m pip install --upgrade pip
pip install -r ./examples/Tutorial/setup-vtk/requirements.txt
```

**Notes**:
 - `venv` was added in Python 3.3.
 - The command lines above assume you are inside the cloned ***trame*** repository
 - On mac with Arm architecture, VTK is only available on Python 3.9

## Running the application

```
cd examples/Tutorial/setup-vtk
python ./app.py --port 1234
```

Your browser should open to `http://localhost:1234/`

<p style="text-align:center;"><img src="../images/tutorial-hello-trame.jpg" alt="Hello trame" style="width: 75%; height: 75%"></p>

**Notes**:
 - The default port is 8080, but since this is very common we will use 1234 for our Tutorial.
 - If you are running this on a remote machine, you may have to set the host to 0.0.0.0 to allow any external connection. (`python ./app.py --port 1234 --host 0.0.0.0`)

## Annotation of Hello ***trame*** Application

We start by importing the basic building blocks for our client-server application.

```
from trame.layouts import SinglePage
```

from ***trame***'s `layouts`, we import a skeleton for a single page client application.

Next, we define the graphical user interface (GUI) using a bare minimum of options. We instantiate a `SinglePage` GUI setting the browser tab title as "Hello trame", and then set the GUI `title` text to hold `"Hello trame"`.

```
layout = SinglePage("Hello trame")
layout.title.set_text("Hello trame")
```

Finally, we start the Web server using

```
if __name__ == "__main__":
    layout.start()
```

`start` can take an optional argument of a *port* number. However, this can be set with command-line arguments (`--port 1234`).

**Running the Application**

```bash
cd examples/Tutorial/setup-vtk
python ./app.py --port 1234
```

Open a browser to `http://localhost:1234/`