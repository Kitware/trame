# Server relay

The idea behind the server relay is to connect 2 client ws together and allow server process to act as a client.

WS  /proxy/xyz  =>  first: process ws / second: client ws

## Setup

```bash
# Working directory
mkdir -p test-relay && cd "$_"

# Virtual environment setup
python -m venv .venv
source ./.venv/bin/activate
pip install -U pip trame

# Generate static content
python -m trame.tools.www --output ./www

# Start relay
python -m wslink.relay --www ./www --mode relay
```

## Testing

In a different terminal but with same venv run a test process

```bash
python $TRAME_ROOT/examples/06_vtk/01_SimpleCone/RemoteRendering.py --reverse-url ws://localhost:8080/proxy/xyz-123
```

Then try connecting your browser to the following set of URLs

### Working connection

Open your browser to `http://localhost:8080/index.html?sessionURL=ws://localhost:8080/proxy/xyz-123`.
The application should work even when you reload the page.

If you open a second tab with that same URL, that one should fail.

### Invalid endpoint

Open your browser to `http://localhost:8080/index.html?sessionURL=ws://localhost:8080/proxy/abc`.
Since no process is listening on 1235, the connection should fail.