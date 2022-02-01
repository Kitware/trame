#!/usr/bin/env bash

venv_dir=/deploy/server/venv

if [ ! -d $venv_dir ]
then
  # We have access to PyYAML in the root python environment.
  # Convert the apps.yml file to json and put it in the right place.
  python /opt/trame/yaml_to_json.py /deploy/setup/apps.yml /opt/trame/apps.json

  # Create and install the virtual environment
  python -m venv $venv_dir
  . $venv_dir/bin/activate

  # Upgrade pip
  pip install -U pip

  # Run the initialize script (if it exists)
  if [ -f /deploy/setup/initialize.sh ]
  then
    . /deploy/setup/initialize.sh
  fi

  # Install requirements (if it exists)
  if [ -f /deploy/setup/requirements.txt ]
  then
    pip install -r /deploy/setup/requirements.txt
  fi

  # Generate launcher.json and the www directory
  python /opt/trame/generate_launcher_config.py
  python /opt/trame/generate_www.py

  # Merge any user-created www directories with the generated one
  if [ -d /deploy/setup/www ]
  then
    cp -r /deploy/setup/www/* /deploy/server/www
  fi
else
  . $venv_dir/bin/activate
fi

if [[ $TRAME_BUILD_ONLY == 1 ]]; then
  echo "Build complete. Exiting."
  exit 0
fi

# Copy the launcher config into the location where the start script expects
# to find it.  The config may or may not have replacement values in it, if it
# does not, the start script will not change it in any way.  Here we expect
# that the user doing the "docker run ..." has set up an external directory
# containing a "server/launcher.json" filepath and mounts that path as
# "/deploy".
cp /deploy/server/launcher.json /opt/trame/config-template.json

# This performs replacements on the launcher-template.json copied into place
# above, based on the presence of environment variables passed with "-e" to the
# "docker run ..." command.
. /opt/trame/start.sh
