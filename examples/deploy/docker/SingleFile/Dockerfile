FROM kitware/trame:py3.10

COPY --chown=trame-user:trame-user . /deploy

ENV TRAME_CLIENT_TYPE=vue2
RUN /opt/trame/entrypoint.sh build
