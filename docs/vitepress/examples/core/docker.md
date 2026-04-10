# Docker

Trame applications can easily be deployed in the cloud via docker.

For instance you could deploy the following on a CapRover instance by just running `caprover deploy`

[![Simple deployment over https](/assets/images/deployment/cone-caprover.png)](https://github.com/Kitware/trame-app-cone)

::: code-group
<<< @/../../examples/deploy/docker/Dockerfile
<<< @/../../examples/deploy/docker/captain-definition
<<< @/../../examples/deploy/docker/VtkRendering/app.py
<<< @/../../examples/deploy/docker/VtkRendering/setup/apps.yml [./setup/apps.yaml]
<<< @/../../examples/deploy/docker/VtkRendering/setup/requirements.txt [./setup/requirements.txt]
:::
