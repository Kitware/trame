FROM kitware/trame:uv-glvnd

ENV TRAME_PYTHON=3.13

RUN apt-get update \
    && apt-get install -y \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=trame-user:trame-user . /deploy

RUN /opt/trame/entrypoint.sh build
