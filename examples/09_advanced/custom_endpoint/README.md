# Trame app with custom endpoint

This allow you to register special HTTP endpoint for your app.
While it works by default locally, when using docker bundling, you need to add special handling.

## Run locally without docker

```bash
python ./app.py
```

## Build the image

```bash
docker build -t trame-app-api .
```

## Run the image on port 8080

```bash
docker run -it --rm -p 8080:80 trame-app-api
```
