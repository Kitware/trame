FROM kitware/trame:uv-glvnd

ENV TRAME_PYTHON=3.12

RUN install -d -o trame-user -g trame-user /deploy

ARG PV_URL='https://www.paraview.org/files/v6.1/ParaView-6.1.0-MPI-Linux-Python3.12-x86_64.tar.gz'
RUN mkdir -p /opt/paraview && cd /opt/paraview && wget -qO- $PV_URL | tar --strip-components=1 -xzv
ENV TRAME_PARAVIEW=/opt/paraview

COPY --chown=trame-user:trame-user . /deploy

RUN /opt/trame/entrypoint.sh build
