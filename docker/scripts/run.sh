#!/usr/bin/env bash

# This script is used to start the trame server.
# If the `TRAME_USE_HOST` environment variable is set, this
# will replace `USE_HOST` in the launcher json file. If it contains
# `://`, it will replace `ws://USE_HOST` instead.

if [ ! -d /deploy/server ]; then
  echo "ERROR: The the server directory must be in the container at '/deploy/server'"
  exit 1
fi

# First, activate the venv
. /opt/trame/activate_venv.sh

# We will copy the launcher and make any needed edits to it
LAUNCHER_TEMPLATE_PATH=/deploy/server/launcher.json
LAUNCHER_PATH=/opt/trame/config.json

OUTPUT=$(<"${LAUNCHER_TEMPLATE_PATH}")

if [[ -n $TRAME_USE_HOST ]]; then
  REPLACEMENT_STRING="USE_HOST"
  if [[ $TRAME_USE_HOST == *"://"* ]]; then
    # If the string contains "://", then we are replacing the "ws://" at
    # the beginning as well
    REPLACEMENT_STRING="ws://$REPLACEMENT_STRING"
  fi
  OUTPUT="${OUTPUT//$REPLACEMENT_STRING/$TRAME_USE_HOST}"
fi

echo -e "$OUTPUT" > "${LAUNCHER_PATH}"

# Run the launcher in the foreground so this script doesn't end
echo "Starting the wslink launcher at"
python -m wslink.launcher ${LAUNCHER_PATH}
