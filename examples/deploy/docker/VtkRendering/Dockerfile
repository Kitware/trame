FROM kitware/trame:py3.10-glvnd

RUN apt-get update \
    && apt-get install -y \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=trame-user:trame-user . /deploy

RUN /opt/trame/entrypoint.sh build
