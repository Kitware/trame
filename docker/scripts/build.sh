#!/usr/bin/env bash

if [ ! -d /deploy/setup ]; then
  echo "ERROR: The 'setup' directory must be present in the container at '/deploy/setup'"
  exit 1
fi

# Put any arguments into the `TRAME_BUILD` variable
# This is so you can do things like `/opt/trame/build.sh no_www venv`, etc.,
# or "build no_www venv" via the default entrypoint.
TRAME_BUILD="$*"

LAUNCHER_OUTPUT_PATH=/deploy/server/launcher.json
WWW_PATH=/deploy/server/www

# Convert the apps.yml file to json and put it in the right place.
# This needs PyYAML, which is in the root python environment, so
# we must do this before activating the venv.
# We will do this every time, because it is needed in both the launcher
# step and the www step.
python /opt/trame/yaml_to_json.py /deploy/setup/apps.yml /opt/trame/apps.json

# launcher
# Build if it does not exist, or if "launcher" is in `TRAME_BUILD`
if [[ ! -f $LAUNCHER_OUTPUT_PATH || $TRAME_BUILD == *"launcher"* ]]; then
  # Generate the launcher config
  python /opt/trame/generate_launcher_config.py
fi

# venv
# Build if it does not exist, or if "venv" is in `TRAME_BUILD`
if [[ ! -d $TRAME_VENV || $TRAME_BUILD == *"venv"* ]]; then
  # In case we are doing a force rebuild, make sure the directory is deleted
  rm -rf $TRAME_VENV

  # Create (and activate) the venv
  . /opt/trame/create_venv.sh

  # Run the initialize script (if it exists)
  if [[ -f /deploy/setup/initialize.sh ]]; then
    . /deploy/setup/initialize.sh
  fi

  # Install any specified requirements
  . /opt/trame/install_requirements.sh
else
  # Activate it if we skipped building it
  . /opt/trame/activate_venv.sh
fi

# www
# This must be done after activating the venv.
# This directory should already exist.
# Build if "no_www" is not in `TRAME_BUILD` and either it is empty or "www" is in `TRAME_BUILD`
if [[ $TRAME_BUILD != *"no_www"* ]] && [[ -z "$(ls -A $WWW_PATH)" || $TRAME_BUILD == *"www"* ]]; then
  # Generate the www directory
  python /opt/trame/generate_www.py

  # Merge any user-created www directories with the generated one
  if [[ -d /deploy/setup/www ]]; then
    cp -r /deploy/setup/www/* /deploy/server/www
  fi
fi
