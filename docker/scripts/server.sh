#!/usr/bin/env bash

LAUNCHER_OUTPUT_PATH=/deploy/server/launcher.json
WWW_PATH=/deploy/server/www

# Convert the apps.yml file to json and put it in the right place.
# This needs PyYAML, which is in the root python environment, so
# we must do this before activating the venv.
python /opt/trame/yaml_to_json.py /deploy/setup/apps.yml /opt/trame/apps.json

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

# launcher
# Build if it does not exist, or if "launcher" is in `TRAME_BUILD`
if [[ ! -f $LAUNCHER_OUTPUT_PATH || $TRAME_BUILD == *"launcher"* ]]; then
  python /opt/trame/generate_launcher_config.py
fi

# www
# This must be done after activating the venv.
# This directory should already exist.
# Build if "no_www" is not in `TRAME_BUILD` and either it is empty or "www" is in `TRAME_BUILD`
if [[ $TRAME_BUILD != *"no_www"* ]] && [[ -z "$(ls -A $WWW_PATH)" || $TRAME_BUILD == *"www"* ]]; then
  # Generate launcher.json and the www directory
  python /opt/trame/generate_www.py

  # Merge any user-created www directories with the generated one
  if [[ -d /deploy/setup/www ]]; then
    cp -r /deploy/setup/www/* /deploy/server/www
  fi
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
cp $LAUNCHER_OUTPUT_PATH /opt/trame/config-template.json

# This performs replacements on the launcher-template.json copied into place
# above, based on the presence of environment variables passed with "-e" to the
# "docker run ..." command.
. /opt/trame/start.sh
