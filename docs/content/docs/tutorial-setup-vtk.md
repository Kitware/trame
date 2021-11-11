## Setup environment for VTK

Trame requires Python 3.6+

```bash
python3 -m venv .venv
source ./.venv/bin/activate
python -m pip install --upgrade pip
pip install -r ./examples/Tutorial/setup-vtk/requirements.txt
```

**Notes**:
 - `venv` was added in Python 3.3.
 - The command lines above assume you are inside the cloned `trame` repository
 - On mac with Arm architecture, VTK is only available on Python 3.9

## Running the application

```
cd examples/Tutorial/setup-vtk
python ./app.py --port 1234
```

Your browser should open to `http://localhost:1234/`

**Notes**:
 - The default port is 8080, but since this is very common we will use 1234 for our Tutorial.
 - If you are running this on a remote machine, you may have to set the host to 0.0.0.0 to allow any external connection. (`python ./app.py --port 1234 --host 0.0.0.0`)

## Annotation of Hello Trame Application

We start by importing the two basic building blocks for our client-server application.

```
from trame import start
from trame.layouts import SinglePage
```

From **Trame** we import the method for starting the Web server, and from Trame's `layouts`, we import a skeleton for a single page client application.

Next, we define the graphical user interface (GUI) using a bare minimum of options. We instantiate a `SinglePage` GUI setting the browser tab title as `"Hello Trame"`, and then set the GUI `title.content` to hold `"Hello Trame"`.

```
layout = SinglePage("Hello Trame")
layout.title.set_text("Hello Trame")
```

Finally, we start the Web server using

```
if __name__ == "__main__":
    start(layout)
```

`start` can take a number of optional arguments. In this case, we pass in the optional GUI `layout`. If not provided, `start` will look for a `./template.html`.

You can also optionally set the tab *name*, a *favicon*, a *port* number, and an *on_ready* function to call when the server is up and running. However, these items can either be set with command-line arguments (`--port 1234`) or with calls exposed through the SinglePage layout.
