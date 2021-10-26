## Setup environment for VTK

Trame requires Python 3.6+

```
python3 -m venv .venv
source ./.venv/bin/activate
python -m pip install --upgrade pip
pip install -r ./examples/Tutorial/setup/requirements.txt
```

**Note**: `venv` was added in Python 3.3.

## Running the application

```
cd examples/Tutorial/setup
python ./app.py --port 1234
```

Open browser to `http://localhost:1234/`

**Note**: The default port is 8080, but since this is very common we will use 1234 for our **Tutorial**.

Note: If you are running this on a remote machine, then on Linux you define the host to be open (0.0.0.0) to any external connection.

```
python ./app.py --port 1234 --host 0.0.0.0
```

**Note**: Firewalls will be more complicated.

## Annotation of Hello Trame Application

We start by importing the two basic building blocks for our client-server application.

```
from trame import start
from trame.layouts import SinglePage
```

From **Trame** we import the method for starting the Web server, and from Trame's `layouts`, we import a skeleton for a single page client application.

Next, we define the graaphics user interface (GUI) using a bare minimum of options. We instantiate a `SinglePage` GUI setting the browser tab title as `"Hello Trame"`, and then set the GUI `title.content` to hold `"Hello Trame"`.

```
layout = SinglePage("Hello Trame")
layout.title.content = "Hello Trame"
```

Finally, we start the Web server using 

```
if __name__ == "__main__":
    start(layout)
```

`start` can take a number of optional arguments. In this case, we pass in the optional GUI `layout`. if not provided, `start` will look for a `./template.html`.

You can also optionally set tab *name*, *favicon*, *port* number, and *on_ready* function to call when the server is up and running. However, these items can either be set with command-line arguments (--port 1234) or with calls exposed through the SinglePage layout.