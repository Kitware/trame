#!/usr/bin/env bash

# Put any arguments into the `TRAME_BUILD` variable
# This is so you can do things like `/opt/trame/build.sh no_www venv`, etc.
export TRAME_BUILD="$*"
export TRAME_BUILD_ONLY=1

/opt/trame/entrypoint.sh
