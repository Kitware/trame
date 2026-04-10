# Build the image

```bash
docker build -t trame-app .
```

# Run the image on port 9000

```bash
docker run -it --rm -p 9000:80 trame-app
```

Or if you need some prefix

```bash
docker run -it --rm -p 9000:80 -e TRAME_URL_PREFIX=/my-app/sub/path trame-app
```


# Deploying into CapRover

If that directory was at the root of a git repo you could run the following command line

```bash
caprover deploy
```

That app could also be deployed by running the following set of commands

```bash
tar -cvf trame-app.tar captain-definition Dockerfile app.py setup
caprover deploy -t trame-app.tar
```
