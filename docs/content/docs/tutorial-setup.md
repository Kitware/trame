## Setup environment

Trame requires 3.6+

```
python3 -m venv .venv
source ./.venv/bin/activate
python -m pip install --upgrade pip
pip install -r ./examples/Tutorial/setup/requirements.txt
```

Note: venv was added in Python 3.3.

## Running the application

```
cd examples/Tutorial/setup
python ./app.py --port 1234
```

Open browser on `http://localhost:1234/`

Note: The default port is 8080, but since this is very common we will use 1234 for our Tutorial.

Note: If you are running this on a remote machine, then on Linux you define the host to be open (0.0.0.0) to any external connection.

```
python ./app.py --port 1234 --host 0.0.0.0
```
Note: Firewalls will be more complicated.
