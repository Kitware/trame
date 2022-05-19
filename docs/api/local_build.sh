#!/usr/bin/env bash

set -e

# Clean up the current documentation
rm -rf dist
mkdir dist

# Build and open
sphinx-build source dist
google-chrome ./dist/index.html
