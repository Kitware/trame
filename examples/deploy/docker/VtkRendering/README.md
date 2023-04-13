# Disclaimer

The current example rely on OSMesa for doing remote rendering but for good rendering performance
using the nvidia-runtime with __kitware/trame:glvnd__ base image and an EGL build of VTK would be preferred.

# Build the image

```bash
docker build -t trame-vtk-app .
```

# Run the image on port 8080

```bash
docker run -it --rm -p 8080:80 trame-vtk-app
```

# Deploying into CapRover

If that directory was at the root of a git repo you could run the following command line

```bash
caprover deploy
```

That app could also be deployed by running the following set of commands

```bash
tar -cvf trame-vtk-app.tar captain-definition Dockerfile app.py setup
caprover deploy -t trame-vtk-app.tar
```
