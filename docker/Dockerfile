ARG BASE_IMAGE=ubuntu:20.04
FROM ${BASE_IMAGE}

# Necessary to install tzdata. It will default to UTC.
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
      python3.9 \
      # python3.9-distutils is required to install pip
      # it unfortunately has to install python3.8-minimal as well...
      python3.9-distutils \
      # python-is-python3 creates a symlink for python to python3
      python-is-python3 \
      # For creating virtual environments
      python3.9-venv \
      # wget is used to obtain pip
      wget \
      # apache
      apache2 \
      apache2-dev \
      libapr1-dev \
      apache2-utils \
      gosu && \
    rm -rf /var/lib/apt/lists/*

# Set python3 to python3.9 (otherwise, it will be python3.8)
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# Never use a cache directory for pip, both here in this Dockerfile
# and when we run the container.
ENV PIP_NO_CACHE_DIR=1

# Install and upgrade pip
RUN wget -O- https://bootstrap.pypa.io/get-pip.py | python3.9 && \
    pip install -U pip

# Install setup dependencies
RUN pip install PyYAML

# Set up needed permissions and users
RUN groupadd trame-user -g 1000 && \
    groupadd proxy-mapping -g 1001 && \
    useradd -u 1000 -g trame-user -G proxy-mapping -s /sbin/nologin trame-user && \
    usermod -a -G proxy-mapping www-data && \
    mkdir -p /opt/trame && \
    chown -R trame-user:trame-user /opt/trame && \
    touch /opt/trame/proxy-mapping.txt && \
    chown trame-user:proxy-mapping /opt/trame/proxy-mapping.txt && \
    chmod 660 /opt/trame/proxy-mapping.txt

# Copy the apache configuration file into place
COPY config/apache/001-trame.conf /etc/apache2/sites-available/001-trame.conf
COPY config/default-launcher.json /opt/trame/default-launcher.json

# Copy the scripts into place
COPY scripts/entrypoint.sh \
     scripts/fix_uid_gid.sh \
     scripts/generate_launcher_config.py \
     scripts/generate_www.py \
     scripts/make_directories.sh \
     scripts/server.sh \
     scripts/start.sh \
     scripts/yaml_to_json.py \
     /opt/trame/

# Configure the apache web server
RUN a2enmod vhost_alias && \
    a2enmod proxy && \
    a2enmod proxy_http && \
    a2enmod proxy_wstunnel && \
    a2enmod rewrite && \
    a2enmod headers && \
    a2dissite 000-default.conf && \
    a2ensite 001-trame && \
    a2dismod autoindex -f

# Open port 80 to the world outside the container
EXPOSE 80

ENV PV_VENV=/deploy/server/venv
ENV VTK_VENV=$PV_ENV

ENTRYPOINT ["/opt/trame/entrypoint.sh"]
