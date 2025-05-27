# Trame Docker

The Trame Docker images are intended to be used for deploying multi-client ParaviewWeb/Trame applications. With these images, multiple clients can connect to the same URL, and each client will be viewing and running their own separate process.

The images include an Apache front-end that is able to serve static web content and manage WebSocket routing, a launcher for starting new processes, and a Python virtual environment containing the runtime requirements for the ParaviewWeb/Trame application.

A few different flavors of the Trame Docker images exist, including pip, pip with glvnd (for nvidia runtimes), and conda.

An example of its usage can be found [here](https://github.com/Kitware/trame/tree/master/examples/deploy/docker/SingleFile). The `trame-cookiecutter` package [also contains an example](https://github.com/Kitware/trame-cookiecutter/tree/master/%7B%7Bcookiecutter.package_name%7D%7D/bundles/docker).

## Usage

To run a docker image of a trame application (for example, after building the one located [here](https://github.com/Kitware/trame/tree/master/examples/deploy/docker/SingleFile)), a command similar to the following may be invoked:

```bash
docker run -it --rm -p 8080:80 trame-app
```

After the container is running, the application may be accessed at `localhost:8080`. Each time the URL is accessed, a new application process is created and displayed.

### Environment variable option

By default a trame application will use the serving host and path for its sessionURL, but if the application get served by another host, you will need to provide the host/path that should be used instead. To support this use-case, you can provide the **TRAME_USE_HOST** environment variable for overriding that sessionURL.

- __TRAME_USE_HOST__

   The sessionURL by default is defined as: `ws://USE_HOST/proxy?sessionId=${id}&path=ws` but if the `TRAME_USE_HOST` environment variable is set, then `USE_HOST` will be replaced with the contents of `TRAME_USE_HOST`. If `TRAME_USE_HOST` contains `://`, however, then it is assumed that it will be overwriting the `ws://` part at the beginning as well, and the whole `ws://USE_HOST` section will be replaced by the contents of `TRAME_USE_HOST`.

In case you aim the trame application to read/write files on a mounted directory, you can also provide another environment variable to ensure the trame-user to execute the process as the same use as the one owning that directory. Typically that overcome issue where the docker user does not match the host user.

- __TRAME_USER_DATA__

    Path iniside docker for checking ownership and remapping that UID/GID to the unpriviledge trame-user within docker. 

- __TRAME_URL_PREFIX__

    Path to serve content from. Rather that serving everything from `/`, when `TRAME_URL_PREFIX` is defined to `/app`, that means you should connect to `/app` in order to get access to the trame content. Same for `/app/launcher` and `/app/api/*`.

- __TRAME_LAUNCHER_TIMEOUT__

    Number of second to wait for the session to start before assuming a timeout. The default value is set to 25 seconds.

## Building the Server

To run your application in a Trame Docker image, a server directory must be present that contains everything required to run the application. This includes the static website (www) that needs to be served, instructions for starting the application (launcher) when a user requests access, and the Python dependencies that are needed to run it (venv).

The server directory may either be built within the Dockerfile itself (see [here](https://github.com/Kitware/trame/tree/master/examples/deploy/docker/SingleFile) for an example), or a pre-existing server directory may be mounted at `/deploy/server` at runtime (see [here](https://github.com/Kitware/trame-cookiecutter/blob/master/%7B%7Bcookiecutter.package_name%7D%7D/bundles/docker/scripts/build_server.sh) for an example of building the server directory outside the container that can be mounted inside later).

To build the server, a `setup` directory is expected to be mounted in `/deploy/setup`. This directory could contain 3 files and a directory:

### apps.yml (mandatory)

The apps.yml file contains instructions for running the trame application, along with different endpoints for a multi-endpoint setup. The most basic application is as follows:

```yaml
trame: # Default app under /index.html
  app: trame-app
```

This indicates that the docker image should run the `trame-app` package when a user connects.

Additional options at the same level as __app__ include __www_modules__ if there are custom Vue components that should be included, and `cmd` if a custom command should be used for launching the application (this will replace the `app` key). __www_modules__ expect a list of package names that should be enabled on the server when not already defined within `trame.modules.*`

Additional endpoints may also be specified. For instance:

```yaml
hello: # /hello.html
  app: trame-app
```

This indicates that the app `trame-app` may also be accessed at the `/hello.html` end point.

### requirements.txt (optional)

This file contains requirements that will be installed during setup.
For pip, the file will be installed via `pip install -r requirements.txt`.
For conda, the file will be installed via `conda install -y --file requirements.txt`.
This file may include the actual trame application itself.

### initialize.sh  (optional)

This file is optional. If present, it may be used to run additional commands that are necessary during setup. It is executed before the `requirements.txt` is installed. It may include the installation of the actual Trame application itself.

### www/ (optional)

This directory will be merged with the generated one at build time inside `/deploy/server/www`. Its content if overlapping existing files will override any previously generated one. This allow you to add or customize/replace specific files for your static file delivery. 

### The Build Command

The build command is invoked as an argument after the entrypoint. If you are building the server outside of a `Dockerfile`, this can be done like so:

```bash
docker run --rm           \
  -v "$DEPLOY_DIR:/deploy" \
  kitware/trame build
```

Or if you are building the server within a `Dockerfile`, this can be done like so:

```Dockerfile
RUN /opt/trame/entrypoint.sh build
```

Once the server is built, it is expected to be found in `/deploy/server` at runtime.

### Build Options

Building the server consists of three parts: `launcher`, `venv`, and `www`. By default, each of these will be built if they do not already exist, and they will not be re-built if they are already present.

Any combination of these strings, however, can be passed as arguments to indicate that those steps should be built, even if they are already present. For instance, if building externally:

```bash
docker run --rm           \
  -v "$DEPLOY_DIR:/deploy" \
  kitware/trame build launcher venv www
```

This indicates to re-build all three parts, even if they are already present.

The `www` part is the only part that may be optionally skipped entirely. This can be done by providing `no_www` as one of the arguments.
