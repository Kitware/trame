FROM kitware/trame:uv

ENV TRAME_PYTHON=3.13
ENV TRAME_CLIENT_TYPE=vue2

COPY --chown=trame-user:trame-user . /deploy

RUN /opt/trame/entrypoint.sh build
