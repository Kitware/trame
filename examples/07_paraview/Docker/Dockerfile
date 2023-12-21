FROM kitware/trame:py3.10-ubuntu22.04

RUN install -d -o trame-user -g trame-user /deploy
RUN apt update -y && apt install -y libosmesa6-dev

ARG PV_URL='https://www.paraview.org/files/v5.12/ParaView-5.12.0-RC1-osmesa-MPI-Linux-Python3.10-x86_64.tar.gz'
RUN mkdir -p /opt/paraview && cd /opt/paraview && wget -qO- $PV_URL | tar --strip-components=1 -xzv
ENV TRAME_PARAVIEW=/opt/paraview

COPY --chown=trame-user:trame-user . /deploy

RUN /opt/trame/entrypoint.sh build
