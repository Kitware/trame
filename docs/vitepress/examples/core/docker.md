# Docker

Trame applications can easily be deployed in the cloud via docker.

For instance you could deploy the following on a CapRover instance by just running `caprover deploy`

[![Simple deployment over https](/assets/images/deployment/cone-caprover.png)](https://github.com/Kitware/trame-app-cone)

::: code-group

```Dockerfile
FROM kitware/trame:py3.10-glvnd

RUN apt-get update \
    && apt-get install -y \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=trame-user:trame-user . /deploy

RUN /opt/trame/entrypoint.sh build
```

```captain-definition
{
  "schemaVersion": 2,
  "dockerfilePath": "./Dockerfile"
}
```
<<< @/../../examples/deploy/docker/VtkRendering/app.py
<<< @/../../examples/deploy/docker/VtkRendering/setup/apps.yml [./setup/apps.yaml]
<<< @/../../examples/deploy/docker/VtkRendering/setup/requirements.txt [./setup/requirements.txt]
:::
