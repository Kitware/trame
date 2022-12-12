# Trame Docker

The Trame Docker images are intended to be used for deploying multi-client
Trame applications. With these images, multiple clients can connect to the same
URL, and each client will be viewing and running their own separate process
of the Trame application.

A few different flavors of the Trame Docker images exist, including pip,
pip with glvnd (for nvidia runtimes), and conda.

An example can be found [in the trame-cookiecutter package](https://github.com/Kitware/trame-cookiecutter/tree/master/%7B%7Bcookiecutter.package_name%7D%7D/bundles/docker).

## Building the Server

For building the server, a `setup` directory is expected to be mounted in
`/deploy/setup`. This directory should contain 3 files:

### apps.yml

The apps.yml file contains instructions for running the trame application,
along with different endpoints for a multi-endpoint setup. The most basic
application is as follows:

```yaml
trame: # Default app under /index.html
  app: trame-app
```

This indicates that the docker image should run the `trame-app` package
when a user connects.

Additional options at the same level as `app` include `www_modules`, if
there are custom Vue components that should be included, and `cmd` if
a custom command should be used for launching the application (this
will replace the `app` key).

Additional endpoints may also be specified. For instance:


```yaml
trame-app: # /trame-app.html
  app: trame-app
```

This indicates that the app `trame-app` may also be accessed at the
`/trame-app.html` end point.

### requirements.txt

This file contains requirements that will be installed during setup.
For pip, the file will be installed via `pip install -r requirements.txt`.
For conda, the file will be installed via
`conda install -y --file requirements.txt`. This file may include the
actual trame application itself.

### initialize.sh

This file is optional. If present, it may be used to run additional
commands that are necessary during setup. It is executed before the
`requirements.txt` is installed. It may include the installation
of the actual Trame application itself.

Once the server is built, it may be mounted instead of the `setup`
directory in `/deploy/`.

## Options

When running the Trame Docker images through the main entrypoint, there
are a few environment variables available that provide some options.

### TRAME_BUILD_ONLY

If this is equal to `1`, then the application will exit immediately after
building the server. It will not proceed to deploy the application.

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
