# Docker

When running your trame application with docker, you may want to leverage the GPU of your host machine for either AI or 3D visualization. 

Usually you can do that by running your image with `--gpus all` argument.
But if you want to enable it by default in system like CapRover, you need to edit the defaults of your docker daemon and choose __nvidia__ as your default runtime. 

```json /etc/docker/daemon.json
{
  "default-runtime": "nvidia",
    "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
        }
    }
}
```

Since docker don't aim to provide desktop graphic environment, with VTK/ParaView we tend to rely on EGL for an offscreen setup such as docker. 

For that you may want to use the special build of ParaView for EGL or the vtk wheel for EGL.

```bash
pip uninstall vtk vtk-osmesa
pip install --extra-index-url https://wheels.vtk.org vtk-egl
```

## EGL Caution

Modern Ubuntu provide a Mesa implementation of EGL which is great as an alternative to OSMesa but that also mean you can get slow performance even though you might think that you are using your GPU. 

Possible issue, you forgot to 
- setup the default runtime to nvidia
- the `--gpus all` arg
- nvidia driver version not properly exposing EGL (545 had/has a bug - could be fixed by the time of reading)

The best way to test if your docker can properly leverage your NVIDIA card for EGL is by running the following commands:

```bash
docker pull nvidia/opengl:1.0-glvnd-runtime 
docker run --gpus all -it nvidia/opengl:1.0-glvnd-runtime

# Then inside the docker shell

# First make sure you have access to your GPU
nvidia-smi 

# Second make sure EGL will leverage your NVIDIA card
apt-get update && apt-get install mesa-utils-extra -y && eglinfo
# => output should contain
#   Device platform:
#   EGL API version: 1.5
#   EGL vendor string: NVIDIA
```
