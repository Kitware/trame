#!/usr/bin/env bash

# The entrypoint provides some branching logic as to what we
# are going to do. By default, it runs the server.
# If the first argument is "build", however, it will build the
# server instead, and forward any extra args to the build script.

# First, perform initial setup
. /opt/trame/setup.sh

if [[ "$1" == "build" ]]; then
  # Run the build
  # Forward all arguments after `build`, so the user can pass things
  # like `www venv launcher` etc.
  echo "Running build..."
  gosu trame-user /opt/trame/build.sh ${@:2}
  echo "Build complete"
else
  # Start the server
  /opt/trame/runtime_patch.sh
  echo "Starting server..."
  gosu trame-user /opt/trame/run.sh
fi
