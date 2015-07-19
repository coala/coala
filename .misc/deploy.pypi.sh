#!/bin/bash

# Do not use `set -x` here as then it displays the PYPIPW in logs
set -e

# Get environment variables, readily decrypted by rultor
source ../rultor_secrets.sh

# Ship it!
echo "Uploading coala to pypi"
pip3 install twine wheel
python3 setup.py sdist bdist_wheel
twine upload dist/* -u "$PYPIUSER" -p "$PYPIPW"

echo "Installing coala from pypi"
pip3 install --pre coala --upgrade
echo coala versions: pip=`coala -v` repo=`cat coalib/VERSION`
[ `coala -v` = `cat coalib/VERSION` ]
