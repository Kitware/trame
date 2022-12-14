# Trame Docker

The Trame Docker images are intended to be used for deploying multi-client ParaviewWeb/trame applications. With these images, multiple clients can connect to the same URL, and each client will be viewing and running their own separate process. 

Such image include an Apache front-end that is able to serve static web content and manage WebSocket routing, a launcher for starting new processes and a custom Python environment to handle any ParaviewWeb/trame application runtime.

A few different flavors of the Trame Docker images exist, including pip, pip with glvnd (for nvidia runtimes), and conda.

An example of its usage can be found [in the trame-cookiecutter package](https://github.com/Kitware/trame-cookiecutter/tree/master/%7B%7Bcookiecutter.package_name%7D%7D/bundles/docker).

## Usage

The basic gist imply the creation of a server directory that should contain everything specific to your application from the static website (www) that needs to be serve to the way your application needs to be started (launcher) when a user request access to what kind of Python dependency are needed to run it (venv).

That server can be generated with the help of a setup directory. The process of creating and configuring that server can be achieve either within the docker image at build time or done directly on a mounted directory.

## Building the Server

For building the server, a `setup` directory is expected to be mounted in `/deploy/setup`. This directory should contain 3 files:

### apps.yml

The apps.yml file contains instructions for running the trame application, along with different endpoints for a multi-endpoint setup. The most basic application is as follows:

```yaml
trame: # Default app under /index.html
  app: trame-app
```

This indicates that the docker image should run the `trame-app` package when a user connects.

Additional options at the same level as `app` include `www_modules`, if there are custom Vue components that should be included, and `cmd` if a custom command should be used for launching the application (this will replace the `app` key).

Additional endpoints may also be specified. For instance:


```yaml
hello: # /hello.html
  app: trame-app
```

This indicates that the app `trame-app` may also be accessed at the `/hello.html` end point.

### requirements.txt

This file contains requirements that will be installed during setup.
For pip, the file will be installed via `pip install -r requirements.txt`.
For conda, the file will be installed via `conda install -y --file requirements.txt`. 
This file may include the actual trame application itself.

### initialize.sh

This file is optional. If present, it may be used to run additional commands that are necessary during setup. It is executed before the `requirements.txt` is installed. It may include the installation of the actual Trame application itself.

Once the server is built, it may be mounted instead of the `setup` directory in `/deploy/`.

## Options

When running the Trame Docker images through the main entrypoint, there
are a few environment variables available that provide some options.

### TRAME_BUILD_ONLY

If this is equal to `1`, then the application will exit immediately after
building the server. It will not proceed to run the server.

### TRAME_BUILD

There are three parts to the server build: `launcher`, `venv`, and `www`.
By default, each of these will be built if they are missing, and they will
not be re-built if they are already present.

Any combination of these strings can be used to indicate that those steps
should be re-built every time (even if they are already present). For
instance:

```bash
export TRAME_BUILD="launcher;venv;www"
```

This indicates to re-build all three parts every time, even if they are
present.

The `www` part is the only part that may be optionally skipped entirely.
This can be done by providing `no_www` as one of the strings.

### TRAME_USE_HOST

The sessionURL by default is defined as: `ws://USE_HOST/proxy?sessionId=${id}&path=ws`

If the `TRAME_USE_HOST` environment variable is set, then `USE_HOST` will be replaced
with the contents of `TRAME_USE_HOST`.

If `TRAME_USE_HOST` contains `://`, however, then it is assumed that it will be
overwriting the `ws://` part at the beginning as well, and the whole
`ws://USE_HOST` section will be replaced by the contents of `TRAME_USE_HOST`.
