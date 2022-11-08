# Build the image

```bash
docker build -t trame-app .
```

# Run the image on port 8080

```bash
docker run -it --rm -p 8080:80 trame-app
```