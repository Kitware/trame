# Cloud

Trame applications can be bundled into a standalone docker container image that can then be deployed in the cloud with various mechanisms.

The [trame-cookiecutter](https://github.com/Kitware/trame-cookiecutter) provide an initial example for building such image under `bundles/docker/*`.

For single file application you can find an example in that [repository](https://github.com/Kitware/trame-app-cone) along with [a multi-application setup](https://github.com/Kitware/trame-app-cone/tree/multi-app).

## CapRover

To even streamline the deployment of such docker image, you can leverage [CapRover](https://caprover.com/) to automatically enable HTTPS/WSS on public domains for your trame app.

Both the cookiecutter in `bundles/docker/DEPLOY.md` and the [single file app repo](https://github.com/Kitware/trame-app-cone) go over the steps to deploy any trame application to CapRover.

## Infinite scaling

Trame applications have the possibility to be launched on server less architecture and therefore virtually scale to infinity by using a routing server and the reverse connection infrastructure of its server. Such feature can be leverage both in the cloud or in HPC.

For more details on that feature please reach out to [Kitware](https://www.kitware.com/contact/).
