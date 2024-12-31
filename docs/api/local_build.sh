#!/usr/bin/env bash

set -e

# Clean up the current documentation
rm -rf dist
mkdir dist

# Build and open
sphinx-build source dist
# rm -rf _build/doctrees
# python -m sphinx -T -b html -d _build/doctrees -D language=en source dist

cd dist
python -m http.server 8000
