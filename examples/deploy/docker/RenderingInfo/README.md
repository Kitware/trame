# Disclaimer

The current example rely trame.tools.vtk to display rendering capabilities of your server.

# Build the image

```bash
docker build -t trame-vtk-info .
```

# Run the image on port 8080

```bash
docker run -it --rm -p 8080:80 trame-vtk-info
```

# Deploying into CapRover

If that directory was at the root of a git repo you could run the following command line

```bash
caprover deploy
```

That app could also be deployed by running the following set of commands

```bash
tar -cvf trame-vtk-info.tar captain-definition Dockerfile setup
caprover deploy -t trame-vtk-info.tar
```
