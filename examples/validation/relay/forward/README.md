# Forward relay

The idea behind the forward relay is to serve static content from a local directory and forward ws connection to a local process running on a different port.

GET /*           =>  serve --www /path/to/dir
WS  /proxy/1234  =>  forward to ws://localhost:1234/ws

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
python -m wslink.relay --www ./www
```

## Testing

In a different terminal but with same venv run a test process

```bash
python $TRAME_ROOT/examples/06_vtk/01_SimpleCone/RemoteRendering.py --server --port 1234
```

Then try connecting your browser to the following set of URLs

### Working connection

Open your browser to `http://localhost:8080/index.html?sessionURL=ws://localhost:8080/proxy/1234`.
The application should work even when you reload the page.

If you open a second tab with that same URL, that one should fail.

### Invalid endpoint

Open your browser to `http://localhost:8080/index.html?sessionURL=ws://localhost:8080/proxy/1235`.
Since no process is listening on 1235, the connection should fail.