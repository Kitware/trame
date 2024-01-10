FROM kitware/trame

COPY --chown=trame-user:trame-user . /deploy

ENV TRAME_CLIENT_TYPE=vue2
RUN /opt/trame/entrypoint.sh build
