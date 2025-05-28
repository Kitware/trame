FROM kitware/trame:py3.10-glvnd

COPY --chown=trame-user:trame-user . /deploy

RUN /opt/trame/entrypoint.sh build
